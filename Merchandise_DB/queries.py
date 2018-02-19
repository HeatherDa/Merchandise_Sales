from Merchandise_DB import ui, database


def search_by_profit_ui():
    ui.show_message("\n1. Profit for a specific item ID\n2. Total Profit per item\n3. Total profit this year\n"
                    "4. Average Profit\n5. Profit by event\n6. Exit")
    choice = ui.get_numeric_input("Enter your selection: ", 'i')
    if choice == 6:
        return
    elif choice == 1:
        item_ID = ui.get_numeric_input("\nWhat item ID do you want to use?", 'i')
        records = database.search_by_profit(choice, item_ID)
        ui.profits_header()
        for record in records:
            ui.profit_result_format(record)
    elif choice == 4:
        avg_profit_ui()
    elif choice == 2:
        records = database.search_by_profit(choice)
        ui.profits_header()
        for record in records:
            ui.profit_result_format(record)
    elif choice == 3:
        records = database.search_by_profit(choice)
        total = records[0][0]
        ui.show_message('\nTotal Profit made so far this year: ' + ('%.2f' % total))
    elif choice == 5:
        records = database.search_by_profit(choice)
        m = "\n\033[1m" + "\033[4m" + 'Event ID: \tProfits: ' + "\033[0m"
        ui.show_message(m)
        for record in records:
            ui.profit_result_format(record)


def search_by_id_ui():
    table = ui.get_table_input()
    if table == 0:
        return
    elif table == 'items':
        i_id = ui.get_numeric_input("Enter the id you wish to search by: ", 'i')
        records = database.get_from_items(i_id, 'all')
        ui.items_header()
        ui.item_record_format(records)
    elif table == 'events':
        e_id = ui.get_numeric_input("Enter the id you wish to search by: ", 'i')
        records = database.get_from_events(e_id, 'all')
        ui.events_header()
        ui.event_record_format(records)
    elif table == 'orders':
        o_id = ui.get_numeric_input("Enter the id you wish to search by: ", 'i')
        records = database.get_from_orders(o_id, 'all')
        ui.orders_header()
        ui.order_record_format(records)
    elif table == 'event_sales':
        e_id = ui.get_numeric_input("Enter the event id you wish to search by: ", 'i')
        i_id = ui.get_numeric_input("Enter the items id you wish to search by: ", 'i')
        records = database.get_from_event_sales(e_id, i_id, 'all')
        ui.event_sales_header()
        ui.event_sales_record_format(records)
    elif table == 'order_items':
        o_id = ui.get_numeric_input("Enter the order id you wish to search by: ", 'i')
        i_id = ui.get_numeric_input("Enter the items id you wish to search by: ", 'i')
        records = database.get_from_order_items(o_id, i_id, 'all')
        ui.order_items_header()
        ui.order_items_record_format(records)


def avg_profit_ui():
    choice = ui.get_numeric_input('1. Items with above average profit\n2. Items with below average profit\n'
                                  '3. Exit', 'i')
    if choice == 3:
        return
    ch = ui.get_numeric_input('1. Average over all data\n2. Average over period of time', 'i')
    if ch == 1:
        v = [choice, ch]
        records = database.avg_profit(v)
        message = 'Average profit per item: \t' + str(records[2])
        ui.show_message(message)
        ui.show_message('item_ID: \t\tProfit per item')
        for i in records[0]:
            m = str(i[0]) + ' \t\t ' + str(i[1])
            ui.show_message(m)
    elif ch == 2:
        d1 = ui.get_date_input('Enter starting date')
        d2 = ui.get_date_input('Enter ending date (or now for current date)')
        v = [choice, ch, d1, d2]
        records = database.avg_profit(v)
        message = 'Average profit per item: \t' + str(records[2])
        ui.show_message(message)
        ui.show_message('item_ID: \t\tProfit per item')
        for i in records[0]:
            m = str(i[0]) + ' \t\t ' + str(i[1])
            ui.show_message(m)


def search_by_type_ui():
    table = ui.get_type_table_input()
    if table == 0:
        return
    else:
        types = database.get_types(table)
        ty = ui.get_type_input(types)
        v = (table, ty)
        records = database.search_by_type(v)

        if table == 'items':
            ui.items_header()
            for record in records:
                ui.item_record_format(record)
        elif table == 'events':
            ui.events_header()
            for record in records:
                ui.event_record_format(record)


def search_by_date_ui():
    choice = ui.get_numeric_input(
        '1. Search for event by date\n'
        '2. Display events table in order by date, from today forward.\n\n'
        'Enter selection: ', 'i')
    if choice == 1:
        day = ui.get_date_input('Enter the event date you are looking for')
        records = database.search_by_date(choice, day)
        ui.events_header()
        for r in records:
            ui.event_record_format(r)
    else:
        records = database.search_by_date(choice)
        ui.events_header()
        for r in records:
            ui.event_record_format(r)


def search_by_event_ui():
    """return all event_sales items sold at a given event"""
    while True:
        event=ui.get_numeric_input('Enter the event ID for searching or type 0 to exit', 'i')
        if event == 0:
            return
        elif database.is_ID('events', event):
            records = database.search_by_event(event)
            ui.event_sales_header()
            for rec in records:
                ui.event_sales_record_format(rec)
            return
        else:
            ui.show_message('No records found for that ID.')


def search_by_on_hand_ui():
    pass


def search_by_sales_tax_due():
    pass
