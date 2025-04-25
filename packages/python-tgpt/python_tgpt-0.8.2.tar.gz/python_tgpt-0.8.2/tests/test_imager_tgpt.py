import pytgpt.imager as imager
from typing import List
from typing import Generator
import unittest
import os


class TestImager(unittest.TestCase):

    def setUp(self):
        self.imager = imager.Imager()
        self.prompt: str = "hello world"

    @unittest.skipUnless(
        os.getenv("PYTGPT_TEST_MEDIA", "") == "true",
        "PYTGPT_TEST_MEDIA environment variable is not set to 'true' ",
    )
    def test_non_stream(self):
        """Test one photo generation"""
        img = self.imager.generate(self.prompt)
        self.assertIsInstance(img, List), "Image not generated"
        self.assertIsInstance(img[0], bytes), "Image not generated"

    @unittest.skipUnless(
        os.getenv("PYTGPT_TEST_MEDIA", "") == "true",
        "PYTGPT_TEST_MEDIA environment variable is not set to 'true' ",
    )
    def test_stream(self):
        """Test multiple photo generation"""
        generator = self.imager.generate(self.prompt, amount=2, stream=True)
        self.assertIsInstance(generator, Generator)


class TestProdia(TestImager):
    def setUp(self):
        self.imager = imager.Prodia()
        self.prompt: str = "hello world"


# Tests for AsyncImager and AsyncProdia to be implemented
if __name__ == "__main__":
    unittest.main()
