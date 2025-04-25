"""inprompt: CLI to output files as Markdown code blocks for LLM prompts.

It uses four backticks (````) for code fences instead of three, to avoid delimiter
collisions when source contains triple backticks.

Example usage:
    inprompt path/to/file.py '**/*.py' | pbcopy
"""

from __future__ import annotations

import glob

from absl import app
from loguru import logger


def print_usage() -> None:
    """Log usage info."""
    logger.info("Usage: inprompt <files or patterns> [<files or patterns> ...]")
    logger.info("Example: inprompt my_script.py '**/*.py' | pbcopy")


def match_file_patterns(patterns: list[str]) -> list[str]:
    """Glob patterns and return sorted, unique matches.

    Args:
        patterns (list[str]): Glob patterns.

    Returns:
        list[str]: De-duplicated, sorted filenames.
    """
    filenames = []
    for pattern in patterns:
        matched_files = sorted(glob.glob(pattern, recursive=True))
        if not matched_files:
            logger.warning("No files matched pattern: {}", pattern)
        filenames.extend(matched_files)
    return list(dict.fromkeys(filenames))  # Preserve order while removing duplicates


def _count_lines(text: str) -> int:
    """Return the number of lines in text."""
    return len(text.splitlines())


def read_and_format_source_code(filename: str) -> tuple[str, int]:
    """Return file contents as a Markdown code fence and its line count.

    Args:
        filename: Path to the file.

    Returns:
        Tuple where the first element is the Markdown code-fenced string and the
        second element is the number of lines in the file.

    Raises:
        FileNotFoundError: If filename does not exist.
    """
    try:
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read().strip()
        lines = _count_lines(content)
        logger.info("Formatting file: {} ({} lines)", filename, lines)
        fenced = f"{filename}\n````\n{content}\n````"
        return fenced, lines
    except FileNotFoundError:
        logger.error("File not found: {}", filename)
        raise


def main(argv: list[str]) -> int:
    """CLI entry point.

    Args:
        argv: Command-line arguments.

    Returns:
        Exit code.
    """
    if len(argv) < 2:
        logger.error("No files or file patterns specified.")
        print_usage()
        return 2

    file_patterns = argv[1:]
    filenames = match_file_patterns(file_patterns)

    if not filenames:
        logger.error("No matching files found.")
        return 3

    formatted_results = [read_and_format_source_code(fname) for fname in filenames]
    formatted_contents = [result[0] for result in formatted_results]
    total_lines = sum(result[1] for result in formatted_results)

    # Emit the markdown to STDOUT.
    print("\n\n".join(formatted_contents))

    logger.info(
        "Formatted and outputted {} files ({} lines)", len(filenames), total_lines
    )
    return 0


def run() -> None:
    """Console script entry point."""
    app.run(main)


if __name__ == "__main__":
    run()
