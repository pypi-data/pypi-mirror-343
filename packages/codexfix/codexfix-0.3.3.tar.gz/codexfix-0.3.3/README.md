# CodexFix 🛠️

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Mypy: Checked](https://img.shields.io/badge/mypy-checked-brightgreen.svg)](http://mypy-lang.org/)

A powerful type-aware linter runner and Codex orchestrator that automatically fixes code issues using AI. CodexFix combines static analysis with OpenAI's Codex to provide intelligent, automated code improvements while preserving behavior.

> ⚠️ **Warning**: This tool was mostly implemented by VibeCoding 😊

## Features

- 🔍 Integrated type checking and linting with mypy, pyright, and ESLint
- 🎯 Support for Python, TypeScript, and Dart/Flutter analysis
- 🤖 AI-powered automatic code fixes using OpenAI's Codex
- ⚡ Fast and efficient analysis with parallel processing
- 🔄 Iterative improvement with automatic re-analysis
- 🎨 Beautiful console output with rich formatting
- 📊 Comprehensive JSON reporting of fixed issues
- 🔌 Shell completion for Bash, Zsh, and Fish (v0.3.3+)
- 📦 Global installation support via Pix package manager

## Installation

### Prerequisites

#### OpenAI API Key

```bash
# You must have a valid OpenAI API key set in your environment
export OPENAI_API_KEY="your-openai-api-key"

# For Windows PowerShell
$env:OPENAI_API_KEY="your-openai-api-key"

# For Windows Command Prompt
set OPENAI_API_KEY=your-openai-api-key
```

#### Python Environment
```bash
# Install Python 3.13 or later
# macOS
brew install python@3.13

# Linux
sudo apt install python3.13 python3.13-venv python3.13-dev

# Create and activate a virtual environment
python3.13 -m venv venv
source venv/bin/activate
```

### Install UV

```bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or on macOS with Homebrew
brew install astral/tap/uv
```

### Install Pix

```bash
# Install Pix
curl -LsSf https://astral.sh/pix/install.sh | sh

# Or on macOS with Homebrew
brew install astral/tap/pix
```

### UV vs Pix

- **UV**: Fast dependency resolver and installer for project-level dependencies in virtual environments. Use UV for development work within specific projects.
- **Pix**: Global package manager for Python. Use Pix when you want to install command-line tools globally and make them available from any terminal.

For CodexFix:
- Use **UV** when working on CodexFix development or when you want to install it in a project-specific environment
- Use **Pix** when you want to use CodexFix as a global command-line tool

#### Install Required Tools

```bash
# Install analysis tools using UV (for project environments)
uv pip install mypy==1.8.0 pyright==1.1.350

# Or install analysis tools globally using Pix
pix install mypy==1.8.0 pyright==1.1.350

# TypeScript analysis tools
npm install -g typescript
npm install -g eslint @typescript-eslint/parser @typescript-eslint/eslint-plugin

# For Dart/Flutter analysis
# Install Flutter SDK from https://docs.flutter.dev/get-started/install
```

#### Install CodexFix

##### Install from PyPI

```bash
# Install the package using UV
uv pip install codexfix

# Install globally using Pix
pix install codexfix
```

##### Global Usage with Pix

[Pix](https://astral.sh/pix) is a new package manager that provides a seamless global installation experience:

```bash
# Install CodexFix globally
pix install codexfix

# Run CodexFix from anywhere
codexfix --path /path/to/project

# Update to the latest version
pix update codexfix

# List globally installed packages
pix list
```

Note: Pix installs packages globally by default, making command-line tools like CodexFix available system-wide without virtual environments.

##### Install from Source

```bash
# Clone the repository
git clone https://github.com/yourusername/codexfix.git
cd codexfix

# Install in development mode using UV
uv pip install -e .
```

##### Building and Publishing

If you're a contributor or maintainer who wants to build and publish the package:

```bash
# Build the package
uv build

# Publish to PyPI (requires appropriate credentials)
uv publish

# Test installation of the published package
uv run --with codexfix --no-project -- python -c "import codexfix"
```

Note: For publishing to PyPI, you'll need to set up authentication using token:
```bash
# Set the PyPI token
export UV_PUBLISH_TOKEN="your-pypi-token"
```

## Usage

```bash
# Run analysis only on current directory (without fixing)
codexfix

# Apply automatic fixes with Codex
codexfix --applyFix

# Run on specific path
codexfix --path /path/to/project

# Generate a comprehensive report
codexfix --applyFix --report issues_report.json

# Run with specific language
codexfix --language python  # or typescript, dart

# Different approval modes
codexfix --approval-mode suggest  # or auto-edit, full-auto

# Install shell completion (bash, zsh, or fish)
codexfix --install-completion bash
```

### Shell Completion

CodexFix v0.3.0+ provides built-in shell completion scripts for Bash, Zsh, and Fish shells to make command-line usage more convenient:

```bash
# Install Bash completion
codexfix --install-completion bash

# Install Zsh completion
codexfix --install-completion zsh

# Install Fish completion
codexfix --install-completion fish
```

After installing shell completion, you can press Tab to complete CodexFix command-line options and arguments:

```bash
# Start typing and press Tab to see available options
codexfix --[TAB]

# Tab completion for option values
codexfix --language [TAB]  # Shows python, typescript, dart
codexfix --approval-mode [TAB]  # Shows suggest, auto-edit, full-auto
```

## Configuration

CodexFix supports various configuration options:

- `--path`: Path to analyze (default: current directory)
- `--language`: Choose between 'python', 'typescript', or 'dart' analysis (default: python)
- `--approval-mode`: Control how fixes are applied ('suggest', 'auto-edit', 'full-auto')
- `--max-iterations`: Stop after N Codex rounds (default: 3)
- `--model`: Specify custom Codex model
- `--verbose`: Enable verbose debug output
- `--applyFix`: Apply automatic fixes using Codex (default: only show diagnostics)
- `--analyze`: Severity levels to analyze ('default' or 'all')
- `--report`: Filename to save a comprehensive report of all fixed issues

## Requirements

- Python 3.13+
- UV package manager (https://astral.sh/uv)
- Pix package manager (https://astral.sh/pix)
- OpenAI API key for Codex integration
- CodexFix 0.3.3+ for shell completion support
- For Python analysis:
  - mypy (`uv pip install mypy`)
  - pyright (`uv pip install pyright`)
- For TypeScript analysis:
  - TypeScript (`npm install -g typescript`) - must be installed first
  - ESLint (`npm install -g eslint`)
  - TypeScript ESLint plugins (`npm install -g @typescript-eslint/parser @typescript-eslint/eslint-plugin`)
- For Dart analysis:
  - Flutter SDK (https://docs.flutter.dev/get-started/install)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a list of changes and version history.