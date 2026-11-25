// Branch picker and preview banner for the published site. build_all.py copies this file to the site
// root and adds it to every page; it is not part of a normal mkdocs build or the local preview.
// Reads versions.json: [{branch, path, reviewed, commit}], master first with path "".
(function () {
  const root = new URL(".", document.currentScript.src).href;

  // Draw from the copy of the previous page first, so the picker does not push the menu down later.
  const key = "dx-versions " + root;
  let cached = null;
  try { cached = JSON.parse(sessionStorage.getItem(key)); } catch {}
  if (cached) render(cached);

  fetch(root + "versions.json")
    .then((r) => r.json())
    .then((versions) => {
      try { sessionStorage.setItem(key, JSON.stringify(versions)); } catch {}
      if (!cached) render(versions);
    })
    .catch(() => {}); // no versions.json: show nothing

  function render(versions) {
    // Current build = the one whose folder is the longest prefix of this page's address.
    const here = location.href.split("#")[0].split("?")[0];
    const current = versions
      .filter((v) => here.startsWith(root + v.path))
      .sort((a, b) => b.path.length - a.path.length)[0];
    if (!current) return;
    const rest = here.slice((root + current.path).length); // page path inside the build

    // Picker, placed in the left sidebar right under the search box (above the repo link).
    const box = document.createElement("div");
    box.className = "dx-version";
    box.innerHTML = '<label for="dx-version-select">Branch</label>';
    const select = document.createElement("select");
    select.id = "dx-version-select";
    for (const v of versions) {
      const o = document.createElement("option");
      o.value = v.path;
      o.textContent = v.reviewed ? v.branch + " (reviewed)" : v.branch;
      o.selected = v === current;
      select.append(o);
    }
    select.addEventListener("change", () => {
      const base = root + select.value;
      // Same page on the other branch if it exists there, else that branch's home page.
      fetch(base + rest, { method: "HEAD" })
        .then((r) => (location.href = r.ok ? base + rest : base))
        .catch(() => (location.href = base));
    });
    box.append(select);
    const side = ".md-sidebar--primary ";
    const search = document.querySelector(side + ".md-search");
    const brand = document.querySelector(side + ".dx-brand");
    const inner = document.querySelector(side + ".md-sidebar__inner");
    if (search) search.after(box);
    else if (brand) brand.after(box);
    else if (inner) inner.prepend(box);

    // Banner on every preview page, and on any build that fell back to an older commit.
    if (!current.reviewed || current.failed_commit) {
      const main = versions.find((v) => v.reviewed) || versions[0];
      const banner = document.createElement("div");
      banner.className = "dx-preview-banner";
      const parts = [];
      if (!current.reviewed)
        parts.push(
          "Preview of branch <code data-f=branch></code> (commit <code data-f=commit></code>). " +
            'Not reviewed: it may be wrong, change or disappear. <a href="">Open the reviewed version</a>.'
        );
      if (current.failed_commit)
        parts.push(
          "The newest commit <code data-f=failed_commit></code> failed to build; this is the last " +
            "version that built (<code data-f=commit></code>)."
        );
      banner.innerHTML = parts.join(" ");
      banner.querySelectorAll("code").forEach((c) => (c.textContent = current[c.dataset.f]));
      const link = banner.querySelector("a");
      if (link) link.href = root + main.path;
      const content = document.querySelector(".md-content__inner") || document.body;
      content.prepend(banner);
    }

    const css = document.createElement("style");
    css.textContent = `
      .dx-version { padding: 0.5rem 0.44rem 0; font-size: 0.66rem; }
      .dx-version label { display: block; margin-bottom: 0.15rem;
        color: var(--md-default-fg-color--light); }
      .dx-version select { width: 100%; padding: 0.2rem 0.3rem; font: inherit;
        color: var(--md-default-fg-color); background: var(--md-default-bg-color);
        border: 1px solid var(--md-default-fg-color--lighter); border-radius: 0.2rem; }
      .dx-preview-banner { margin: 0 0 1.2rem; padding: 0.6rem 0.8rem; font-size: 0.7rem;
        border-left: 0.2rem solid #e0a100; background: rgba(224, 161, 0, 0.12);
        border-radius: 0.2rem; }
      .dx-preview-banner code { font-size: 0.65rem; }`;
    document.head.append(css);
  }
})();
