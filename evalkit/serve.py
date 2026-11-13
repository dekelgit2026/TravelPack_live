"""Serve the prototype and run REAL evals with the API key kept on this machine ("secret mode").

    python evalkit/serve.py            # then open http://127.0.0.1:8765/trip-planner.html and use the Eval tab

The key is read from the environment or from .env by evalkit.run_eval (the same way the command-line runner does).
It stays inside this process: it is never sent to the browser, never put in a response, never written to a file.
Only this computer can reach the server (127.0.0.1), and a request must carry a localhost Host header.
The Eval tab's "Actual API" mode calls /api/case once per test case, so you see progress and the cost of every call.
Python 3.10+, standard library only.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from evalkit import run_eval as R  # noqa: E402

SAFE = re.compile(r"^[A-Za-z0-9_-]{1,40}$")
STATE: dict = {"claude": None, "cases": {}, "max_usd": 0.50}


def claude() -> R.Claude:
    if STATE["claude"] is None:
        STATE["claude"] = R.Claude(R.load_prices(), STATE["max_usd"])
    return STATE["claude"]


def cases_for(pack: str) -> dict:
    if pack not in STATE["cases"]:
        STATE["cases"][pack] = {c["id"]: c for c in R.read_cases(pack)}
    return STATE["cases"][pack]


def run_case(body: dict) -> dict:
    pack, version, cid, model = (str(body.get(k, "")) for k in ("pack", "version", "id", "model"))
    if not (SAFE.match(pack) and SAFE.match(version) and SAFE.match(cid) and SAFE.match(model or "haiku")):
        raise R.EvalError("bad request")
    case = cases_for(pack).get(cid)
    if not case:
        raise R.EvalError(f"no case {cid}")
    c = claude()
    if not c.key:
        raise R.EvalError("the server has no API key: put ANTHROPIC_API_KEY in .env, then restart it")
    system, _ = R.read_prompt(pack, version)
    schema = R.read_schema(pack)
    tools = R.read_tools(pack)
    r = {"id": cid, "version": version, "model": R.model_id(model or "haiku"), "critical": case["critical"],
         "checks": [], "output": None, "error": None, "cost_usd": 0.0, "latency_ms": 0, "input_tokens": 0,
         "output_tokens": 0, "cache_read": 0, "cache_write": 0}
    try:
        out, meta = c.structured(r["model"], system, case["input"], schema, tools, cache=True)
        r.update({k: meta[k] for k in ("cost_usd", "latency_ms", "input_tokens", "output_tokens", "cache_read", "cache_write")})
        r["output"] = out
        for chk in case["parsed"]:
            if chk["kind"] == "judge":
                r["checks"].append({"check": chk["text"], "passed": None, "seen": "judge checks are not run here"})
            else:
                ok, seen = R.run_check(chk, out)
                r["checks"].append({"check": chk["text"], "passed": ok, "seen": seen})
    except R.CaseError as e:
        r["error"] = str(e)
    scored = [k for k in r["checks"] if k["passed"] is not None]
    r["passed"] = (not r["error"]) and bool(scored) and all(k["passed"] for k in scored)
    r["spent_usd"] = round(c.spent, 6)
    r["max_usd"] = c.max_usd
    return r


RUN_KEYS = ("id", "critical", "passed", "output", "cost_usd", "latency_ms", "input_tokens", "output_tokens", "cache_read", "cache_write")


def save_run(d: dict) -> dict:
    """Write one finished series to results/<pack>/ and the scoreboard, exactly like the command-line runner does."""
    pack, ver, model = "travel", str(d.get("ver", "")), str(d.get("model", ""))
    if not (SAFE.match(ver) and SAFE.match(model)):
        raise R.EvalError("bad request")
    rows = [{k: x.get(k) for k in RUN_KEYS} for x in (d.get("results") or [])[:50] if isinstance(x, dict)]
    if not rows:
        raise R.EvalError("no results to save")
    n = len(rows)
    passed = sum(1 for x in rows if x["passed"])
    lat = sorted(x["latency_ms"] for x in rows if x.get("latency_ms"))
    tot_in = sum((x.get("input_tokens") or 0) + (x.get("cache_read") or 0) + (x.get("cache_write") or 0) for x in rows)
    cache = sum(x.get("cache_read") or 0 for x in rows)
    cost = sum(x.get("cost_usd") or 0 for x in rows)
    rep = {"pack": pack, "prompt": ver, "model": R.model_id(model), "engine": "live", "ran_at": R.datetime.now().strftime("%Y-%m-%d %H:%M"),
           "context_files": [], "cases": n, "passed": passed, "score_pct": round(100 * passed / n),
           "critical_cases": sum(1 for x in rows if x["critical"]),
           "critical_failed": [x["id"] for x in rows if x["critical"] and not x["passed"]], "judge": "off",
           "judge_checks_skipped": 0, "cost_usd": round(cost, 5), "cost_per_case_usd": round(cost / n, 6), "judge_cost_usd": 0,
           "latency_ms_median": lat[len(lat) // 2] if lat else 0, "latency_ms_max": lat[-1] if lat else 0,
           "input_tokens": tot_in, "output_tokens": sum(x.get("output_tokens") or 0 for x in rows), "cache_read_tokens": cache,
           "cache_read_pct": round(100 * cache / tot_in) if tot_in else 0, "results": rows}
    return {"file": R.save(rep, 80).name}


def save_baseline(d: dict) -> dict:
    """The approved baseline: one version + model run the team is happy with. Later runs are compared with it."""
    keep = {k: d.get(k) for k in ("ver", "model", "label", "when", "score", "n", "costPerCase", "lat", "critFailed", "passMap", "source")}
    if not (SAFE.match(str(keep["ver"])) and SAFE.match(str(keep["model"])) and isinstance(keep["passMap"], dict)):
        raise R.EvalError("bad request")
    keep["passMap"] = {str(k)[:12]: bool(v) for k, v in list(keep["passMap"].items())[:50]}
    p = R.ROOT / "prompts" / "travel" / "approved_baseline.json"
    p.write_text(json.dumps(keep, ensure_ascii=False, indent=1), encoding="utf-8")
    return {"file": str(p.relative_to(R.ROOT)).replace("\\", "/")}


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=str(R.ROOT / "prototype"), **kw)

    def end_headers(self):  # never let the browser keep an old copy of the page or of an answer
        self.send_header("cache-control", "no-store")
        super().end_headers()

    def log_message(self, fmt, *args):  # quiet: nothing about requests is worth logging, and never log bodies
        pass

    def _local_only(self) -> bool:
        host = (self.headers.get("Host") or "").split(":")[0].lower()
        return host in ("127.0.0.1", "localhost")

    def _json(self, code: int, obj: dict) -> None:
        data = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("content-type", "application/json; charset=utf-8")
        self.send_header("content-length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if not self._local_only():
            return self._json(403, {"error": "local only"})
        if self.path == "/api/health":
            c = claude()
            return self._json(200, {"ok": True, "has_key": bool(c.key), "spent_usd": round(c.spent, 6), "max_usd": c.max_usd})
        return super().do_GET()

    def do_POST(self):
        if not self._local_only():
            return self._json(403, {"error": "local only"})
        routes = {"/api/case": (run_case, 10_000), "/api/save-run": (save_run, 400_000), "/api/save-baseline": (save_baseline, 20_000)}
        if self.path not in routes:
            return self._json(404, {"error": "not found"})
        try:
            fn, cap = routes[self.path]
            n = int(self.headers.get("content-length") or 0)
            if n > cap:
                raise R.EvalError("request too large")
            body = json.loads(self.rfile.read(n) or b"{}")
            return self._json(200, fn(body))
        except R.EvalError as e:
            return self._json(400, {"error": str(e)})
        except Exception:  # never leak internals
            return self._json(500, {"error": "the server could not run this case"})


def main() -> int:
    ap = argparse.ArgumentParser(description="Serve the prototype and run real evals with the key kept server-side.")
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--max-usd", type=float, default=0.50, help="budget guard for everything this server run spends")
    a = ap.parse_args()
    R.load_env()
    STATE["max_usd"] = a.max_usd
    has_key = bool(os.getenv("ANTHROPIC_API_KEY"))
    srv = ThreadingHTTPServer(("127.0.0.1", a.port), Handler)
    print(f"\n  Eval server on http://127.0.0.1:{a.port}/trip-planner.html  (this computer only)")
    print(f"  API key found: {'yes' if has_key else 'NO: mock modes still work'}  ·  budget guard ${a.max_usd:.2f}  ·  Ctrl+C to stop\n")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\n  stopped")
    return 0


if __name__ == "__main__":
    sys.exit(main())
