"""MkDocs hook: build the navigation and page titles from the docs/ folder itself.

Nothing to keep in sync: rename, add, move or delete pages and folders in Obsidian and the menu follows.

  Sections (top tabs)  = folders under docs/. Order: `doc: order: N` in the folder's index.md
                         frontmatter, then alphabetical. Tab label: that index.md's first "# Heading".
  Pages in a section   = its .md files, index.md first, then by file name (prefix 01-, 02- to order).
  Page title           = first "# Heading"; if the page has none, the file name without its number
                         prefix: "01-getting-started" -> "Getting started", "01 Getting Started" -> "Getting Started".
Folders without any .md file (e.g. assets/) are skipped.
"""
import logging
import posixpath
import re

from mkdocs.utils.meta import get_data

log = logging.getLogger("mkdocs.hooks.autonav")

H1 = re.compile(r"^#\s+(.+?)\s*#*\s*$", re.M)


def pretty(name):
    stem = posixpath.splitext(posixpath.basename(name))[0]
    words = re.sub(r"[-_]+", " ", re.sub(r"^\d+[\s._-]*", "", stem)).strip() or stem
    return words if words != words.lower() else words[0].upper() + words[1:]


def _read(f):
    try:
        body, meta = get_data(f.content_string)
    except Exception:  # unreadable page must not take the menu down
        body, meta = "", {}
    if f.content_string.lstrip("﻿").startswith("---") and not meta:
        log.warning("%s: frontmatter (the --- block at the top) is not valid YAML", f.src_uri)
    doc = meta.get("doc") if isinstance(meta.get("doc"), dict) else {}
    h1 = H1.search(body)
    return (h1.group(1).strip() if h1 else None), doc.get("order")


def _section(folder, tree, pages):
    """Return a nav entry for one folder: {title: [index, pages..., subsections...]}."""
    index = posixpath.join(folder, "index.md") if folder else "index.md"
    files = sorted(p for p in tree.get(folder, []) if p != index)
    subs = sorted(_order_key(d, pages) + (d,) for d in tree if posixpath.dirname(d) == folder and d != folder)
    items = ([index] if index in pages else []) + files + [_section(d, tree, pages) for *_, d in subs]
    title = (pages[index][0] if index in pages else None) or pretty(folder)
    return {title: items}


def _order_key(folder, pages):
    order = pages.get(posixpath.join(folder, "index.md"), (None, None))[1]
    return (0, order, "") if isinstance(order, (int, float)) else (1, 0, folder.lower())


def on_files(files, config, **kwargs):
    pages, tree = {}, {}
    for f in files.documentation_pages():
        pages[f.src_uri] = _read(f)
        folder = posixpath.dirname(f.src_uri)
        tree.setdefault(folder, []).append(f.src_uri)
        while folder:  # make sure every parent folder exists in the tree
            folder = posixpath.dirname(folder)
            tree.setdefault(folder, [])
    root = _section("", tree, pages)
    config["nav"] = next(iter(root.values()))  # the root's items: Home, then one entry per section
    if "index.md" in pages:
        config["nav"][0] = {"Home": "index.md"}
    return files


def on_page_markdown(markdown, page, **kwargs):
    if not H1.search(markdown):  # no "# Heading": show the cleaned-up file name as the title
        return f"# {pretty(page.file.src_uri)}\n\n{markdown}"
    return markdown
