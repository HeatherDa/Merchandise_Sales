import sqlite3
import traceback
from datetime import datetime

from Merchandise_DB import ui

db = sqlite3.connect('merchandising_db.db') #Creates db file or opens if it already exists
c=db.cursor()
global state #homestate of organization
global percent #percent of salestax due when selling in homestate

def set_globals():
    '''
    set global variables of state and percent for use in salestax calculations.  Gets them from organizations table.
    Assumes that there is only one organization in organizations table.
    '''
    global state
    global percent
    c.execute('SELECT * FROM organizations')
    r=c.fetchone()
    state=r[1]
    percent=float(r[2])

def create_items_table():
    #Create items table
    try:
        c.execute('CREATE TABLE if not exists items (item_ID integer primary key, item_Type text not null, '
                  'item_Description text not null, item_Taxable int)')
        c.execute('SELECT * FROM items')
        rec=c.fetchall()
        recs= [('T-Shirt', 'black, yellow logo', 0),
                ('T-Shirt', 'white, blue logo', 0),
                ('CD', 'Adajio',  1),
                ('CD', 'Fortisimo', 1),
                ('Poster', '2017 Holiday Band Photo', 1),
                ('Poster', 'Adajio cover', 1)]

        if len(rec)<1:  #If table is empty, add data
            c.executemany('INSERT INTO items (item_Type, item_Description, item_Taxable) '
                          'VALUES (?,?,?)', recs)
            db.commit()  #save changes

    except sqlite3.Error:
        ui.show_message('An error occurred.')
        traceback.print_exc()

def new_item(orderID,type,description,total_ordered,cost_per_item,taxable,orderNote):
    """Add new item to items table"""
    # if there's a new item, there's a new order_items record too
    try:
        '''
        
        item_types=get_types('items')
        item= ui.get_type_input(item_types)
        description= ui.get_input("Please describe the item. (Example: 'white, blue logo' for a T-Shirt, or the title "
                                 "for a CD or Poster.): ")
        total_ordered= ui.get_numeric_input("How many items were ordered?", 'i')
        cost_per_item= ui.get_numeric_input("How much does each item cost?", 'f')
        taxable= ui.get_numeric_input("Enter 1 if this item is subject to sales tax, 0 if not: ", 'i')
        '''
        if taxable !=1:
            taxable=0

        sql='INSERT INTO items (item_Type, item_Description, item_Taxable)' \
            'VALUES(?,?,?)'
        sql2='SELECT item_ID FROM items WHERE item_Description = ?'
        sql3='INSERT INTO order_items (order_ID, item_ID, ordered_Total, ordered_Cost, ordered_Note, ordered,Remaining) VALUES (?,?,?,?,?,?)'
        c.execute(sql, (type,description, taxable))
        item_ID=c.execute(sql2, (description))
        c.execute(sql3, (orderID,item_ID,total_ordered, cost_per_item, orderNote, total_ordered))
        db.commit()  #save changes

    except sqlite3.IntegrityError:
        ui.show_message ('wrong data type?  Changes will be rolled back.')
        traceback.print_exc()
        db.rollback()

    except sqlite3.Error:
        ui.show_message('An error occurred.  Changes will be rolled back.')
        traceback.print_exc()
        db.rollback()


def update_items(choice,updateData,item_ID):
    try:
        if choice == 1: #update type
            sql = '''UPDATE items SET item_Type=? WHERE item_ID=?'''
            c.execute(sql, (updateData, item_ID,))
            db.commit()
            return
        elif choice == 2: #update description
            sql = '''UPDATE items SET item_Description=? WHERE item_ID=?'''
            c.execute(sql, (updateData, item_ID,))
            db.commit()
            return

    except sqlite3.Error:
        ui.show_message('An error occured while trying to update items table.  Changes will '
                        'be rolled back.')
        traceback.print_exc()
        db.rollback()

def get_from_items(item_ID, value):
    results=c.execute('SELECT * FROM items WHERE item_ID=?', (item_ID,))
    c.row_factory=sqlite3.Row
    try:
        if value=='all':
            for result in results:
                return result
        elif value=='description':
            for result in results:
                return result['item_Description']
        elif value=='type':
            for result in results:
                return result['item_Type']
        elif value=='taxable':
            tax=0
            for result in results:
                tax = result['item_Taxable']
            if tax == 1:
                return True
            else:
                return False
        else:
            raise MyError('option passed with no corresponding code')
    except sqlite3.Error:
        ui.show_message("An error ocurred while searching for " + value + ".")
        traceback.print_exc()

def create_events_table():
    """ Create events table"""
    try:
        c.execute(
            'create table if not exists events (event_ID integer primary key, event_Type text not null, '
            'event_Date DATETIME, event_Street text, event_City text, event_State text, event_Zip text, '
            'event_Contact text, event_Contact_Phone text)')
        c.execute('SELECT * FROM events')
        rec = c.fetchall()
        events = [('Concert', '2018-01-28 18:00:00', '203 Robert St.', 'Minneapolis', 'MN', '55116',
                   'Candice Jennings', '612-287-6830'),
                  ('Signing', '2018-02-07 15:00:00', '151 Afton Ave.', 'Milwakee', 'WI', '52964',
                   'Alice Milton', '952-600-8700'),
                  ('Concert', '2018-02-12 19:30:00', '523 Bolton Rd.', 'Fargo', 'ND', '59721',
                   'John Cobbler', '542-890-7231'),
                  ('Signing', '2018-03-15 14:30:00', '3030 Colton Way', 'New Olm', 'MN', '57382',
                   'Kaiser Tannenburg', '472-113-9157')]

        if len(rec) < 1:  # If table is empty, add data
            c.executemany('INSERT INTO events (event_Type, event_Date, event_Street, event_City, event_State, event_Zip, '
                          'event_Contact, event_Contact_Phone) VALUES (?,?,?,?,?,?,?,?)', events)
            db.commit()  # save changes

    except sqlite3.Error as e:
        ui.show_message('An error occurred.')
        traceback.print_exc()

def new_event(values):
    """Add new event to events table"""
    try:
        sql='INSERT INTO events (event_Type, event_Date, event_Street, event_City, event_State,event_Zip, ' \
            'event_Contact, event_Contact_Phone) VALUES (?,?,?,?,?,?,?,?)'
        c.execute(sql,(values))
        db.commit()  #save changes

    except sqlite3.IntegrityError:
        ui.show_message ('wrong data type?  Changes will be rolled back.')
        traceback.print_exc()
        db.rollback()

    except sqlite3.Error as e:
        ui.show_message('An error occurred.  Changes will be rolled back.')
        traceback.print_exc()
        db.rollback()

def update_event(choice, event_ID, updateData):
    try:
        if choice=='1':
            sql = '''UPDATE events SET event_Type=? WHERE event_ID=?'''
            c.execute(sql, (updateData, event_ID,))
            db.commit()
        elif choice=='2':
            sql = '''UPDATE events SET event_Date=? WHERE event_ID=?'''
            c.execute(sql, (updateData, event_ID,))
            db.commit()
        elif choice=='3':
            sql = '''UPDATE events SET event_Street=? WHERE event_ID=?'''
            c.execute(sql, (updateData, event_ID,))
            db.commit()
        elif choice=='4':
            sql = '''UPDATE events SET event_City=? WHERE event_ID=?'''
            c.execute(sql, (updateData, event_ID,))
            db.commit()
        elif choice=='5':
            sql = '''UPDATE events SET event_State=? WHERE event_ID=?'''
            c.execute(sql, (updateData, event_ID,))
            db.commit()
        elif choice=='6':
            sql = '''UPDATE events SET event_zip=? WHERE event_ID=?'''
            c.execute(sql, (updateData, event_ID,))
            db.commit()
        elif choice=='7':
            sql = '''UPDATE events SET event_Contact=? WHERE event_ID=?'''
            c.execute(sql, (updateData, event_ID,))
            db.commit()
        elif choice=='8':
            sql = '''UPDATE events SET event_Contact_Phone=? WHERE event_ID=?'''
            c.execute(sql, (updateData, event_ID,))
            db.commit()
        else:
            raise MyError('Data passed to get from events for which there is no code written')
    except sqlite3.Error:
        ui.show_message('An error occured while trying to update events table.  Changes will be rolled back.')
        traceback.print_exc()
        db.rollback()



def get_from_events(event_ID, value):
    results=c.execute('SELECT * FROM events WHERE event_ID=?', (event_ID,))
    c.row_factory=sqlite3.Row
    r=""
    try:
        if value=='all':
            for result in results:
                return result
        if value=='date':
            for result in results:
                return result['event_Date']
        elif value=='type':
            for result in results:
                return result['event_Type']
        elif value=='street':
            for result in results:
                return result['event_Street']
        elif value == 'city':
            for result in results:
                return result['event_City']
        elif value=='state':
            for result in results:
                return result['event_State']
        elif value == 'zip':
            for result in results:
                return result['event_Zip']
        elif value=='contact':
            for result in results:
                return result['event_Contact']
        elif value=='phone':
            for result in results:
                return result['event_Contact_Phone']
        else:
            raise MyError('value passed with no corresponding code')
    except sqlite3.Error:
        ui.show_message("An error ocurred while searching for " + value + ".")
        traceback.print_exc()








def create_event_sales_table():
    """Create event_sales table"""
    try:
        #delete_table()
        sql='CREATE TABLE if not exists event_sales (event_ID integer not null, item_ID integer not null, ' \
            'sales_Total integer, sales_Price real not null, CONSTRAINT event_sales PRIMARY KEY (event_ID, item_ID))'
        c.execute(sql)

        c.execute('SELECT * FROM event_sales')
        rec = c.fetchall()
        sales = [(1, 1, 5, 10.00),
                 (1, 2, 4, 10.00),
                 (1, 3, 8, 10.00),
                 (1, 4, 2, 10.00),
                 (1, 5, 3, 8.00),
                 (1, 6, 1, 8.00)]


        if len(rec) < 1:  # If table is empty, add data
            c.executemany('INSERT INTO event_sales (event_ID, item_ID, sales_Total, sales_Price) '
                          'VALUES (?,?,?,?)', sales)
            db.commit()  # save changes

    except sqlite3.Error as e:
        ui.show_message('An error occurred.')
        traceback.print_exc()






def new_event_sales(values):
    try:
        sql = 'INSERT INTO event_sales (event_ID, item_ID, sales_Total, sales_Price) VALUES (?,?,?,?)'
        c.execute(sql, values)
        db.commit()
        v=[('remaining', values[1], values[2])]
        update_order_items(v) #update remaining in order_items to show how many items are left from the order

    except sqlite3.IntegrityError:
        ui.show_message('wrong data type?  Changes will be rolled back.')
        traceback.print_exc()
        db.rollback()

    except sqlite3.Error:
        ui.show_message("An error occured while trying to add a new event_sales record.  Changes will be rolled back.")
        traceback.print_exc()
        db.rollback()

def update_event_sales(choice,e_ID,i_ID,updateData):
    try:
        if choice==1:
            sql = '''UPDATE event_sales SET sales_Total=? WHERE event_ID=? AND item_ID=?'''
            c.execute(sql, (updateData, e_ID, i_ID))
            db.commit()
        elif choice == '2':
            sql = '''UPDATE event_sales SET sales_Price=? WHERE event_ID=? AND item_ID=?'''
            c.execute(sql, (updateData, e_ID, i_ID))
            db.commit()
    except sqlite3.Error:
        ui.show_message('An error occured while trying to update event_sales table.  '
                        'Changes will be rolled back.')
        traceback.print_exc()
        db.rollback()

def get_from_event_sales(e_ID, i_ID, value):
    results = c.execute('SELECT * FROM event_sales WHERE event_ID=? AND item_ID=?', (e_ID, i_ID,))
    c.row_factory = sqlite3.Row
    r = ""
    try:
        if value == 'all':
            for result in results:
                return result
        if value == 'total':
            for result in results:
                return result['ordered_Total']
        elif value == 'price':
            for result in results:
                return result['ordered_Price']
        else:
            raise MyError('value passed with no corresponding code')
    except sqlite3.Error:
        ui.show_message("An error occurred while searching for " + value + ".")
        traceback.print_exc()




def display_event_sales():
    '''calculates sales tax column, and displays table'''
    sql = 'SELECT event_sales.event_ID, event_sales.item_ID, event_State, sales_Total, sales_Price, ' \
          'item_Taxable ' \
          'FROM event_sales ' \
          'INNER JOIN events ON events.event_ID=event_sales.event_ID ' \
          'INNER JOIN items ON items.item_ID=event_sales.item_ID'
    records = c.execute(sql)
    c.row_factory = sqlite3.Row

    for record in records:
        if taxable(record['event_ID'],record['item_ID']):
            tax = salesTax(record['sales_Price'], record['sales_Total'])  # sales tax for this item
            ui.event_sales_record_format(record, tax)
        else:
            ui.event_sales_record_format(record, 0.00)
    return





def create_order_items_table():
    try:
        sql='create table if not exists order_items ' \
            '(order_ID integer not null, item_ID integer not null, ordered_Total integer not null, ' \
            'ordered_Cost real not null, ordered_Memo text DEFAULT NULL, ordered_Remaining int, ' \
            'CONSTRAINT order_items PRIMARY KEY (order_ID, item_ID))'
        c.execute(sql)
        db.commit()
        c.execute('SELECT * FROM order_items')
        rec=c.fetchall()
        ordered=[(1,1,50,8.00, '5 percent off for bulk order', 50),
                 (1,2,75,8.00, '5 percent off for bulk order', 75),
                 (2,3,80,3.00, 'Nothing ', 80),
                 (2,4,70,3.00, 'Nothing ', 70),
                 (3,5,40,5.00, 'Nothing ', 40),
                 (3,6,40,5.00, 'Nothing ', 40)]

        if len(rec) <1:
            sql2='INSERT INTO order_items ' \
                 '(order_ID, item_ID, ordered_Total, ordered_Cost, ordered_Memo, ordered_Remaining) VALUES (?,?,?,?,?,?)'

            c.executemany(sql2, ordered)
            db.commit()
    except sqlite3.Error:
        ui.show_message('An error occurred while trying to create order_items table')
        traceback.print_exc()

# def get_order_items_remaining(item_ID):
#     sql = 'SELECT order_items.order_ID, ordered_Total, ordered_Cost, ordered_Remaining, orders.order_Received' \
#           'FROM order_items' \
#           'INNER JOIN orders ON orders.order_ID=order_items.order_ID' \
#           'WHERE item_ID=? AND ordered_Remaining > 0' \
#           'ORDER BY orders.Received DESC'
#
#     while True:
#         records = c.execute(sql, (item_ID,))
#         c.row_factory = sqlite3.Row
#         for record in records:
#             if record['ordered_Remaining']

def get_from_order_items(order_ID, item_ID, value):
    '''get record or column value by order ID and item ID value'''
    sql2='SELECT * FROM order_items WHERE order_ID=? AND item_ID=?'
    c.execute(sql2, (order_ID, item_ID,))

    r=c.fetchone()
    if value=='all':
        return r
    if value=='order':
        return r[0]
    elif value=='total':
        return r[1]
    elif value=='cost':
        return r[2]
    elif value=='remaining':
        return r[3]

def update_order_items(values): #choice, order_ID, item_ID, value, *total
    if values[0]=='total':
        sql='UPDATE order_items SET ordered_Total=? WHERE order_ID=? AND item_ID=?'
        c.execute(sql,(values[3],values[1],values[2],))
    elif values[0]=='cost':
        sql = 'UPDATE order_items SET ordered_Cost=? WHERE order_ID=? AND item_ID=?'
        c.execute(sql, (values[3], values[1], values[2],))
    elif values[0]=='note':
        sql = 'UPDATE order_items SET ordered_Memo=? WHERE order_ID=? AND item_ID=?'
        c.execute(sql, (values[3], values[1], values[2],))
    elif values[0]=='remaining': #choice, item_ID, total
        total=values[3]
        while True:
            sql = 'SELECT order_items.order_ID, ordered_Total, ordered_Cost, ordered_Remaining, orders.order_Received' \
                  'FROM order_items' \
                  'INNER JOIN orders ON orders.order_ID=order_items.order_ID' \
                  'WHERE item_ID=? AND ordered_Remaining > 0' \
                  'ORDER BY orders.Received DESC'
            c.execute(sql, (values[2],))  # Might need comma after item_ID
            # previously had while loop and test for order_Remaining being larger than 0
            r = c.fetchone()
            order_ID = r[0]
            rem = r[3]
            left=rem-total
            if left<0:
                # calculate difference, set this id to 0 and then look for next record in get_from_order_items
                sql='UPDATE order_items SET ordered_Remaining = 0 WHERE order_ID=? AND item_ID=?'
                c.execute(sql,(order_ID,values[2]))
                total=left

            elif left >= 0:

                # Update order_items SET ordered_Rem.. = ? WHERE order_ID=? AND item_ID=? (remain,order_ID,values[2])
                sql2 = 'UPDATE order_items SET orderd_Remaining =? WHERE order_ID=? AND item_ID=?'
                c.execute(sql2, (left, order_ID, values[2]))

def receive_Order(items):
    '''Add list of items from an order to database'''
    while True:

        sql = 'INSERT INTO orders (order_ID, item_ID, order_Total, order_Cost, order_Note, order_Remaining) VALUES(?,?,?,?,?,?,?,?)'
        if len(items) > 1:
            c.executemany(sql, items)
        else:
            c.execute(sql, items)
        db.commit()
        '''
        ch = ui.get_numeric_input('\n1. Update cost \n2. Quit without update. \n\n'
                                  'Enter Selection: ', 'i')

        if ch == 1:
            v = ui.get_numeric_input('Enter the new value: ', 'f')
            if DataValidation.is_Float(ch):
                updateData = float(v)
                ui.show_message('update data is ' + str(updateData))
            sql = 'UPDATE items SET item_Cost=? WHERE item_ID=?'
            c.execute(sql, ('receieved',updateData, item_ID))
            db.commit()
            ui.show_message("Updated Cost: " + str(get_from_item(item_ID, 'cost')))
            break
        elif ch == 2:
            ui.show_message('okay, no update.')
            break
        else:
            ui.show_message('Please enter a 1 or a 2.')'''
        # return


def create_orders_table():
    try:
        sql='CREATE TABLE IF NOT EXISTS orders (order_ID integer primary key, vendor_ID integer not Null, ' \
            'order_Date DATETIME not Null, order_Received DATETIME DEFAULT NULL) '
        c.execute(sql)
        c.execute('SELECT * FROM orders')
        rec=c.fetchall()
        orders=[('1','2018-01-01 10:30','2018-01-10 14:00'),
                ('2','2018-01-01 11:00','2018-01-15 9:00'),
                ('3','2018-01-05 23:15','2018-01-15 9:00')]
        openOrder=('1','2018-02-01 12:30')
        if len(rec) <1:
            c.executemany('INSERT INTO orders (vendor_ID, order_Date, order_Received) VALUES (?,?,?)', orders)
            db.commit()
            c.execute('INSERT INTO orders (vendor_ID, order_Date) VALUES (?,?)', openOrder)
            db.commit()
    except sqlite3.Error:
        ui.show_message('An error occurred while trying to create orders table')
        traceback.print_exc()

def new_Order(vendor, ordered):
    sql='INSERT INTO orders (vendorID, order_date) VALUES (?,?)'
    c.execute(sql,(vendor, ordered,))
    db.commit()

def update_order(choice,order_ID,value):
    if choice=='received':
        sql='UPDATE orders SET order_Received=? WHERE order_ID=?'
        c.execute(sql,(value,order_ID))
        db.commit()
    elif choice=='ordered':
        sql='UPDATE orders SET order_Date=? WHERE order_ID=?'
        c.execute(sql,(value,order_ID))
        db.commit()

def get_from_orders(order_ID, value):  #TODO: write it
    pass

def create_organization_table():
    #The point of this is to store state and sales tax information in the database so it can be updated if necessary
    try:
        c.execute('create table if not exists organizations (org_ID integer primary key, state, salesTaxPercent)')
        c.execute('SELECT * FROM organizations')
        rec=c.fetchall()
        org=[('MN',7.375)]
        if len(rec) <1:
            c.executemany('INSERT INTO organizations (state, salesTaxPercent) VALUES (?,?)', org)
            db.commit()
    except sqlite3.Error:
        ui.show_message('An error occurred while trying to create organizations table')
        traceback.print_exc()

def change_settings(sta, tax): #Assumes this table only has one record
    try:
        sql='UPDATE organizations SET state = ? AND salesTaxPercent = ?'
        c.execute(sql, (sta, tax))
    except sqlite3.Error:
        ui.show_message('An error occurred while trying to update organizations table')



def drop_settings():
    c.execute('DROP TABLE IF EXISTS organization') #Delete table
    db.commit()





#TODO: fix me!
def delete_Record():
    """Delete a record from the database by ID"""
    try:
        ui.show_message("Which table contains the record you want to delete?")
        t= ui.get_table_input()
        print(t)
        if t=='items':
            id = ui.get_numeric_input("What is the ID of the record you wish to delete?", 'i')
            results=c.execute('SELECT * FROM event_sales')
            c.row_factory=sqlite3.Row
            count=0
            for result in results:
                if result['item_ID']==id:
                   count=count+1
            if count>0:
                ui.show_message('Cannot delete that record, as it is in use in another table.')
            else:
                sql='''DELETE FROM items WHERE item_ID=?'''
                c.execute(sql,(id,))
                db.commit()
                ui.show_message("Record Deleted")
        elif t=='events':
            id= ui.get_numeric_input("What is the ID of the record you wish to delete?", 'i')
            results = c.execute('SELECT * FROM event_sales')
            c.row_factory = sqlite3.Row
            count = 0
            for result in results:
                if result['event_ID'] == id:
                    count = count + 1
            if count > 0:
                ui.show_message('Cannot delete that record, as it is in use in another table.')
            else:
                sql='''DELETE FROM events WHERE event_ID=?'''
                c.execute(sql, (id,))
                db.commit()
                ui.show_message("Record Deleted")
        elif t=='event_sales':
            e_id = ui.get_numeric_input("What is the event ID of the record you wish to delete?", 'i')
            m_id = ui.get_numeric_input("What is the item ID of the record you wish to delete?", 'i')

            sql = '''DELETE FROM event_sales WHERE event_ID=? AND item_ID=?'''
            c.execute(sql, (e_id, m_id,))
            db.commit()
            ui.show_message("Record Deleted")
    except sqlite3.Error:
        ui.show_message('An error occurred.  Record could not be deleted.  Changes will be rolled back.')
        traceback.print_exc()
        db.rollback()









def search_by_id_ui():
    table = ui.get_table_input()

    if table == 'items':
        i_id = ui.get_numeric_input("Enter the id you wish to search by: ", 'i')
        records = get_from_items(i_id,'all')
        c.row_factory = sqlite3.Row

        ui.items_header()
        for record in records:
            ui.item_record_format(record)
    elif table == 'events':
        e_id = ui.get_numeric_input("Enter the id you wish to search by: ", 'i')
        records = get_from_events(e_id,'all')
        c.row_factory = sqlite3.Row
        ui.events_header()
        for record in records:
            ui.event_record_format(record)
    elif table == 'event_sales':
        e_id = ui.get_numeric_input("Enter the event id you wish to search by: ", 'i')
        i_id = ui.get_numeric_input("Enter the items id you wish to search by: ", 'i')
        records = get_from_event_sales(e_id, i_id, 'all')
        c.row_factory = sqlite3.Row
        ui.show_message('\033[2m'+'Event Sales'+'\033[0m')
        ui.event_sales_header()
        for record in records:
            if taxable(e_id,i_id):
                tax = salesTax(record['sales_Price'], record['sales_Total'])
                ui.event_sales_record_format(record, tax)
            else:
                ui.event_sales_record_format(record, 0.00)

def search_by_type():
    table = ui.get_numeric_input('1. items table\n2.events table\n\nEnter your selection: ', 'i')
    if table == 1:
        a = ""
        item_types = get_types('items')
        for i in item_types:
            a = a + " \n" + str(item_types.index(i) + 1) + ". " + str(i)
        ui.show_message(a)
        t = ui.get_numeric_input("Enter the type you wish to search by: ", 'i')
        ty = item_types[t - 1]
        records = c.execute('SELECT * FROM items WHERE item_Type = ?', (ty,))
        c.row_factory = sqlite3.Row
        ui.items_header()
        for record in records:
            ui.item_record_format(record)
    elif table == 2:
        a = ""
        event_types = get_types('events')
        for i in event_types:
            a = a + str(event_types.index(i) + 1) + ". " + str(i) + ' \n'
        ui.show_message(a)
        t = ui.get_numeric_input("Enter the type you wish to search by: ", 'i')
        ty = event_types[t - 1]
        records = c.execute('SELECT * FROM events WHERE event_Type = ?', (ty,))
        c.row_factory = sqlite3.Row
        ui.items_header()
        for record in records:
            ui.event_record_format(record)

def search_by_date():
    # Show events ordered by date
    #today=datetime.today()
    #records = c.execute('SELECT * FROM events WHERE event_Date > ? ORDER BY event_Date ASC', (today,))
    #c.row_factory = sqlite3.Row
    #ui.events_header()
    #for r in records:
    #    event_record_format(r)

    # Show events ordered by date
    # Maybe I should have a get input for formatting dates received from user.
    choice= ui.get_numeric_input('1. Search for event by date\n2. Display events table in order by date, from today forward.\n\nEnter selection: ', 'i')
    
    if choice == 1:
        d= ui.get_date_input('Enter the event date you are looking for')
        records=c.execute('SELECT * FROM events WHERE event_Date = ? ORDER BY event_Date ASC',(d,))
        c.row_factory = sqlite3.Row
        ui.events_header()
        for r in records:
            ui.event_record_format(r)
    elif choice == 2:
        d=datetime.today()
        records=c.execute('SELECT * FROM events WHERE event_Date >= ? ORDER BY event_Date ASC',(d,))
        c.row_factory = sqlite3.Row
        ui.events_header()
        for r in records:
            ui.event_record_format(r)




def search_by_on_hand_ui():
    # Get items by quantity in inventory
    par = ui.get_numeric_input("Return items where remaining inventory is less than: ", 'i')
    a=search_by_on_hand()
    ui.inventory_header()


    for i in a:
        sold = i[1]
        #order = get_from_order_items(i[0], 'ordered')
        order= i[2]
        rem = order - sold
        if rem < par:
            ui.inventory_record_format([i[0], sold, order, rem])

def search_by_on_hand():
    sql='SELECT items.item_ID, SUM(ordered_Remaining) ' \
        'FROM order_items ' \
        'INNER JOIN items ON items.item_ID=order_items.item_ID ' \
        'GROUP BY items.item_ID '

    sql2='SELECT items.item_ID, SUM(ordered_Total) ' \
         'FROM order_items ' \
         'INNER JOIN items ON items.item_ID=order_items.item_ID ' \
         'GROUP BY items.item_ID '

    sql3='(SELECT DISTINCT item_ID FROM order_items), ' \
         '(SELECT items.item_ID, SUM(ordered_Remaining) ' \
         ' FROM order_items ' \
         ' INNER JOIN items ON items.item_ID=order_items.item_ID ' \
         ' GROUP BY items.item_ID ), ' \
         '(SELECT items.item_ID, SUM(ordered_Total) ' \
         ' FROM order_items ' \
         ' INNER JOIN items ON items.item_ID=order_items.item_ID ' \
         ' GROUP BY items.item_ID )' \

    c.execute(sql)
    a=c.fetchall()
    c.execute(sql2)
    b=c.fetchall()
    c.execute(sql3)
    all=c.fetchall()
    #this code is the beginning of combining a and b if all doesn't work right.
    #for i in a:
    #    ind=a.index(i)
    #    if i[0]==(b[ind])[0]: #if the item ID is the same in both records
    return all






def search_by_salesTax_due():
    """How much sales tax was collected by the band for this year to date?"""
    # sqlite doesn't support calculated columns, so I'm improvising here.
    try:
        year = ui.get_numeric_input("Enter the year you want to know sales tax information about (YYYY): ", 'i')
        current_year = datetime.today().strftime("%Y")
        if year == current_year:
            data_since = (str(current_year) + "-01-01 01:01")
            data_before = datetime.today()
        else:
            data_since = str(year) + "-01-01 00:00"
            data_before = str(year) + "-12-31 23:59"

        sql = 'SELECT event_State, sales_Price, sales_Total, item_Taxable ' \
              'FROM event_sales ' \
              'INNER JOIN events on events.event_ID=event_sales.event_ID ' \
              'INNER JOIN items ON items.item_ID=event_sales.item_ID ' \
              'WHERE event_Date BETWEEN ? AND ? '

        records = c.execute(sql, (data_since, data_before))
        c.row_factory = sqlite3.Row
        sale_tax = 0
        for record in records:
            if (record['event_State'] == 'MN') & (record['item_Taxable'] == 1):
                tax = salesTax(record['sales_Price'], record['sales_Total'])  # sales tax for this item
                sale_tax = sale_tax + tax

        ui.show_message("Total sales tax owed for this year is: " + str(sale_tax))


    except sqlite3.Error:
        ui.show_message('trouble searching by date')
        traceback.print_exc()

def search_by_profit_ui():
    ui.show_message("\n1. Profit for a specific item ID\n2. Total Profit per item\n3. Total profit this year\n")
    choice = ui.get_numeric_input("Enter your selection: ", 'i')

    if choice == 1:
        item_ID = ui.get_numeric_input("\nWhat item ID do you want to use?", 'i')
        records=search_by_profit(choice,item_ID)
        ui.profits_header()
        #TODO: check how I did this in view table
        for record in records:
            profit = (record['sales_Price'] - record['item_Cost']) * record['sales_Total']
            if taxable(record['event_ID'], record['item_ID']):
                tax = salesTax(record['sales_Price'], record['sales_Total'])
                profit = profit - tax
            ui.profit_result_format(record, profit)
    elif choice ==2:
        records = search_by_profit(choice)
        r = {}
        ui.profits_header()

        for record in records:  # get distinct item_ID's and make them keys in a dictionary
            if record['item_ID'] not in r:
                r[record['item_ID']] = 0

        for record in records:  # get running total of profit per item and store as value paired with item_ID key (like a subquery)
            profit = (record['sales_Price'] - record['item_Cost']) * record['sales_Total']
            if taxable(record['event_ID'], record['item_ID']):
                tax = salesTax(record['sales_Price'], record['sales_Total'])
                profit = profit - tax
            r[record['item_ID']] += profit

        for key in r.keys():
            record = get_from_items(key, 'all')
            ui.profit_result_format(record, r[record['item_ID']])  # one record for each item_ID in results
    elif choice ==3:
        records=search_by_profit(choice)
        total = 0
        for r in records:
            total = total + r[1]  # should add sums for each item together
        ui.show_message('Gross sale profits this year: ' + str(total))


def search_by_profit(choice,*item_ID):

    if choice == 1:

        sql = 'SELECT event_sales.event_ID, items.item_ID, sales_Price, item_Cost, sales_Total, event_State, ' \
              'item_Taxable, item_Type, item_Description ' \
              'FROM items ' \
              'INNER JOIN event_sales ON items.item_ID=event_sales.item_ID ' \
              'INNER JOIN events ON event_sales.event_ID=events.event_ID ' \
              'WHERE items.item_ID=? '

        records = c.execute(sql, (item_ID,))
        c.row_factory = sqlite3.Row
        return(records)

        # ui.profits_header()
        # ui.profits_header()
        # for record in records:
        #     profit = (record['sales_Price'] - record['item_Cost']) * record['sales_Total']
        #     if taxable(record['event_ID'], record['item_ID']):
        #         tax = salesTax(record['sales_Price'], record['sales_Total'])
        #         profit = profit - tax
        #     ui.profit_result_format(record, profit)
    elif choice == 2:

        sql = 'SELECT event_sales.event_ID, items.item_ID, sales_Price, item_Cost, sales_Total, event_State, ' \
              'item_Taxable, item_Type, item_Description ' \
              'FROM items ' \
              'INNER JOIN event_sales ON items.item_ID=event_sales.item_ID ' \
              'INNER JOIN events ON event_sales.event_ID=events.event_ID ' \
              'ORDER BY items.item_ID '
        # This SQL query does not return a sum of profit per item
        # Couldn't get that query to work the way I wanted.
        # So I extracted the information myself.

        records = c.execute(sql)
        c.row_factory = sqlite3.Row
        return records
        # r={}
        # ui.profits_header()
        #
        # for record in records:  #get distinct item_ID's and make them keys in a dictionary
        #     if record['item_ID'] not in r:
        #         r[record['item_ID']]=0
        #
        # for record in records: #get running total of profit per item and store as value paired with item_ID key (like a subquery)
        #     profit = (record['sales_Price'] - record['item_Cost']) * record['sales_Total']
        #     if taxable(record['event_ID'],record['item_ID']):
        #         tax=salesTax(record['sales_Price'], record['sales_Total'])
        #         profit=profit-tax
        #     r[record['item_ID']]+=profit
        #
        # for key in r.keys():
        #     record=get_from_items(key,'all')
        #     ui.profit_result_format(record, r[record['item_ID']]) #one record for each item_ID in results

    elif choice == 3:
        current_year = datetime.today().strftime("%Y")
        data_since = (str(current_year) + "-01-01 01:01")

        sql = 'SELECT items.item_ID, sales_Price, item_Cost, sales_Total, event_State, item_Taxable, ' \
              'item_Type, item_Description, event_Date ' \
              'FROM items ' \
              'INNER JOIN event_sales ON items.item_ID=event_sales.item_ID ' \
              'INNER JOIN events ON event_sales.event_ID=events.event_ID ' \
              'WHERE event_Date > ? ' \
              'ORDER BY event_Date '

        records = c.execute(sql, (data_since,))
        c.row_factory = sqlite3.Row
        total = 0
        for r in records:
            total = total + r[1]  # should add sums for each item together
        ui.show_message('Total Profit made so far: ' + str(total))

def search_by_event():
    e_id = ui.get_numeric_input("Enter the event id for which you would like to search: ", 'i')
    sql = "SELECT * " \
          "FROM event_sales " \
          "WHERE event_ID = ? " \
          "ORDER BY event_ID "

    c.execute(sql, (e_id,))

    a = c.fetchall()
    ui.event_sales_header()
    for i in a:
        if taxable(e_id,i[1]):
            t=salesTax(i[3],i[2])
        else:
            t=0.00
        #t = get_from_event_sales(i[0], i[1], 'tax')
        tax = "%.2f" % t
        ui.show_message(add_spaces(str(i[0]), 'event_ID') + add_spaces(str(i[1]), 'item_ID') +
                        add_spaces(str(i[2]), 'sales_Total') + add_spaces(str(i[3]), 'sales_Price') + str(tax))

def taxable(e_id,m_id):

    if (get_from_events(e_id, 'state')=='MN')&(get_from_items(m_id,'taxable')):
        return True
    else:
        return False








def view_table(name):
    """View a given table"""
    try:
        if name == 'items':
            records = c.execute('SELECT * FROM items')
            c.row_factory = sqlite3.Row  # so that you can access columns by name
            r=[]
            for record in records:
                r.append(record)
            return r

        elif name == 'events':
            records = c.execute('SELECT * FROM events')
            c.row_factory = sqlite3.Row  # so that you can access columns by name
            r = []
            for record in records:
                r.append(record)
            return r

        elif name == 'event_sales':
            records = c.execute('SELECT * FROM event_sales')
            c.row_factory = sqlite3.Row
            r = []
            for record in records:
                r.append(record)
            return r

        elif name == 'orders':
            records = c.execute('SELECT * FROM orders')
            c.row_factory = sqlite3.Row  # so that you can access columns by name
            r = []
            for record in records:
                r.append(record)
            return r
        elif name == 'order_items':
            records = c.execute('SELECT * FROM order_items')
            c.row_factory = sqlite3.Row  # so that you can access columns by name
            r = []
            for record in records:
                r.append(record)
            return r

    except sqlite3.Error:
        raise MyError('Something went wrong when trying to display the table')


def delete_table():
    """Used to delete a table.  Only intended for debugging use."""
    '''Have not made and will not make unit test for this.  It is only used for debugging and I don't want to write a 
       function to feed it the name of the table to delete.'''
    try:
        name= ui.get_table_input()
        c.execute('DROP TABLE IF EXISTS '+name) #Delete table
        db.commit() #save changes

    except sqlite3.Error as e:
        ui.show_message('An error occurred.  Changes will be rolled back.')
        traceback.print_exc()
        db.rollback()


def is_ID(table, id1 , *id2):
    """Searches given table for incidence of given id.  returns True if found, otherwise False."""

    try:
        if table=="items":
            result=get_from_items(id1,'all')
            if len(result)>0:
                return True
            else:
                return False
        elif table=="events":
            result=get_from_events(id1,'all')
            if len(result) > 0:
                return True
            else:
                return False
        elif table=="event_sales":
            i_id=id2[0] #Get value from tuple (don't know why this is coming in as a tuple, but this fixes it.)
            results=get_from_event_sales(id1, i_id, 'all')
            c.row_factory=sqlite3.Row
            for r in results:
                if len(r.keys()) > 0:
                    return True
                else:
                    return False
        elif table=='orders':
            c.execute('SELECT * FROM orders WHERE order_ID=?',(id,))
            result=c.fetchone()
            if len(result)>0:
                return True
            else:
                return False

    except sqlite3.Error:
        #ui.show_message("An error occurred while searching for ID")
        raise MyError('An error occured while searching for ID')
        #traceback.print_exc()

def salesTax(price, total):
    """Sales tax owed using home state set in user settings"""
    global percent
    return ((price * percent)/100)*total #percent is global set from database (for MN, percent should be 7.375)

def get_types(table):
    try:
        if table=='items':
            records=c.execute('SELECT DISTINCT item_Type FROM items')
            c.row_factory=sqlite3.Row
            types = []
            for record in records:
                types.append(record['item_Type'])
            return types
        elif table=='events':
            records=c.execute('SELECT DISTINCT event_Type FROM events')
            c.row_factory = sqlite3.Row
            types = []
            for record in records:
                types.append(record['item_Type'])
            return types
    except sqlite3.Error:
        ui.show_message('An error occured while trying to get types')






# def get_total_SalesTax():
#     """How much sales tax was collected by the band for this year to date?"""
#     #sqlite doesn't support calculated columns, so I'm improvising here.
#     try:
#         year= ui.get_numeric_input("Enter the year you want to know sales tax information about (YYYY): ", 'i')
#         current_year=datetime.today().strftime("%Y")
#         if year==current_year:
#             data_since=(str(current_year)+"-01-01 01:01")
#             data_before=datetime.today()
#         else:
#             data_since=str(year)+"-01-01 00:00"
#             data_before=str(year)+"-12-31 23:59"
#
#         sql = 'SELECT event_State, sales_Price, sales_Total, item_Taxable ' \
#               'FROM event_sales ' \
#               'INNER JOIN events on events.event_ID=event_sales.event_ID ' \
#               'INNER JOIN items ON items.item_ID=event_sales.item_ID ' \
#               'WHERE event_Date BETWEEN ? AND ? '
#
#         records=c.execute(sql, (data_since,data_before))
#         c.row_factory=sqlite3.Row
#         sale_tax=0
#         for record in records:
#             if (record['event_State']=='MN') & (record['item_Taxable']==1):
#                 tax=salesTax(record['sales_Price'],record['sales_Total']) #sales tax for this item
#                 sale_tax=sale_tax+tax
#
#         return sale_tax
#
#
#     except sqlite3.Error:
#          ui.show_message('trouble searching by date')
#          traceback.print_exc()












def close_database():
    db.close()









class MyError(Exception):
    """ Custom exception class """
    pass







'''def receive_order_ui():
    done=False
    order=0
    date=datetime.today()
    while done == False:
        choice=ui.get_numeric_input('1. New item\n2. Reorder of previous item\n3. Exit','i')
        if choice==3:
            return
        elif choice==1:
            add_record('items')
        elif choice==2:
            order=ui.get_numeric_input('Enter the order id for this order: ','i')
            item_ID=ui.get_numeric_input('','i')
            date=ui.get_date_input('Enter the date the order was received')
            total=ui.get_numeric_input('','i')
            cost=ui.get_numeric_input('','f')
            note=ui.get_input('')
            item=[order,item_ID,date,total,cost,note]
            receive_Order  (item)

        elif choice==3:
            done=True
    update_Orders('date', order, date)
    #choice, item_ID, date, total, cost, note, vendorID

    pass
'''







