#!/usr/bin/env python3
"""Fail if built site/ HTML contains a literal "[[" outside <code>/<pre>.

Simple HTMLParser-based scan: text inside <code> and <pre> is ignored.
Usage: python tools/docs/check_wikilink_leak.py [site_dir]
"""
import sys
from html.parser import HTMLParser
from pathlib import Path


class Scanner(HTMLParser):
    def __init__(self):
        super().__init__()
        self.depth = 0
        self.hit = False

    def handle_starttag(self, tag, attrs):
        if tag in ("code", "pre"):
            self.depth += 1

    def handle_endtag(self, tag):
        if tag in ("code", "pre") and self.depth:
            self.depth -= 1

    def handle_data(self, data):
        if not self.depth and "[[" in data:
            self.hit = True


def main():
    site = Path(sys.argv[1] if len(sys.argv) > 1 else "site")
    if not site.is_dir():
        print(f"ERROR: {site} not found; build first")
        return 2
    bad = []
    for f in sorted(site.rglob("*.html")):
        s = Scanner()
        s.feed(f.read_text(encoding="utf-8", errors="replace"))
        if s.hit:
            bad.append(f)
    if bad:
        print("Unresolved wikilinks ('[[') found in:")
        for f in bad:
            print(f"  {f}")
        return 1
    print("No leaked wikilinks.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
