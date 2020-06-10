from matplotlib.text import Text
from unittest.case import TestCase

from mpl_format.text.text_utils import wrap_text


class TestTextUtils(TestCase):

    def setUp(self) -> None:

        self.a_to_z = 'abcdefghijklmnopqrstuvwxyz'
        self.digits = '0123456789'
        self.a_to_z__wrapped_10 = 'abcdefghij\nklmnopqrst\nuvwxyz'
        self.a_to_z__wrapped_5 = 'abcde\nfghij\nklmno\npqrst\nuvwxy\nz'
        self.digits__wrapped_5 = '01234\n56789'

    def test_wrap_text__str(self):

        wrapped = wrap_text(text=self.a_to_z, max_width=10)
        self.assertEqual(self.a_to_z__wrapped_10, wrapped)

    def test_wrap_text__text(self):

        text__a_to_z = Text(text=self.a_to_z)
        wrapped = wrap_text(text=text__a_to_z, max_width=10)
        self.assertEqual(self.a_to_z__wrapped_10, wrapped)

    def test_wrap_text__list_str(self):

        expected = [self.a_to_z__wrapped_5, self.digits__wrapped_5]
        wrapped = wrap_text(text=[self.a_to_z, self.digits], max_width=5)
        self.assertEqual(expected, wrapped)
