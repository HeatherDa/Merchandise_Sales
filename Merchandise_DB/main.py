from Merchandise_DB import database, ui, databaseTools, queries
import sys

#def close_database():
#    db.close()


def use_choice(choice):
    if choice==1:
        databaseTools.view_table_ui()
        return 1

    elif choice==2:
        update_record()
        return 2

    elif choice==3:
        databaseTools.add_record()
        return 3

    elif choice==4:
        delete_record()
        return 4

    elif choice==5:
        search()
        return 5

    elif choice==6:
        databaseTools.settings_ui()
        return 6

    elif choice==7:
        database.close_database()
        return 7



def main():
    choice=None
    #database.delete_table()
    #database.create_tables()
    database.reInitialize_database() #go back to default values
    database.auto_update_inventory()
    database.set_globals()

    while choice !='7':
        choice= ui.display_menu()
        use_choice(choice)
    database.close_database()
    ui.show_message("Goodbye!")

def view_table():
    pass

def update_record():
    table= ui.get_table_input()
    if table == 'items':
        databaseTools.update_items_ui()
    elif table == 'events':
        databaseTools.update_event_ui()
    elif table == 'event_sales':
        databaseTools.update_event_sales_ui()
    elif table == 'orders':
        databaseTools.update_order_ui()
    elif table == 'order_items':
        databaseTools.update_order_item_ui()

def add_record():
    pass

def delete_record():
    pass

def search():
    choice = ui.get_search_menu_input()
    if choice == 0:
        return
    elif choice == 1:
        queries.search_by_id_ui()
    elif choice == 2:
        queries.search_by_type_ui()
    elif choice == 3:
        queries.search_by_date_ui() #use original choice 3 code to display results, use ui to get date input from user
    elif choice == 4:
        queries.search_by_on_hand_ui()
    elif choice == 5:
        queries.search_by_salesTax_due_ui()
    elif choice == 6:#TODO make new menu with sub options
        queries.search_by_profit_ui()
    elif choice == 7:
        queries.search_by_event_ui()


main()