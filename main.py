"""Command-line entry point for the fractal render project."""

import argparse

from modules.api_client import get_json


def main() -> None:
    parser = argparse.ArgumentParser(description="Fractal render project")
    parser.add_argument(
        "--api-url",
        help="Optional URL to fetch JSON data from",
    )
    args = parser.parse_args()

    if args.api_url:
        print(get_json(args.api_url))
    else:
        print("Add source images to input_images/.")
        print("Rendered images and GIFs belong in output/images/ and output/gifs/.")


if __name__ == "__main__":
    main()
