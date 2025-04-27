**Record, replay, and export pip installation sequences to ensure consistent and reproducible Python environments, especially when package installation order is critical.**

## The Problem

Standard `pip freeze > requirements.txt` captures the final state of your environment but loses the *history* and *sequence* of how packages were installed. In complex projects, the order in which packages are installed can sometimes affect dependency resolution, leading to subtle differences or "works on my machine" issues when setting up the environment elsewhere.

## The Solution: `pip-sequencer`

`pip-sequencer` acts as a wrapper around `pip install` and `pip uninstall`. It meticulously logs:

*   **Which packages you explicitly install** and the exact versions `pip` resolves for them at that moment.
*   **Which packages you explicitly uninstall**.
*   **The order** in which you perform these actions.

This recorded history allows you to recreate the environment by replaying the installations *in the same sequence*, significantly increasing reproducibility.

## Key Features

*   **Sequential Recording:** Logs `pip install` and `pip uninstall` operations chronologically.
*   **Version Pinning:** Automatically records the installed version during `install` actions.
*   **History File:** Stores the detailed sequence in a human-readable JSON file (`.pip_sequence.json`).
*   **Environment Replay:** Reinstalls packages sequentially using the recorded history (`replay` command).
*   **State Export:** Generates a filtered sequence file (`pip_sequence_export.json`) containing only the install steps relevant to the *currently installed* packages (`export` command).
*   **Standard Freeze Output:** Creates a regular `requirements_frozen.txt` alongside the export for compatibility.
*   **Command-Line Interface:** Simple wrapper commands (`pip-sequencer install`, `pip-sequencer uninstall`, etc.).

## Installation

Install `pip-sequencer` directly from PyPI:

```bash
pip install pip-sequencer
```

## Usage Guide

**Important:** Always use `pip-sequencer` within an activated Python virtual environment for the project you want to manage.

**1. Activate Your Environment:**

```bash
# Example:
# python -m venv .venv
# source .venv/bin/activate  # Linux/macOS
# .\ .venv\Scripts\activate  # Windows
```

**2. Recording Installations (`pip-sequencer install ...`)**

Use `pip-sequencer install` instead of `pip install`. Arguments intended for `pip` itself must follow `--`.

```bash
# Install a single package
pip-sequencer install requests

# Install with version specifiers
pip-sequencer install "flask>=2.0,<3.0"

# Install multiple packages (recorded as one step)
pip-sequencer install django djangorestframework

# Pass arguments like --no-cache-dir or --upgrade to pip
pip-sequencer install colorama -- --no-cache-dir --upgrade

# Install from a requirements file
pip-sequencer install -r requirements.txt
```

*   This executes `pip install` and logs the action, command, timestamp, and detected installed versions to `.pip_sequence.json`.

**3. Recording Uninstallations (`pip-sequencer uninstall ...`)**

Use `pip-sequencer uninstall` instead of `pip uninstall`. It automatically confirms (`-y`). Arguments for `pip` follow `--`.

```bash
pip-sequencer uninstall requests

# Uninstall multiple packages
pip-sequencer uninstall django djangorestframework
```

*   This executes `pip uninstall -y` and logs the action, command, timestamp, and requested packages to `.pip_sequence.json`.

**4. Exporting the Current Sequence (`pip-sequencer export`)**

Generate a sequence file reflecting the installation order of packages currently present.

```bash
# Creates pip_sequence_export.json and requirements_frozen.txt
pip-sequencer export

# Specify custom output/history files
pip-sequencer export -o my_final_sequence.json
pip-sequencer --file old_history.json export
```

*   Reads `.pip_sequence.json`, checks installed packages, writes the filtered sequence to `pip_sequence_export.json` (or specified file), and creates `requirements_frozen.txt`.

**5. Replaying Installations (`pip-sequencer replay`)**

Use this command in a **new, clean virtual environment** to recreate the setup.

```bash
# Activate the NEW clean environment first!
# source new_env/bin/activate

# Make sure pip-sequencer is installed in the new env
# pip install pip-sequencer

# Option A: Replay installs from the full history
# (Copies .pip_sequence.json or uses --file)
pip-sequencer replay

# Option B: Replay installs from an export file (Recommended for final state)
# (Copies pip_sequence_export.json or uses the path)
pip-sequencer replay --from-export
pip-sequencer replay --from-export my_final_sequence.json

# Replay specific sequence number ranges
pip-sequencer replay --start 5 --end 10
pip-sequencer replay --from-export --start 2
```

*   Reads the specified file (history or export) and runs `pip install package==version` sequentially for relevant entries.

## Generated Files Explained

*   **.pip_sequence.json** (Default name)
    *   **Purpose:** Complete log of all recorded `install`/`uninstall` actions.
    *   **Handling:** **Commit this file to version control.** It's the source of truth for your project's setup history.

*   **pip_sequence_export.json** (Default name)
    *   **Purpose:** Filtered sequence of `install` steps for packages still present when `export` was run. Useful for recreating the *final* state sequentially.
    *   **Handling:** **Commit this file to version control.**

*   **requirements_frozen.txt**
    *   **Purpose:** Standard `pip freeze` output. Useful for comparison or tools that expect this format, but **lacks sequence info**.
    *   **Handling:** Optional. You might commit it or add it to `.gitignore`, depending on whether the export JSON is your primary sequenced definition.

## Limitations & Considerations

*   **Requires Explicit Use:** Only tracks actions performed via `pip-sequencer` commands. Direct `pip` calls, editable installs (`pip install -e .`), or tools like `conda`, `poetry`, `pdm` are not tracked.
*   **Dependency Nuances:** While sequence helps, `pip`'s dependency resolution can still vary based on package availability changes on PyPI between recording and replay.
*   **Parsing Limitations:** Complex requirements (VCS URLs, local paths) might not have their versions perfectly auto-detected and recorded, though the install should proceed.
*   **Uninstall Tracking:** Only records the *request* to uninstall, not the full dependency tree removed by `pip`. Replay *does not* perform uninstalls.
*   **Export Scope:** `export` includes install steps only if the *explicitly* installed package from that step is still present. Dependencies installed implicitly are not included in the export sequence file (but are in `requirements_frozen.txt`).
