import unittest
from urlify import shorten_url

class TestUrlify(unittest.TestCase):
    def test_shorten_url_success(self):
        """Test successful URL shortening"""
        test_url = "https://www.example.com/very/long/url/path"
        shortened = shorten_url(test_url)
        self.assertTrue(shortened.startswith("https://tinyurl.com/") or 
                       shortened.startswith("http://tinyurl.com/"))
        self.assertLess(len(shortened), len(test_url))

    def test_invalid_url(self):
        """Test error handling for invalid URLs"""
        with self.assertRaises(Exception):
            shorten_url("not_a_valid_url")

if __name__ == '__main__':
    unittest.main()
