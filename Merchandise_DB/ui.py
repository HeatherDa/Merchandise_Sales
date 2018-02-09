from Merchandise_DB import DataValidation


def display_menu():
    '''Show Main Menu'''
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
    else:
        raise FormatError('please enter a number from 1-6')

def show_message(message):
    '''Display a given message'''
    print(message)

def get_numeric_input(message, t):
    '''Get numeric input back in numeric format as either int or float'''
    while True:
        n=input(message)
        if (DataValidation.is_int(n)) & (t== 'i') :
            return int(n)
        elif (DataValidation.is_Float(n)) & (t== 'f'):
            return float(n)
        else:
            print("Entry is not a valid integer or decimal.")
            raise FormatError('This entry is not a valid integer or decimal')

def get_input(message):
    """check string for non alphanumeric characters, leaving in these"/,.-:'" for phone, date, and descriptions.
        Return only good strings."""

    ok=""
    while True:
        s= input(message)
        for char in s:
            if char.isalnum():
                ok=ok+char
            elif char in '/,.-: ':
                ok=ok+char
            else:
                show_message("This string contains a forbidden character. Try again.")
                ok=""
                raise FormatError('This string has forbidden characters')
        if len(ok)==len(s):
            return ok
        else:
            raise FormatError('This string has forbidden characters')

def get_type_input(types):
    message=""
    count=0
    for i in types:
        option=str(types.index(i)+1) + '. ' + i + "\n"
        message=message+option
        count=count+1
    message=message+"Enter 0 to add a new type\n"
    while True: #Accept only valid input
        print(message)
        choice = input("Enter your selection: ")
        if (DataValidation.is_int(choice)):
            if  choice=='0': #if user wants to add a new type
                if 'CD' in types: #Basically checking for which type list to add it to.
                    t=get_input("Enter the new item Type: ")
                    return t
                else:
                    t=get_input("Enter the new event Type: ")
                    return t

            elif int(choice)<count:
                return types[int(choice)-1]
            else:
                raise FormatError('use only numbers from 1 to ', len(types))

def get_table_input():
    while True:
        name = input("\n1. merchandise table\n2. events table\n3. event sales table\n\nEnter your selection: ")
        if name=='1':
            return "merchandise"
        elif name=='2':
            return "events"
        elif name=='3':
            return "event_sales"
        else:
            raise FormatError('input should be a number from 1-3')

def get_search_menu_input():
    while True:
        choice=input("1. Get Record by ID \n2. Get Record by Type \n3. Get Events sorted by Date \n"
                     "4. Get items by quantity in inventory \n5. Get Total Sales Tax Owed for a given year \n"
                     "6. Get list of items by profit \n7. Get items sold by event_ID\n8. Exit to main menu\n\nEnter your selection: ")
        if choice in ('12345678'):
            return choice
        else:
            raise FormatError('input should be a number from 1 to 8')

def get_date_input():
    # could maybe revise to check for dashes and colons and spaces by inex. probably faster and easier.

    while True:
        d=input("Please enter the date and time you are looking for using YYYY-MM-DD HH:MM format: ")
        da=d.split(' ')
        count=0

        dash=0
        count2=0
        colon=0
        if (len(da[0])==10) & ((len(da[1])==5)|(len(da[1])==8)):
            for char in da[0]: #date portion
                if char in '0123456789':
                    count=count+1
                elif char =='-':
                    dash=dash+1
            for char in da[1]:
                if char in '0123456789':
                    count2=count2+1
                elif char == ':':
                    colon=colon+1
            if ((count+dash)==len(da[0])) & ((count2+colon)==len(da[1])) & (count==8) & (dash==2) & (((count2==4)&(colon==1))|(count2==6)&(colon==2)): #count2 could be HH:MM, or HH:MM:SS
                if (count2==4)&(colon==1): #add seconds if not present
                    d=d+":00"
                return d
        print('Please copy the format exactly')
        raise FormatError('Please use the given format.')

def get_state_input(message):
    while True:
        a=get_input(message)
        if len(a)==2:
            return a
        else:
            raise FormatError('please use state code')

def get_zip_input(message): #only accepts 5 digit zip codes
    while True:
        a=get_numeric_input(message,'i')
        if len(str(a))==5:
            return a
        else:
            raise FormatError('please use 5 digit zip code')

def get_phone_input(message):
    while True:
        a=get_input(message)
        s=a.split('-')
        if (len(str(a))==12) & (len(s)==3):
            return a
        else:
            raise FormatError('please use xxx-xxx-xxxx format')



def merchandise_header():
    show_message("Item ID: \tType: \t\tDescription: \t\t\t\t\tTotal Ordered: \tCost: \t\tTaxable?")

def events_header():
    show_message("Event ID: \tType: \t\tDate: \t\t\t\t\tAddress: \t\t\t\t\t\t\t\t\tContact: \t\t\t\t\tContact Phone: ")

def event_sales_header():
    show_message("Event ID: \tItem ID: \tTotal Sold: \tSale Price: \tSale Tax Collected: ")

def inventory_Header():
    show_message("Item ID: \tItems Sold: \tItems Purchased: \tItems Remaining: ")


class FormatError(Exception):
    """ Custom exception class """
    pass