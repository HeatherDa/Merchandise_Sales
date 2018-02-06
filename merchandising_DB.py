import sqlite3
import traceback
import ui
import DataValidation
from datetime import datetime

db = sqlite3.connect('merchandising_db.db') #Creates db file or opens if it already exists
c=db.cursor() #Cursor object

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
        ui.show_message('An error occurred.')
        traceback.print_exc()


def create_events_table():
    """ Create events table"""
    try:
        c.execute(
            'create table if not exists events (event_ID integer primary key, event_Type text not null, event_Date DATETIME,'
            ' event_Street text, event_City text, event_State text, event_Zip text, event_Contact text, event_Contact_Phone text)')
        c.execute('SELECT * FROM events')
        rec = c.fetchall()
        events = [('Concert', '2018-01-28 18:00:00', '203 Robert St.', 'Minneapolis', 'MN', '55116', 'Candice Jennings', '612-287-6830'),
                  ('Signing', '2018-02-07 15:00:00', '151 Afton Ave.', 'Milwakee', 'WI', '52964', 'Alice Milton', '952-600-8700'),
                  ('Concert', '2018-02-12 19:30:00', '523 Bolton Rd.', 'Fargo', 'ND', '59721', 'John Cobbler', '542-890-7231'),
                  ('Signing', '2018-03-15 14:30:00', '3030 Colton Way', 'New Olm', 'MN', '57382', 'Kaiser Tannenburg', '472-113-9157')]

        if len(rec) < 1:  # If table is empty, add data
            c.executemany('INSERT INTO events (event_Type, event_Date, event_Street, event_City, event_State, event_Zip, event_Contact, event_Contact_Phone) VALUES (?,?,?,?,?,?,?,?)', events)
            db.commit()  # save changes

    except sqlite3.Error as e:
        ui.show_message('An error occurred.')
        traceback.print_exc()

def salesTax(price, total):
    """Sales tax owed assuming the user lives in MN"""
    return ((price*7.375)/100)*total


def create_event_sales_table():
    """Create event_sales table"""
    try:
        #delete_table()
        sql='CREATE TABLE if not exists event_sales (event_ID integer not null, merch_ID integer not null, sales_Total integer, ' \
            'sales_Price real not null, CONSTRAINT event_sales PRIMARY KEY (event_ID, merch_ID))'

        c.execute(sql)
            #'CREATE TABLE if not exists event_sales (events_ID integer, merch_ID integer, sales_Total integer, sales_Price real not null)')
        c.execute('SELECT * FROM event_sales')
        rec = c.fetchall()
        sales = [(1, 1, 5, 10.00),
                 (1, 2, 4, 10.00),
                 (1, 3, 8, 10.00),
                 (1, 4, 2, 10.00),
                 (1, 5, 3, 8.00),
                 (1, 6, 1, 8.00)]


        if len(rec) < 1:  # If table is empty, add data
            c.executemany('INSERT INTO event_sales (event_ID, merch_ID, sales_Total, sales_Price) VALUES (?,?,?,?)', sales)
            db.commit()  # save changes

    except sqlite3.Error as e:
        ui.show_message('An error occurred.')
        traceback.print_exc()

def get_types(table):
    try:
        if table=='merchandise':
            c.execute('SELECT DISTINCT merch_Type FROM merchandise')
            a=c.fetchall()
            types=[]
            for ty in a:
                types.append(ty)
            return types
        elif table=='events':
            c.execute('SELECT DISTINCT event_Type FROM events')
            a = c.fetchall()
            types = []
            for ty in a:
                types.append(ty)
            return types
    except sqlite3.Error:
        ui.show_message('An error occured while trying to get types')


def new_item():
    """Add new item to merchandise table"""
    try:
        item_types=get_types('merchandise')
        item=ui.get_type_input(item_types)
        description=ui.get_input("Please describe the item. (Example: 'white, blue logo' for a T-Shirt, or the title for a CD or Poster.): ")
        total_ordered=ui.get_numeric_input("How many items were ordered?",'i')
        cost_per_item=ui.get_numeric_input("How much does each item cost?",'f')
        taxable=ui.get_numeric_input("Enter 1 if this item is subject to sales tax. Otherwise, type 0: ",'i')
        if taxable !=1:
            taxable=0
        sql='INSERT INTO merchandise (merch_Type, merch_Description, merch_Total_Ordered, merch_Cost, merch_Taxable)VALUES(?,?,?,?,?)'
        c.execute(sql, (item,description,total_ordered, cost_per_item, taxable))
        db.commit()  #save changes

    except sqlite3.IntegrityError:
        ui.show_message ('wrong data type?  Changes will be rolled back.')
        traceback.print_exc()
        db.rollback()

    except sqlite3.Error as e:
        ui.show_message('An error occurred.  Changes will be rolled back.')
        traceback.print_exc()
        db.rollback()



def get_SalesTax(choice):
    """How much sales tax was collected by the band for this year to date?"""
    #sqlite doesn't support calculated columns, so I'm improvising here.
    try:
        if choice == 'display':
            sql = 'SELECT event_sales.event_ID, event_sales.merch_ID, event_State, sales_Total, sales_Price, merch_Taxable ' \
                  'FROM event_sales ' \
                  'INNER JOIN events ON events.event_ID=event_sales.event_ID ' \
                  'INNER JOIN merchandise ON merchandise.merch_ID=event_sales.merch_ID'
            records = c.execute(sql)
            c.row_factory = sqlite3.Row

            for record in records:
                if (record['event_State']) !='MN':
                    event_sales_record_format(record, 0.00)
                elif (record['event_State'] == 'MN') & (record['merch_Taxable']==1) :
                    tax = salesTax(record['sales_Price'], record['sales_Total'])  # sales tax for this item
                    event_sales_record_format(record,tax)
                else:
                    event_sales_record_format(record, 0.00)

            return

        elif choice=='total':
            year=ui.get_numeric_input("Enter the year you want to know sales tax information about (YYYY): ",'i')
            current_year=datetime.today().strftime("%Y")
            if year==current_year:
                data_since=(str(current_year)+"-01-01 01:01")
                data_before=datetime.today()
            else:
                data_since=str(year)+"-01-01 00:00"
                data_before=str(year)+"-12-31 23:59"

            sql = 'SELECT event_State, sales_Price, sales_Total, merch_Taxable ' \
                   'FROM event_sales ' \
                   'INNER JOIN events on events.event_ID=event_sales.event_ID ' \
                   'INNER JOIN merchandise ON merchandise.merch_ID=event_sales.merch_ID ' \
                   'WHERE event_Date BETWEEN ? AND ? '

            records=c.execute(sql, (data_since,data_before))
            c.row_factory=sqlite3.Row
            sale_tax=0
            for record in records:
                if (record['event_State']=='MN') & (record['merch_Taxable']==1):
                    tax=salesTax(record['sales_Price'],record['sales_Total']) #sales tax for this item
                    sale_tax=sale_tax+tax

            return sale_tax


    except sqlite3.Error:
         ui.show_message('trouble searching by date')
         traceback.print_exc()

def new_event():
    """Add new event to events table"""
    try:
        type=ui.get_type_input(get_types('events'))
        date = ui.get_date_input()
        street=ui.get_input("Enter the street address of the event: ")
        city=ui.get_input("Enter the name of the city in which the event is located: ")
        state=ui.get_input("Enter the state code of the state in which the event will take place: ")
        zip=ui.get_input("Enter the zip code of the event location: ")
        contact=ui.get_input("Enter the name of the contact person for this event: ")
        phone=ui.get_input("Enter the phone number of the contact person for this event: ")

        sql='INSERT INTO events (event_Type, event_Date, event_Street, event_City, event_State,event_Zip, event_Contact, event_Contact_Phone) VALUES (?,?,?,?,?,?,?,?)'
        c.execute(sql,(type,date,street,city,state,zip,contact,phone))
        db.commit()  #save changes

    except sqlite3.IntegrityError:
        ui.show_message ('wrong data type?  Changes will be rolled back.')
        traceback.print_exc()
        db.rollback()

    except sqlite3.Error as e:
        ui.show_message('An error occurred.  Changes will be rolled back.')
        traceback.print_exc()
        db.rollback()





def new_event_sales():
    try:
        while True:
            e_ID=ui.get_numeric_input("Enter the event ID: ",'i')
            m_ID=ui.get_numeric_input("Enter the merchandise ID: ",'i')
            if is_ID('event_sales', e_ID, m_ID): #if this entry already exists in the table don't make a new one
                ui.show_message("This record already exists in the table.  To change it, update the table.")
                return
            elif((is_ID('events',e_ID))& (is_ID('merchandise',m_ID))): #These ID's exists, but the combination of the two doesn't exist yet
                s_total=ui.get_numeric_input("How many of the item were sold at this event?",'i')
                s_price=ui.get_numeric_input("What price was charged per item at this event?",'f')

                sql = 'INSERT INTO event_sales (event_ID, merch_ID, sales_Total, sales_Price) VALUES (?,?,?,?)'
                c.execute(sql, (e_ID, m_ID, s_total, s_price))
                db.commit()
                return

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
        print(t)
        if t=='merchandise':
            id = ui.get_numeric_input("What is the ID of the record you wish to delete?",'i')
            results=c.execute('SELECT * FROM event_sales')
            c.row_factory=sqlite3.Row
            count=0
            for result in results:
                if result['merch_ID']==id:
                   count=count+1
            if count>0:
                ui.show_message('Cannot delete that record, as it is in use in another table.')
            else:
                sql='''DELETE FROM merchandise WHERE merch_ID=?'''
                c.execute(sql,(id,))
                db.commit()
                ui.show_message("Record Deleted")
        elif t=='events':
            id=ui.get_numeric_input("What is the ID of the record you wish to delete?",'i')
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
            e_id = ui.get_numeric_input("What is the event ID of the record you wish to delete?",'i')
            m_id = ui.get_numeric_input("What is the item ID of the record you wish to delete?",'i')

            sql = '''DELETE FROM event_sales WHERE event_ID=? AND merch_ID=?'''
            c.execute(sql, (e_id, m_id,))
            db.commit()
            ui.show_message("Record Deleted")
    except sqlite3.Error:
        ui.show_message('An error occurred.  Record could not be deleted.  Changes will be rolled back.')
        traceback.print_exc()
        db.rollback()

def view_table():
    """View a given table"""
    ui.show_message('')

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
            ui.show_message('Event Sales Table')
            ui.event_sales_header()
            get_SalesTax('display')
            return

def delete_table():
    """Used to delete a table.  Only intended for debugging use."""
    try:
        name=ui.get_table_input()
        c.execute('drop table '+name) #Delete table
        db.commit() #save changes

    except sqlite3.Error as e:
        ui.show_message('An error occurred.  Changes will be rolled back.')
        traceback.print_exc()
        db.rollback()


def is_ID(table, id , *id2):
    """Searches given table for incidence of given id.  returns True if found, otherwise False."""

    try:
        if table=="merchandise":
            c.execute('SELECT * FROM merchandise WHERE merch_ID=?',(id,))
            result=c.fetchone()
            if len(result)>0:
                return True
            else:
                return False
        elif table=="events":
            c.execute('SELECT * FROM events WHERE event_ID=?',(id,))
            result=c.fetchone()
            if len(result) > 0:
                return True
            else:
                return False
        elif table=="event_sales":
            m_id=id2[0] #Get value from tuple (don't know why this is coming in as a tuple, but this fixes it.)
            results=c.execute('SELECT * FROM event_sales WHERE event_ID = ? AND merch_ID = ?',(id, m_id,))
            c.row_factory=sqlite3.Row
            for r in results:
                if len(r.keys()) > 0:
                    return True
                else:
                    return False
    except sqlite3.Error:
        ui.show_message("An error occurred while searching for ID")
        traceback.print_exc()

def get_from_merch(merch_ID, value):
    results=c.execute('SELECT * FROM merchandise WHERE merch_ID=?', (merch_ID,))
    c.row_factory=sqlite3.Row
    r=""
    try:
        if value=='cost':
            for result in results:
                r=result['merch_Cost']
            return r
        elif value=='description':
            for result in results:
                r = result['merch_Description']
            return r
        elif value=='ordered':
            for result in results:
                r = result['merch_Total_Ordered']
            return r
        elif value=='type':
            for result in results:
                r=result['merch_Type']
            return r
        elif value=='taxable':

            tax=0
            for result in results:
                tax = result['merch_Taxable']

            if tax == 1:

                return True
            elif tax == 0:

                return False
            else:
                a = ui.get_numeric_input(
                    "Bad data in Taxable column for this id. Enter 1 if this item should be taxable.",'i')
                if a == '1':
                    return True
                else:
                    return False
    except sqlite3.Error:
        ui.show_message("An error ocurred while searching for "+value+".")
        traceback.print_exc()

def get_from_events(event_ID, value):
    results=c.execute('SELECT * FROM events WHERE event_ID=?', (event_ID,))
    c.row_factory=sqlite3.Row
    r=""
    try:
        if value=='date':
            for result in results:
                r=result['event_Date']
            return r
        elif value=='type':
            for result in results:
                r=result['event_Type']
            return r
        elif value=='street':
            for result in results:
                r=result['event_Street']
            return r
        elif value == 'city':
            for result in results:
                r = result['event_City']
            return r
        elif value=='state':
            for result in results:
                r=result['event_State']
            return r
        elif value == 'zip':
            for result in results:
                r = result['event_Zip']
            return r
        elif value=='contact':
            for result in results:
                r=result['event_Contact']
            return r
        elif value=='phone':
            for result in results:
                r=result['event_Contact_Phone']
            return r
    except sqlite3.Error:
        ui.show_message("An error ocurred while searching for "+value+".")
        traceback.print_exc()

def get_from_event_sales(e_ID, m_ID, value):
    results=c.execute('SELECT * FROM event_sales WHERE event_ID=? AND merch_ID=?',(e_ID,m_ID,))
    c.row_factory=sqlite3.Row
    r=""
    try:
        if value=='total':
            for result in results:
                r=result['sales_Total']
            return r
        elif value=='price':
            for result in results:
                r=result['sales_Price']
            return r
        elif value=='tax':
            c.execute('SELECT * FROM event_sales WHERE event_ID=? AND merch_ID=?', (e_ID, m_ID,))
            ro = c.fetchone()
            t = get_from_merch(m_ID, 'taxable')
            s = get_from_events(e_ID, 'state')
            pri = ro[2]
            tot = ro[3]
            tax = salesTax(pri, tot)
            if (t) & (s == 'MN'):
                return tax
            else:
                return 0.00
                #Don't know why the bellow code doesn't work.  It just skips the contents of the inner most for loop and returns none.
            # t=get_from_merch(m_ID,'taxable')
            # s=get_from_events(e_ID, 'state')
            # tax=0.00
            # if t ==True:
            #     if s =='MN':
            #         for result in results:
            #             tax=salesTax(result['sales_Price'],result['sales_Total'])
            #         return tax
            # elif t==False:
            #     return tax

    except sqlite3.Error:
        ui.show_message("An error occurred while searching for "+value+".")
        traceback.print_exc()

def search_menu():
    choice=ui.get_search_menu_input()
    if choice=='0':
        return
    elif choice=='1':
        table=ui.get_table_input()

        if table=='merchandise':
            id=ui.get_numeric_input("Enter the id you wish to search by: ",'i')
            records=c.execute('SELECT * FROM merchandise WHERE merch_ID=?',(id,))
            c.row_factory=sqlite3.Row
            ui.merchandise_header()
            for record in records:
                merch_record_format(record)
        elif table=='events':
            id=ui.get_numeric_input("Enter the id you wish to search by: ",'i')
            records=c.execute('SELECT * FROM events WHERE event_ID=?',(id,))
            c.row_factory=sqlite3.Row
            ui.events_header()
            for record in records:
                event_record_format(record)
        elif table=='event_sales':
            e_id=ui.get_numeric_input("Enter the event id you wish to search by: ",'i')
            m_id=ui.get_numeric_input("Enter the merchandise id you wish to search by: ",'i')
            records=c.execute('SELECT * FROM event_sales WHERE event_ID=? AND merch_ID=?', (e_id, m_id,))
            c.row_factory=sqlite3.Row
            ui.event_sales_header()
            for record in records:
                t=get_from_event_sales(e_id,m_id,'tax')
                event_sales_record_format(record,t)

    elif choice=='2':
        #choice 2 is search by type
        table=ui.get_numeric_input('1. merchandise table\n2.events table\n\nEnter your selection: ','i')
        if table==1:
            a=""
            item_types=get_types('merchandise')
            for i in item_types:
                a=a+" \n"+str(item_types.index(i)+1)+". "+str(i)
            ui.show_message(a)
            t = ui.get_numeric_input("Enter the type you wish to search by: ",'i')
            ty= item_types[t-1]
            records=c.execute('SELECT * FROM merchandise WHERE merch_Type = ?' , (ty,))
            c.row_factory=sqlite3.Row
            ui.merchandise_header()
            for record in records:
                merch_record_format(record)
        elif table==2:
            a = ""
            event_types=get_types('events')
            for i in event_types:
                a = a + str(event_types.index(i) + 1) + ". " + str(i)+' \n'
            ui.show_message(a)
            t = ui.get_numeric_input("Enter the type you wish to search by: ",'i')
            ty=event_types[t-1]
            records=c.execute('SELECT * FROM events WHERE event_Type = ?',(ty,))
            c.row_factory = sqlite3.Row
            ui.events_header()
            for record in records:
                event_record_format(record)

    elif choice=='3':
        #Show events ordered by date
        #Maybe I should have a get input for formatting dates received from user.
        records=c.execute('SELECT * FROM events ORDER BY event_Date ASC')
        c.row_factory = sqlite3.Row
        ui.events_header()
        for r in records:
            event_record_format(r)

    elif choice=='4':
        #Get items by quantity in inventory
        par=ui.get_numeric_input("Return items where remaining inventory is less than: ",'i')
        sql3= 'SELECT merchandise.merch_ID, SUM(sales_Total) ' \
              'FROM event_sales ' \
              'JOIN merchandise ON merchandise.merch_ID = event_sales.merch_ID ' \
              'GROUP BY merchandise.merch_ID '

        c.execute(sql3)
        a=c.fetchall()
        ui.inventory_Header()
        for i in a:
            sold=i[1]
            order=get_from_merch(i[0], 'ordered')
            rem=order-sold
            if rem<par:
                inventory_record_format([i[0],sold,order,rem])

    elif choice=='5':
        #Get Total Sales Tax Owed for year to date
        ui.show_message("Total sales tax owed for this year is: "+str(get_SalesTax('total')))

    elif choice=='6': #TODO event sales no longer has column for sales tax. adjust function.
        #Get list of items by profit
        ui.show_message("\n1. Profit for a specific item ID\n2. Total Profit per item\n3. Total profit this year\n")
        choice=ui.get_numeric_input("Enter your selection: ",'i')
        if choice==1:
            merch_ID=ui.get_numeric_input("\nWhat item ID do you want to use?",'i')

            sql='SELECT merchandise.merch_ID, sales_Price, merch_Cost, sales_Total, event_State, merch_Taxable ' \
                 'FROM merchandise ' \
                 'INNER JOIN event_sales ON merchandise.merch_ID=event_sales.merch_ID ' \
                 'INNER JOIN events ON event_sales.event_ID=events.event_ID ' \
                 'WHERE merchandise.merch_ID=? '

            records = c.execute(sql, (merch_ID,))
            c.row_factory=sqlite3.Row

            ui.show_message("Item ID \tProfit")
            for record in records:
                if (record['event_State'] !='MN') | (record['merch_Taxable'] ==0):
                    profit = str(((record['sales_Price'] - record['merch_Cost']) * record['sales_Total']))
                else:
                    profit=str(((record['sales_Price'] - record['merch_Cost'])*record['sales_Total']) - salesTax(record['sales_Price'], record['sales_Total']))
                ui.show_message(str(merch_ID)+ "\t \t \t" + profit)
        elif choice==2:

            sql = 'SELECT merchandise.merch_ID, sales_Price, merch_Cost, sales_Total, event_State, merch_Taxable, merch_Type, merch_Description ' \
                  'FROM merchandise ' \
                  'INNER JOIN event_sales ON merchandise.merch_ID=event_sales.merch_ID ' \
                  'INNER JOIN events ON event_sales.event_ID=events.event_ID ' \
                  'ORDER BY merchandise.merch_ID '

            records = c.execute(sql)
            c.row_factory = sqlite3.Row

            ui.show_message("\nItem ID \tItem Type \tItem Description \t\t\t\tProfit")
            for record in records:
                if (record['event_State'] != 'MN') | (record['merch_Taxable'] == 0):
                    profit = str(((record['sales_Price'] - record['merch_Cost']) * record['sales_Total']))
                else:
                    profit = str(((record['sales_Price'] - record['merch_Cost']) * record['sales_Total']) - salesTax(
                        record['sales_Price'], record['sales_Total']))
                ui.show_message(add_spaces(str(record['merch_ID']),'merch_ID') + add_spaces(str(record['merch_Type']),'merch_Type') + add_spaces(str(record['merch_Description']),'merch_Description')+profit)
        elif choice==3:
            current_year = datetime.today().strftime("%Y")
            data_since = (str(current_year) + "-01-01 01:01")

            sql='SELECT merchandise.merch_ID, sales_Price, merch_Cost, sales_Total, event_State, merch_Taxable, merch_Type, merch_Description, event_Date ' \
                  'FROM merchandise ' \
                  'INNER JOIN event_sales ON merchandise.merch_ID=event_sales.merch_ID ' \
                  'INNER JOIN events ON event_sales.event_ID=events.event_ID ' \
                  'WHERE event_Date > ? ' \
                  'ORDER BY event_Date '

            records = c.execute(sql,(data_since,))
            c.row_factory = sqlite3.Row
            total=0
            for r in records:
                total=total+r[1]#should add sums for each item together
            ui.show_message('Total Profit made so far: '+str(total))

    elif choice=='7':
        #Get items sold by event_ID
        e_id=ui.get_numeric_input("Enter the event id for which you would like to search: ",'i')
        sql="SELECT * " \
            "FROM event_sales " \
            "WHERE event_ID = ? " \
            "ORDER BY event_ID "

        c.execute(sql,(e_id,))


        a=c.fetchall()
        ui.event_sales_header()
        for i in a:
            t = get_from_event_sales(i[0], i[1], 'tax')
            tax="%.2f" % t
            ui.show_message(add_spaces(str(i[0]),'event_ID')+add_spaces(str(i[1]),'merch_ID')+add_spaces(str(i[2]),'sales_Total')+add_spaces(str(i[3]),'sales_Price')+str(tax))

def update_entry():
    '''Update a record from any table'''
    table=ui.get_table_input()
    if table=='merchandise':
        while True:
            merch_ID=ui.get_numeric_input("What is the ID of the item that you wish to update?  Type 0 to quit without updating.",'i')

            if merch_ID == 0:
                return
            elif is_ID(table,merch_ID):

                try:
                    while True:
                        choice=ui.get_numeric_input("What column do you want to update?\n1. Type\n2. Description\n3. Total ordered\n4. Cost\nEnter Choice: ",'i')
                        if choice==1:
                            ui.show_message("Previous item Type: "+str(get_from_merch(merch_ID,'type')))
                            ui.show_message('Select the new item type:')
                            updateData=ui.get_type_input(get_types('merchandise'))
                            sql='''UPDATE merchandise SET merch_Type=? WHERE merch_ID=?'''
                            c.execute(sql, (updateData, merch_ID,))
                            db.commit()
                            ui.show_message ("Updated item Type: " + str(get_from_merch(merch_ID, 'type')))
                            return
                        elif choice == 2:
                            ui.show_message("Previous item description: "+str(get_from_merch(merch_ID, 'description')))
                            updateData=ui.get_input("Enter the new description: ")
                            sql = '''UPDATE merchandise SET merch_Description=? WHERE merch_ID=?'''
                            c.execute(sql, (updateData, merch_ID,))
                            db.commit()
                            ui.show_message("Updated description: "+str(get_from_merch(merch_ID, 'description')))
                            return
                        elif choice == 3:
                            ui.show_message("Previous order total: "+ str(get_from_merch(merch_ID, 'ordered')))
                            m_order=ui.get_numeric_input("How many were ordered?",'i')#TODO: maybe order new items should be a menu option which would then update this?
                            updateData=m_order+get_from_merch(merch_ID, 'ordered') #How many were ordered before + new quantity
                            sql = '''UPDATE merchandise SET merch_Total_Ordered=? WHERE merch_ID=?'''
                            c.execute(sql, (updateData, merch_ID))
                            db.commit()
                            ui.show_message("Updated order total: "+ str( get_from_merch(merch_ID, 'ordered')))
                            return
                        elif choice == 4:
                            ui.show_message("Previous Cost: "+ str(get_from_merch(merch_ID, 'cost')))
                            ch=0
                            updateData=0
                            ui.show_message('Cost should only be updated if an error was made.  '
                                                '\nA change in item cost should be reflected by adding a new item.\n')
                            while (ch !=2): #This is not how I would handle this in a real inventory system.  I'd have a vendor's table, orders table, and order line item table to track changes in item costs.
                                ch=ui.get_numeric_input('\n1. Update cost \n2. Quit without update. \n\nEnter Selection: ','i')

                                if ch==1:
                                    v=ui.get_numeric_input('Enter the new value: ','f')
                                    if DataValidation.is_Float(ch):
                                        updateData=float(v)
                                        ui.show_message('update data is '+str(updateData))
                                    sql = '''UPDATE merchandise SET merch_Cost=? WHERE merch_ID=?'''
                                    c.execute(sql, (updateData, merch_ID))
                                    db.commit()
                                    ui.show_message("Updated Cost: " + str(get_from_merch(merch_ID, 'cost')))
                                    break
                                elif ch==2:
                                    ui.show_message('okay, no update.')
                                    break
                                else:
                                    ui.show_message('Please enter a 1 or a 2.')
                            return

                except sqlite3.Error:
                    ui.show_message('An error occured while trying to update merchandise table.  Changes will be rolled back.')
                    traceback.print_exc()
                    db.rollback()
            else:
                ui.show_message("Please enter a valid ID.")
    elif table=="events":
        while True:
            event_ID=ui.get_numeric_input("What is the event ID of the event you wish to update? Type 0 to exit without updating.",'i')

            if event_ID ==0:
                return

            elif is_ID(table, event_ID):

                try:
                    while True:
                        choice = ui.get_input("What column do you want to update?\n\n1. Type\n2. Date (MM/DD/YY)\n3. Street Address\n4. City\n5. State\n"
                                              "6. Zip code\n7. Contact\n8. Contact Phone\n\nEnter Selection: ")

                        if choice == '1':
                            ui.show_message("Previous Event Type: " + str(get_from_events(event_ID, 'type')))
                            ui.show_message("Select the new event type:")
                            updateData = ui.get_type_input(get_types('events'))
                            sql = '''UPDATE events SET event_Type=? WHERE event_ID=?'''
                            c.execute(sql, (updateData, event_ID,))
                            db.commit()
                            ui.show_message("Updated event Type: " + str(get_from_events(event_ID, 'type')))
                            return

                        elif choice == '2':
                            ui.show_message("Previous event date and time: " + str(get_from_events(event_ID, 'date')))
                            updateData = ui.get_date_input()
                            sql = '''UPDATE events SET event_Date=? WHERE event_ID=?'''
                            c.execute(sql, (updateData, event_ID,))
                            db.commit()
                            ui.show_message("Updated date: " + str(get_from_events(event_ID, 'date')))
                            return

                        elif choice == '3':
                            ui.show_message("Previous street address: "+ str(get_from_events(event_ID, 'street')))
                            updateData = ui.get_input("Enter the street address of the event: ")
                            sql = '''UPDATE events SET event_Street=? WHERE event_ID=?'''
                            c.execute(sql, (updateData, event_ID,))
                            db.commit()
                            ui.show_message("Updated street address: " + str(get_from_events(event_ID, 'street')))
                            return

                        elif choice == '4':
                            ui.show_message("Previous City: " + str(get_from_events(event_ID, 'city')))
                            updateData=ui.get_input("Enter the City in which the event takes place: ")
                            sql= '''UPDATE events SET event_City=? WHERE event_ID=?'''
                            c.execute(sql, (updateData, event_ID,))
                            db.commit()
                            ui.show_message("Updated City: " + str(get_from_events(event_ID, 'city')))
                            return

                        elif choice == '5':
                            ui.show_message("Previous State: " + str(get_from_events(event_ID, 'state')))
                            updateData=ui.get_state_input("Enter the state in which the event takes place: ")
                            sql = '''UPDATE events SET event_State=? WHERE event_ID=?'''
                            c.execute(sql, (updateData, event_ID,))
                            db.commit()
                            ui.show_message("Updated State: " + str(get_from_events(event_ID, 'state')))
                            return

                        elif choice == '6':
                            ui.show_message("Previous zip code: " + str(get_from_events(event_ID, 'zip')))
                            updateData=ui.get_zip_input("Enter the zip code where the event takes place: ")
                            sql = '''UPDATE events SET event_zip=? WHERE event_ID=?'''
                            c.execute(sql, (updateData, event_ID,))
                            db.commit()
                            ui.show_message("Updated zip code: " + str(get_from_events(event_ID, 'zip')))
                            return

                        elif choice == '7':
                            ui.show_message("Previous event Contact: " + str(get_from_events(event_ID, 'contact')))
                            updateData=ui.get_input("Enter the full name of the contact person for this event: ")
                            sql = '''UPDATE events SET event_Contact=? WHERE event_ID=?'''
                            c.execute(sql, (updateData, event_ID,))
                            db.commit()
                            ui.show_message("Updated event Contact: " + str(get_from_events(event_ID, 'contact')))
                            return

                        elif choice == '8':
                            ui.show_message("Previous Contact phone number: " + str(get_from_events(event_ID, 'phone')))
                            updateData=ui.get_phone_input("Enter the phone number of the contact person for this event (xxx-xxx-xxxx): ")
                            sql = '''UPDATE events SET event_Contact_Phone=? WHERE event_ID=?'''
                            c.execute(sql, (updateData, event_ID,))
                            db.commit()
                            ui.show_message("Updated Contact phone number: " + str(get_from_events(event_ID, 'phone')))
                            return

                        else:
                            ui.show_message("Please enter a choice")
                except sqlite3.Error:
                    ui.show_message('An error occured while trying to update events table.  Changes will be rolled back.')
                    traceback.print_exc()
                    db.rollback()
            else:
                ui.show_message("Please enter a valid ID.")
    elif table=="event_sales":
        while True:
            m_ID=ui.get_numeric_input("What is the merchandise ID of the entry that you wish to update?  Type 0 to exit without updating.",'i')
            e_ID=0
            if m_ID !=0:
                e_ID=ui.get_numeric_input("What is the event ID of the entry that you wish to update? Type 0 to exit without updating.",'i')
            if ((e_ID == '0')|(m_ID=='0')):
                return
            elif is_ID('event_sales', e_ID, m_ID):
                try:
                    while True:

                        choice = ui.get_input("\nWhat column do you want to update?\n\n1. Total Sold\n2. Sale Price\n\nEnter Selection: ")
                        if choice == '1':
                            ui.show_message("Previous number of item sold: "+str(get_from_event_sales(e_ID,m_ID,'total')))
                            updateData = ui.get_numeric_input("Enter the total number of this item sold at the event: ",'i')
                            sql = '''UPDATE event_sales SET sales_Total=? WHERE event_ID=? AND merch_ID=?'''
                            c.execute(sql, (updateData, e_ID, m_ID))
                            db.commit()
                            ui.show_message("Updated number of item sold: " + str(get_from_event_sales(e_ID, m_ID, 'total')))
                            return
                        elif choice == '2':
                            ui.show_message("Previous sales price: "+str(get_from_event_sales(e_ID,m_ID,'price')))
                            updateData=ui.get_numeric_input("Enter the new sale price: ",'f')
                            sql='''UPDATE event_sales SET sales_Price=? WHERE event_ID=? AND merch_ID=?'''
                            c.execute(sql, (updateData, e_ID, m_ID))
                            db.commit()
                            ui.show_message("Updated sales price: " + str(get_from_event_sales(e_ID, m_ID, 'price')))
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

def add_spaces(st, col):
    if (col =='merch_Description') | (col=='iTotal'):
        length=len(st)
        dif=30-length
        st=st+(dif*" ")+"\t"
        return st
    elif col=='address':
        length=len(st)
        dif=40-length
        st=st+(dif*" ")+'\t'
        return st
    elif (col=='event_Contact') :
        length=len(st)
        dif=25-length
        st=st+(dif*" ")+'\t'
        return st
    elif (col=='sales_Total') | (col=='sold'):
        length=len(st)
        dif=14-length
        st=st+(dif*" ")+" \t"
        return st
    elif (col=='sales_Price') | (col=='sales_Tax'):
        length = len(str(st))
        dif = 13 - length
        fl=float(st)
        s="%.2f" %fl
        st = s + (dif * " ") + " \t"
        return st
    elif col=='merch_Total_Ordered':
        length = len(st)
        dif = 10 - length
        st = st + (dif * " ") + " \t\t"
        return st
    elif (col=='iOrdered'):
        length = len(st)
        dif = 16 - length
        st = st + (dif * " ") + " \t"
        return st
    elif (col=='event_Date') :
        length=len(st)
        dif = 20 - length
        st = st + (dif*" ") + " \t"
        return st
    else:
        length=len(st)
        dif=10-length
        st=st+(dif*" ")+" \t"
        return st

def merch_record_format(record):
    '''Format record for display'''
    k=record.keys()
    a=""
    for c in k:
        if c!='merch_Taxable':
            a=a+add_spaces(str(record[c]), str(c))
        elif c=='merch_Taxable':
            if (str(record[c]))=='0':
                a=a+"Tax Exempt"
            elif (str(record[c]))=='1':
                a=a+"Taxable"
    ui.show_message(a)

def event_record_format(record):
    '''Format record for display'''
    address = str(record['event_Street']+ ", " + record['event_City'] +", " + record['event_State'] + ", "+ record['event_Zip']+ " \t ")

    k=record.keys()
    a=""
    for n in k:
        if (n != "event_Street") & (n!="event_City")&(n!="event_State")&(n!="event_Zip"):
            a=a+add_spaces(str(record[n]), str(n))
        elif n == "event_Street":
            a=a+add_spaces(address, 'address')
    ui.show_message (a)


def event_sales_record_format(record, tax):
    '''Format record for display'''
    k=record.keys()
    #print (k)
    a=""
    #if len(tax)>0:
    #    t=float(tax[0])

    if len(k)>4:
        k=["event_ID", 'merch_ID', 'sales_Total', 'sales_Price']

    for c in k:
        a=a+add_spaces(str(record[c]), str(c))
    ui.show_message(a+add_spaces(tax,'sales_Tax'))

def inventory_record_format(k):
    '''Format record for display'''
    a=""
    col=['merch_ID','sold','iOrdered','iTotal']
    for c in k:
        a=a+add_spaces(str(c), str(col[k.index(c)]))
    ui.show_message(a)

def add_record():
    table=ui.get_table_input()
    if table=='merchandise':
        new_item()
    elif table=='events':
        new_event()
    elif table=='event_sales':
        new_event_sales()

