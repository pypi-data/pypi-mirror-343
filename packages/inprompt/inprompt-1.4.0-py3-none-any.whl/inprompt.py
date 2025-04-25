"""inprompt: CLI to output files as Markdown code blocks for LLM prompts.

It uses four backticks (````) for code fences instead of three, to avoid delimiter
collisions when source contains triple backticks.

Example usage:
    inprompt --count-lines path/to/file.py '**/*.py' | pbcopy
"""

from __future__ import annotations

import glob
from pathlib import Path

from absl import app, flags
from loguru import logger

FLAGS = flags.FLAGS
flags.DEFINE_bool(
    "count_lines",
    False,
    "If true, log the number of lines per file and the aggregate total.",
)


def print_usage() -> None:
    """Log usage info."""
    logger.info(
        "Usage: inprompt [--count-lines] <files or patterns> [<files or patterns> ...]"
    )
    logger.info("Example: inprompt --count-lines my_script.py '**/*.py' | pbcopy")


def match_file_patterns(patterns: list[str]) -> list[str]:
    """Glob patterns and return sorted, unique matches.

    Args:
        patterns: Glob patterns.

    Returns:
        De-duplicated, sorted filenames.
    """
    filenames = []
    for pattern in patterns:
        matched_files = sorted(glob.glob(pattern, recursive=True))
        if not matched_files:
            logger.warning("No files matched pattern: {}", pattern)
        filenames.extend(matched_files)

    # Preserve order while removing duplicates
    return list(dict.fromkeys(filenames))


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
    path = Path(filename)
    try:
        content = path.read_text(encoding="utf-8").rstrip()
    except FileNotFoundError:
        logger.error("File not found: {}", filename)
        raise

    lines = _count_lines(content)

    if FLAGS.count_lines:
        logger.info("Formatting file: {} ({} lines)", filename, lines)
    else:
        logger.info("Formatting file: {}", filename)

    fenced = f"{filename}\n````\n{content}\n````"
    return fenced, lines


def main(argv: list[str]) -> int:
    """CLI entry point.

    Args:
        argv: Command-line arguments (argv[0] is the program name).

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

    formatted_results = [read_and_format_source_code(f) for f in filenames]
    formatted_contents = [result[0] for result in formatted_results]

    # Emit the markdown to STDOUT.
    print("\n\n".join(formatted_contents))

    if FLAGS.count_lines:
        total_lines = sum(result[1] for result in formatted_results)
        logger.info(
            "Formatted and outputted {} files ({} lines).", len(filenames), total_lines
        )
    else:
        logger.info("Formatted and outputted {} files.", len(filenames))

    return 0


def run() -> None:
    """Console script entry point."""
    app.run(main)


if __name__ == "__main__":
    run()
