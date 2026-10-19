import tempfile
import unittest
from io import BytesIO
from pathlib import Path

from PIL import Image

from modules.processor import process_image


def create_image(image_format: str, color: str = "red") -> bytes:
    image = Image.new("RGB", (2, 2), color)
    output = BytesIO()
    image.save(output, format=image_format)
    return output.getvalue()


class ProcessImageTests(unittest.TestCase):
    def test_converts_input_to_selected_output_format(self) -> None:
        result = process_image(create_image("PNG"), "JPEG")

        with Image.open(BytesIO(result)) as converted:
            self.assertEqual(converted.format, "JPEG")
            self.assertEqual(converted.size, (2, 2))

    def test_converts_still_image_to_gif(self) -> None:
        result = process_image(create_image("PNG"), "GIF")

        with Image.open(BytesIO(result)) as converted:
            self.assertEqual(converted.format, "GIF")
            self.assertEqual(converted.n_frames, 1)

    def test_rejects_unknown_output_format(self) -> None:
        with self.assertRaises(ValueError):
            process_image(create_image("PNG"), "UNKNOWN")


if __name__ == "__main__":
    unittest.main()
