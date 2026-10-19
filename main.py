"""Command-line entry point for local processing or the HTTP API."""

import argparse
from pathlib import Path

from modules.processor import OUTPUT_FORMATS, SUPPORTED_EXTENSIONS, process_image


def choose_input_image(input_dir: Path) -> Path | None:
    if not input_dir.is_dir():
        raise FileNotFoundError(f"Input directory does not exist: {input_dir}")

    images = sorted(
        path
        for path in input_dir.iterdir()
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
    )
    if not images:
        print(f"No supported images found in {input_dir}.")
        return None

    print("Choose an input image:")
    for index, path in enumerate(images, start=1):
        print(f"{index}. {path.name}")

    while True:
        choice = input("Enter a number (or q to quit): ").strip().lower()
        if choice == "q":
            return None
        if choice.isdecimal() and 1 <= int(choice) <= len(images):
            return images[int(choice) - 1]
        print(f"Enter a number from 1 to {len(images)}, or q to quit.")


def choose_output_format() -> str:
    formats = list(OUTPUT_FORMATS)
    print("Choose an output format:")
    for index, format_name in enumerate(formats, start=1):
        print(f"{index}. {format_name.upper()}")

    while True:
        choice = input("Enter a number: ").strip()
        if choice.isdecimal() and 1 <= int(choice) <= len(formats):
            return formats[int(choice) - 1]
        print(f"Enter a number from 1 to {len(formats)}.")


def main() -> None:
    project_dir = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description="Process images locally or serve the OpenAPI endpoint")
    parser.add_argument(
        "--serve",
        action="store_true",
        help="Start the HTTP API instead of processing local images",
    )
    parser.add_argument("--input-dir", type=Path, default=project_dir / "input_images")
    parser.add_argument("--output-dir", type=Path, default=project_dir / "output")
    parser.add_argument("--host", default="127.0.0.1", help="API server host")
    parser.add_argument("--port", type=int, default=8000, help="API server port")
    args = parser.parse_args()

    if args.serve:
        import uvicorn

        uvicorn.run("modules.api:app", host=args.host, port=args.port)
        return

    input_path = choose_input_image(args.input_dir)
    if input_path is None:
        return

    output_format = choose_output_format()
    format_name, extension, output_folder = OUTPUT_FORMATS[output_format]
    output_dir = args.output_dir / output_folder
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{input_path.stem}{extension}"
    if output_path.exists():
        overwrite = input(f"{output_path} already exists. Overwrite? [y/N]: ").strip().lower()
        if overwrite not in {"y", "yes"}:
            print("Cancelled; existing output was not changed.")
            return

    output_path.write_bytes(process_image(input_path.read_bytes(), format_name))
    print(f"Saved {output_path}")


if __name__ == "__main__":
    main()
