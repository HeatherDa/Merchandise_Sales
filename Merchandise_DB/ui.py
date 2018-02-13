#Get user input and validate it

def display_menu():
    '''Show Main Menu'''
    option=get_numeric_input("\n1. Display table\n2. Update Record\n3. Add New Record\n4. Delete Record\n5. Search\n6. Change Settings\n7. Quit\nEnter selection: ",'i')
    print("")
    if (option >0) & (option <8):
        return option
    else:
        show_message('please enter a number from 1-7')

def show_message(message):
    '''Display a given message'''
    print(message)

def get_numeric_input(message, t):
    '''Get numeric input back in numeric format as either int or float'''
    while True:
        n=input(message)
        if (is_int(n)) & (t== 'i') :
            return int(n)
        elif (is_Float(n)) & (t== 'f'):
            return float(n)
        else:
            print("Entry is not a valid integer or decimal.")


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
        if len(ok)==len(s):
            return ok
        else:
            show_message('This string has forbidden characters')

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
        if (is_int(choice)):
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
                show_message('use only numbers from 1 to '+ str(len(types)))

def get_table_input():
    while True:
        name = input("\n1. items table\n2. events table\n3. event sales table\n4. orders table\n5. order items table\n\nEnter your selection: ")
        if name=='1':
            return "items"
        elif name=='2':
            return "events"
        elif name=='3':
            return "event_sales"
        elif name=='4':
            return 'orders'
        elif name=='5':
            return 'order_items'
        else:
            show_message('input should be a number from 1-5')

def get_search_menu_input():
    while True:
        choice=get_numeric_input("1. Get Record by ID \n2. Get Record by Type \n3. Get Events sorted by Date \n"
                     "4. Get items by quantity in inventory \n5. Get Total Sales Tax Owed for a given year \n"
                     "6. Get list of items by profit \n7. Get items sold by event_ID\n8. Exit to main menu\n\nEnter your selection: ",'i')
        if (choice > 0) & (choice <9):
            return choice
        else:
            show_message('input should be a number from 1 to 8')

def get_date_input(message):
    # could maybe revise to check for dashes and colons and spaces by inex. probably faster and easier.

    while True:
        message=message+' using YYYY-MM-DD HH:MM format: '
        d=input(message)
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
        show_message('Please use the given format.')

def get_state_input(message):
    while True:
        a=get_input(message)
        if len(a)==2:
            return a
        else:
            show_message('please use state code')

def get_zip_input(message): #only accepts 5 digit zip codes
    while True:
        a=get_numeric_input(message,'i')
        if len(str(a))==5:
            return a
        else:
            show_message('please use 5 digit zip code')

def get_phone_input(message):
    while True:
        a=get_input(message)
        s=a.split('-')
        if (len(str(a))==12) & (len(s)==3):
            return a
        else:
            show_message('please use xxx-xxx-xxxx format')



def items_header():
    show_message("\033[1m"+"Items Table"+"\033[0m")
    show_message("\033[1m"+"\033[4m"+"Item ID: \tType: \t\tDescription: \t\t\t\t\tTax status: "+"\033[0m")

def events_header():
    show_message("\033[1m" + "Events Table" + "\033[0m")
    show_message("\033[1m"+"\033[4m"+"Event ID: \tType: \t\tDate: \t\t\t\t\tAddress: \t\t\t\t\t\t\t\t\tContact: \t\t\t\t\tContact Phone: "+"\033[0m")

def event_sales_header():
    show_message("\033[1m" + "Event Sales Table" + "\033[0m")
    show_message("\033[1m"+"\033[4m"+"Event ID: \tItem ID: \tTotal Sold: \tSale Price: \tSale Tax: \t\tProfit per item for event: "+"\033[0m")

def inventory_header():
    show_message("\033[1m" + "Inventory Table" + "\033[0m")
    show_message("\033[1m"+"\033[4m"+"Item ID: \tItems Sold: \tItems Purchased: \tItems Remaining: "+"\033[0m")

def orders_header():
    show_message("\033[1m" + "Orders Table" + "\033[0m")
    show_message("\033[1m"+"\033[4m"+"Order ID: \tVendor ID: \tDate Ordered: \t\tDate Received:  "+"\033[0m")

def order_items_header():
    show_message("\033[1m" + "Item Orders Table" + "\033[0m")
    show_message("\033[1m"+"\033[4m"+"Order ID: \tItem ID: \tTotal Ordered: \tCost: \t\t\tOrder Memo: \t\t\t\t\t\tRemaining inventory: "+"\033[0m")

def profits_header():
    show_message("\033[1m" + "Profits Query Results" + "\033[0m")
    show_message("\033[1m"+"\033[4m"+"Item ID: \tItem Type: \tItem Description \t\t\t\tProfit: "+"\033[0m")

#\nItem ID \tItem Type \tItem Description \t\t\t\tProfit

def is_Float(n):
    try:
        if float(n):
            return True
    except ValueError:
        return False

def is_int(n):
    try:
        int(n)
        return True
    except ValueError:
        return False

def add_spaces(st, col):
    d=0
    if (col=='ordered_Memo'):
        length = len(st)
        d = 35 - length
        st = st + (d * " ") + "\t" #if I take this and the following line out, it tells me the d variable is not used. WHY?
        return st
    if (col =='item_Description') | (col=='iTotal'):
        length=len(st)
        d=30-length
    elif (col=='address') :
        length=len(st)
        d=40-length
    elif (col=='event_Contact') :
        length=len(st)
        d=25-length
    elif (col=='sales_Price') | (col=='sales_Total') | (col=='sold') | (col=='ordered_Total') | (col=='sales_Profit') | (col=='sales_Tax'):
        length=len(st)
        d=10-length
        fl = float(st)
        s = "%.2f" % fl
        st = s + (d * " ") + " \t"
        return st

    #elif  :
    #    length = len(str(st))
    #    d = 13 - length
    #    fl=float(st)
    #    s="%.2f" %fl
    #    st = s + (d * " ") + " \t"
    #    return st
    elif (col=='ordered_Cost') | (col=='profit'):
        length = len(str(st))
        d = 10 - length
        fl = float(st)
        s = "%.2f" % fl
        st = s + (d * " ") + " \t"
        return st
    elif (col=='item_Total_Ordered'):
        length = len(st)
        d = 10 - length
    elif (col=='iOrdered'):
        length = len(st)
        d = 16 - length
    elif (col=='event_Date')|(col=='ordered_Date'):
        length=len(st)
        d = 20 - length
    else:
        length=len(st)
        d=10-length
    st = st + (d * " ") + "\t"
    return st

def item_record_format(record):
    '''get record, display row'''

    k=record.keys()
    a=""
    for col in k:
        if col!='item_Taxable':
            a=a+add_spaces(str(record[col]), str(col))
        elif col=='item_Taxable':
            if (str(record[col]))=='0':
                a=a+"Tax Exempt"
            elif (str(record[col]))=='1':
                a=a+"Taxable"
    show_message(a)

def profit_result_format(record, profit):
    k=record.keys()
    a=""
    for col in k:
        if col != 'item_Taxable':
            a=a+add_spaces(str(record[col]), str(col))
    show_message(a+add_spaces(str(profit), 'profit'))



def event_record_format(record):
    '''get record, display row'''

    address = str(record['event_Street'] + ", " + record['event_City'] + ", " + record['event_State'] + ", " +
                  record['event_Zip'])
    k = record.keys()
    a = ""
    for col in k:
        if (col != "event_Street") & (col != "event_City") & (col != "event_State") & (col != "event_Zip"):
            a = a + add_spaces(str(record[col]), str(col))
        elif col == "event_Street":
            a = a + add_spaces(address, 'address')
    show_message(a)

def event_sales_record_format(record):#, tax, profit):
    '''get record and salestax, display row'''
    k=record.keys()
    #print (k)
    a=""
    #if len(tax)>0:
    #    t=float(tax[0])

    # if len(k)>4:
    #     k=["event_ID", 'item_ID', 'sales_Total', 'sales_Price']
    #
    # for col in k:
    #     a=a+add_spaces(str(record[col]), str(col))
    # show_message(a + add_spaces(tax, 'sales_Tax') + add_spaces(profit, 'profit'))
    for col in k:
        if record[col] is not None:
            a = a + add_spaces(str(record[col]), str(col))
        else:
            a = a + "None \t\t "
    show_message(a)

    def order_items_record_format(record):  # TODO write this
        k = record.keys()
        a = ""
        for n in k:
            a = a + add_spaces(str(record[n]), str(n))
        show_message(a)

def order_record_format(record):
    '''get record, display row'''
    k = record.keys()
    # print (k)
    a = ""
    # if len(tax)>0:
    #    t=float(tax[0])
    if len(k) > 3:
        k = ["order_ID", 'vendor_ID', 'order_Date']
    for c in k:
        a = a + add_spaces(str(record[c]), str(c))
    if len(str(record[3]))>5:
        a = a + add_spaces(record[3],'order_Received') #if we have received it, display the date
    else:
        a = a + " " #if we haven't displayed it, show a blank instead of None
    show_message(a)

def inventory_record_format(k):
    '''get list of column values, display row'''
    a=""
    column=['item_ID','sold','iOrdered','iTotal']
    for col in k:
        a=a+add_spaces(str(col), str(column[k.index(col)]))
    show_message(a)

def order_items_record_format(record):
    a=""
    k=record.keys()

    for col in k:
        a=a+add_spaces(str(record[col]),str(col))
    show_message(a)