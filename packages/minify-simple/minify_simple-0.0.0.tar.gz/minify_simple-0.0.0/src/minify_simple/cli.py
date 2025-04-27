#!/usr/bin/env python3
import os
import argparse

from glob import glob

from rich.console import Console

from .minify import Language, minify_file


def main():
    languages = [language.value for language in Language]
    parser = argparse.ArgumentParser(description="Minify web file: js, css, html")
    parser.add_argument("path", help="Input path. Directory or file")
    parser.add_argument("-o", "--output", help="Output filename")
    parser.add_argument("-l", "--language", choices=languages, help="Language of code")
    parser.add_argument("-s", "--suffix", help="Add suffix to output filename")
    parser.add_argument(
        "-r",
        "--recursively",
        action="store_true",
        help="Include subdirectories"
    )
    parser.add_argument(
        "--no-with-suffix",
        action="store_true",
        help="Do not minify if it already has the suffix"
    )
    args = parser.parse_args()
    console = Console()

    paths = [args.path]
    if os.path.isdir(args.path):
        paths = glob(f"{args.path}/**", recursive=args.recursively)

    if 1 < len(paths) and args.output:
        console.print(
            "WARNING:",
            "Multiple file input. '--output' parameter ignored",
            style="yellow"
        )
        out_filename = None
    else:
        out_filename = args.output or None

    out_filenames = _minify(
        paths,
        out_filename=out_filename,
        language=Language(args.language) if args.language else None,
        suffix=args.suffix or None,
        check_suffix=args.no_with_suffix
    )
    for filename in out_filenames:
        print(filename)


def _minify(
    filenames: list[str],
    out_filename: str | None = None,
    language: Language | None = None,
    suffix: str | None = None,
    check_suffix: bool = True
) -> list[str]:
    out_filenames = []
    for filename in filenames:
        try:
            min_filename = minify_file(
                filename,
                out_filename=out_filename,
                language=language,
                suffix=suffix,
                check_suffix=check_suffix
            )
        except Exception as err:
            print(err)
            continue
        else:
            out_filenames.append(min_filename)
    return out_filenames


if __name__ == "__main__":
    main()
