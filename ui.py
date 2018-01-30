import DataValidation

def display_menu():
    option=input("\n1. Display table\n2. Update Record\n3. Add New Record\n4. Delete Record\n5. Search\n6. Quit\nEnter selection: ")
    print("")
    if option=='1':
        return '1'
    elif option =='2':
        return '2'
    elif option =='3':
        return '3'
    elif option =='4':
        return '4'
    elif option == '5':
        return '5'
    elif option =='6':
        return '6'

def show_message(message):
    print(message)

def get_numeric_input(message):
    n=input(message)
    while True:
        if DataValidation.is_int(n):
            return int(n)
        elif DataValidation.is_Float(n):
            return float(n)
        else:
            print("Please only use numeric characters (Decimals are okay.)")

def get_input(message):
    """check string for non alphanumeric characters, leaving in '/' , '.', or ',' for phone, date, and descriptions.
        Return only good strings."""
    s= input(message)
    ok=""
    while True:
        for char in s:
            if char.isalnum():
                ok=ok+char
            elif char in '/,. ':
                ok=ok+char
            else:
                show_message("This string contains a forbidden character. Try again.")
                ok=""
        if len(ok)==s:
            return ok


def get_type_input(types):
    message=""
    for i in types:
        option=str(types[i]+1) + ': ' + i + "\n"
        message=message+option

    while True: #Accept only valid input
        print(message)
        choice = input("\nPlease enter the number of your selection.")
        if DataValidation.is_int(choice):
            return types[int(choice)-1]

def get_table_input():
    while True:
        name = input("\n1. merchandise table\n2. events table\n3. event sales table\n\nEnter your selection")
        if name=='1':
            return "merchandise"
        elif name=='2':
            return "events"
        elif name=='3':
            return "event_sales"

def get_search_menu_input():
    while True:
        choice=input("1. Get Record by ID \n2. Get Record by Type \n3. Get Events sorted by Date \n"
                     "4. Get items by quantity in inventory \n5. Get Total Sales Tax Owed for year to date \n"
                     "6. Get list of items by profit \n7. Get items sold by event_ID\n\nEnter your selection: ")
        if choice in ('1234567'):
            return choice
def get_date_input():
    d=input("Please enter the date and time using this format YYYY-MM-DD HH:MM.")
    da=d.split(' ')
    count=0
    count2=0
    while True:
        if (len(da[0])==10) & (len(da[1])==5):
            for char in da[0]:
                if char in '0123456789-':
                    count=count+1
            for char in da[1]:
                if char in '0123456789:':
                    count2=count2+1
            if (count==len(da[0])) & (count2==len(da[1])):
                d=d+":00"
                return d
            else:
                print('Please copy the format exactly')
        else:
            print('Please copy the format exactly')

def merchandise_header():
    show_message("Item ID: \tType: \tDescription: \t\t\tTotal Ordered: \tCost: \tTaxable?")

def events_header():
    show_message("Event ID: \t Event Type: \t Event Address: \t\t\tName of Contact: \t\tContact Phone: ")

def event_sales_header():
    show_message("Event ID: \t Item ID: \t Total Sold: \t Sale Price: \t Sale Tax Collected: ")

def inventory_Header():
    show_message("Item ID: \t Total Number Sold: \t Total Purchased: \t Remaining Inventory: ")