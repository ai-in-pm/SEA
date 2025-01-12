```python
import logging
import unittest
from unittest.mock import patch, MagicMock
import scraper


class TestScraper(unittest.TestCase):
    """
    Class to provide test cases for scraper.py
    """

    def setUp(self):
        """
        Set up logging for testing
        """
        logging.basicConfig(level=logging.DEBUG)

    @patch('scraper.requests.get')
    def test_get_html_content(self, mock_get: MagicMock):
        """
        Test to verify the function get_html_content in scraper.py is working properly.
        """
        url: str = "https://example.com"
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = "Mock Text Data"

        response = scraper.get_html_content(url)
        self.assertEqual(response, "Mock Text Data")

    @patch('scraper.requests.get')
    def test_get_html_content_error(self, mock_get: MagicMock):
        """
        Test to verify the function get_html_content in scraper.py handles errors properly.
        """
        url: str = "https://badexample.com"
        mock_get.return_value.status_code = 404

        with self.assertRaises(scraper.ScraperException) as context:
            scraper.get_html_content(url)

        self.assertTrue("Error fetching data from URL" in str(context.exception))


if __name__ == '__main__':
    unittest.main()
```
This is a basic test suit for `scraper.py` that checks for the success and error handling of the `get_html_content` function. Note that to apply this test suit to a specific codebase and situation, you may need to adjust the assertion logic.