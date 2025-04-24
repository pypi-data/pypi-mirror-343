# CodexFix Installation Guide

This guide explains how to install CodexFix as a global command-line tool.

## Prerequisites

Before installing CodexFix, ensure you have the following:

1. Python 3.13 or higher
2. pip (Python package installer)
3. OpenAI API key

## Installation Methods

### 1. Install via pip

The easiest way to install CodexFix is via pip:

```bash
pip install codexfix
```

This will install the `codexfix` command globally, making it available in your PATH.

### 2. Install from source

Clone the repository and install:

```bash
git clone https://github.com/yourusername/codexfix.git
cd codexfix
pip install -e .
```

Or use the provided build script:

```bash
git clone https://github.com/yourusername/codexfix.git
cd codexfix
./build.sh
```

## Verifying Installation

After installation, you can verify that CodexFix is properly installed:

```bash
codexfix --help
```

This should display the help message with available commands and options.

## Setting Up Required Tools

CodexFix requires different linting tools depending on which languages you'll be analyzing:

### For Python Analysis

```bash
pip install mypy==1.8.0 pyright==1.1.350
```

### For TypeScript Analysis

```bash
npm install -g typescript
npm install -g eslint @typescript-eslint/parser @typescript-eslint/eslint-plugin
```

### For Dart/Flutter Analysis

Install the Flutter SDK from https://docs.flutter.dev/get-started/install

## Setting Up OpenAI API Key

CodexFix uses OpenAI's Codex API to generate fixes. Set your API key:

```bash
# For Unix/Linux/macOS
export OPENAI_API_KEY="your-openai-api-key"

# For Windows PowerShell
$env:OPENAI_API_KEY="your-openai-api-key"

# For Windows Command Prompt
set OPENAI_API_KEY=your-openai-api-key
```

For persistent setup, add the export command to your shell profile (~/.bashrc, ~/.zshrc, etc.).

## Troubleshooting

If you encounter any issues during installation:

1. Ensure Python 3.13+ is installed: `python --version`
2. Check if pip is up to date: `pip install --upgrade pip`
3. Verify your OpenAI API key is set correctly
4. Ensure all dependencies are installed for your target language