---
title: "Getting Started with GitHub Actions"
date: "2022-12-17"
description: "A hands-on intro to GitHub Actions: build a workflow that compiles a Python script to an exe and publishes it as a release artifact."
tags: ["github", "ci-cd", "devtools"]
---

Github Actions is a CI/CD platform. The full software development life cycle can be managed using GitHub Actions.

To understand this tool we will go through an example implementation. All related concepts will be described along the way.

## Project Goal

Implement a GitHub Actions workflow that builds an exe from the project code and uploads it as a release artifact to the GitHub repository. This workflow runs whenever the repository owner pushes a new `tag`.

## Project Structure

We start with a tiny hello world Python project.

```
github-action-tutorial/
├─ main.py
├─ README.md
├─ requirements.txt
```

`main.py` takes a name as input and prints `hello <name>`. All code is [here](https://github.com/kBashar/github-action-tutorial).

GitHub Actions has the following concepts, discussed in the order they appear in a workflow file. Full code is at [the end](#code).

- [Workflows](#workflows)
- [Event](#event)
- [Runner](#runner)
- [Job](#job)
- [Code](#code)

### Workflows

* Workflows are *yml* files residing in `.github/workflows/` in a repository.
* A workflow defines operations to run when an event is triggered, and the computing platform to run them on.
* There can be more than one workflow in a repository, each triggered by different events.
* Example events: `push`, `pull_request`. See [all supported events](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows).

We create `exe-releaser.yml` inside `.github/workflows/`. Updated project structure:

```
github-action-tutorial/
├─ .github/
│  ├─ workflows/
│  │  ├─ exe-releaser.yml
├─ main.py
├─ README.md
├─ requirements.txt
```

Start the workflow file with a name and run-name:

```yml
name: learn-github-actions
run-name: ${{ github.actor }} is learning GitHub Actions
```

### Event

Workflows are triggered when a specific event happens. Our workflow should run whenever a `tag` is pushed:

```yml
on:
  push:
    tags:
      - "*"
```

### Runner

Each workflow job runs on a fresh virtual machine called a **runner**. GitHub provides Windows, Ubuntu, and macOS runners; you can also self-host.

We use Windows to build the exe:

```yml
jobs:
  build-release-exe:
    runs-on: windows-latest
```

### Job

A job is a series of **steps**. Steps use either `uses` (a pre-built action) or `run` (a shell command).

**Steps:**

1. Check out the repository:

```yml
steps:
  - name: Repo-Checkout
    uses: actions/checkout@v3
```

2. Install Python. The `with` key passes input parameters to the action:

```yml
  - name: Setup Python
    uses: actions/setup-python@v4
    with:
      python-version: '3.10'
      cache: 'pip'
      architecture: 'x64'
```

3. Install project dependencies:

```yml
  - name: Install Requirement
    run: pip install -r requirements.txt
```

4. Build the exe with [PyInstaller](https://pyinstaller.org/en/stable/):

```yml
  - name: Build exe
    run: PyInstaller --onefile main.py
```

5. Create a GitHub release and attach the exe using the community action [ncipollo/release-action](https://github.com/ncipollo/release-action):

```yml
  - name: Create Release
    uses: ncipollo/release-action@v1
    with:
      artifacts: 'dist/main.exe'
      artifactContentType: application/zip
      removeArtifacts: true
```

### Code

Complete workflow:

```yml
name: learn-github-actions
run-name: ${{ github.actor }} is learning GitHub Actions
on:
  push:
    tags:
      - "*"
jobs:
  build-release-exe:
    runs-on: windows-latest
    steps:
      - name: Repo Checkout
        uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.10"
          cache: "pip"
          architecture: "x64"
      - name: Install Requirements
        run: pip install -r requirements.txt
      - name: Build exe
        run: PyInstaller --onefile main.py
      - name: Create Release
        uses: ncipollo/release-action@v1
        with:
          artifacts: "dist/main.exe"
          artifactContentType: application/zip
          removeArtifacts: true
```

**Thanks for reading.**
