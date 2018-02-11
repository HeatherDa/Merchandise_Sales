from Merchandise_DB import database, ui


#def close_database():
#    db.close()


def use_choice(choice):
    if choice==1:
        database.view_table_ui()
        return

    elif choice==2:
        database.update_record()
        return

    elif choice==3:
        database.add_record()
        return

    elif choice==4:
        database.delete_Record()
        return

    elif choice==5:
        database.search()
        return

    elif choice==6:
        database.settings_ui()

    elif choice==7:
        database.close_database()
        return



def main():
    choice=None
    #for i in range(5):
    #    database.delete_table()
    #database.delete_table()
    #database.drop_settings()
    database.set_globals()


    database.create_items_table()
    database.create_events_table()
    database.create_event_sales_table()
    database.create_orders_table()
    database.create_order_items_table()
    database.create_organization_table()

    while choice !='7':
        choice= ui.display_menu()
        use_choice(choice)

def view_table():
    pass

def update_record():
    pass

def add_record():
    pass

def delete_record():
    pass

def search():
    pass



































main()