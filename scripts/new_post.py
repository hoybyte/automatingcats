
#!/usr/bin/env python3
"""Create a new Markdown draft for Automating Cats."""

import json
import re
import subprocess
import sys
import unicodedata

from datetime import date
from pathlib import Path


# Locate the project relative to this script.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
POST_DIRECTORY = PROJECT_ROOT / "src" / "content" / "blog"

CATEGORIES = {
    "1": "Development",
    "2": "Projects",
    "3": "Life",
}


def make_slug(title: str) -> str:
    """Convert an article title to a URL-friendly filename."""
    normalized = unicodedata.normalize("NFKD", title)
    ascii_title = normalized.encode("ascii", "ignore").decode("ascii")

    slug = ascii_title.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)

    return slug.strip("-")


def get_required_input(prompt: str) -> str:
    """Keep asking until the user supplies a value."""
    while True:
        value = input(prompt).strip()

        if value:
            return value

        print("This field cannot be empty.")


def choose_category() -> str:
    """Display available categories and validate the selection."""
    print("\nChoose a category:")

    for number, category in CATEGORIES.items():
        print(f"  {number}. {category}")

    while True:
        choice = input("\nCategory number: ").strip()

        if choice in CATEGORIES:
            return CATEGORIES[choice]

        print("Please enter 1, 2, or 3.")


def get_tags() -> list[str]:
    """Read comma-separated tags."""
    raw_tags = input("Tags (comma-separated): ").strip()

    if not raw_tags:
        return []

    tags = [tag.strip() for tag in raw_tags.split(",")]

    # Remove empty and duplicate tags.
    return list(dict.fromkeys(tag for tag in tags if tag))


def create_post(
    title: str,
    description: str,
    category: str,
    tags: list[str],
) -> Path:
    """Write a new draft without overwriting existing posts."""

    slug = make_slug(title)

    if not slug:
        raise ValueError(
            "The title must contain letters or numbers "
            "that can form a filename."
        )

    POST_DIRECTORY.mkdir(parents=True, exist_ok=True)

    post_path = POST_DIRECTORY / f"{slug}.md"

    # JSON strings and arrays are valid YAML frontmatter values.
    content = f"""---
title: {json.dumps(title, ensure_ascii=False)}
description: {json.dumps(description, ensure_ascii=False)}
pubDate: {date.today().isoformat()}
category: {json.dumps(category)}
tags: {json.dumps(tags, ensure_ascii=False)}
draft: true
---

## Introduction

Write your introduction here.

## The Challenge

What problem were you trying to solve?

## What I Learned

Document your discoveries and lessons.

## Final Thoughts

What would you do differently next time?
"""

    # Mode "x" refuses to overwrite an existing file.
    with post_path.open("x", encoding="utf-8") as file:
        file.write(content)

    return post_path


def main() -> None:
    """Run the interactive article generator."""
    print("=" * 45)
    print("       Automating Cats - New Post")
    print("=" * 45)

    title = get_required_input("\nArticle title: ")
    description = get_required_input("Description: ")
    category = choose_category()
    tags = get_tags()

    try:
        post_path = create_post(
            title=title,
            description=description,
            category=category,
            tags=tags,
        )

    except FileExistsError:
        print("\nError: An article with this filename already exists.")
        sys.exit(1)

    except (OSError, ValueError) as error:
        print(f"\nError: {error}")
        sys.exit(1)

    print("\nDraft created successfully!")
    print(f"File: {post_path.relative_to(PROJECT_ROOT)}")
    print("\nRemember: draft: true keeps it off the published site.")

    answer = input("\nOpen in Neovim? [Y/n]: ").strip().lower()

    if answer in ("", "y", "yes"):
        try:
            subprocess.run(
                ["nvim", str(post_path)],
                check=True,
            )
        except (OSError, subprocess.CalledProcessError) as error:
            print(f"Could not open Neovim: {error}")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nCancelled.")
        sys.exit(1)
