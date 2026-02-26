#!/usr/bin/env python3
"""
build.py — Markdown → HTML blog builder

Reads .md files from ./posts/, converts to HTML using ./templates/post.html,
writes output to ./blog/posts/<slug>.html, and regenerates ./blog/index.html
from ./templates/blog-listing.html.

Front matter format (YAML between --- delimiters):
    ---
    title: "Post Title"
    date: "2026-02-20"
    description: "One-line summary."
    tags: ["tag1", "tag2"]
    ---
"""

import os
import sys
import re
from datetime import datetime
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Error: PyYAML not installed. Run: pip install -r requirements.txt", file=sys.stderr)
    sys.exit(1)

try:
    import markdown
except ImportError:
    print("Error: Markdown not installed. Run: pip install -r requirements.txt", file=sys.stderr)
    sys.exit(1)


# ── Paths ─────────────────────────────────────────────────────────────────────
ROOT         = Path(__file__).parent
POSTS_SRC    = ROOT / "posts"
POSTS_OUT    = ROOT / "blog" / "posts"
TEMPLATE_POST    = ROOT / "templates" / "post.html"
TEMPLATE_LISTING = ROOT / "templates" / "blog-listing.html"
LISTING_OUT  = ROOT / "blog" / "index.html"

# ── Markdown extensions ───────────────────────────────────────────────────────
MD_EXTENSIONS = ["fenced_code", "tables", "toc", "nl2br"]


def slugify(text: str) -> str:
    """Convert a string to a URL-safe slug."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    text = re.sub(r"^-+|-+$", "", text)
    return text


def parse_frontmatter(source: str) -> tuple[dict, str]:
    """
    Split a Markdown file into (front_matter_dict, body_markdown).
    Expects the file to start with '---' and have a closing '---'.
    """
    source = source.strip()
    if not source.startswith("---"):
        return {}, source

    # Find closing delimiter
    end = source.find("\n---", 3)
    if end == -1:
        return {}, source

    raw_yaml = source[3:end].strip()
    body = source[end + 4:].strip()  # skip '\n---'

    try:
        front = yaml.safe_load(raw_yaml) or {}
    except yaml.YAMLError as exc:
        print(f"  Warning: YAML parse error — {exc}")
        front = {}

    return front, body


def format_date(date_str: str) -> str:
    """Format ISO date string to human-readable form: 'Feb 20, 2026'."""
    try:
        dt = datetime.strptime(str(date_str), "%Y-%m-%d")
        return dt.strftime("%b %-d, %Y")
    except (ValueError, TypeError):
        return str(date_str)


def build_tags_html(tags: list) -> str:
    """Render a list of tags as <span class='tag'>...</span> elements."""
    if not tags:
        return ""
    spans = [f'<span class="tag">{tag}</span>' for tag in tags]
    return "\n".join(spans)


def build_post(md_path: Path, post_template: str) -> dict | None:
    """
    Process a single Markdown file into an HTML post.
    Returns metadata dict on success, None on failure.
    """
    print(f"  Processing: {md_path.name}")

    source = md_path.read_text(encoding="utf-8")
    front, body = parse_frontmatter(source)

    title       = front.get("title", md_path.stem.replace("-", " ").title())
    date        = front.get("date", "")
    description = front.get("description", "")
    tags        = front.get("tags", [])

    # Derive slug from filename (not title) for stable URLs
    slug = md_path.stem

    # Convert Markdown body to HTML
    content_html = markdown.markdown(body, extensions=MD_EXTENSIONS)

    # Build tags HTML
    tags_html = build_tags_html(tags)

    # Fill template
    html = post_template
    html = html.replace("{{title}}", str(title))
    html = html.replace("{{date}}", str(date))
    html = html.replace("{{date_formatted}}", format_date(str(date)))
    html = html.replace("{{description}}", str(description))
    html = html.replace("{{content}}", content_html)
    html = html.replace("{{tags_html}}", tags_html)

    # Write output
    out_path = POSTS_OUT / f"{slug}.html"
    out_path.write_text(html, encoding="utf-8")
    print(f"  → Written: {out_path.relative_to(ROOT)}")

    return {
        "title":       title,
        "date":        str(date),
        "description": description,
        "tags":        tags,
        "slug":        slug,
    }


def build_listing(posts: list[dict], listing_template: str) -> None:
    """Generate blog/index.html from sorted post metadata."""
    items = []
    for post in posts:
        tags_html = build_tags_html(post["tags"])
        date_fmt  = format_date(post["date"])
        item = f"""          <article class="blog-post-item">
            <time class="blog-post-date" datetime="{post['date']}">{date_fmt}</time>
            <div>
              <a href="posts/{post['slug']}.html" class="blog-post-title">{post['title']}</a>
              <p class="blog-post-desc">{post['description']}</p>
              <div class="blog-post-tags">{tags_html}</div>
            </div>
          </article>"""
        items.append(item)

    post_list_html = "\n".join(items) if items else "<p>No posts yet.</p>"

    html = listing_template.replace("{{post_list_html}}", post_list_html)
    LISTING_OUT.write_text(html, encoding="utf-8")
    print(f"  → Written: {LISTING_OUT.relative_to(ROOT)}")


def main() -> None:
    print("build.py — starting")

    # Ensure output directory exists
    POSTS_OUT.mkdir(parents=True, exist_ok=True)

    # Load templates
    if not TEMPLATE_POST.exists():
        print(f"Error: template not found: {TEMPLATE_POST}", file=sys.stderr)
        sys.exit(1)
    if not TEMPLATE_LISTING.exists():
        print(f"Error: template not found: {TEMPLATE_LISTING}", file=sys.stderr)
        sys.exit(1)

    post_template    = TEMPLATE_POST.read_text(encoding="utf-8")
    listing_template = TEMPLATE_LISTING.read_text(encoding="utf-8")

    # Collect Markdown source files
    md_files = sorted(POSTS_SRC.glob("*.md"))
    if not md_files:
        print("  No .md files found in posts/. Creating empty blog index.")

    # Build each post
    print(f"\nBuilding {len(md_files)} post(s)...")
    posts_index: list[dict] = []
    for md_path in md_files:
        meta = build_post(md_path, post_template)
        if meta:
            posts_index.append(meta)

    # Sort by date descending (newest first); missing dates go last
    def sort_key(p: dict) -> str:
        return p.get("date", "") or ""

    posts_index.sort(key=sort_key, reverse=True)

    # Build listing
    print("\nBuilding blog index...")
    build_listing(posts_index, listing_template)

    print(f"\nDone — {len(posts_index)} post(s) built.")


if __name__ == "__main__":
    main()
