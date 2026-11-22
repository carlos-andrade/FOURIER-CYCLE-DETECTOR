#!/usr/bin/env python3
"""Validate explicit indicator scope in pull requests and reject execution paths."""
from __future__ import annotations
import json
import os
import sys
import urllib.request

MARKER = "FOURIER-INDICATOR-SCOPE:"
ALLOWED = {
    "INDICATOR_SPECIFICATION", "INDICATOR_MATHEMATICS",
    "INDICATOR_IMPLEMENTATION", "INDICATOR_VALIDATION",
    "NTSL_PORT", "VISUAL_DESIGN", "INTEGRATION", "DOCUMENTATION",
    "OUT_OF_SCOPE",
}
FORBIDDEN = ("/broker/", "/brokers/", "/execution/", "/order_router/",
             "/order-routing/", "/live_trading/")


def api_get(url: str, token: str):
    request = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    })
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.load(response)


def main() -> int:
    with open(os.environ["GITHUB_EVENT_PATH"], encoding="utf-8") as handle:
        event = json.load(handle)
    pr = event.get("pull_request")
    if not pr:
        print("No pull request payload; skipped.")
        return 0
    body = pr.get("body") or ""
    lines = [line for line in body.splitlines() if MARKER in line]
    if not lines:
        print(f"FAIL: PR body must declare {MARKER} <TYPE> and name the indicator.")
        return 1
    declaration = lines[0].split(MARKER, 1)[1].strip()
    kind = declaration.split()[0] if declaration else ""
    if kind not in ALLOWED:
        print(f"FAIL: invalid scope type {kind!r}; allowed: {sorted(ALLOWED)}")
        return 1

    repo = os.environ["GITHUB_REPOSITORY"]
    token = os.environ["GITHUB_TOKEN"]
    number = pr["number"]
    changed = []
    page = 1
    while True:
        batch = api_get(
            f"https://api.github.com/repos/{repo}/pulls/{number}/files?per_page=100&page={page}",
            token,
        )
        changed.extend(batch)
        if len(batch) < 100:
            break
        page += 1

    violations = [
        item["filename"] for item in changed
        if any(part in ("/" + item["filename"].lower()) for part in FORBIDDEN)
    ]
    if violations:
        print("FAIL: broker/order-execution paths are outside default indicator scope:")
        for path in violations:
            print(f" - {path}")
        print("Obtain explicit owner authorization and document the scope change.")
        return 1
    print(f"PASS: declared {kind}; inspected {len(changed)} changed file(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
