import Merchandise_DB.merchandising_DB
from Merchandise_DB.merchandising_DB import MyError
from unittest import TestCase

class TestUi(TestCase):

    def test_display_menu(self):
        with self.assertRaises(MyError):
            Merchandise_DB.ui.display_menu()