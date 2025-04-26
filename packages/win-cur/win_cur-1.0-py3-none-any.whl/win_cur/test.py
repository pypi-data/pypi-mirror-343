import unittest
from os import remove

try:
    from win_cur.cursor import Cursor
except ImportError:
    from cursor import Cursor


class MyTestCase(unittest.TestCase):
    @staticmethod
    def test_something():
        from PIL import Image

        image = Image.open(r"C:\Windows\Cursors\aero_arrow.cur")
        image = image.convert("RGBA")
        test_cur = Cursor()
        test_cur.add_cursor(image.width, image.height, 0, 0, image.tobytes())
        test_cur.save_file("test.cur")
        remove("test.cur")


if __name__ == '__main__':
    unittest.main()
