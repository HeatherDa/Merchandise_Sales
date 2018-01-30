import sqlite3
import traceback
import ui
import DataValidation
from datetime import datetime


db = sqlite3.connect('merchandising_db.db') #Creates db file or opens if it already exists
c=db.cursor() #Cursor object
item_types=['T-Shirt', 'CD', 'Poster']
event_types=['Concert', 'Signing']
#c.row_factory=sqlite3.Row

def create_merchandise_table():
    #Create merchandise table
    try:
        c.execute('CREATE TABLE if not exists merchandise (merch_ID integer primary key, merch_Type text not null,'
                  ' merch_Description text not null, merch_Total_Ordered int, merch_Cost real, merch_Taxable int)')
        c.execute('SELECT * FROM merchandise')
        rec=c.fetchall()
        items= [('T-Shirt', 'black, yellow logo', 100, 8.00, 0),
                ('T-Shirt', 'white, blue logo', 100, 7.00, 0),
                ('CD', 'Adajio', 100, 5.00, 1),
                ('CD', 'Fortisimo', 100, 5.00, 1),
                ('Poster', '2017 Holiday Band Photo', 100, 4.00, 1),
                ('Poster', 'Adajio cover', 100, 4.00, 1)]

        if len(rec)<1:  #If table is empty, add data
            c.executemany('INSERT INTO merchandise (merch_Type, merch_Description, merch_Total_Ordered, merch_Cost, merch_Taxable) VALUES (?,?,?,?,?)', items)
            db.commit()  #save changes

    except sqlite3.Error:
        print('An error occurred.')
        traceback.print_exc()


def create_events_table():
    """ Create events table"""
    try:
        c.execute(
            'create table if not exists events (events_ID integer primary key, event_Type text not null, event_Date DATETIME,'
            ' event_Street text, event_City text, event_State text, event_Zip text, event_Contact text, event_Contact_Phone text)')
        c.execute('SELECT * FROM events')
        rec = c.fetchall()
        events = [('Concert', '2018-01-28 18:00', '203 Robert St.', 'Minneapolis', 'MN', '55116', 'Candice Jennings', '612-287-6830'),
                  ('Signing', '2018-02-07 15:00', '151 Afton Ave.', 'Milwakee', 'WI', '52964', 'Alice Milton', '952-600-8700'),
                  ('Concert', '2018-02-12 19:30', '523 Bolton Rd.', 'Fargo', 'ND', '59721', 'John Cobbler', '542-890-7231'),
                  ('Signing', '2018-03-15 14:30', '3030 Colton Way', 'New Olm', 'MN', '57382', 'Kaiser Tannenburg', '472-113-9157')]

        if len(rec) < 1:  # If table is empty, add data
            c.executemany('INSERT INTO events (event_Type, event_Date, event_Street, event_City, event_State, event_Zip, event_Contact, event_Contact_Phone) VALUES (?,?,?,?,?,?,?,?)', events)
            db.commit()  # save changes

    except sqlite3.Error as e:
        print('An error occurred.')
        traceback.print_exc()

def salesTax(price, total):
    """Sales tax owed assuming the user lives in MN"""
    return (round(((price*7.375)/100),2))*total


def create_event_sales_table():
    """Create event_sales table"""
    try:
        #delete_table()
        sql='CREATE TABLE if not exists event_sales (events_ID integer not null, merch_ID integer not null, sales_Total integer, ' \
            'sales_Price real not null, sales_Tax real, CONSTRAINT event_sales PRIMARY KEY (events_ID, merch_ID))'

        c.execute(sql)
            #'CREATE TABLE if not exists event_sales (events_ID integer, merch_ID integer, sales_Total integer, sales_Price real not null, sales_Tax real)')
        c.execute('SELECT * FROM event_sales')
        rec = c.fetchall()
        a=salesTax(10.00,8)
        sales = [(1, 1, 5, 10.00, 0.00),
                 (1, 2, 4, 10.00, 0.00),
                 (1, 3, 8, 10.00, salesTax(10.00,8)),
                 (1, 4, 2, 10.00, salesTax(10.00,2)),
                 (1, 5, 3, 8.00, salesTax(8.00,3)),
                 (1, 6, 1, 8.00, salesTax(8.00,1))]


        if len(rec) < 1:  # If table is empty, add data
            c.executemany('INSERT INTO event_sales (events_ID, merch_ID, sales_Total, sales_Price, sales_Tax) VALUES (?,?,?,?,?)', sales)
            db.commit()  # save changes

    except sqlite3.Error as e:
        print('An error occurred.')
        traceback.print_exc()
        traceback.print_exception()


def add_item_type():
    """Add new item type.  Appends item type to global item_types list"""
    global item_types
    type=ui.get_input("Enter the name of the new item type: ")
    item_types.append(type)

def add_event_type():
    """Add new event type.  Appends event type to global event_types list"""
    global event_types
    type=ui.get_input("Enter the name of the new event type: ")
    item_types.append(type)

def new_item():
    """Add new item to merchandise table"""
    try:
        item=ui.get_type_input(item_types)
        description=ui.get_input("Please describe the item. (Example: 'white, blue logo' for a T-Shirt, or the title for a CD or Poster.): ")
        total_ordered=ui.get_numeric_input("How many items were ordered?")
        cost_per_item=ui.get_numeric_input("How much does each item cost?")
        taxable=ui.get_numeric_input("Enter 1 if this item is subject to sales tax: ")
        if taxable !=1:
            taxable=0
        c.execute('insert into merchandise values(?,?,?,?,?)',(item,description,total_ordered, cost_per_item, taxable))
        db.commit()  #save changes

    except sqlite3.IntegrityError:
        print ('wrong data type?  Changes will be rolled back.')
        traceback.print_exc()
        db.rollback()

    except sqlite3.Error as e:
        print('An error occurred.  Changes will be rolled back.')
        traceback.print_exc()
        db.rollback()

def get_ordered(id):
    """How many of a given item in the merchandise table have been ordered so far?"""
    try:
        c.row_factory = sqlite3.Row
        record=c.execute('SELECT * FROM merchandise WHERE merch_ID=?', id)
        ordered= record['merch_Total_Ordered'] #May be a problem.  Should work based on pg 482 Murach's Python Programming
        return ordered
    except sqlite3.Error:
        ui.show_message("An error ocurred while searching for order total.")
        traceback.print_exc()

def get_SalesTax_Owed(): #TODO: this sql might be wrong.  Not sure how to compare date properly.  Might simplify to assume that previous year's data no longer stored in database.
    """How much sales tax was collected by the band for this year to date?"""
    today=datetime.today()
    current_year=(datetime(today.year))
    data_since=str(current_year)+"-01-01"
    try:
        c.execute('SELECT SUM (sales_Tax) '
                  'FROM event_sales '
                  'JOIN events on events.event_ID=event_sales.event_ID '
                  'WHERE event_Date >= ?', data_since)
        record=c.fetchone()
        ui.show_message("Total Sales Tax collected since "+data_since+": ")
        ui.show_message(record)
    except sqlite3.Error:
        ui.show_message("An error occurred while calculating total sales tax owed.")
        traceback.print_exc()

def new_event():
    """Add new event to events table"""
    try:
        type=ui.get_type_input(event_types)
        date = ui.get_date_input()
        street=ui.get_input("What is the street address of the event?")
        city=ui.get_input("What is the name of the city in which the event is located?")
        state=ui.get_input("What is the state in which the event takes place?  Please use state code.")
        zip=ui.get_input("What is the zip code of the event location?")
        contact=ui.get_input("What is the name of the contact person for this event?")
        phone=ui.get_input("What is the phone number of the contact person for this event?")

        c.execute('insert into merchandise values(?,?,?,?)',(type,date,street,city,state,zip,contact,phone))
        db.commit()  #save changes

    except sqlite3.IntegrityError:
        print ('wrong data type?  Changes will be rolled back.')
        traceback.print_exc()
        db.rollback()

    except sqlite3.Error as e:
        print('An error occurred.  Changes will be rolled back.')
        traceback.print_exc()
        db.rollback()


def get_Taxable(m_ID):
    c.row_factory = sqlite3.Row
    result = c.execute('SELECT * FROM merchandise WHERE merch_ID=?', m_ID)
    tax = result['merch_Taxable']
    if tax==1:
        return True
    elif tax==0:
        return False
    else:
        a=ui.get_numeric_input("Bad data in Taxable column for this id. Enter 1 if this item should be taxable.")
        if a=='1':
            return True
        else:
            return False



def new_event_sales():
    try:
        e_ID=ui.get_numeric_input("Enter the event ID: ")
        m_ID=ui.get_numeric_input("Enter the merchandise ID: ")
        s_total=0
        s_price=0
        while (is_ID('events',e_ID))& (is_ID('merchandise',m_ID)):
            s_total=ui.get_numeric_input("How many of the item were sold at this event?")
            s_price=ui.get_numeric_input("What price was charged per item at this event?")
        if ((get_State(e_ID))=='MN') & ((get_Taxable(m_ID))==1):
            s_tax=salesTax(s_total)
        else:
            s_tax=0.00
        sql='insert into event_sales values(?????)'
        c.execute(sql,(e_ID,m_ID,s_total,s_price,s_tax))
    except sqlite3.IntegrityError:
        ui.show_message('wrong data type?  Changes will be rolled back.')
        traceback.print_exc()
        db.rollback()

    except sqlite3.Error:
        ui.show_message("An error occured while trying to add a new event_sales record.  Changes will be rolled back.")
        traceback.print_exc()
        db.rollback()




def delete_Record():
    """Delete a record from the database by ID"""
    try:
        ui.show_message("Which table contains the record you want to delete?")
        t=ui.get_table_input()
        if t=='merchandise':
            id = ui.get_numeric_input("What is the ID of the record you wish to delete?")
            if is_ID(id,'event_sales'):
                ui.show_message('Cannot delete that record, as it is in use in another table.')
            else:
                sql='''DELETE FROM merchandise WHERE merchID=?'''
                c.execute(sql,(id,))
                db.commit()
        elif t=='events':
            id=ui.get_numeric_input("What is the ID of the record you wish to delete?")
            if is_ID(id, 'event_sales'):
                ui.show_message('Cannot delete that record, as it is in use in another table.')
            else:
                sql='''DELETE FROM events WHERE event_ID=?'''
                c.execute(sql, (id,))
                db.commit()
    except sqlite3.Error:
        ui.show_message('An error occurred.  Record could not be deleted.  Changes will be rolled back.')
        traceback.print_exc()
        db.rollback()

def view_table():
    """View a given table"""
    print('')
    name1=''
    while True:
        name=ui.get_table_input()
        if name =='merchandise':
            records=c.execute('SELECT * FROM merchandise')
            c.row_factory=sqlite3.Row #so that you can access columns by name
            ui.show_message("Merchandise Table")
            ui.merchandise_header()
            for record in records:
                merch_record_format(record)
            return
        elif name =='events':
            records=c.execute('SELECT * FROM events')
            c.row_factory=sqlite3.Row #so that you can access columns by name
            ui.show_message("Events Table")
            ui.events_header()
            for record in records:
                event_record_format(record)
            return
        elif name =='event_sales':
            records=c.execute('SELECT * FROM event_sales')
            c.row_factory=sqlite3.Row #so that you can access columns by name
            ui.show_message('Event Sales Table')
            ui.event_sales_header()
            for record in records:
                event_sales_record_format(record)
            return

def delete_table():
    """Used to delete a table.  Only intended for debugging use."""
    try:
        name=ui.get_table_input()
        c.execute('drop table '+name) #Delete table
        db.commit() #save changes

    except sqlite3.Error as e:
        print('An error occurred.  Changes will be rolled back.')
        traceback.print_exc()
        db.rollback()


def is_ID(table, id , *id2):
    """Searches given table for incidence of given id.  returns True if found, otherwise False."""
    try:
        if table=="merchandise":
            c.execute('SELECT * FROM merchandise WHERE merch_ID=?',id)
            results=c.fetchone()
            if len(results)>0:
                return True
            else:
                return False
        elif table=="events":
            c.execute('SELECT * FROM events WHERE event_ID=?',id)
            results=c.fetchone()
            if len(results) > 0:
                return True
            else:
                return False
        elif table=="event_sales":
            c.execute('SELECT * FROM event_sales WHERE event_ID = ? & merch_ID = ?',id, id2)
            results=c.fetchone()
            if len(results) > 0:
                return True
            else:
                return False
    except sqlite3.Error:
        ui.show_message("An error occurred while searching for ID")
        traceback.print_exc()

def get_State(e_ID):
    c.row_factory = sqlite3.Row
    result=c.execute('SELECT * FROM events WHERE event_ID=?',e_ID)
    state=result['event_State']
    return state

def get_Type(table, id):
    c.row_factory=sqlite3.Row
    if table=='events':
        result=c.execute('SELECT * FROM events WHERE event_ID=?',id)
        type=result['event_Type']
        return type
    elif table=='merchandise':
        result=c.execute('SELECT * FROM merchandise WHERE merch_ID=?',id)
        type=result['merch_Type']
        return type

def search_menu():
    choice=ui.get_search_menu_input()
    if choice=='1':
        table=ui.get_table_input()

        if table=='merchandise':
            id=ui.get_numeric_input("Enter the id you wish to search by: ")
            c.execute('SELECT * FROM merchandise WHERE merch_ID=?',id)
            # TODO: copy the following function and usage for following elifs also in other choices below where applicable
            record=c.fetchone()
            merch_record_format(record)
        elif table=='events':
            id=ui.get_numeric_input("Enter the id you wish to search by: ")
            c.execute('SELECT * FROM events WHERE event_ID=?',id)
            record=c.fetchone()
            event_record_format(record)
        elif table=='event_sales':
            e_id=ui.get_numeric_input("Enter the event id you wish to search by: ")
            m_id=ui.get_numeric_input("Enter the merchandise id you wish to search by: ")
            c.execute('SELECT * FROM events WHERE event_ID=? AND merch_ID=?', (e_id, m_id))
            record=c.fetchone()
            event_sales_record_format(record)

    elif choice=='2':
        table=ui.get_table_input()
        type=ui.get_numeric_input("Enter the type you wish to search by")
        if table=='merchandise':
            c.execute('SELECT * FROM merchandise WHERE merch_Type = ?',type)
            records=c.fetchall()
            for record in records:
                merch_record_format(record)
        elif table=='events':
            c.execute('SELECT * FROM events WHERE event_Type = ?',type)
            records=c.fetchall()
            for record in records:
                event_record_format(record)
        elif table=='event_sales':
            ui.show_message("This table does not have any column Type.")

    elif choice=='3':
        #Get Event by Date
        c.execute('SELECT * FROM events ORDER BY event_Date ASC')
        records=c.fetchall()
        ui.events_header()
        for r in records:
            ui.show_message(r)
    elif choice=='4':
        #Get items by quantity in inventory
        par=ui.get_input("Return items where remaining inventory is less than: ")
        #I tested the following in Access, but not sure if it works here.
        sql= 'SELECT merchandise.merch_ID, SUM(event_sales.sales_Total) AS items_sold, merchandise.merch_Total_Ordered, ' \
             '(merch_Total_Ordered-SUM(event_sales.sales_Total)) AS Remaining Inventory ' \
             'FROM merchandise INNER JOIN event_sales on event_sales.merch_ID=merchandise.merch_ID ' \
             'GROUP BY merchandise.merch_ID, merchandise.merch_Total_Ordered' \
             'HAVING (merch_Total_Ordered-SUM(event_sales.sales_Total))<?'
        c.execute(sql,par)
        records=c.fetchall()
        ui.inventory_Header()
        for record in records:
            ui.show_message(record) #TODO: format output
    elif choice=='5':
        #Get Total Sales Tax Owed for year to date
        get_SalesTax_Owed()
    elif choice=='6':
        #Get list of items by profit
        ui.show_message("1. Profit for a specific item ID\n2. Total Profit per item\n3. Total profit to date")
        choice=ui.get_numeric_input("Enter your selection: ")
        if choice==1:
            merch_ID=ui.get_numeric_input("What item ID do you want to use?")
            sql='SELECT merchandise.merch_ID, SUM(((event_sales.sales_Price-merchandise.merch_Cost)*event_sales.sales_Total)-event_sales.sales_Tax)' \
                'FROM merchandise INNER JOIN merchandise.merch_ID=event_sales.merch_ID' \
                'WHERE merchandise.merch_ID=? GROUP BY merchandise.merchID'
            c.row_factory=sqlite3.Row
            record=c.execute(sql,merch_ID)
            ui.show_message("Item ID\tProfit")
            ui.show_message(str(merch_ID, "\t" , record['Profit']))
        elif choice==2:
            sql='SELECT merchandise.merch_ID, SUM(((event_sales.sales_Price-merchandise.merch_Cost)*event_sales.sales_Total)-event_sales.sales_Tax)' \
                'FROM merchandise INNER JOIN merchandise.merch_ID=event_sales.merch_ID' \
                'GROUP BY merchandise.merchID'
            c.row_factory = sqlite3.Row
            records = c.execute(sql)
            ui.show_message("Item ID\tProfit")
            for r in records:
                ui.show_message(str(r['merch_ID'], "\t", r['Profit']))
        elif choice==3:
            sql='SELECT merchandise.merch_ID, SUM(((event_sales.sales_Price-merchandise.merch_Cost)*event_sales.sales_Total)-event_sales.sales_Tax)' \
                'FROM merchandise INNER JOIN merchandise.merch_ID=event_sales.merch_ID' \
                'GROUP BY merchandise.merchID'
            c.row_factory = sqlite3.Row
            records = c.execute(sql)
            total=0
            for r in records:
                total=total+r[1]
            ui.show_message('Total Profit made so far: '+str(total))

    elif choice=='7':
        #Get items sold by event_ID
        e_id=ui.get_numeric_input("Enter the event id for which you would like to search: ")
        sql="SELECT * " \
            "FROM event_sales" \
            "WHERE event_ID=?"
        c.row_factory=sqlite3.Row
        c.execute(sql,e_id)
        records=c.fetchall()
        ui.event_sales_header()
        for record in records:
            event_sales_record_format(record)

    #handle input from search menu in ui.


def update_entry():
    table=ui.get_table_input()
    a=True
    if table=='merchandise':
        while a==True:
            merch_ID=ui.get_input ("What is the merchandise ID of the item that you wish to update?  Type Q to quit without updating.")
            if (merch_ID == 'Q') | (merch_ID=='q'):
                return
            elif is_ID('merchandise',merch_ID):
                b=True
                sql=""
                updateData=""
                while b:
                    choice=ui.get_input("1. Type\n2. Description\n3. Total ordered\n4. Cost")
                    if choice=='1':
                        updateData=ui.get_input("Enter the new item type: ")
                        sql='''UPDATE merchandise SET merch_Type=? WHERE merch_ID=?'''
                        break
                    elif choice == '2':
                        updateData=ui.get_input("Enter the new description: ")
                        sql = '''UPDATE merchandise SET merch_Description=? WHERE merch_ID=?'''
                        break
                    elif choice == '3':
                        m_order=ui.get_numeric_input("How many were ordered?")#TODO: maybe order new items should be a menu option which would then update this?
                        updateData=m_order+get_ordered(merch_ID) #How many were ordered before + new quantity
                        sql = '''UPDATE merchandise SET merch_Total_Ordered=? WHERE merch_ID=?'''
                        break
                    elif choice == '4':
                        ch=0
                        updateData=0
                        while (ch !='Q') & (ch !='q') : #This is not how I would handle this in a real inventory system.  I'd have a vendor's table, orders table, and order line item table to track changes in item costs.
                            ch=ui.get_input('Cost should only be updated if an error was made.  '
                                            '\nA change in item cost should be reflected by adding a new item.'
                                            '\nEnter the updated cost or Q to quit without update. ')
                            if DataValidation.is_Float(ch):
                                updateData=float(ch)
                        sql = '''UPDATE merchandise SET merch_Cost=? WHERE merch_ID=?'''
                        break
                try:
                    c.execute(sql, (updateData, merch_ID))
                    db.commit()
                    return
                except sqlite3.Error:
                    ui.show_message('An error occured while trying to update merchandise table.  Changes will be rolled back.')
                    traceback.print_exc()
                    db.rollback()
            else:
                ui.show_message("Please enter a valid ID.")
    elif table=="events":
        while a==True:
            event_ID=ui.get_numeric_input("What is the event ID of the event you wish to update? Type Q to exit without updating.")
            if (event_ID == 'Q') | (event_ID == 'q'):
                return
            elif is_ID('events', event_ID):
                b = True #this and the next two lines are unreferenced if while loop is just while True.  Would it work better that way?
                sql = ""
                updateData = ""
                while b:
                    choice = ui.get_input("1. Type\n2. Date (MM/DD/YY)\n3. Street Address\n4. City\n5. State\n"
                                          "6. Zip code\n7. Price\n8. Contact\n9. Contact Phone")
                    if choice == '1':
                        updateData = ui.get_input("Enter the event type: ")
                        sql = '''UPDATE events SET event_Type=? WHERE event_ID=?'''
                        break
                    elif choice == '2':
                        updateData = ui.get_input("Enter the date of the event (MM/DD/YY): ")
                        sql = '''UPDATE events SET event_Date=? WHERE event_ID=?'''
                        break
                    elif choice == '3':
                        updateData = ui.get_input("Enter the street address of the event: ")
                        sql = '''UPDATE events SET event_Street=? WHERE event_ID=?'''
                        break
                    elif choice == '4':
                        updateData=ui.get_input("Enter the City in which the event takes place: ")
                        sql= '''UPDATE events SET event_City=? WHERE event_ID=?'''
                        break
                    elif choice == '5':
                        updateData=ui.get_input("Enter the state in which the event takes place: ")
                        sql = '''UPDATE events SET event_City=? WHERE event_ID=?'''
                        break
                    elif choice == '6':
                        updateData=ui.get_input("Enter the zip code where the event takes place: ")
                        sql = '''UPDATE events SET event_City=? WHERE event_ID=?'''
                        break
                    elif choice == '7':
                        updateData=ui.get_input("Enter the full name of the contact person for this event: ")
                        sql = '''UPDATE events SET event_City=? WHERE event_ID=?'''
                        break
                    elif choice == '8':
                        updateData=ui.get_input("Enter the phone number of the contact person for this event: ")
                        sql = '''UPDATE events SET event_City=? WHERE event_ID=?'''
                        break
                    else:
                        ui.show_message("Please enter a choice")
                try:
                    c.execute(sql, (updateData, event_ID))
                    db.commit()
                    return
                except sqlite3.Error:
                    ui.show_message('An error occured while trying to update events table.  Changes will be rolled back.')
                    traceback.print_exc()
                    db.rollback()
            else:
                ui.show_message("Please enter a valid ID.")
    elif table=="event_sales":
        while a==True:
            m_ID=ui.get_numeric_input("What is the merchandise ID of the entry that you wish to update?  Type Q to exit without updating.")
            e_ID=ui.get_numeric_input("What is the event ID of the entry that you wish to update? Type Q to exit without updating.")
            if ((e_ID == 'Q') | (e_ID == 'q'))|((m_ID=='Q')|(m_ID=='q')):
                return
            elif is_ID('event_sales', e_ID, m_ID):
                b = True #this and the next two lines are unreferenced if while loop is just while True.  Would it work better that way?
                sql = ""
                updateData = ""
                while b:
                    choice = ui.get_input("1. Total Sold\n2. Sale Price")
                    if choice == '1':
                        updateData = ui.get_input("Enter the total number of this item sold at the event: ")
                        sql = '''UPDATE event_sales SET sales_Total=? WHERE event_ID=? & merch_ID=?'''
                        break
                    elif choice == '2':
                        updateData=ui.get_numeric_input("Enter the ")
                        sql='''UPDATE event_sales SET sales_Price=? WHERE event_ID=? & merch_ID=?'''
                        break
                try:
                    c.execute(sql, (updateData, e_ID, m_ID))
                    db.commit()
                    return
                except sqlite3.Error:
                    ui.show_message('An error occured while trying to update event_sales table.  Changes will be rolled back.')
                    traceback.print_exc()
                    db.rollback()
            else:
                if (is_ID('events', e_ID)) & (is_ID('merchandise',m_ID)):
                    ui.show_message("No record of this item being sold at this event.")
                elif (is_ID('events',e_ID)):
                    ui.show_message("Please verify that this merchandise ID is correct")
                elif (is_ID('merchandise', m_ID)):
                    ui.show_message("Please verify that this event ID is correct")

def close_database():
    db.close()

def add_spaces(str, col):
    if col =='merch_Description':
        length=len(str)
        dif=30-length
        str=str+(dif*" ")+"\t"
        return str
    elif col=='address':
        str=str+' \t'
        return str
    else:
        length=len(str)
        dif=10-length
        str=str+(dif*" ")+" \t"
        return str

def merch_record_format(record):
    taxable=''
    if record['merch_Taxable']==0:
        taxable='False'
    else:
        taxable='True'

    ui.show_message(add_spaces(str(record["merch_ID"]),'merch_ID')+
                    add_spaces(str(record["merch_Type"]),'merch_Type') +
                    add_spaces(str(record["merch_Description"]),'merch_Description') +
                    add_spaces(str(record["merch_Total_Ordered"]),'merch_Total_Ordered')+
                    add_spaces(str(record["merch_Cost"]),'merch_Cost') + taxable)
#TODO: Figure out why above works, but bellow two functions don't work.  They should work the same way....
def event_record_format(record):
    address = str(record['event_Street']+ ", " + record['event_City'] +", " + record['event_State'] + ", "+ record['event_Zip']+ " \t ")
    print (address)
    ui.show_message(add_spaces(str(record["event_ID"]),'event_ID')+
                    add_spaces(str(record["event_Type"]),'event_Type') +
                    add_spaces(str(record["event_Date"]),'event_Date')+
                    add_spaces(address, 'address')+
                    add_spaces((record["event_Contact"]),'event_Contact')+
                    add_spaces(str(record["event_Contact_Phone"]),'event_Contact_Phone'))

def event_sales_record_format(record):
    ui.show_message(add_spaces(str(record["event_ID"]),"event_ID")+
                    add_spaces(str(record["merch_ID"]),"merch_ID")+
                    add_spaces(str(record["sales_Total"]),"sales_Total")+
                    add_spaces(str(record["sales_Price"]),"sales_Price")+
                    add_spaces(str(record["sales_Tax"]),"sales_Tax"))


def add_record():
    table=ui.get_table_input()
    if table=='merchandise':
        new_item()
    elif table=='events':
        new_event()
    elif table=='event_sales':
        new_event_sales()

