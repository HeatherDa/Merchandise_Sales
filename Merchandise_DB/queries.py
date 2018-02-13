from Merchandise_DB import ui,database

def search_by_profit_ui():
    ui.show_message("\n1. Profit for a specific item ID\n2. Total Profit per item\n3. Total profit this year\n")
    choice = ui.get_numeric_input("Enter your selection: ", 'i')

    if choice == 1:
        item_ID = ui.get_numeric_input("\nWhat item ID do you want to use?", 'i')
        records=database.search_by_profit(choice,item_ID) #returns list (record,profit)
        ui.profits_header()

        for rec in records:
            profit = rec[1]
            record = rec[0]
            if database.is_taxable(record['event_ID'], record['item_ID']):
                tax = database.salesTax(record['sales_Price'], record['sales_Total'])
                profit = profit - tax
            ui.profit_result_format(record, profit)
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