from Merchandise_DB import ui, database
from datetime import datetime


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
        while True:
            d1 = ui.get_date_input("Enter the beginning date: ", 'date')
            d2 = ui.get_date_input("Enter the ending date: ", 'date')
            bdate = datetime.strptime(d1, '%Y-%m-%d').date()
            edate = datetime.strptime(d2, '%Y-%m-%d').date()
            if bdate < edate:  # this should check whether the beginning date is in fact before the ending date
                v = [choice, ch, d1, d2]
                break
            else:
                ui.show_message('Your beginning date is after your ending date.  Try again.')

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
        event = ui.get_numeric_input('Enter the event ID you want to look for or type 0 to exit: ', 'i')
        if event == 0:
            return
        elif database.is_ID('events', event):
            records = database.search_by_event(event)
            if len(records) > 0:
                ui.event_sales_header()
                for rec in records:
                    ui.event_sales_record_format(rec)
                return
            else:
                ui.show_message('No records found for that event ID.')
        else:
            ui.show_message('There is no event associated with that ID.')


def search_by_remaining_inventory_ui():
    par = ui.get_numeric_input("Return items where remaining inventory is less than: ", 'i')
    a = database.search_available_inventory_by_item('all', par)
    ui.inventory_header()
    for i in a:
        sold = i[1]
        order = i[2]
        rem = order - sold
        if rem < par:
            ui.inventory_record_format([i[0], sold, order, rem])


def search_by_sales_tax_due_ui():
    v = []
    choice = ui.get_numeric_input('1. Get sale tax due for this year to date\n'
                                  '2. Get sale tax due for a previous year\n'
                                  '3. Get sale tax due for a given time period\n'
                                  '4. Exit\n\n'
                                  'Enter Selection: ', 'i')
    if choice == 4:
        return
    elif choice == 3:
        while True:
            d1 = ui.get_date_input("Enter the beginning date: ", 'date')
            d2 = ui.get_date_input("Enter the ending date: ", 'date')
            bdate = datetime.strptime(d1, '%Y-%m-%d').date()
            edate = datetime.strptime(d2, '%Y-%m-%d').date()
            if bdate < edate: #this should check whether the beginning date is in fact before the ending date
                v = [choice, d1, d2]
                break
            else:
                ui.show_message('Your beginning date is after your ending date.  Try again.')
    else:
        year = ui.get_numeric_input("Enter the year you want to know sales tax information about (YYYY): ", 'i')
        v = [choice, year]
    sale_tax_total = database.search_by_sales_tax_due(v)
    if sale_tax_total == None:
        sale_tax_total = "0.00"
    ui.show_message("Total sales tax owed for this period is: " + str(sale_tax_total))
