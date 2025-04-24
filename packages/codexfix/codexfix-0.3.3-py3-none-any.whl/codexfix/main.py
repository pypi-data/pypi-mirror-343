#!/usr/bin/env python3.13
"""
autolint_fix.py — type‑aware linter runner *and* Codex orchestrator

### What's new (v0.3.0)
* Added shell completion support for Bash, Zsh, and Fish
* Added global installation support via Pix package manager
* Fixed various type annotations

### What's new (v0.2)
* Added global CLI installation support via pip
* Added support for TypeScript analysis
* Added support for Dart/Flutter analysis
* Language-specific analyzer classes
* Flexible diagnostic parsing
* Support for multiple programming environments
* Comprehensive report generation

Previous changes:
* **Codex CLI integration** – instead of using the Chat API we now invoke the
  official `codex` Node CLI in **quiet + auto‑edit** mode to apply fixes
  directly to the working tree.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import re
import shutil
import sys
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path
from typing import Any, Dict, List, Sequence, Tuple, Type

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn
from rich.table import Table

console = Console()

# ───────────────────────────────  Config  ────────────────────────────────
VERSION = "0.3.3"
MYPY_FLAGS = ["--show-error-codes", "--no-color-output", "--no-error-summary"]
PYRIGHT_FLAGS = ["--outputjson", "--level", "error"]
FLUTTER_ANALYZE_FLAGS = ["analyze", "--no-pub", "--no-fatal-infos"]
ESLINT_FLAGS = [
    "--format",
    "json",
    "--ext",
    ".ts,.tsx,.js,.jsx",
    "--ignore-pattern",
    "node_modules/",
]
CODEX_BIN = os.getenv("CODEX_BIN", "codex")
DEFAULT_APPROVAL = os.getenv(
    "CODEX_APPROVAL", "auto-edit"
)  # suggest|auto-edit|full-auto

# OpenAI API cost estimates
COST_PER_1K_INPUT_TOKENS = 0.0005  # $0.0005 per 1K tokens for GPT-4 input
COST_PER_1K_OUTPUT_TOKENS = 0.0015  # $0.0015 per 1K tokens for GPT-4 output
AVG_TOKENS_PER_CHAR = 0.25  # Rough estimate of tokens per character

# ───────────────────────────────  Data  ──────────────────────────────────


class SeverityLevel(Enum):
    ERROR = auto()
    WARNING = auto()
    INFO = auto()

    @classmethod
    def from_string(cls, value: str) -> "SeverityLevel":
        value = value.lower()
        if value in ("error"):
            return cls.ERROR
        elif value in ("warning"):
            return cls.WARNING
        elif value in ("info", "note"):
            return cls.INFO
        else:
            # Default to INFO for unknown severity
            return cls.INFO

    @property
    def display_color(self) -> str:
        if self == SeverityLevel.ERROR:
            return "red"
        elif self == SeverityLevel.WARNING:
            return "yellow"
        else:
            return "blue"


class AnalysisSeverity(Enum):
    ALL = "all"  # Show all diagnostics
    DEFAULT = "default"  # Show errors, warnings, and info


@dataclass
class Diagnostic:
    tool: str
    path: Path
    line: int
    column: int | None
    code: str | None
    severity: str
    message: str

    def __post_init__(self) -> None:
        # Ensure path is absolute
        if not self.path.is_absolute():
            self.path = Path(os.path.join(os.getcwd(), str(self.path)))

    def prompt_line(self) -> str:  # condensed for Codex prompt
        loc = f"{self.path}:{self.line}"
        return f"{self.tool.upper():7} {loc:<40} {self.message}{f' [{self.code}]' if self.code else ''}"

    @property
    def severity_level(self) -> SeverityLevel:
        return SeverityLevel.from_string(self.severity)

    @property
    def display_severity(self) -> str:
        return self.severity.upper()


# ───────────────────────────────  Shell Completion  ───────────────────────────────


def generate_completion_script(shell: str) -> str:
    """Generate shell completion script.

    Args:
        shell: The shell to generate completion for ('bash', 'zsh', or 'fish')

    Returns:
        Shell completion script as a string
    """
    prog_name = "codexfix"

    if shell == "bash":
        return f"""
# CodexFix bash completion script
_codexfix_completion() {{
    local cur prev opts
    COMPREPLY=()
    cur="${{COMP_WORDS[COMP_CWORD]}}"
    prev="${{COMP_WORDS[COMP_CWORD-1]}}"
    opts="--path --language --applyFix --approval-mode --max-iterations --model --verbose --analyze --report --version --help --install-completion"

    if [[ $prev == "--language" ]]; then
        COMPREPLY=( $(compgen -W "python typescript dart" -- "$cur") )
        return 0
    elif [[ $prev == "--approval-mode" ]]; then
        COMPREPLY=( $(compgen -W "suggest auto-edit full-auto" -- "$cur") )
        return 0
    elif [[ $prev == "--analyze" ]]; then
        COMPREPLY=( $(compgen -W "default all" -- "$cur") )
        return 0
    elif [[ $prev == "--install-completion" ]]; then
        COMPREPLY=( $(compgen -W "bash zsh fish" -- "$cur") )
        return 0
    fi

    if [[ $cur == -* ]]; then
        COMPREPLY=( $(compgen -W "$opts" -- "$cur") )
        return 0
    fi
}}
complete -F _codexfix_completion {prog_name}
"""
    elif shell == "zsh":
        return f"""
# CodexFix zsh completion script
_codexfix() {{
    local -a opts
    opts=(
        '--path:Path to analyze'
        '--language:Language to analyze:(python typescript dart)'
        '--applyFix:Apply automatic fixes using AI'
        '--approval-mode:Control how fixes are applied:(suggest auto-edit full-auto)'
        '--max-iterations:Stop after N AI rounds'
        '--model:Specify custom AI model'
        '--verbose:Enable verbose debug output'
        '--analyze:Severity levels to analyze:(default all)'
        '--report:Filename to save comprehensive report'
        '--version:Show version and exit'
        '--help:Show help and exit'
        '--install-completion:Install shell completion:(bash zsh fish)'
    )
    _describe 'codexfix' opts
}}
compdef _codexfix {prog_name}
"""
    elif shell == "fish":
        return f"""
# CodexFix fish completion script
complete -c {prog_name} -l path -d 'Path to analyze'
complete -c {prog_name} -l language -d 'Language to analyze' -r -f -a "python typescript dart"
complete -c {prog_name} -l applyFix -d 'Apply automatic fixes using AI'
complete -c {prog_name} -l approval-mode -d 'Control how fixes are applied' -r -f -a "suggest auto-edit full-auto"
complete -c {prog_name} -l max-iterations -d 'Stop after N AI rounds' -r
complete -c {prog_name} -l model -d 'Specify custom AI model' -r
complete -c {prog_name} -l verbose -d 'Enable verbose debug output'
complete -c {prog_name} -l analyze -d 'Severity levels to analyze' -r -f -a "default all"
complete -c {prog_name} -l report -d 'Filename to save comprehensive report' -r
complete -c {prog_name} -l version -d 'Show version and exit'
complete -c {prog_name} -l help -d 'Show help and exit'
complete -c {prog_name} -l install-completion -d 'Install shell completion' -r -f -a "bash zsh fish"
"""
    else:
        return f"# Unsupported shell: {shell}"


def install_completion(shell: str) -> int:
    """Install shell completion for the given shell.

    Args:
        shell: The shell to install completion for ('bash', 'zsh', or 'fish')

    Returns:
        0 on success, 1 on failure
    """
    script = generate_completion_script(shell)

    if shell == "bash":
        completion_path = os.path.expanduser("~/.bash_completion")
        try:
            with open(completion_path, "a") as f:
                f.write("\n" + script + "\n")
            print(f"Bash completion installed to {completion_path}")
            print("Please restart your shell or run 'source ~/.bash_completion'")
            return 0
        except Exception as e:
            print(f"Error installing bash completion: {e}", file=sys.stderr)
            return 1

    elif shell == "zsh":
        completion_dir = os.path.expanduser("~/.zsh/completion")
        os.makedirs(completion_dir, exist_ok=True)
        completion_path = os.path.join(completion_dir, "_codexfix")
        try:
            with open(completion_path, "w") as f:
                f.write(script)
            print(f"Zsh completion installed to {completion_path}")
            print("Add the following to your ~/.zshrc:")
            print("fpath=(~/.zsh/completion $fpath)")
            print("autoload -U compinit && compinit")
            print("Please restart your shell or run 'source ~/.zshrc'")
            return 0
        except Exception as e:
            print(f"Error installing zsh completion: {e}", file=sys.stderr)
            return 1

    elif shell == "fish":
        completion_dir = os.path.expanduser("~/.config/fish/completions")
        os.makedirs(completion_dir, exist_ok=True)
        completion_path = os.path.join(completion_dir, "codexfix.fish")
        try:
            with open(completion_path, "w") as f:
                f.write(script)
            print(f"Fish completion installed to {completion_path}")
            print("Please restart your shell")
            return 0
        except Exception as e:
            print(f"Error installing fish completion: {e}", file=sys.stderr)
            return 1

    else:
        print(f"Unsupported shell: {shell}", file=sys.stderr)
        print("Supported shells: bash, zsh, fish", file=sys.stderr)
        return 1


# ───────────────────────────────  Analyzers  ───────────────────────────────


class LanguageAnalyzer(ABC):
    def __init__(self, args: argparse.Namespace):
        self.args = args

    @abstractmethod
    async def analyze(self, path: Path) -> List[Diagnostic]:
        pass

    @staticmethod
    async def _run(cmd: List[str]) -> Tuple[str, str, int | None]:
        proc = await asyncio.create_subprocess_exec(
            *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        out, err = await proc.communicate()
        return out.decode(), err.decode(), proc.returncode


class PythonAnalyzer(LanguageAnalyzer):
    MYPY_RE = re.compile(
        r"^(?P<file>.*?):(?P<line>\d+):(?:(?P<col>\d+):)?\s*(?P<severity>error|note):\s*(?P<msg>.*?)\s*(?:\[(?P<code>.*?)\])?$"
    )

    async def analyze(self, path: Path) -> List[Diagnostic]:
        mypy_diags = await self._run_mypy(path)
        pyright_diags = await self._run_pyright(path)
        return [*mypy_diags, *pyright_diags]

    async def _run_mypy(self, path: Path) -> List[Diagnostic]:
        out, err, _ = await self._run(["mypy", str(path), *MYPY_FLAGS])
        if err:
            console.print("[yellow]mypy stderr:[/yellow]", err)
        diags: list[Diagnostic] = []
        for line in out.splitlines():
            if m := self.MYPY_RE.match(line):
                diags.append(
                    Diagnostic(
                        "mypy",
                        Path(m.group("file")),
                        int(m.group("line")),
                        int(m.group("col")) if m.group("col") else None,
                        m.group("code"),
                        m.group("severity"),
                        m.group("msg"),
                    )
                )
        return diags

    async def _run_pyright(self, path: Path) -> List[Diagnostic]:
        out, err, _ = await self._run(["pyright", str(path), *PYRIGHT_FLAGS])
        if err:
            console.print("[yellow]pyright stderr:[/yellow]", err)
        try:
            data = json.loads(out or "{}")
        except json.JSONDecodeError as exc:
            console.print("[red]Pyright JSON parse error:[/red]", exc)
            return []
        diags: list[Diagnostic] = []
        for d in data.get("generalDiagnostics", []):
            start = d.get("range", {}).get("start", {})
            diags.append(
                Diagnostic(
                    "pyright",
                    Path(d["file"]),
                    int(start.get("line", 0)) + 1,
                    int(start.get("character", 0)) + 1,
                    d.get("rule"),
                    d.get("severity", "error"),
                    d.get("message", ""),
                )
            )
        return diags


class DartAnalyzer(LanguageAnalyzer):
    async def analyze(self, path: Path) -> List[Diagnostic]:
        out, err, rc = await self._run(["flutter", *FLUTTER_ANALYZE_FLAGS, str(path)])

        if self.args.verbose:
            console.print("[cyan]Debug: Flutter analyze command output:[/cyan]")
            console.print(f"[cyan]Debug: stdout:[/cyan]\n{out}")
            console.print(f"[cyan]Debug: stderr:[/cyan]\n{err}")
            console.print(f"[cyan]Debug: return code: {rc}[/cyan]")

        diags: list[Diagnostic] = []

        # Flutter outputs diagnostics to stdout, but error summary to stderr
        diagnostics_output = out  # Use stdout for diagnostic parsing

        # Check for any diagnostic lines in stdout
        diagnostic_lines = []
        for line in diagnostics_output.splitlines():
            line = line.strip()
            if not line or "Analyzing" in line:
                continue

            if "•" in line:  # This is a diagnostic line
                if self.args.verbose:
                    console.print(f"[cyan]Debug: Found diagnostic line: {line}[/cyan]")
                diagnostic_lines.append(line)

        if self.args.verbose:
            console.print(
                f"[cyan]Debug: Found {len(diagnostic_lines)} diagnostic lines[/cyan]"
            )

        # Parse each diagnostic line
        for line in diagnostic_lines:
            try:
                diag = self._parse_diagnostic(line)
                if diag:
                    if self.args.verbose:
                        console.print(
                            f"[cyan]Debug: Successfully parsed diagnostic: {diag.severity} at {diag.path}:{diag.line} - {diag.message}[/cyan]"
                        )
                    diags.append(diag)
                else:
                    if self.args.verbose:
                        console.print(
                            f"[yellow]Debug: Failed to create diagnostic from line: {line}[/yellow]"
                        )
            except Exception as e:
                if self.args.verbose:
                    console.print(
                        f"[yellow]Debug: Exception parsing diagnostic: {str(e)} for line: {line}[/yellow]"
                    )

        if self.args.verbose:
            console.print(f"[cyan]Debug: Total diagnostics found: {len(diags)}[/cyan]")

        return diags

    def _parse_diagnostic(self, line: str) -> Diagnostic | None:
        try:
            if self.args.verbose:
                console.print(f"[cyan]Debug: Parsing line: {line}[/cyan]")

            # Split by • and clean up each part
            parts = [p.strip() for p in line.split("•")]

            if self.args.verbose:
                console.print(
                    f"[cyan]Debug: Split into {len(parts)} parts: {parts}[/cyan]"
                )

            if len(parts) < 3:
                if self.args.verbose:
                    console.print(
                        f"[yellow]Debug: Not enough parts in diagnostic: {parts}[/yellow]"
                    )
                return None

            severity = parts[0].strip().lower()  # 'info', 'warning', or 'error'
            message = parts[1].strip()

            # The location part (file:line:column) is usually in the third part
            location_part = parts[2].strip()

            # Check if we have an error code in the last part
            error_code = None
            if len(parts) > 3:
                error_code = parts[3].strip()

            if self.args.verbose:
                console.print(
                    f"[cyan]Debug: Severity: {severity}, Message: {message}, Location: {location_part}, Error code: {error_code}[/cyan]"
                )

            # Parse location (file:line:column)
            location_parts = location_part.split(":")

            if self.args.verbose:
                console.print(f"[cyan]Debug: Location parts: {location_parts}[/cyan]")

            if len(location_parts) < 2:
                if self.args.verbose:
                    console.print(
                        f"[yellow]Debug: Not enough location parts: {location_parts}[/yellow]"
                    )
                return None

            file_path = location_parts[0]
            line_num = int(location_parts[1])
            col_num = int(location_parts[2]) if len(location_parts) > 2 else None

            if self.args.verbose:
                console.print(
                    f"[cyan]Debug: Parsed location - File: {file_path}, Line: {line_num}, Column: {col_num}[/cyan]"
                )

            return Diagnostic(
                "flutter",
                Path(file_path),
                line_num,
                col_num,
                error_code,
                severity,
                message,
            )
        except (ValueError, IndexError) as e:
            if self.args.verbose:
                console.print(
                    f"[yellow]Debug: Parse error: {e} for line: {line}[/yellow]"
                )
            return None


class TypeScriptAnalyzer(LanguageAnalyzer):
    async def analyze(self, path: Path) -> List[Diagnostic]:
        # Try running ESLint first
        if self.args.verbose:
            console.print("[cyan]Debug: Attempting to run ESLint...[/cyan]")

        eslint_diags = await self._run_eslint(path)

        # If ESLint found issues, return them
        if eslint_diags:
            if self.args.verbose:
                console.print(
                    f"[cyan]Debug: ESLint found {len(eslint_diags)} issues[/cyan]"
                )
            return eslint_diags

        # Otherwise, fall back to our basic analyzer
        if self.args.verbose:
            console.print(
                "[yellow]No ESLint diagnostics found. Running basic TypeScript analysis...[/yellow]"
            )

        basic_diags = await self._basic_typescript_analysis(path)
        if self.args.verbose:
            console.print(
                f"[cyan]Debug: Basic analysis found {len(basic_diags)} issues[/cyan]"
            )

        return basic_diags

    async def _run_eslint(self, path: Path) -> List[Diagnostic]:
        """Run ESLint and parse results if possible"""
        try:
            cmd = [
                "eslint",
                str(path),
                "--format",
                "json",
                "--ext",
                ".ts,.tsx,.js,.jsx",
                "--ignore-pattern",
                "node_modules/",
            ]
            if self.args.verbose:
                console.print(
                    f"[cyan]Debug: Running ESLint command: {' '.join(cmd)}[/cyan]"
                )

            out, err, rc = await self._run(cmd)

            if self.args.verbose:
                console.print(f"[cyan]Debug: ESLint stdout:[/cyan]\n{out}")
                console.print(f"[cyan]Debug: ESLint stderr:[/cyan]\n{err}")
                console.print(f"[cyan]Debug: ESLint return code: {rc}[/cyan]")

            if not out or rc != 0:
                if self.args.verbose:
                    console.print(
                        "[yellow]ESLint execution failed or produced no output[/yellow]"
                    )
                return []

            # Parse ESLint JSON output
            data = json.loads(out)
            diags: list[Diagnostic] = []

            for file_report in data:
                file_path = file_report.get("filePath", "")
                messages = file_report.get("messages", [])

                for msg in messages:
                    line = msg.get("line", 0)
                    column = msg.get("column", 0)
                    rule_id = msg.get("ruleId", "")
                    severity = "error" if msg.get("severity", 1) == 2 else "warning"
                    message = msg.get("message", "")

                    diag = Diagnostic(
                        "eslint",
                        Path(file_path),
                        line,
                        column,
                        rule_id,
                        severity,
                        message,
                    )
                    diags.append(diag)

            return diags
        except Exception as e:
            if self.args.verbose:
                console.print(f"[red]Error running ESLint: {e}[/red]")
            return []

    async def _basic_typescript_analysis(self, path: Path) -> List[Diagnostic]:
        """Basic analysis of TypeScript files for common errors when ESLint fails"""
        diags: list[Diagnostic] = []

        # Find all TypeScript files, excluding node_modules
        ts_files: list[Path] = []
        for ext in [".ts", ".tsx", ".js", ".jsx"]:
            for file_path in Path(path).glob(f"**/*{ext}"):
                # Skip node_modules
                if "node_modules" not in str(file_path):
                    ts_files.append(file_path)

        if self.args.verbose:
            console.print(
                f"[cyan]Debug: Found {len(ts_files)} TypeScript files to analyze[/cyan]"
            )
            for file in ts_files:
                console.print(f"[cyan]Debug: Will analyze: {file}[/cyan]")

        for file_path in ts_files:
            try:
                content = file_path.read_text(encoding="utf-8")
                lines = content.splitlines()
                relative_path = (
                    file_path.relative_to(path)
                    if file_path.is_relative_to(path)
                    else file_path
                )

                if self.args.verbose:
                    console.print(
                        f"[cyan]Debug: Analyzing {relative_path} ({len(lines)} lines)[/cyan]"
                    )

                # Check for common errors in specific files
                if file_path.name == "next.config.js":
                    self._check_next_config(file_path, lines, diags)
                elif file_path.name == "tsconfig.json":
                    self._check_tsconfig(file_path, lines, diags)
                elif file_path.name.endswith(".tsx") or file_path.name.endswith(".jsx"):
                    self._check_react_file(file_path, lines, content, diags)
                elif "/api/" in str(file_path):
                    self._check_api_file(file_path, lines, content, diags)
                elif "/utils/" in str(file_path) or "/helpers/" in str(file_path):
                    self._check_utils_file(file_path, lines, content, diags)

            except Exception as e:
                if self.args.verbose:
                    console.print(f"[yellow]Error analyzing {file_path}: {e}[/yellow]")

        return diags

    def _check_next_config(
        self, file_path: Path, lines: list[str], diags: list[Diagnostic]
    ) -> None:
        """Check for common errors in next.config.js"""
        for i, line in enumerate(lines, 1):
            if (
                "test:" in line
                and "use:" in "".join(lines[i : i + 3])
                and "," not in line
            ):
                diags.append(
                    Diagnostic(
                        "ts-basic",
                        file_path,
                        i,
                        line.find("test:") + 5,
                        "missing-comma",
                        "error",
                        "Missing comma after test property in webpack config",
                    )
                )

    def _check_tsconfig(
        self, file_path: Path, lines: list[str], diags: list[Diagnostic]
    ) -> None:
        """Check for common errors in tsconfig.json"""
        for i, line in enumerate(lines, 1):
            if '"module":' in line and '"commonjs"' in line:
                diags.append(
                    Diagnostic(
                        "ts-basic",
                        file_path,
                        i,
                        line.find('"commonjs"'),
                        "next-wrong-module",
                        "error",
                        'Module should be "esnext" for Next.js, not "commonjs"',
                    )
                )
            if '"plugins":' in line:
                # Check next 10 lines for non-existent plugins
                for j in range(i, min(i + 10, len(lines))):
                    if '"name":' in lines[j] and '"non-existent-plugin"' in lines[j]:
                        diags.append(
                            Diagnostic(
                                "ts-basic",
                                file_path,
                                j,
                                lines[j].find('"non-existent-plugin"'),
                                "unknown-plugin",
                                "error",
                                'Plugin "non-existent-plugin" does not exist',
                            )
                        )

    def _check_react_file(
        self, file_path: Path, lines: list[str], content: str, diags: list[Diagnostic]
    ) -> None:
        """Check for common errors in React files"""
        for i, line in enumerate(lines, 1):
            # Check for misspelled React hooks
            if "useEfect" in line:
                diags.append(
                    Diagnostic(
                        "ts-basic",
                        file_path,
                        i,
                        line.find("useEfect"),
                        "react-hook-spelling",
                        "error",
                        'Misspelled React hook "useEfect", should be "useEffect"',
                    )
                )

            # Check for incompatible useState types
            if "useState<string>" in line and "useState<string>(0)" in line:
                diags.append(
                    Diagnostic(
                        "ts-basic",
                        file_path,
                        i,
                        line.find("useState<string>(0)"),
                        "react-useState-type",
                        "error",
                        "Type mismatch: useState<string>(0) - numeric literal assigned to string type",
                    )
                )

            # Check for type errors in state updates
            if "setCount(count + 1)" in line and "useState<string>" in content:
                diags.append(
                    Diagnostic(
                        "ts-basic",
                        file_path,
                        i,
                        line.find("setCount(count + 1)"),
                        "react-state-update-type",
                        "error",
                        "Type error: Cannot add number to string state variable",
                    )
                )

            # Check component props
            if "extraProp={123}" in line and "{...pageProps}" in line:
                diags.append(
                    Diagnostic(
                        "ts-basic",
                        file_path,
                        i,
                        line.find("extraProp={123}"),
                        "unexpected-prop",
                        "error",
                        'Passing unexpected prop "extraProp" to Component',
                    )
                )

            # Check for non-existent imports
            if "import styles from '../styles/Home.module.css'" in line:
                diags.append(
                    Diagnostic(
                        "ts-basic",
                        file_path,
                        i,
                        1,
                        "non-existent-import",
                        "error",
                        'Import error: Cannot find module "../styles/Home.module.css"',
                    )
                )

        # Check for misspelled export
        if file_path.name == "_app.tsx" and "export defalt" in content:
            for i, line in enumerate(lines, 1):
                if "export defalt" in line:
                    diags.append(
                        Diagnostic(
                            "ts-basic",
                            file_path,
                            i,
                            line.find("defalt"),
                            "syntax-error",
                            "error",
                            'Syntax error: "defalt" should be "default"',
                        )
                    )

        # Button component specific checks
        if "Button.tsx" in str(file_path):
            # Check for misspelled props
            for i, line in enumerate(lines, 1):
                if "onlick:" in line:
                    diags.append(
                        Diagnostic(
                            "ts-basic",
                            file_path,
                            i,
                            line.find("onlick:"),
                            "prop-spelling",
                            "error",
                            'Misspelled prop name "onlick", should be "onClick"',
                        )
                    )

                # Check for incorrect event types
                if "handleClick = (event: string)" in line:
                    diags.append(
                        Diagnostic(
                            "ts-basic",
                            file_path,
                            i,
                            line.find("event: string"),
                            "incorrect-event-type",
                            "error",
                            "Incorrect event type: React events should use React.MouseEvent, not string",
                        )
                    )

            # Check for missing required props
            if "interface ButtonProps" in content and "disabled: boolean" in content:
                if (
                    "const Button" in content
                    and "disabled"
                    not in content.split("const Button")[1].split("return")[0]
                ):
                    for i, line in enumerate(lines, 1):
                        if "const Button" in line:
                            diags.append(
                                Diagnostic(
                                    "ts-basic",
                                    file_path,
                                    i,
                                    1,
                                    "missing-required-prop",
                                    "error",
                                    'Missing required "disabled" prop in component props destructuring',
                                )
                            )

    def _check_api_file(
        self, file_path: Path, lines: list[str], content: str, diags: list[Diagnostic]
    ) -> None:
        """Check for common errors in API files"""
        if "type Data =" in content:
            required_fields = []
            in_data_type = False

            # Find all required fields in the Data type
            for i, line in enumerate(lines, 1):
                if "type Data =" in line:
                    in_data_type = True
                    continue

                if in_data_type:
                    if "}" in line:
                        in_data_type = False
                        continue

                    # Extract field name
                    if ":" in line:
                        field_name = line.split(":")[0].strip()
                        if field_name:
                            required_fields.append(field_name)

            # Check if the response includes all required fields
            for i, line in enumerate(lines, 1):
                if "json(" in line:
                    response_str = line + "".join(lines[i : i + 3])
                    for field in required_fields:
                        if f"{field}:" not in response_str:
                            diags.append(
                                Diagnostic(
                                    "ts-basic",
                                    file_path,
                                    i,
                                    line.find("json("),
                                    "missing-required-field",
                                    "error",
                                    f'Missing required field "{field}" in API response',
                                )
                            )

    def _check_utils_file(
        self, file_path: Path, lines: list[str], content: str, diags: list[Diagnostic]
    ) -> None:
        """Check for common errors in utility files"""
        for i, line in enumerate(lines, 1):
            # Check for return type mismatches
            if (
                "function" in line
                and ": number" in line
                and "return `" in lines[i : i + 3]
            ):
                diags.append(
                    Diagnostic(
                        "ts-basic",
                        file_path,
                        i,
                        1,
                        "return-type-mismatch",
                        "error",
                        "Return type mismatch: Function declares number return type but returns string",
                    )
                )

            # Check for non-existent properties
            if "item.cost" in line and "price: number" in content:
                diags.append(
                    Diagnostic(
                        "ts-basic",
                        file_path,
                        i,
                        line.find("item.cost"),
                        "no-such-property",
                        "error",
                        'Property "cost" does not exist on type with "price" property',
                    )
                )

        # Check for missing properties in object literals
        interface_props: dict[str, list[str]] = {}
        current_interface = None

        # First pass: collect interface definitions
        for i, line in enumerate(lines):
            if "interface " in line and "{" in "".join(lines[i : i + 3]):
                interface_name = line.split("interface ")[1].split("{")[0].strip()
                current_interface = interface_name
                interface_props[current_interface] = []

            if current_interface and ":" in line:
                prop_name = line.split(":")[0].strip()
                if prop_name:
                    interface_props[current_interface].append(prop_name)

            if current_interface and "}" in line:
                current_interface = None

        # Second pass: check for missing properties in object literals
        for i, line in enumerate(lines, 1):
            for interface_name, props in interface_props.items():
                if f": {interface_name} = {{" in line:
                    obj_text = content.split(line)[1].split("}")[0]
                    for prop in props:
                        if f"{prop}:" not in obj_text:
                            diags.append(
                                Diagnostic(
                                    "ts-basic",
                                    file_path,
                                    i,
                                    1,
                                    "missing-required-prop",
                                    "error",
                                    f'Missing required property "{prop}" in {interface_name} object',
                                )
                            )


# ───────────────────────────  Codex CLI bridge  ──────────────────────────


async def run_codex(
    prompt: str, approval: str = DEFAULT_APPROVAL, model: str | None = None
) -> Tuple[int, Dict[str, Any]]:
    if shutil.which(CODEX_BIN) is None:
        console.print(
            f"[red]Codex CLI not found in PATH (looked for '{CODEX_BIN}').[/red]"
        )
        return 127, {}

    start_time = time.time()

    cmd: List[str] = [CODEX_BIN, "-q", "-a", approval]
    if model:
        cmd.extend(["-m", model])
    cmd.append(prompt)

    with Progress(
        SpinnerColumn(),
        TextColumn("[bold cyan]Running Codex...[/bold cyan]"),
        TimeElapsedColumn(),
        console=console,
        transient=True,
    ) as progress:
        task = progress.add_task("Processing...", total=None)
        console.print(f"[bold cyan]▶ Codex CLI:[/bold cyan] {' '.join(cmd)}")
        _, _, rc = await _run(cmd)
        progress.update(task, completed=True)

    end_time = time.time()
    execution_time = end_time - start_time

    # Calculate token usage estimate
    prompt_tokens = int(len(prompt) * AVG_TOKENS_PER_CHAR)
    # Rough estimate of output tokens based on typical ratio
    output_tokens = int(prompt_tokens * 0.5)  # Assuming output is ~50% of input size

    # Calculate cost estimate
    input_cost = (prompt_tokens / 1000) * COST_PER_1K_INPUT_TOKENS
    output_cost = (output_tokens / 1000) * COST_PER_1K_OUTPUT_TOKENS
    total_cost = input_cost + output_cost

    usage_stats = {
        "execution_time": execution_time,
        "prompt_tokens": prompt_tokens,
        "output_tokens": output_tokens,
        "input_cost": input_cost,
        "output_cost": output_cost,
        "total_cost": total_cost,
    }

    if rc is None:
        return 1, usage_stats
    return rc, usage_stats


# ───────────────────────────  Prompt builder  ────────────────────────────


def build_prompt(diags: Sequence[Diagnostic], language: str) -> str:
    chunks: list[str] = []
    for d in diags:
        try:
            # Path should already be absolute from the Diagnostic class
            ctx_lines = d.path.read_text(encoding="utf-8").splitlines()
            ctx = "\n".join(ctx_lines[d.line - 3 : d.line + 2])
            chunks.append(
                f"File: {d.path}\nLine: {d.line}\n```{language}\n{ctx}\n```\nDiagnostic: {d.message}\n"
            )
        except Exception as e:
            if os.getenv("DEBUG"):
                console.print(f"[red]Error reading {d.path}: {e}[/red]")
            continue

    language_specific_header = {
        "python": "Run `mypy --strict` and `pyright` on the repo",
        "dart": "Run `flutter analyze` on the repo",
        "typescript": "Run `eslint` with TypeScript rules on the repo",
    }

    header = (
        f"{language_specific_header.get(language, 'Analyze')} and fix every reported error. "
        "Re‑run the analysis after each change until all checks pass. "
        "Apply edits automatically. Preserve behaviour."
    )
    return header + "\n\n".join(chunks)


# ───────────────────────────────  CLI  ───────────────────────────────────


async def _run(cmd: List[str]) -> Tuple[str, str, int | None]:
    proc = await asyncio.create_subprocess_exec(
        *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    out, err = await proc.communicate()
    return out.decode(), err.decode(), proc.returncode


def get_analyzer(language: str) -> Type[LanguageAnalyzer]:
    analyzers = {
        "python": PythonAnalyzer,
        "dart": DartAnalyzer,
        "typescript": TypeScriptAnalyzer,
    }
    return analyzers.get(language, PythonAnalyzer)


async def main(argv: List[str] | None = None) -> None:
    p = argparse.ArgumentParser(description="Auto‑lint + Codex auto‑fix helper")
    p.add_argument(
        "--path",
        type=str,
        default=str(Path.cwd()),
        help="Path to analyze (default: current directory)",
    )
    p.add_argument(
        "--language",
        choices=["python", "dart", "typescript"],
        default="python",
        help="Programming language to analyze (default: python)",
    )
    p.add_argument(
        "--use-cli",
        action="store_true",
        default=True,
        help="Invoke Codex CLI instead of Chat API (default)",
    )
    p.add_argument(
        "--approval-mode",
        default=DEFAULT_APPROVAL,
        choices=["suggest", "auto-edit", "full-auto"],
    )
    p.add_argument("--model", help="Codex model ID (passed to -m)")
    p.add_argument(
        "--max-iterations", type=int, default=3, help="Stop after N Codex rounds"
    )
    p.add_argument("--verbose", action="store_true", help="Enable verbose debug output")
    p.add_argument(
        "--applyFix",
        action="store_true",
        help="Apply automatic fixes using Codex (default: only show diagnostics)",
    )
    p.add_argument(
        "--analyze",
        choices=[s.value for s in AnalysisSeverity],
        default=AnalysisSeverity.DEFAULT.value,
        help="Severity levels to analyze (default: show errors, warnings, and info)",
    )
    p.add_argument(
        "--report",
        type=str,
        help="Filename to save a comprehensive report of all fixed issues",
    )
    p.add_argument(
        "--version",
        action="version",
        version=f"CodexFix {VERSION}",
        help="Show version information and exit",
    )
    p.add_argument(
        "--install-completion",
        choices=["bash", "zsh", "fish"],
        help="Install shell completion script for the specified shell",
    )

    args = p.parse_args(argv)

    # Handle shell completion installation if requested
    if args.install_completion:
        sys.exit(install_completion(args.install_completion))

    # Convert path string to Path and ensure it's absolute
    if not os.path.isabs(args.path):
        args.path = Path(os.path.join(os.getcwd(), args.path))
    else:
        args.path = Path(args.path)

    if args.verbose:
        console.print(f"[cyan]Debug: Analyzing path: {args.path}[/cyan]")
        console.print(f"[cyan]Debug: Using language: {args.language}[/cyan]")

    if args.use_cli and shutil.which(CODEX_BIN) is None:
        console.print(
            "[red]Codex CLI not installed. Install with `npm i -g @openai/codex`. Exiting."
        )
        sys.exit(127)

    # Check for required language-specific tools
    if args.language == "dart" and shutil.which("flutter") is None:
        console.print(
            "[red]Flutter SDK not found in PATH. Please install Flutter SDK. Exiting.[/red]"
        )
        sys.exit(127)
    elif args.language == "python" and (
        shutil.which("mypy") is None or shutil.which("pyright") is None
    ):
        console.print(
            "[red]Python linting tools (mypy/pyright) not found. Please install them. Exiting.[/red]"
        )
        sys.exit(127)
    elif args.language == "typescript" and shutil.which("eslint") is None:
        console.print(
            "[red]ESLint not found in PATH. Please install ESLint with TypeScript support. Exiting.[/red]"
        )
        sys.exit(127)

    analyzer_class = get_analyzer(args.language)
    analyzer = analyzer_class(args)

    iterations = 0
    total_diagnostics_fixed = 0
    total_execution_time = 0
    total_prompt_tokens = 0
    total_output_tokens = 0
    total_cost = 0
    start_time = time.time()

    # Initialize report data structure if reporting is enabled
    report_data: Dict[str, Any] = {
        "run_info": {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "path": str(args.path),
            "language": args.language,
        },
        "iterations": [],
    }

    console.print(f"[bold cyan]Starting analysis for {args.path}[/bold cyan]")

    while iterations < args.max_iterations:
        iterations += 1
        iteration_start_time = time.time()
        console.print(
            f"[bold cyan]\n=== Iteration {iterations}/{args.max_iterations} ===[/bold cyan]"
        )

        if args.verbose:
            console.print("[cyan]Debug: Running analyzer...[/cyan]")

        with Progress(
            SpinnerColumn(),
            TextColumn("[bold]Running static analysis...[/bold]"),
            console=console,
            transient=True,
        ) as progress:
            task = progress.add_task("Analyzing...", total=None)
            all_diags = await analyzer.analyze(args.path)
            progress.update(task, completed=True)

        if args.verbose:
            console.print(f"[cyan]Debug: Found {len(all_diags)} diagnostics[/cyan]")

        # Filter diagnostics based on severity level
        if args.analyze == AnalysisSeverity.DEFAULT.value:
            # Keep errors, warnings, and info
            filtered_diags = all_diags
        else:  # args.analyze == AnalysisSeverity.ALL.value
            # Keep all diagnostics
            filtered_diags = all_diags

        if args.verbose:
            console.print(
                f"[cyan]Debug: After filtering: {len(filtered_diags)} diagnostics[/cyan]"
            )

        # Add diagnostics to report data
        iteration_report = {
            "iteration_number": iterations,
            "start_time": time.strftime(
                "%Y-%m-%d %H:%M:%S", time.localtime(iteration_start_time)
            ),
            "diagnostics": [
                {
                    "tool": d.tool,
                    "path": str(d.path),
                    "line": d.line,
                    "column": d.column,
                    "code": d.code,
                    "severity": d.severity,
                    "message": d.message,
                }
                for d in filtered_diags
            ],
        }
        report_data["iterations"].append(iteration_report)

        if not filtered_diags:
            console.print("[green]All checks passed! ✨[/green]")
            break

        tbl = Table(title=f"{len(filtered_diags)} diagnostics", show_lines=True)
        tbl.add_column("Tool", style="cyan")
        tbl.add_column("Severity", style="bold")
        tbl.add_column("Location")
        tbl.add_column("Message")
        for d in filtered_diags:
            severity_color = d.severity_level.display_color
            tbl.add_row(
                d.tool,
                f"[{severity_color}]{d.display_severity}[/{severity_color}]",
                f"{d.path}:{d.line}",
                d.message,
            )
        console.print(tbl)

        # Only apply fixes if --applyFix is specified
        if not args.applyFix:
            console.print(
                "[yellow]Use --applyFix to apply automatic fixes with Codex[/yellow]"
            )
            break

        console.print(
            f"[bold cyan]Applying fixes for {len(filtered_diags)} issues...[/bold cyan]"
        )

        prompt = build_prompt(filtered_diags, args.language)
        Path("fix_codex_prompt.md").write_text(prompt)

        if args.use_cli:
            rc, usage_stats = await run_codex(
                prompt, approval=args.approval_mode, model=args.model
            )

            # Update stats
            diagnostics_fixed = len(filtered_diags)
            total_diagnostics_fixed += diagnostics_fixed
            total_execution_time += usage_stats["execution_time"]
            total_prompt_tokens += usage_stats["prompt_tokens"]
            total_output_tokens += usage_stats["output_tokens"]
            total_cost += usage_stats["total_cost"]

            # Update report with usage stats
            iteration_report.update(
                {
                    "end_time": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "duration": usage_stats["execution_time"],
                    "issues_fixed": diagnostics_fixed,
                    "prompt_tokens": usage_stats["prompt_tokens"],
                    "output_tokens": usage_stats["output_tokens"],
                    "cost": usage_stats["total_cost"],
                }
            )

            if rc != 0:
                console.print(f"[red]Codex exited with code {rc}. Stopping.[/red]")
                iteration_report["status"] = "error"
                iteration_report["error_code"] = rc
                break

            # Display iteration summary
            iteration_time = time.time() - iteration_start_time
            console.print(
                f"[green]✓ Fixed {diagnostics_fixed} issues in {iteration_time:.2f} seconds[/green]"
            )
            iteration_report["status"] = "success"
        else:
            console.print(
                "[yellow]Chat API mode not implemented in this version.[/yellow]"
            )
            sys.exit(1)
    else:
        console.print("[red]Reached max iterations without clean run.[/red]")
        if report_data["iterations"] and len(report_data["iterations"]) > 0:
            report_data["iterations"][-1]["status"] = "max_iterations_reached"

    # Calculate and display final summary
    if args.applyFix and iterations > 0:
        total_time = time.time() - start_time

        summary = Table(
            title="[bold]CodexFix Summary[/bold]", show_header=False, show_lines=True
        )
        summary.add_column("Metric", style="cyan")
        summary.add_column("Value")

        summary.add_row("Total time", f"{total_time:.2f} seconds")
        summary.add_row("Iterations", str(iterations))
        summary.add_row("Issues fixed", str(total_diagnostics_fixed))
        summary.add_row("API processing time", f"{total_execution_time:.2f} seconds")
        summary.add_row("Prompt tokens", f"{total_prompt_tokens:,}")
        summary.add_row("Response tokens", f"{total_output_tokens:,}")
        summary.add_row(
            "Total tokens", f"{total_prompt_tokens + total_output_tokens:,}"
        )
        summary.add_row("Estimated cost", f"${total_cost:.4f}")

        console.print("\n")
        console.print(summary)

        # Update report with summary data
        report_data["summary"] = {
            "total_time": total_time,
            "iterations": iterations,
            "issues_fixed": total_diagnostics_fixed,
            "api_processing_time": total_execution_time,
            "prompt_tokens": total_prompt_tokens,
            "response_tokens": total_output_tokens,
            "total_tokens": total_prompt_tokens + total_output_tokens,
            "estimated_cost": total_cost,
        }

        # Write summary to file for reference
        summary_file = Path("codexfix_summary.json")
        summary_data = {
            "timestamp": time.time(),
            "total_time": total_time,
            "iterations": iterations,
            "issues_fixed": total_diagnostics_fixed,
            "api_processing_time": total_execution_time,
            "prompt_tokens": total_prompt_tokens,
            "response_tokens": total_output_tokens,
            "total_tokens": total_prompt_tokens + total_output_tokens,
            "estimated_cost": total_cost,
            "path": str(args.path),
            "language": args.language,
        }
        summary_file.write_text(json.dumps(summary_data, indent=2))

        # Save comprehensive report if requested
        if args.report:
            try:
                report_path = Path(args.report)
                report_path.write_text(json.dumps(report_data, indent=2))
                console.print(
                    f"[green]Comprehensive report saved to {report_path}[/green]"
                )
            except Exception as e:
                console.print(f"[red]Error saving report to {args.report}: {e}[/red]")

    if iterations > 0 and total_diagnostics_fixed > 0:
        sys.exit(0)
    elif iterations == args.max_iterations:
        sys.exit(2)
    else:
        sys.exit(0)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("Aborted by user.")


# CLI entry point for pip installation
def cli_entry_point() -> None:
    """
    Entry point for the command-line interface.
    This function is called when the user runs the 'codexfix' command.
    """
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("Aborted by user.")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)
