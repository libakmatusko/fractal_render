"""Image processing shared by local runs and the HTTP API."""

from io import BytesIO

from PIL import Image, ImageSequence


SUPPORTED_EXTENSIONS = {".bmp", ".gif", ".jpeg", ".jpg", ".png", ".tif", ".tiff", ".webp"}
OUTPUT_FORMATS = {
    "png": ("PNG", ".png", "images"),
    "jpg": ("JPEG", ".jpg", "images"),
    "gif": ("GIF", ".gif", "gifs"),
}


def process_image(image_data: bytes, output_format: str | None = None) -> bytes:
    """Process an image and encode it in the requested format.

    The image algorithm is currently a pass-through; GIF animation is retained
    when saving as GIF. Converting an animated GIF to a still format uses its
    first frame.
    """
    with Image.open(BytesIO(image_data)) as image:
        target_format = (output_format or image.format or "PNG").upper()
        if target_format not in {details[0] for details in OUTPUT_FORMATS.values()}:
            raise ValueError(f"Unsupported output format: {target_format}")

        output = BytesIO()
        if target_format == "GIF":
            frames = [frame.convert("RGBA") for frame in ImageSequence.Iterator(image)]
            durations = [
                frame.info.get("duration", image.info.get("duration", 100))
                for frame in ImageSequence.Iterator(image)
            ]
            frames[0].save(
                output,
                format="GIF",
                save_all=True,
                append_images=frames[1:],
                duration=durations,
                loop=image.info.get("loop", 0),
            )
        else:
            image.seek(0)
            frame = image.copy()
            if target_format == "JPEG":
                rgba = frame.convert("RGBA")
                background = Image.new("RGB", rgba.size, "white")
                background.paste(rgba, mask=rgba.getchannel("A"))
                frame = background
            frame.save(output, format=target_format)
        return output.getvalue()
