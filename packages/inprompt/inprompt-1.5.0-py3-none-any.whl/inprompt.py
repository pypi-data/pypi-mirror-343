"""inprompt: A tiny CLI that prints files as Markdown-formatted code blocks.

It supports a --fence flag (or -f) that lets you specify the exact delimiter
string used for the Markdown code fences.

By default, it uses four backticks (````) instead of the more common three to
avoid delimiter collisions when the source already contains triple backticks.

Example:
    inprompt path/to/file.py '**/*.py' | pbcopy
"""

import glob
from pathlib import Path

from absl import app, flags
from loguru import logger

FLAGS = flags.FLAGS
flags.DEFINE_string(
    "fence",
    "````",
    "Fence delimiter string placed before and after each file's contents.",
)
flags.DEFINE_alias("f", "fence")


def print_usage() -> None:
    """Log usage information."""
    logger.info("Usage: inprompt [--fence <fence>] <files or patterns> ...")
    logger.info("Example: inprompt my_script.py '**/*.py' | pbcopy")


def match_file_patterns(patterns: list[str]) -> list[str]:
    """Expand glob patterns and return sorted, unique file paths."""
    filenames = []
    for pattern in patterns:
        matched = sorted(glob.glob(pattern, recursive=True))
        if not matched:
            logger.warning("No files matched pattern: {}", pattern)
        filenames.extend(matched)
    # Preserve order while removing duplicates
    return list(dict.fromkeys(filenames))


def read_and_format_source_code(filename: str, fence: str) -> str:
    """Read file contents and wrap them in a Markdown code fence."""
    path = Path(filename)
    try:
        content = path.read_text(encoding="utf-8").rstrip()
    except FileNotFoundError:
        logger.error("File not found: {}", filename)
        raise
    logger.info("Formatting file: {}", filename)
    return f"{filename}\n{fence}\n{content}\n{fence}"


def main(argv: list[str]) -> int:
    """Main CLI entry point."""
    if len(argv) < 2:
        logger.error("No files or file patterns specified.")
        print_usage()
        return 2

    file_patterns = argv[1:]
    filenames = match_file_patterns(file_patterns)
    if not filenames:
        logger.error("No matching files found.")
        return 3

    fence = FLAGS.fence
    formatted = [read_and_format_source_code(fname, fence) for fname in filenames]

    # Output formatted content to STDOUT.
    print("\n\n".join(formatted))

    logger.info("Formatted and outputted {} files.", len(filenames))
    return 0


def run() -> None:
    """Console script entry point."""
    app.run(main)


if __name__ == "__main__":
    run()
