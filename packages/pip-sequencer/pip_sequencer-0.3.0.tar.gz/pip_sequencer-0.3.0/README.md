# Pip Sequencer

[![PyPI version](https://badge.fury.io/py/pip-sequencer.svg)](https://badge.fury.io/py/pip-sequencer) <!-- Optional: Add this if/when you publish to PyPI -->
<!-- Optional: Add other badges like build status, license, etc. -->

Record, replay, and export pip installation/uninstallation sequences to help recreate Python virtual environments more predictably, especially when installation order matters.

## Overview

`pip-sequencer` wraps the standard `pip install` and `pip uninstall` commands. It meticulously records the packages you explicitly request (along with their installed versions for installs) in the order you perform these actions. This recorded sequence can then be used to:

1.  Replay the installations in a new environment.
2.  Export a filtered sequence representing the installation order of packages *currently* present in the environment.

This helps mitigate issues where dependency resolution might differ based on the order packages are installed.

## Features

*   Wraps `pip install` to record explicitly requested packages and their successfully installed versions.
*   Wraps `pip uninstall` to record packages explicitly requested for removal.
*   Stores the sequence of operations with timestamps in a JSON history file (`.pip_sequence.json`).
*   Provides a `replay` command to reinstall packages sequentially based on the history or an export file.
*   Provides an `export` command to generate a filtered sequence file (`pip_sequence_export.json`) containing the install steps for packages still present in the environment.
*   Generates a standard `requirements_frozen.txt` file during export for compatibility.

## Installation

You can install `pip-sequencer` directly from PyPI:

```bash
pip install pip-sequencer