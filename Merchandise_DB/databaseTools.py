from Merchandise_DB import ui
from Merchandise_DB import database

def view_table_ui():
    '''View a given table'''
    ui.show_message(' ')
    name=ui.get_table_input()
    if name=='items':
        records=database.view_table(name)
        ui.items_header()
        for record in records:
            ui.item_record_format(record)

    elif name=='events':
        records=database.view_table(name)
        ui.events_header()
        for record in records:
            ui.event_record_format(record)
    elif name=='event_sales':
        records = database.view_table(name)
        ui.event_sales_header()
        for record in records:
            #tax=0.00
            #if database.is_taxable(record['event_ID'], record['item_ID']):
            #    tax+=database.salesTax(record['sales_Price'],record['sales_Total'])
            ui.event_sales_record_format(record)#,tax)
    elif name=='orders':
        records = database.view_table(name)
        ui.orders_header()
        for record in records:
            ui.order_record_format(record)
    elif name=='order_items':
        records = database.view_table(name)
        ui.order_items_header()
        for record in records:
            ui.order_items_record_format(record)

def update_items_ui():
    while True:
        item_ID = ui.get_numeric_input(
            "What is the ID of the item that you wish to update?  Type 0 to quit without updating.", 'i')
        if item_ID == 0:
            return
        elif database.is_ID('items', item_ID):
            while True:
                choice = ui.get_numeric_input("What column do you want to update?\n1. Type\n2. Description\n"
                                              "3. Taxable\n\nEnter Choice: ", 'i')
                if choice == 1:
                    ui.show_message("Previous item Type: " + str(database.get_from_items(item_ID, 'type')))
                    ui.show_message('Select the new item type:')
                    updateData = ui.get_type_input(database.get_types('items'))
                    database.update_items(choice, updateData, item_ID)
                    ui.show_message("Updated item Type: " + str(database.get_from_items(item_ID, 'type')))
                    return
                elif choice == 2:
                    ui.show_message(
                        "Previous item description: " + str(database.get_from_items(item_ID, 'description')))
                    updateData = ui.get_input("Enter the new description: ")
                    database.update_items(choice, updateData, item_ID)
                    ui.show_message("Updated description: " + str(database.get_from_items(item_ID, 'description')))
                    return
                elif choice == 3:
                    t = database.get_from_items(item_ID, 'taxable')
                    tax_status = 'False'
                    if t == 1:
                        tax_status = 'True'
                    ui.show_message("Item subject to sales tax: " + tax_status)
                    updateData = ui.get_numeric_input(
                        "1. Item is subject to sales tax\n2. Item is not subject to sales tax\nEnter Selection: ", 'i')
                    database.update_items(choice, updateData, item_ID)

                    t = database.get_from_items(item_ID, 'taxable')
                    tax_status = 'False'
                    if t == 1:
                        tax_status = 'True'
                    ui.show_message("Updated Item subject to sales tax: " + tax_status)
                    return
        else:
            ui.show_message("Please enter a valid ID.")

def update_event_ui():
    while True:
        event_ID = ui.get_numeric_input("What is the event ID of the event you wish to update? "
                                        "Type 0 to exit without updating.", 'i')
        if event_ID == 0:
            return
        elif database.is_ID('events', event_ID):
            while True:
                choice = ui.get_input("What column do you want to update?\n\n1. Type\n2. Date (MM/DD/YY)\n"
                                      "3. Street Address\n4. City\n5. State\n"
                                      "6. Zip code\n7. Contact\n8. Contact Phone\n\nEnter Selection: ")
                if choice == '1':
                    ui.show_message("Previous Event Type: " + str(database.get_from_events(event_ID, 'type')))
                    ui.show_message("Select the new event type:")
                    updateData = ui.get_type_input(database.get_types('events'))
                    database.update_event(choice, event_ID, updateData)
                    ui.show_message("Updated event Type: " + str(database.get_from_events(event_ID, 'type')))
                    return

                elif choice == '2':
                    ui.show_message("Previous event date and time: " + str(database.get_from_events(event_ID, 'date')))
                    updateData = ui.get_date_input('Enter the new event date')
                    database.update_event(choice,event_ID,updateData)
                    ui.show_message("Updated date: " + str(database.get_from_events(event_ID, 'date')))
                    return

                elif choice == '3':
                    ui.show_message("Previous street address: " + str(database.get_from_events(event_ID, 'street')))
                    updateData = ui.get_input("Enter the street address of the event: ")
                    database.update_event(choice, event_ID, updateData)
                    ui.show_message("Updated street address: " + str(database.get_from_events(event_ID, 'street')))
                    return

                elif choice == '4':
                    ui.show_message("Previous City: " + str(database.get_from_events(event_ID, 'city')))
                    updateData = ui.get_input("Enter the City in which the event takes place: ")
                    database.update_event(choice, event_ID, updateData)
                    ui.show_message("Updated City: " + str(database.get_from_events(event_ID, 'city')))
                    return

                elif choice == '5':
                    ui.show_message("Previous State: " + str(database.get_from_events(event_ID, 'state')))
                    updateData = ui.get_state_input("Enter the state in which the event takes place: ")
                    database.update_event(choice, event_ID, updateData)
                    ui.show_message("Updated State: " + str(database.get_from_events(event_ID, 'state')))
                    return

                elif choice == '6':
                    ui.show_message("Previous zip code: " + str(database.get_from_events(event_ID, 'zip')))
                    updateData = ui.get_zip_input("Enter the zip code where the event takes place: ")
                    database.update_event(choice, event_ID, updateData)
                    ui.show_message("Updated zip code: " + str(database.get_from_events(event_ID, 'zip')))
                    return

                elif choice == '7':
                    ui.show_message("Previous event Contact: " + str(database.get_from_events(event_ID, 'contact')))
                    updateData = ui.get_input("Enter the full name of the contact person for this event: ")
                    database.update_event(choice, event_ID, updateData)
                    ui.show_message("Updated event Contact: " + str(database.get_from_events(event_ID, 'contact')))
                    return

                elif choice == '8':
                    ui.show_message("Previous Contact phone number: " + str(database.get_from_events(event_ID, 'phone')))
                    updateData = ui.get_phone_input("Enter the phone number of the contact person for this event "
                                                    "(xxx-xxx-xxxx): ")
                    database.update_event(choice, event_ID, updateData)
                    ui.show_message("Updated Contact phone number: " + str(database.get_from_events(event_ID, 'phone')))
                    return

                else:
                    ui.show_message("Please enter a choice")

        else:
            ui.show_message("Please enter a valid ID.")

def update_event_sales_ui(): #TODO must write function to undo changes to inventory when sales_Total is decreased. This requires knowing which order_items record was decreased by the entry.
    while True:
        choice = ui.get_input("\nWhat column do you want to update?\n\n1. Total Sold\n"
                              "2. Sale Price\n3. Exit\n\nEnter Selection: ")
        if (choice>0)&(choice<4):
            break
        if choice==3:
            return
        else:

            while True:
                i_ID = ui.get_numeric_input("What is the item ID of the entry that you wish to update?  "
                                    "Type 0 to exit without updating.", 'i')

                if database.is_ID('items',i_ID):
                    e_ID = ui.get_numeric_input("What is the event ID of the entry that you wish to update? "
                                        "Type 0 to exit without updating.", 'i')
                    if database.is_ID('events',e_ID):
                        break
        if database.is_ID('event_sales', e_ID, i_ID):
            if choice == '1':
                ui.show_message("Previous number of item sold: " + str(database.get_from_event_sales(e_ID, i_ID, 'total')))
                updateData = ui.get_numeric_input("Enter the total number of this item sold at the event: ", 'i')
                v=[choice, e_ID, i_ID, updateData]
                database.update_event_sales(v)
                ui.show_message("Updated number of item sold: "+str(database.get_from_event_sales(e_ID, i_ID, 'total')))
                return
            elif choice == '2':
                ui.show_message("Previous sales price: " + str(database.get_from_event_sales(e_ID, i_ID, 'price')))
                updateData = ui.get_numeric_input("Enter the new sale price: ", 'f')
                v=[choice, e_ID, i_ID, updateData]
                database.update_event_sales(v)
                ui.show_message("Updated sales price: " + str(database.get_from_event_sales(e_ID, i_ID, 'price')))
                return
        else:
            if (database.is_ID('events', e_ID)) & (database.is_ID('items', i_ID)):
                ui.show_message("No record of this item being sold at this event.")
            elif (database.is_ID('events', e_ID)):
                ui.show_message("Please verify that this item ID is correct")
            elif (database.is_ID('items', i_ID)):
                ui.show_message("Please verify that this event ID is correct")
            else:
                ui.show_message("Some error occured trying to update event_sales")

def update_order_ui():
    while True:
        choice=ui.get_numeric_input('1. Update date order was made\n2. Update date order was received\n3. Cancel\n\nEnter selection: ','i')
        if (choice >0) & (choice<4):
            break
    if choice==3:
        return
    else:
        order_ID=ui.get_numeric_input('Enter the order ID: ','i')
        if database.is_ID('orders',order_ID):
            if choice==1:
                ui.show_message("Previous date order was placed: "+str(database.get_from_orders(order_ID,'order_Date')))
                value=ui.get_date_input("Enter the new date and time")
                database.update_order('ordered',order_ID,value)
                ui.show_message("Updated Date order was placed: "+str(database.get_from_orders(order_ID,'order_Date')))
                return
            elif choice==2:
                ui.show_message("Previous date order was received: " + str(database.get_from_orders(order_ID, 'order_Received')))
                value = ui.get_date_input("Enter the new date and time")
                database.update_order('received',order_ID,value)
                ui.show_message("Updated Date order was received: " + str(database.get_from_orders(order_ID, 'order_Received')))
                return
def update_order_item_ui():
    while True:
        choice=ui.get_numeric_input('1. Update Total Ordered\n2. Update Ordered Cost\n3. Update Order Memo\n'
                                '4. Update Remaining Inventory\n5. Cancel\n\nEnter selection: ','i')
        if (choice <0) & (choice>6):
            break
    if choice == 5:
        return
    else:
        order_ID = ui.get_numeric_input('Enter the order ID: ', 'i')
        item_ID = ui.get_numeric_input('Enter the item ID: ', 'i')

        if choice == 1:
            ui.show_message("")
            value=ui.get_numeric_input('Enter the new total: ', 'i')
            values = ['total', order_ID, item_ID, value]
            database.update_order_items(values) #choice (st), order_ID, item_ID, value, *total
            return
        elif choice ==2:#cost
            ui.show_message("")
            value = ui.get_numeric_input('Enter the new cost: ', 'f')
            values = ['cost', order_ID, item_ID, value]
            database.update_order_items(values)
            return
        elif choice ==3:#note
            ui.show_message("")
            value = ui.get_input('Enter the new note: ')
            values = ['note', order_ID, item_ID, value]
            database.update_order_items(values)
            return
        elif choice ==4:#this is allowed because inventory could decrease due to some cause other than sales (theft etc.)
            ui.show_message("")
            value = ui.get_numeric_input('Enter the new remaining inventory: ', 'i')
            values = ['remainder', order_ID, item_ID, value]
            database.update_order_items(values)
            return
        else:
            ui.show_message('Not a valid choice')




def add_record(t=None):
    x=0
    if t is None:
        table= ui.get_table_input()
        x+=1
    else:
        table=t
    if table=='items':
        item_types = database.get_types('items')
        item = ui.get_type_input(item_types)
        description = ui.get_input("Please describe the item. (Example: 'white, blue logo' for a T-Shirt, or the title "
                                   "for a CD or Poster.): ")
        is_taxable = ui.get_numeric_input("Enter 1 if this item is subject to sales tax, 0 if not: ", 'i')
        i_id=database.new_item(item,description,is_taxable,1) #if there's a new item, there's a new order_items record
        if x==0: #if a parameter was passed then the function was called by receive order and I need this back there.
            return int(i_id)
    elif table=='events':
        type = ui.get_type_input(database.get_types('events'))
        date = ui.get_date_input('Enter the event date')
        street = ui.get_input("Enter the street address of the event: ")
        city = ui.get_input("Enter the name of the city in which the event is located: ")
        state = ui.get_input("Enter the state code of the state in which the event will take place: ")
        zip = ui.get_input("Enter the zip code of the event location: ")
        contact = ui.get_input("Enter the name of the contact person for this event: ")
        phone = ui.get_input("Enter the phone number of the contact person for this event: ")
        values = (type, date, street, city, state, zip, contact, phone)
        database.new_event(values)
    elif table=='event_sales':
        while True:
            e_ID = ui.get_numeric_input("Enter the event ID: ", 'i')
            i_ID = ui.get_numeric_input("Enter the item ID: ", 'i')
            if database.is_ID('event_sales', e_ID, i_ID):  # if this entry already exists in the table don't make a new one
                ui.show_message("This record already exists in the table.  To change it, update the table.")
                return
            elif ((database.is_ID('events', e_ID)) & (database.is_ID('items', i_ID))):  # ID's exist, but the combo of them doesn't
                s_total = ui.get_numeric_input("How many of the item were sold at this event?", 'i')
                s_price = ui.get_numeric_input("What price was charged per item at this event?", 'f')
                values = (e_ID, i_ID, s_total, s_price)
                database.new_event_sales(values)
                return
    elif table =='orders':
        vendor=ui.get_numeric_input('Enter the vendor ID for this order: ','i')
        date=ui.get_date_input('Enter the date and time this order was placed: ')
        print('vendor_ID is ',vendor, ', order_Date is ',date)
        database.new_Order(vendor,date)
    elif table =='order_items':
        receive_order_ui()

def receive_order_ui():
    choice=0
    values=[]
    o_ID=ui.get_numeric_input("Enter the order ID: ", 'i')
    date = ui.get_date_input('Enter the date the order was received, or Now for current date time')
    while choice !=3:
        choice = ui.get_numeric_input('\n1. New item\n2. Reorder of previous item\n3. Exit\nEnter selection: ', 'i')
        if choice==3:
            break
        i_ID=0
        if choice == 1:
            print('new item')
            i_ID=add_record('items')
            #print('i_ID is ', i_ID)

        if i_ID ==0:
            i_ID = ui.get_numeric_input("Enter the item ID: ", 'i')

#is_ID seems to be failing....Need to check this out.
        if database.is_ID('order_items', o_ID, i_ID):  # this primary key already exists, don't repeat
            ui.show_message("This record already exists in the table.  To change it, update the table.")

        elif ((database.is_ID('orders', o_ID)) & (database.is_ID('items', i_ID))):

            total = ui.get_numeric_input('Enter the total number of items purchase: ', 'i')
            cost = ui.get_numeric_input('Enter the cost of each item: ', 'f')
            memo = ui.get_input('Enter any notes about this purchase, such as discount amount: ')
            #item = [(o_ID, i_ID, total, cost, memo, total), (o_ID, date,)]
            #database.receive_Order(item)
            item = (o_ID, i_ID, total, cost, memo, total)
            values.append(item)

        else:
            if database.is_ID ('orders',o_ID):
                ui.show_message('Orders id may be incorrect')

            elif database.is_ID('items', i_ID):
                ui.show_message('Item id may be incorrect')
    if len(values)==1:
        item=values[0]
        updateData=[item, o_ID, date, 'one']
        database.receive_Order(updateData)
    elif len(values)>1:
        updateData=[values, o_ID, date, 'many']
        database.receive_Order(updateData)
    else:
        #if exit before any data is entered
        print('no data entered')
        return



def settings_ui():
    choice=ui.get_numeric_input('1. Change state and saleTax percentage\n2. Exit\n\nEnter your selection: ','i')
    if choice==0:
        return
    elif choice==1:
        sta=ui.get_state_input("Enter the new state code: ")
        per=ui.get_numeric_input('Enter the new sales tax percent as a decimal: ','f')
        database.change_settings(sta,per)