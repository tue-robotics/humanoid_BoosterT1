"""MkDocs hook: convert Obsidian wikilinks to ordinary Markdown links at build time.

Replaces mkdocs-ezlinks-plugin (Windows path bug, fussy about spaces). Resolution follows Obsidian:
the target is matched by file name anywhere under docs/ (case-insensitive; spaces, hyphens and
underscores are treated alike), or by a path suffix such as [[tutorials/index]].

  [[page]]  [[page#Heading]]  [[page|alias]]  [[#Heading]]  ![[image.png]]

The output is a relative Markdown link, so MkDocs' own link validation still checks it.
An unresolved or ambiguous link logs a WARNING: fatal under `strict`, harmless in a lenient preview.
Code blocks and inline code are left untouched.
"""
import logging
import posixpath
import re

from markdown.extensions.toc import slugify

log = logging.getLogger("mkdocs.hooks.wikilinks")

WIKILINK = re.compile(r"(!?)\[\[([^\]|#]*)(?:#([^\]|]*))?(?:\|([^\]]*))?\]\]")
CODE = re.compile(r"(^(?P<fence>```|~~~).*?^(?P=fence)[^\n]*$|`[^`\n]+`)", re.S | re.M)


def _key(name):
    return re.sub(r"[\s_-]+", "-", name.strip().lower())


def _index(files):
    idx = {}
    for f in files:
        uri = f.src_uri
        stem = uri[:-3] if uri.endswith(".md") else uri
        for k in {_key(posixpath.basename(stem)), _key(posixpath.basename(uri)), _key(stem)}:
            idx.setdefault(k, []).append(uri)
    return idx


def _convert(text, page_uri, idx):
    def repl(m):
        embed, alias = m.group(1), m.group(4)
        # inside a table cell the alias separator is written "\|": drop the escaping backslash
        target = m.group(2).strip().rstrip("\\").strip()
        anchor = m.group(3).rstrip("\\") if m.group(3) else None
        frag = "#" + slugify(anchor.strip(), "-") if anchor else ""
        label = (alias or (target + (" > " + anchor if anchor else "") if target else anchor or "")).strip()
        if not target:  # [[#Heading]] -> same page
            return f"[{label}]({frag})"
        hits = sorted(set(idx.get(_key(target), [])))
        if len(hits) != 1:
            why = "not found" if not hits else f"ambiguous ({', '.join(hits)})"
            log.warning("%s: wikilink [[%s]] %s", page_uri, m.group(2), why)
            return label
        rel = posixpath.relpath(hits[0], posixpath.dirname(page_uri) or ".")
        dest = f"<{rel}{frag}>" if " " in rel else f"{rel}{frag}"
        return f"{embed}[{label}]({dest})"

    return WIKILINK.sub(repl, text)


def on_page_markdown(markdown, page, config, files, **kwargs):
    idx = _index(files)
    out, pos = [], 0
    for m in CODE.finditer(markdown):
        out.append(_convert(markdown[pos:m.start()], page.file.src_uri, idx))
        out.append(m.group(0))
        pos = m.end()
    out.append(_convert(markdown[pos:], page.file.src_uri, idx))
    return "".join(out)
