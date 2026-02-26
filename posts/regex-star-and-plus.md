---
title: "How * and + Work in Regex"
date: "2018-09-12"
description: "A clear explanation of the + and * quantifiers in regular expressions, with practical examples."
tags: ["regex", "explainer"]
---

`+` and `*` are both quantifiers. They don't themselves match any pattern but check for repetition or presence of the pattern they follow. One example will clear things up.

Assume we want to match some numbers:

* 9
* 90
* 234
* 2275258292335728520

To match numbers we can use character class `[0-9]` or `\d`, both work the same. But there is one problem — `\d` or `[0-9]` both match a number with one digit only, i.e. will match 9 but not numbers with more digits. So to match two digit numbers our regex should be `\d\d`, for three digits `\d\d\d` and so on. You see the problem?

Firstly, it's tiring to write repeating characters and secondly what if we don't know the count of digits beforehand. Here come the quantifiers to the rescue.

`+` → matches **one or more** of the pattern it's used after.
`*` → matches **zero or more** of the pattern it's used after.

Going back to the previous example, we want to match numbers be it one digit or more. We make our regex `\d+` — one `+` after the digit-matching pattern `\d`. Now it matches all of the numbers.

Now let's imagine a scenario where we want to match `a` that has no `b` after it, or lots of `b`:

* a
* ab
* abbbb

We need a regex that matches all three. If we write `ab+` we fail to match the lone `a`, because `+` requires at least one `b`. Here we use `*`. It matches none or more of the pattern, so `ab*` matches all three strings including the first where there is no `b`.

Hope this demystifies `*` and `+` for you.
