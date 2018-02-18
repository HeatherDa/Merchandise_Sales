from Merchandise_DB import ui,database

def search_by_profit_ui():
    ui.show_message("\n1. Profit for a specific item ID\n2. Total Profit per item\n3. Total profit this year\n")
    choice = ui.get_numeric_input("Enter your selection: ", 'i')

    if choice == 1:
        item_ID = ui.get_numeric_input("\nWhat item ID do you want to use?", 'i')
        records=database.search_by_profit(choice,item_ID) #returns list (record,profit)
        ui.profits_header()
        #TODO Finish this function
        #for rec in records:
        #    profit = rec[1]
        #    record = rec[0]
        #    if database.is_taxable(record['event_ID'], record['item_ID']):
        #        tax = database.salesTax(record['sales_Price'], record['sales_Total'])
        #        profit = profit - tax
        #    ui.profit_result_format(record, profit)
    else:
        # This SQL query does not return a sum of profit per item
        # Couldn't get that query to work the way I wanted.
        # So I extract the information myself bellow
        records = database.search_by_profit(choice)
        r = {}
        ui.profits_header()


        if  choice ==2:
            for key in r.keys():
                record = database.get_from_items(key, 'all')
                ui.profit_result_format(record, r[record['item_ID']])  # one record for each item_ID in results

        elif choice ==3:
            total=0
            for key in r.keys():
                total+= r[key]
            ui.show_message('Total Profit made so far: ' + ('%.2f' %total))

def search_by_id_ui():
    table = ui.get_table_input()

    if table == 'items':
        i_id = ui.get_numeric_input("Enter the id you wish to search by: ", 'i')
        records = database.get_from_items(i_id,'all')
        #c.row_factory = sqlite3.Row
        ui.items_header()
        ui.item_record_format(records)
    elif table == 'events':
        e_id = ui.get_numeric_input("Enter the id you wish to search by: ", 'i')
        records = database.get_from_events(e_id,'all')
        #c.row_factory = sqlite3.Row
        ui.events_header()
        ui.event_record_format(records)
    elif table == 'orders':
        o_id = ui.get_numeric_input("Enter the id you wish to search by: ", 'i')
        records = database.get_from_orders(o_id, 'all')
        #c.row_factory = sqlite3.Row
        ui.orders_header()
        print(records,'is a ', type(records))
        ui.order_record_format(records)
    elif table == 'event_sales':
        e_id = ui.get_numeric_input("Enter the event id you wish to search by: ", 'i')
        i_id = ui.get_numeric_input("Enter the items id you wish to search by: ", 'i')
        records = database.get_from_event_sales(e_id, i_id, 'all')
        #c.row_factory = sqlite3.Row
        ui.event_sales_header()
        ui.event_sales_record_format(records)
    elif table == 'order_items':
        o_id = ui.get_numeric_input("Enter the order id you wish to search by: ", 'i')
        i_id = ui.get_numeric_input("Enter the items id you wish to search by: ", 'i')
        records = database.get_from_order_items(o_id, i_id, 'all')
        #c.row_factory = sqlite3.Row
        ui.order_items_header()
        ui.order_items_record_format(records)