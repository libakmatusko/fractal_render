import unittest
from unittest.mock import MagicMock, patch

from modules.api_client import get_json


class GetJsonTests(unittest.TestCase):
    @patch("modules.api_client.urlopen")
    def test_returns_decoded_json_response(self, mock_urlopen: MagicMock) -> None:
        response = MagicMock()
        response.read.return_value = b'{"message": "ok"}'
        mock_urlopen.return_value.__enter__.return_value = response

        result = get_json("https://example.com/data")

        self.assertEqual(result, {"message": "ok"})
        mock_urlopen.assert_called_once()


if __name__ == "__main__":
    unittest.main()
