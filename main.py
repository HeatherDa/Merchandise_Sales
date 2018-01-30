import ui
import merchandising_DB
#def close_database():
#    db.close()


def use_choice(choice):
    if choice=='1':
        merchandising_DB.view_table()
        return

    elif choice=='2':
        merchandising_DB.update_entry()
        return

    elif choice=='3':
        merchandising_DB.add_record()
        return

    elif choice=='4':
        merchandising_DB.delete_Record()
        return

    elif choice=='5':
        merchandising_DB.search_menu()
        return

    elif choice=='6':
        merchandising_DB.close_database()
        return

def main():
    choice=None
    #delete_juggler_table()

    while choice !='6':
        choice=ui.display_menu()
        use_choice(choice)

main()