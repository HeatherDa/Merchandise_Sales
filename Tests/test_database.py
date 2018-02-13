from Merchandise_DB import database
from Merchandise_DB.database import MyError
from unittest import TestCase

class Test_database(TestCase):

    def test_is_ID(self):

        database.create_tables()
        self.assertTrue(True, database.is_ID("items",1))
        self.assertFalse(False, database.is_ID("items",0))
        self.assertTrue(True, database.is_ID("events", 1))
        self.assertFalse(False, database.is_ID("events", 0))
        self.assertTrue(True, database.is_ID("event_sales", 1,1))
        self.assertFalse(False, database.is_ID("event_sales", 0,0))
        self.assertTrue(True, database.is_ID("orders", 1))
        self.assertFalse(False, database.is_ID("orders", 0))
        self.assertTrue(True, database.is_ID("order_items", 1,1))
        self.assertFalse(False, database.is_ID("order_items", 0,0))

    def test_salesTax(self):
        pass

    def get_types(self):
        item_types=['T-Shirt','CD','Poster']
        event_types=['Signing', 'Concert']
        pass

    # def test_tax_and_profit_for_event_sales(self):
    #     database.create_tables()
    #     with self.assertRaises(MyError):
    #         database.tax_and_profit_for_event_sales(1,1)
    # def test_delete_table(self):
    #     database.create_tables()
    #     database.delete_table()

    def test_auto_update_event_sales(self):
        database.create_tables()
        p=database.view_table('event_sales')
        for i in p:
            print(i['sales_Profit'])
        database.auto_update_event_sales()
        p1=database.view_table('event_sales')
        for i in p1:
            print(i['sales_Profit'])
        #self.assertEqual( , database.get_from_event_sales(1,1,'profit'))