#!/usr/bin/env python3
"""Best-effort external-link audit for the scheduled CI workflow.

This is intentionally separate from deterministic validation. Network errors,
rate limits, and temporary upstream failures are reported as ``transient`` and
do not block ordinary pull requests.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from collections import Counter, defaultdict
from collections.abc import Mapping, Sequence
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

try:
    from .lib.loader import load_catalog
except ImportError:  # Direct execution.
    from lib.loader import load_catalog


ROOT = Path(__file__).resolve().parents[1]
LINK_TYPES = ("paper", "code", "article", "project", "artifact", "model", "dataset")
USER_AGENT = "awesome-kernel-agent-link-audit/2 (+https://github.com/youyve/awesome-kernel-agent)"


def _sequence(value: object) -> list[object]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        return []
    return list(value)


def collect_urls(catalog: Mapping[str, object]) -> dict[str, list[dict[str, str]]]:
    usages: dict[str, list[dict[str, str]]] = defaultdict(list)
    for entry in _sequence(catalog.get("agents")):
        if not isinstance(entry, Mapping):
            continue
        entry_id = str(entry.get("id"))
        links = entry.get("links")
        links = links if isinstance(links, Mapping) else {}
        for link_type in LINK_TYPES:
            for link in _sequence(links.get(link_type)):
                if isinstance(link, Mapping) and link.get("url"):
                    usages[str(link["url"])].append({"entry_id": entry_id, "type": link_type})
        for claim in _sequence(entry.get("claims")):
            if not isinstance(claim, Mapping):
                continue
            claim_id = str(claim.get("id"))
            source = claim.get("primary_source")
            if isinstance(source, Mapping) and source.get("url"):
                usages[str(source["url"])].append(
                    {"entry_id": entry_id, "type": "claim-primary-source", "claim_id": claim_id}
                )
            reproducibility = claim.get("reproducibility")
            if isinstance(reproducibility, Mapping) and reproducibility.get("artifact_url"):
                usages[str(reproducibility["artifact_url"])].append(
                    {"entry_id": entry_id, "type": "claim-artifact", "claim_id": claim_id}
                )
            baseline = claim.get("baseline")
            evidence = baseline.get("evidence") if isinstance(baseline, Mapping) else None
            if isinstance(evidence, Mapping) and evidence.get("url"):
                usages[str(evidence["url"])].append(
                    {"entry_id": entry_id, "type": "baseline-evidence", "claim_id": claim_id}
                )
    return dict(usages)


def _request(url: str, method: str, timeout: float) -> tuple[int, str]:
    headers = {"User-Agent": USER_AGENT, "Accept": "text/html,application/json;q=0.9,*/*;q=0.8"}
    if method == "GET":
        headers["Range"] = "bytes=0-1023"
    request = Request(url, headers=headers, method=method)
    with urlopen(request, timeout=timeout) as response:
        return int(response.status), response.geturl()


def _github_repo(url: str) -> tuple[str, str] | None:
    parsed = urlparse(url)
    if parsed.netloc.casefold() not in {"github.com", "www.github.com"}:
        return None
    parts = [part for part in parsed.path.split("/") if part]
    if len(parts) < 2:
        return None
    return parts[0], parts[1].removesuffix(".git")


def _github_archived(url: str, timeout: float) -> bool | None:
    repo = _github_repo(url)
    if repo is None:
        return None
    owner, name = repo
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = Request(f"https://api.github.com/repos/{owner}/{name}", headers=headers)
    try:
        with urlopen(request, timeout=timeout) as response:
            payload = json.load(response)
        return bool(payload.get("archived"))
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError):
        return None


def check_url(url: str, timeout: float = 15.0, retries: int = 2) -> dict[str, object]:
    last_error = ""
    status_code: int | None = None
    final_url = url
    for attempt in range(retries + 1):
        try:
            try:
                status_code, final_url = _request(url, "HEAD", timeout)
            except HTTPError:
                # A substantial number of valid paper/project hosts reject or
                # mis-handle HEAD. Confirm every HTTP failure with a bounded
                # GET before classifying a URL as broken.
                status_code, final_url = _request(url, "GET", timeout)
            if 200 <= status_code < 400:
                github_repo = _github_repo(final_url)
                archived = _github_archived(final_url, timeout) if github_repo else None
                archive_status = (
                    "not-applicable"
                    if github_repo is None
                    else "unknown"
                    if archived is None
                    else "yes"
                    if archived
                    else "no"
                )
                status = "archived" if archived else ("redirect" if final_url != url else "ok")
                return {
                    "url": url,
                    "status": status,
                    "http_status": status_code,
                    "final_url": final_url,
                    "github_archive_status": archive_status,
                }
            last_error = f"HTTP {status_code}"
        except HTTPError as exc:
            status_code = exc.code
            last_error = f"HTTP {exc.code}"
            if exc.code in {404, 410}:
                return {"url": url, "status": "broken", "http_status": exc.code, "error": last_error}
            if exc.code not in {408, 425, 429, 500, 502, 503, 504}:
                return {"url": url, "status": "unknown", "http_status": exc.code, "error": last_error}
        except (URLError, TimeoutError, OSError) as exc:
            last_error = str(exc)
        if attempt < retries:
            time.sleep(1.0 * (attempt + 1))
    return {
        "url": url,
        "status": "transient",
        "http_status": status_code,
        "error": last_error or "request failed",
    }


def run_audit(catalog: Mapping[str, object], workers: int, timeout: float) -> dict[str, object]:
    usages = collect_urls(catalog)
    results: list[dict[str, object]] = []
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(check_url, url, timeout): url for url in sorted(usages)}
        for future in as_completed(futures):
            result = future.result()
            result["usages"] = usages[futures[future]]
            results.append(result)
    results.sort(key=lambda result: str(result["url"]))
    counts = Counter(str(result["status"]) for result in results)
    return {
        "checked_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "total_unique_urls": len(results),
        "counts": dict(sorted(counts.items())),
        "results": results,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="write the JSON result to this path")
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--timeout", type=float, default=15.0)
    parser.add_argument(
        "--strict",
        action="store_true",
        help="return non-zero when a confirmed 404/410 is found",
    )
    args = parser.parse_args()
    if not 1 <= args.workers <= 16:
        parser.error("--workers must be between 1 and 16")

    report = run_audit(load_catalog(), args.workers, args.timeout)
    output = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
    else:
        sys.stdout.write(output)
    print(
        "link audit: " + ", ".join(f"{key}={value}" for key, value in report["counts"].items()),
        file=sys.stderr,
    )
    if args.strict and report["counts"].get("broken", 0):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
