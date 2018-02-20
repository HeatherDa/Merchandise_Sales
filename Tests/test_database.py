from Merchandise_DB import database
from Merchandise_DB.database import MyError
from unittest import TestCase


class TestDatabase(TestCase):

    def test_is_ID(self):
        #this tests is_ID and also tests whether tables were created
        database.create_tables()
        self.assertTrue(True, database.is_ID("items", 1))
        self.assertFalse(False, database.is_ID("items", 0))
        self.assertTrue(True, database.is_ID("events", 1))
        self.assertFalse(False, database.is_ID("events", 0))
        self.assertTrue(True, database.is_ID("event_sales", 1, 1))
        self.assertFalse(False, database.is_ID("event_sales", 0, 0))
        self.assertTrue(True, database.is_ID("orders", 1))
        self.assertFalse(False, database.is_ID("orders", 0))
        self.assertTrue(True, database.is_ID("order_items", 1, 1))
        self.assertFalse(False, database.is_ID("order_items", 0, 0))

    def test_salesTax(self):
        pass

    def get_types(self):
        item_types = ['T-Shirt','CD','Poster']
        event_types = ['Signing', 'Concert']


    def test_auto_update_inventory(self):
        database.create_tables()
        self.assertEqual
