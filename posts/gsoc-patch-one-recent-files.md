---
title: "Patch One: Recent Files Feature"
date: "2015-06-01"
description: "Notes from my first GSoC patch — implementing the recent files feature for PDFDebugger and a lesson on Java's Preference API."
tags: ["gsoc", "open-source", "java"]
---

Main code for this patch was ready for GSOC as I've coded it [earlier](https://issues.apache.org/jira/browse/PDFBOX-2748) for PDFReader of the PDFBox tools. So it was just about reusing the RecentFiles class with PDFDebugger.

From this patch I've learnt an interesting thing. In RecentFiles class I've used Preference API of java to store application preference data. [Preference API](http://docs.oracle.com/javase/7/docs/api/java/util/prefs/Preferences.html) gives you one instance per Package.

PDFReader and PDFDebugger both are in same the package so they show the same recent files log. Though I was first confused about the behaviour and was planning to move PDFDebugger to a new package but Tilman happened to like it :). So a potential bug became a feature. :)

### Patch link

[Jira comment of the patch](https://issues.apache.org/jira/browse/PDFBOX-2530?focusedCommentId=14553244&page=com.atlassian.jira.plugin.system.issuetabpanels:comment-tabpanel#comment-14553244)
