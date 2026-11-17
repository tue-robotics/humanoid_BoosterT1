#!/usr/bin/env python3
"""Build the whole published site: master at the root, every other branch as a preview.

    site/                      master (reviewed), strict build + wikilink check
    site/branch/<slug>/        one lenient build per other branch, e.g. docs/x -> docs-x
    site/versions.json         list of the builds, read by versions.js
    site/versions.js           branch picker in the sidebar + banner on previews
    site/heads.json            branch -> commit seen at build time, for --changed

Each branch is built from its own mkdocs.yml, docs/ and hooks (a git worktree), so a branch shows
exactly what it would look like once merged. Branches without a mkdocs.yml are ignored.

If the newest commit of a branch fails to build, the commit that built last time (read from the live
site's versions.json) is built instead, and the page banner says so. Only when master fails with no
working fallback does the run fail; the live site then stays as it was.

Run from the repo root after `git fetch` (CI: actions/checkout with fetch-depth 0).
Usage: python tools/docs/build_all.py [--site site] [--remote origin] [--main master]
       python tools/docs/build_all.py --changed    print true/false: does the live site need a rebuild?
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

HERE = Path(__file__).resolve().parent


def git(*args, cwd=None):
    return subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True,
                          text=True).stdout.strip()


def has(spec, cwd):
    return subprocess.run(["git", "cat-file", "-e", spec], cwd=cwd,
                          capture_output=True).returncode == 0


def fetch_json(url):
    """Live file from the published site, or None (first run, offline, old format)."""
    try:
        with urllib.request.urlopen(url, timeout=20) as r:
            return json.load(r)
    except Exception:
        return None


def slug(branch):
    return re.sub(r"[^A-Za-z0-9._-]+", "-", branch).strip("-")


def heads(repo, remote):
    """branch -> full commit id, for every remote branch."""
    out = git("for-each-ref", "--format=%(refname:strip=3) %(objectname)",
              f"refs/remotes/{remote}", cwd=repo)
    return dict(line.split(" ", 1) for line in out.splitlines()
                if line and not line.startswith("HEAD "))


class Builder:
    def __init__(self, repo, tmp):
        self.repo, self.tmp, self.n = repo, tmp, 0

    def build(self, commit, out, strict, site_url):
        """Build one commit into out. True on success; out is removed on failure."""
        self.n += 1
        wt = self.tmp / f"wt{self.n}"
        git("worktree", "add", "--detach", str(wt), commit, cwd=self.repo)
        cfg = wt / "_build_all.mkdocs.yml"  # same config, own site_url
        cfg.write_text(f"INHERIT: mkdocs.yml\nsite_url: {site_url}\n", encoding="utf-8")
        env = dict(os.environ, DOCS_STRICT="true" if strict else "false")
        cmd = [sys.executable, "-m", "mkdocs", "build", "-f", str(cfg), "-d", str(out)]
        ok = subprocess.run(cmd + (["--strict"] if strict else []), cwd=wt, env=env).returncode == 0
        if ok and strict:
            ok = subprocess.run([sys.executable, str(HERE / "check_wikilink_leak.py"),
                                 str(out)]).returncode == 0
        if not ok:
            shutil.rmtree(out, ignore_errors=True)
        return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--site", default="site")
    ap.add_argument("--remote", default="origin")
    ap.add_argument("--main", default="master")
    ap.add_argument("--changed", action="store_true")
    a = ap.parse_args()

    repo = Path(git("rev-parse", "--show-toplevel"))
    m = re.search(r"^site_url:\s*(\S+)", (repo / "mkdocs.yml").read_text(encoding="utf-8"), re.M)
    root_url = m.group(1).rstrip("/") + "/"   # https://tue-robotics.github.io/humanoid_BoosterT1/
    now = heads(repo, a.remote)

    if a.changed:
        print("true" if fetch_json(root_url + "heads.json") != now else "false")
        return 0

    # Last good commit per branch on the live site; used when the newest commit fails.
    live = fetch_json(root_url + "versions.json")
    last_good = {v["branch"]: v["sha"] for v in live or [] if isinstance(v, dict) and "sha" in v}

    site = (repo / a.site).resolve()
    shutil.rmtree(site, ignore_errors=True)
    branches = [a.main] + sorted(b for b in now if b != a.main)
    versions = []
    tmp = Path(tempfile.mkdtemp(prefix="docs-branches-"))
    b_ = Builder(repo, tmp)
    try:
        for b in branches:
            head = now.get(b)
            if not head or not has(f"{head}:mkdocs.yml", repo):
                print(f"skip {b}: no mkdocs.yml")
                continue
            main = b == a.main
            path = "" if main else f"branch/{slug(b)}/"
            out, url = site / path, root_url + path
            entry = {"branch": b, "path": path, "reviewed": main}
            # master is first and strict; the branch builds land in subfolders of its output.
            ok = b_.build(head, out, main, url)
            built = head
            if not ok:
                prev = last_good.get(b)
                print(f"::warning::docs for branch {b} failed to build at {head[:7]}")
                if prev and prev != head and has(f"{prev}^{{commit}}", repo) \
                        and b_.build(prev, out, main, url):
                    built = prev
                    entry["failed_commit"] = head[:7]
                    print(f"::warning::{b}: published the last good build {prev[:7]} instead")
                elif main:
                    print(f"::error::{a.main} failed and has no working fallback; nothing published")
                    return 1
                else:
                    print(f"::warning::{b}: no earlier good build; left out")
                    continue
            entry.update(sha=built, commit=built[:7])
            versions.append(entry)
    finally:
        for wt in tmp.iterdir():
            subprocess.run(["git", "worktree", "remove", "--force", str(wt)], cwd=repo)
        shutil.rmtree(tmp, ignore_errors=True)

    (site / "versions.json").write_text(json.dumps(versions, indent=2), encoding="utf-8")
    (site / "heads.json").write_text(json.dumps(now, indent=2), encoding="utf-8")
    shutil.copy(HERE / "versions.js", site / "versions.js")
    tag = f'<script src="{urlparse(root_url).path}versions.js" defer></script>'
    for f in site.rglob("*.html"):
        html = f.read_text(encoding="utf-8")
        f.write_text(html.replace("</head>", f"{tag}\n</head>", 1), encoding="utf-8")
    print("Built:", ", ".join(f"{v['branch']} {v['commit']} -> /{v['path']}" for v in versions))
    return 0


if __name__ == "__main__":
    sys.exit(main())
