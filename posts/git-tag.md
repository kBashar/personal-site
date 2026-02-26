---
title: "git tag"
date: "2022-11-24"
description: "A quick reference on git tag — creating, listing, pushing, and the difference between lightweight and annotated tags."
tags: ["git", "devtools"]
---

`git tag` marks a specific commit in the source repository. A common use case is to denote software release versions by marking the points of commit history where the software was stable to release.

1. `git tag` gives the list of all tags.
2. `git tag <tagname>` creates a tag named **tagname**. This tag points to the commit that was HEAD at the time of tag creation.
3. Tags can be made to point to any commit, not just HEAD.
4. Tags are not pushed to the remote by default. Use `git push <remotename> <tagname>` to push one.
5. To push all tags at once: `git push <remotename> --tags`
6. `git tag -d <tagname>` deletes a tag from the repo.
7. There are two types of tags: **lightweight** and **annotated**. Lightweight tags have only a name. Annotated tags contain additional metadata — the author's name, email, and an annotation message. By default `git tag <tagname>` creates a lightweight tag. To create an annotated tag: `git tag -a -m "annotation msg" <tagname>`.
