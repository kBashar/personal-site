# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Commands

```bash
# Set up environment (first time)
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Build blog (Markdown → HTML) — run after editing any posts/*.md
python build.py

# Serve locally
python -m http.server 8000
# → http://localhost:8000
```

## Architecture

This is a static site: no build framework, no bundler. HTML pages are served directly. The only build step is `build.py`, which generates blog output from Markdown source.

### Page structure

The four hand-authored pages (`index.html`, `about.html`, `portfolio.html`, `contact.html`) live at the root. `blog/index.html` and `blog/posts/*.html` are **generated** — never edit them directly.

### Blog pipeline

```
posts/*.md  →  build.py  →  blog/posts/<slug>.html
                         →  blog/index.html
```

`build.py` uses `templates/post.html` and `templates/blog-listing.html` as shells. Placeholders use `{{double_braces}}` and are filled with `str.replace()` — no template engine. The slug comes from the filename (not the title), keeping URLs stable.

Front matter format:
```yaml
---
title: "Post Title"
date: "YYYY-MM-DD"
description: "One-line summary."
tags: ["tag1", "tag2"]
---
```

### CSS architecture

`assets/css/style.css` defines all color tokens and spacing via CSS custom properties at `:root`. Dark mode is a single `data-theme="dark"` attribute on `<html>` that overrides the color tokens — no class toggling, no duplicate rules. `assets/css/blog.css` adds prose typography only for post pages and the blog listing.

Layout primitives (`.container`, `.prose`, `.grid-2`) are defined in `style.css` and used directly in HTML — no utility-class system.

### JS

`assets/js/main.js` handles three things only: mobile nav toggle, dark/light theme toggle (reads/writes `localStorage`), and active nav link highlighting. No dependencies.

### Asset paths

Path depth varies by page level:
- Root pages (`index.html` etc.): `assets/css/style.css`, `assets/js/main.js`
- `blog/index.html`: `../assets/css/style.css`, `../assets/js/main.js`
- `blog/posts/*.html`: `../../assets/css/style.css`, `../../assets/js/main.js`

The templates already have the correct relative paths for generated post pages.

## Adding Content

**New blog post:** create `posts/<slug>.md` with YAML front matter, run `python build.py`, commit everything including the generated files in `blog/`.

**New project card:** edit the `.grid-2` section in `portfolio.html` and the featured strip in `index.html`.

## Deployment

GitHub Actions (`.github/workflows/deploy.yml`) runs on push to `main`: installs deps → `python build.py` → deploys to GitHub Pages. The repo must have Pages source set to "GitHub Actions" in Settings → Pages. Generated files are committed to the repo so the site is browsable without CI.
