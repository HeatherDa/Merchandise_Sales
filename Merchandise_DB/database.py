import sqlite3
import traceback
from datetime import datetime

from Merchandise_DB import ui

db = sqlite3.connect('merchandising_db.db') #Creates db file or opens if it already exists
c = db.cursor()


def get_settings(v):
    record = c.execute('SELECT * FROM organizations')
    c.row_factory = sqlite3.Row
    for r in record:
        return r[v]


def create_items_table():
    """Create items table"""
    try:
        c.execute('CREATE TABLE if not exists items (item_ID integer primary key, item_Type text not null, '
                  'item_Description text not null, item_Taxable int)')
        c.execute('SELECT * FROM items')
        rec = c.fetchall()
        recs = [('T-Shirt', 'black, yellow logo', 0),
                ('T-Shirt', 'white, blue logo', 0),
                ('CD', 'Adajio',  1),
                ('CD', 'Fortisimo', 1),
                ('Poster', '2017 Holiday Band Photo', 1),
                ('Poster', 'Adajio cover', 1)]

        if len(rec) < 1:  #If table is empty, add data
            c.executemany('INSERT INTO items (item_Type, item_Description, item_Taxable) '
                          'VALUES (?, ?, ?)', recs)
            db.commit()  #save changes

    except sqlite3.Error:
        ui.show_message('An error occurred.')
        traceback.print_exc()

def new_item(type,description,taxable,*v): #v is 1 if expecting item_ID returned, else no return expected
    """Add new item to items table"""
    try:
        if taxable != 1:
            taxable = 0

        sql = 'INSERT INTO items (item_Type, item_Description, item_Taxable) VALUES(?,?,?)'
        c.execute(sql, (type, description, taxable))

        db.commit()  #save changes
        c.execute('SELECT last_insert_rowid()')
        a = c.fetchone()
        item_ID = a[0]
        if v[0]>0:
            return item_ID
        else:
            return

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
            sql = '''UPDATE items SET item_Type = ? WHERE item_ID = ?'''
            c.execute(sql, (updateData, item_ID,))
            db.commit()
            return
        elif choice == 2: #update description
            sql = '''UPDATE items SET item_Description = ? WHERE item_ID = ?'''
            c.execute(sql, (updateData, item_ID,))
            db.commit()
            return

    except sqlite3.Error:
        ui.show_message('An error occured while trying to update items table.  Changes will '
                        'be rolled back.')
        traceback.print_exc()
        db.rollback()

def get_from_items(item_ID, value):
    results=c.execute('SELECT * FROM items WHERE item_ID = ?', (item_ID,))
    c.row_factory=sqlite3.Row
    try:
        if value == 'all':
            for result in results:
                return result
        elif value == 'description':
            for result in results:
                return result['item_Description']
        elif value == 'type':
            for result in results:
                return result['item_Type']
        elif value == 'taxable':
            tax = 0
            for result in results:
                tax = result['item_Taxable']
            if tax == 1:
                return True
            else:
                return False
        else:
            raise MyError('option passed with no corresponding code')
    except sqlite3.Error:
        ui.show_message("An error occurred while searching for " + value + ".")
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
                  ('Concert', '2018-03-12 19:30:00', '523 Bolton Rd.', 'Fargo', 'ND', '59721',
                   'John Cobbler', '542-890-7231'),
                  ('Signing', '2018-04-15 14:30:00', '3030 Colton Way', 'New Olm', 'MN', '57382',
                   'Kaiser Tannenburg', '472-113-9157')]

        if len(rec) < 1:  # If table is empty, add data
            c.executemany('INSERT INTO events (event_Type, event_Date, event_Street, event_City, event_State, '
                          'event_Zip, event_Contact, event_Contact_Phone) VALUES (?,?,?,?,?,?,?,?)', events)
            db.commit()  # save changes

    except sqlite3.Error:
        ui.show_message('An error occurred.')
        traceback.print_exc()

def new_event(values):
    """Add new event to events table"""
    try:
        sql = 'INSERT INTO events (event_Type, event_Date, event_Street, event_City, event_State,event_Zip, ' \
              'event_Contact, event_Contact_Phone) VALUES (?,?,?,?,?,?,?,?)'
        c.execute(sql, (values))
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
        if choice == '1':
            sql = '''UPDATE events SET event_Type = ? WHERE event_ID = ?'''
            c.execute(sql, (updateData, event_ID, ))
            db.commit()
        elif choice == '2':
            sql = '''UPDATE events SET event_Date = ? WHERE event_ID = ?'''
            c.execute(sql, (updateData, event_ID, ))
            db.commit()
        elif choice == '3':
            sql = '''UPDATE events SET event_Street = ? WHERE event_ID = ?'''
            c.execute(sql, (updateData, event_ID, ))
            db.commit()
        elif choice == '4':
            sql = '''UPDATE events SET event_City = ? WHERE event_ID = ?'''
            c.execute(sql, (updateData, event_ID, ))
            db.commit()
        elif choice == '5':
            sql = '''UPDATE events SET event_State = ? WHERE event_ID = ?'''
            c.execute(sql, (updateData, event_ID, ))
            db.commit()
        elif choice == '6':
            sql = '''UPDATE events SET event_zip = ? WHERE event_ID = ?'''
            c.execute(sql, (updateData, event_ID, ))
            db.commit()
        elif choice == '7':
            sql = '''UPDATE events SET event_Contact = ? WHERE event_ID = ?'''
            c.execute(sql, (updateData, event_ID, ))
            db.commit()
        elif choice == '8':
            sql = '''UPDATE events SET event_Contact_Phone = ? WHERE event_ID = ?'''
            c.execute(sql, (updateData, event_ID, ))
            db.commit()
        else:
            raise MyError('Data passed to get from events for which there is no code written')
    except sqlite3.Error:
        ui.show_message('An error occured while trying to update events table.  Changes will be rolled back.')
        traceback.print_exc()
        db.rollback()


def get_from_events(event_ID, value):
    results = c.execute('SELECT * FROM events WHERE event_ID = ?', (event_ID, ))
    c.row_factory = sqlite3.Row
    try:
        if value == 'all':
            for result in results:
                return result
        elif value == 'date':
            for result in results:
                return result['event_Date']
        elif value == 'type':
            for result in results:
                return result['event_Type']
        elif value == 'street':
            for result in results:
                return result['event_Street']
        elif value == 'city':
            for result in results:
                return result['event_City']
        elif value == 'state':
            for result in results:
                return result['event_State']
        elif value == 'zip':
            for result in results:
                return result['event_Zip']
        elif value == 'contact':
            for result in results:
                return result['event_Contact']
        elif value == 'phone':
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
        sql = 'CREATE TABLE if not exists event_sales (event_ID integer not null, item_ID integer not null, ' \
              'sales_Total integer, sales_Price real not null, sales_Tax real, sales_Profit real DEFAULT 0, ' \
              'PRIMARY KEY (event_ID, item_ID) FOREIGN KEY (event_ID) REFERENCES events (event_ID), ' \
              'FOREIGN KEY (item_ID) REFERENCES items (item_ID))'
        c.execute(sql)

        c.execute('SELECT * FROM event_sales')
        rec = c.fetchall()
        sales = [(1, 1, 5, 10.00, 0, 0),
                 (1, 2, 4, 10.00, 0, 0),
                 (1, 3, 8, 10.00, 0, 0),
                 (1, 4, 2, 10.00, 0, 0),
                 (1, 5, 3, 8.00, 0, 0),
                 (1, 6, 1, 8.00, 0, 0)]


        if len(rec) < 1:  # If table is empty, add data
            c.executemany('INSERT INTO event_sales (event_ID, item_ID, sales_Total, sales_Price, sales_Tax, '
                          'sales_Profit) VALUES (?, ?, ?, ?, ?, ?)', sales)
            db.commit()  # save changes

        auto_update_inventory()

    except sqlite3.Error as e:
        ui.show_message('An error occurred.')
        traceback.print_exc()

def reInitialize_database():
    delete_table(1)
    create_tables()

def new_event_sales(values): #TODO Fix ME
    """Takes tupple with event_ID, item_ID, sales_Total, sales_Price and adds record to event_sales table if enough
    inventory exists to cover sales_Total"""
    try:
        sql = 'INSERT INTO event_sales (event_ID, item_ID, sales_Total, sales_Price) VALUES (?, ?, ?, ?)'
        if values[2] <= search_available_inventory_by_item(values[1]):
            c.execute(sql, values)
            db.commit()
            auto_update_inventory()
        else:
            ui.show_message("There is not enough inventory available to record this sale.")

    except sqlite3.IntegrityError:
        ui.show_message('wrong data type?  Changes will be rolled back.')
        traceback.print_exc()
        db.rollback()

    except sqlite3.Error:
        ui.show_message("An error occured while trying to add a new event_sales record.  Changes will be rolled back.")
        traceback.print_exc()
        db.rollback()

def update_event_sales(values): #choice,e_ID,i_ID,updateData, *updateData2):
    try:
        if values[0] == 1:
            sql = '''UPDATE event_sales SET sales_Total = ? WHERE event_ID = ? AND item_ID = ?'''
            c.execute(sql, (values[4], values[1], values[2], ))
            db.commit()
            #TODO: write method that will reverse changes to order_items that were made based on original numbers if total sold decreased
            #TODO: otherwise, update salesTax and salesProfit to reflect change
            #Maybe add record to another table each time an event_sales entry uses more than one order_items record.
            # This would be a one to one table with event_sales,
            # and would have event_ID, item_ID, "order_ID,order_ID,orderID..."
            # where each orderID in the string refers to the order_ID from which the 'cost' was used
        elif values[0] == '2':
            sql = '''UPDATE event_sales SET sales_Price=? WHERE event_ID=? AND item_ID=?'''
            c.execute(sql, (values[4], values[1], values[2], ))
            db.commit()
            #TODO: write a method to change calculated Profit and sales_Tax for this item when this value is changed
    except sqlite3.Error:
        ui.show_message('An error occured while trying to update event_sales table.  '
                        'Changes will be rolled back.')
        traceback.print_exc()
        db.rollback()

def get_from_event_sales(e_ID, i_ID, value):
    results = c.execute('SELECT * FROM event_sales WHERE event_ID = ? AND item_ID = ?', (e_ID, i_ID, ))
    c.row_factory = sqlite3.Row
    print(value)
    #value=value.strip()
    try:
        if value == 'all':
            for result in results:
                print(result['sales_Total'])
                return result
        elif value == 'total':
            for result in results:
                return result['sales_Total']
        elif value == 'price':
            for result in results:
                return result['sales_Price']
        elif value == 'sales_Tax':
            for result in results:
                return result['sales_Tax']
        elif value == 'sales_Profit':
            for result in results:
                return result['sales_Profit']
        else:
            raise MyError('value passed with no corresponding code')
    except sqlite3.Error:
        ui.show_message("An error occurred while searching for " + value + ".")
        traceback.print_exc()


def create_order_items_table():
    try:
        sql = 'create table if not exists order_items ' \
              '(order_ID integer not null, item_ID integer not null, ordered_Total integer not null, ' \
              'ordered_Cost real not null, ordered_Memo text DEFAULT " ", ordered_Remaining int, ' \
              'CONSTRAINT order_items PRIMARY KEY (order_ID, item_ID) FOREIGN KEY (order_ID) ' \
              'REFERENCES orders (order_ID), FOREIGN KEY (item_ID) REFERENCES items (item_ID))'
        c.execute(sql)
        db.commit()
        c.execute('SELECT * FROM order_items')
        rec = c.fetchall()
        ordered = [(1, 1, 50, 8.00, '5 percent off for bulk order', 50),
                   (1, 2, 75, 8.00, '5 percent off for bulk order', 75),
                   (1, 5, 14, 6.00, ' ', 14),
                   (1, 6, 13, 6.00, ' ', 13),
                   (2, 1, 15, 7.00, ' ', 15),
                   (2, 2, 10, 7.00, ' ', 10),
                   (2, 3, 80, 3.00, ' ', 80),
                   (2, 4, 70, 3.00, ' ', 70),
                   (3, 3, 20, 4.00, ' ', 20),
                   (3, 4, 25, 4.00, ' ', 25),
                   (3, 5, 40, 5.00, ' ', 40),
                   (3, 6, 40, 5.00, ' ', 40)]

        if len(rec) < 1:
            sql2 = 'INSERT INTO order_items ' \
                   '(order_ID, item_ID, ordered_Total, ordered_Cost, ordered_Memo, ordered_Remaining) ' \
                   'VALUES (?,?,?,?,?,?)'
            c.executemany(sql2, ordered)
            db.commit()
    except sqlite3.Error:
        ui.show_message('An error occurred while trying to create order_items table')
        traceback.print_exc()


# noinspection PyPep8Naming
def get_from_order_items(order_ID, item_ID, value):
    sql = 'SELECT * FROM order_items WHERE item_ID = ? AND order_ID = ? '
    values = (item_ID, order_ID, )
    rec = c.execute(sql, values)
    c.row_factory = sqlite3.Row
    for r in rec:
        if (value == 'all') | (value == 'all for cost'):
            return r
        elif value == 'total':
            return r[2]
        elif value == 'cost':
            return r[3]
        elif value == 'memo':
            return r[4]
        elif value == 'remaining':
            return r[5]


def update_order_items(values): #choice, order_ID, item_ID, value, *total
    if values[0] == 'total':
        sql = 'UPDATE order_items SET ordered_Total = ? WHERE order_ID = ? AND item_ID = ?'
        c.execute(sql, (values[3], values[1], values[2], ))
    elif values[0] == 'cost':
        sql = 'UPDATE order_items SET ordered_Cost = ? WHERE order_ID = ? AND item_ID = ?'
        c.execute(sql, (values[3], values[1], values[2], ))
    elif values[0] == 'note':
        sql = 'UPDATE order_items SET ordered_Memo = ? WHERE order_ID = ? AND item_ID = ?'
        c.execute(sql, (values[3], values[1], values[2], ))
    elif values[0] == 'remainder': #this change is allowed because inventory could be lost through breakage, defects, or theft
        sql = 'UPDATE order_items SET ordered_Remaining = ? WHERE order_ID = ? AND item_ID = ?'
        c.execute(sql, (values[3], values[1], values[2], ))


def receive_Order(items): #items is: [tuples for records to be added], order_ID, order_Date, 'many' or 'one'
    '''Add list of items from an order to database and update order to reflect date received'''
    sql = 'INSERT INTO order_items (order_ID, item_ID, ordered_Total, ordered_Cost, ordered_Memo, ordered_Remaining) ' \
          'VALUES(?, ?, ?, ?, ?, ?)'
    if items[3] == 'many':
        c.executemany(sql, items[0])
        db.commit()
    else:
        values = items[0]
        c.execute(sql, values)
    update_order('received', items[1], items[2])


def create_orders_table():
    try:
        sql = 'CREATE TABLE IF NOT EXISTS orders (order_ID integer primary key, vendor_ID integer not Null, ' \
              'order_Date DATETIME not Null, order_Received DATETIME DEFAULT NULL) '
        c.execute(sql)
        c.execute('SELECT * FROM orders')
        rec = c.fetchall()
        orders = [('1', '2018-01-01 10:30:00', '2018-01-10 14:00:00'),
                  ('2', '2018-01-01 11:00:00', '2018-01-15 9:00:00'),
                  ('3', '2018-01-05 23:15:00', '2018-01-15 9:00:00')]
        openOrder = ('1', '2018-02-01 12:30:00')
        if len(rec) < 1:
            c.executemany('INSERT INTO orders (vendor_ID, order_Date, order_Received) VALUES (?, ?, ?)', orders)
            db.commit()
            c.execute('INSERT INTO orders (vendor_ID, order_Date) VALUES (?, ?)', openOrder)
            db.commit()
    except sqlite3.Error:
        ui.show_message('An error occurred while trying to create orders table')
        traceback.print_exc()

def new_Order(vendor, ordered):
    sql = 'INSERT INTO orders (vendor_ID, order_Date) VALUES (?, ?)'
    c.execute(sql, (vendor, ordered, ))
    db.commit()


def update_order(choice, order_ID, value):
    if choice == 'received':
        sql = 'UPDATE orders SET order_Received=? WHERE order_ID=?'
        c.execute(sql, (value, order_ID))
        db.commit()
    elif choice == 'ordered':
        sql = 'UPDATE orders SET order_Date = ? WHERE order_ID = ?'
        c.execute(sql, (value, order_ID))
        db.commit()


def get_from_orders(order_ID, value):
    sql = 'SELECT * FROM orders WHERE order_ID = ?'
    records = c.execute(sql, (order_ID, ))
    c.row_factory = sqlite3.Row
    for row in records:
        if value == 'all':
            return row
        else:
            return row[value]


def create_organization_table():
    #The point of this is to store state and sales tax information in the database so it can be updated if necessary
    try:
        c.execute('create table if not exists organizations (org_ID integer primary key, state, salesTaxPercent)')
        c.execute('SELECT * FROM organizations')
        rec = c.fetchall()
        org = [('MN', 7.375)]
        if len(rec) < 1:
            c.executemany('INSERT INTO organizations (state, salesTaxPercent) VALUES (?, ?)', org)
            db.commit()
    except sqlite3.Error:
        ui.show_message('An error occurred while trying to create organizations table')
        traceback.print_exc()


def change_settings(sta, tax): #Assumes this table only has one record
    try:
        sql = 'UPDATE organizations SET state = ? AND salesTaxPercent = ?'
        c.execute(sql, (sta, tax))
    except sqlite3.Error:
        ui.show_message('An error occurred while trying to update organizations table')


def drop_settings():
    c.execute('DROP TABLE IF EXISTS organization') #Delete table
    db.commit()


def delete_record(values): #values [table name, id1, id2]
    """Delete a record from the database by ID"""
    t = values[0]
    id1 = values[1]
    try:
        if t == 'items':
            sql = 'SELECT DISTINCT item_ID FROM event_sales WHERE item_ID = ?'
            sql2 = 'SELECT DISTINCT item_ID FROM order_items WHERE item_ID = ?'
            results1 = c.execute(sql, (id1, ))
            results2 = c.execute(sql2, (id1, ))
            c.row_factory = sqlite3.Row
            count = 0
            for result in results1:
                count += 1
            for result in results2:
                count += 1
            if count > 0:
                return 'Cannot delete that record, as it is in use in another table.'
            else:
                sql = '''DELETE FROM items WHERE item_ID = ?'''
                c.execute(sql, (id1, ))
                db.commit()
                return "Record Deleted"
        elif t == 'events':
            results = c.execute('SELECT DISTINCT event_ID * FROM event_sales WHERE event_ID = ?', (id1, ))
            c.row_factory = sqlite3.Row
            count = 0
            for result in results:
                count = count + 1
            if count > 0:
                return 'Cannot delete that record, as it is in use in another table.'
            else:
                sql = '''DELETE FROM events WHERE event_ID = ?'''
                c.execute(sql, (id1, ))
                db.commit()
                return "Record Deleted"
        elif t == 'orders':
            results = c.execute('SELECT DISTINCT order_ID * FROM order_items WHERE order_ID = ?', (id1, ))
            count = 0
            for result in results:
                count +=1
            if count > 0:
                return 'Cannot delete that record, as it is in use in another table.'
            else:
                sql = 'DELETE FROM orders WHERE order_ID = ?'
                c.execute(sql, (id1, ))
                db.commit()
                return 'Record Deleted'
        elif t == 'event_sales':
            if is_ID('event_sales', id1, values[2]):
                sql = '''DELETE FROM event_sales WHERE event_ID = ? AND item_ID = ?'''
                c.execute(sql, (id1, values[3], ))
                db.commit()
                return "Record Deleted"
            else:
                return 'That event_ID, item_ID combination was not found in the table.'
        elif t == 'order_items':
            if is_ID('order_items', id1, values[2]):
                sql = 'DELETE FROM order_items WHERE order_ID = ? AND item_ID = ?'
                c.execute(sql, (id1, values[3], ))
                db.commit()
                return 'Record Deleted'
            else:
                return 'That order_ID item_ID combination was not found in the table.'
    except sqlite3.Error:
        db.rollback()
        return 'An error occurred.  Record could not be deleted.  Changes will be rolled back.', traceback.print_exc()


def search_by_type(v): #v=[table, type]
    """search items or events by type"""
    table = v[0]
    ty = v[1]
    typeName = table[:-1] + '_Type'
    sql = 'SELECT * FROM ' + table + ' WHERE ' + typeName + ' = ? ORDER BY ' + typeName
    records = c.execute(sql, (ty, ))
    c.row_factory = sqlite3.Row
    r = []
    for rec in records:
        r.append(rec)
    return r


def avg_profit(values):
    """takes values=[choice, ch, *d1, *d2] and returns list of rows that are above or below average"""
    sql = 'SELECT * ' \
          'FROM event_sales '
    count = 0
    total_ppitem = 0
    results_Big = []
    results_Small = []
    avg_ppitem = 0.00
    if values[1] == 1:#average over all
        records = c.execute(sql)
        c.row_factory = sqlite3.Row
        for r in records:
            total_ppitem += ((r['sales_Profit'] + r['sales_Tax']) / r['sales_Total'])
            count += 1
        avg_ppitem = total_ppitem/count
        for rec in records:
            ppitem = ((rec['sales_Profit'] + rec['sales_Tax']) / rec['sales_Total'])
            if ppitem > avg_ppitem:
                result = (rec['item_ID'], ppitem)
                results_Big.append(result)
            elif ppitem < avg_ppitem:
                result = (rec['item_ID'], ppitem)
                results_Small.append(result)

    elif values[1] == 2:#average over specific time period
        sql = sql + 'INNER JOIN events ON events.event_ID=event_sales.event_ID WHERE event_Date BETWEEN ? AND ?'
        d1 = values[2]
        d2 = values[3]
        records = c.execute(sql, (d1, d2))
        c.row_factory = sqlite3.Row
        for r in records:
            total_ppitem += ((r['sales_Profit'] + r['sales_Tax']) / r['sales_Total'])
            count += 1
        avg_ppitem = total_ppitem / count
        for rec in records:
            ppitem = ((rec['sales_Profit'] + rec['sales_Tax']) / rec['sales_Total'])
            if ppitem > avg_ppitem:
                result = (rec['item_ID'], ppitem)
                results_Big.append(result)
            elif ppitem < avg_ppitem:
                result = (rec['item_ID'], ppitem)
                results_Small.append(result)

    if values[0] == 1:  # return above avg profit
        return (results_Big, avg_ppitem)
    elif values[0] == 2:#return below avg profit
        return (results_Small, avg_ppitem)


def search_by_date(choice, *day):
    """Sort by date or get event by date"""
    if choice == 1:
        d = day[0]
        records=c.execute('SELECT * FROM events WHERE event_Date = ? ORDER BY event_Date ASC',(d,))
        c.row_factory = sqlite3.Row
        r=[]
        for rec in records:
            r.append(rec)
        return r

    elif choice == 2:
        d=datetime.today()
        records=c.execute('SELECT * FROM events WHERE event_Date >= ? ORDER BY event_Date ASC',(d,))
        c.row_factory = sqlite3.Row
        r = []
        for rec in records:
            r.append(rec)
        return r




def search_by_on_hand_ui(): #TODO Fix ME
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






def search_by_salesTax_due(): #TODO Fix ME
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


def get_order_items_by_itemID(item_ID):
    sql2 = 'SELECT *' \
           'FROM order_items' \
           'INNER JOIN orders ON orders.order_ID=order_items.order_ID' \
           'WHERE item_ID=? AND ordered_Remaining > 0' \
           'ORDER BY: order_Received ASC'
    records = c.execute(sql2, (item_ID))
    c.row_factory = sqlite3.Row
    r=[]
    for record in records:
        r.append(record)
    return r


def search_by_profit(choice,*item_ID): #choice 4 handled separately
    """Take type of search and optional item ID, return various search results"""
    if choice == 1:
        #profit for a given item
        #Couldn't figure out how to do this as one query
        sql = 'SELECT items.item_ID, item_Type, item_Description, SUM(event_sales.sales_Profit) ' \
              'FROM event_sales ' \
              'INNER JOIN items ON items.item_ID=event_sales.item_ID ' \
              'WHERE items.item_ID=? '
        item_ID=item_ID[0]
        records = c.execute(sql, (item_ID,))
        c.row_factory = sqlite3.Row
        r = []
        for record in records:
            r.append(record)
        return r

    elif choice == 2:
        #profit for each item
        sql = 'SELECT items.item_ID, item_Type, item_Description, SUM(event_sales.sales_Profit) ' \
              'FROM event_sales ' \
              'INNER JOIN items ON items.item_ID=event_sales.item_ID ' \
              'GROUP BY items.item_ID, item_Type, item_Description'
        records = c.execute(sql)
        c.row_factory = sqlite3.Row
        r = []
        for record in records:
            r.append(record)
        return r

    elif choice == 3:
        #total profit so far this year
        current_year = datetime.today().strftime("%Y")
        year_begin = current_year + '-01-01 00:00:00'
        year_begin = datetime.strptime(year_begin, "%Y-%m-%d %H:%M:%S")
        sql = 'SELECT SUM(sales_Profit) ' \
              'FROM event_sales ' \
              'INNER JOIN events ON event_sales.event_ID=events.event_ID ' \
              'WHERE events.event_Date > ? '
        records=c.execute(sql,(year_begin,))
        c.row_factory = sqlite3.Row
        r = []
        for record in records:
            r.append(record)
        return r

    elif choice ==5:
        #total profits per event
        sql = 'SELECT events.event_ID, SUM(sales_Profit) ' \
              'FROM event_sales ' \
              'INNER JOIN events ON events.event_ID=event_sales.event_ID ' \
              'GROUP BY events.event_ID'
        records = c.execute(sql)
        c.row_factory = sqlite3.Row
        r = []
        for record in records:
            r.append(record)
        return r


def is_taxable(e_id, i_id):
    state=get_settings('state')
    if (get_from_events(e_id, 'state')==state)&(get_from_items(i_id,'taxable')):
        return True
    else:
        return False


def view_table(name):
    """Return all records from a given table"""
    try:
        sql = 'SELECT * FROM '+name
        records = c.execute(sql)
        c.row_factory = sqlite3.Row  # so that you can access columns by name
        r = []
        for record in records:
            r.append(record)
        return r

    except sqlite3.Error:
        raise MyError('Something went wrong when trying to display the table',traceback.print_exc())


def is_ID(table, id1 , *id2):
    """Searches given table for incidence of given id.  returns True if found, otherwise False."""
    #Has unit test
    try:
        if table == "items":
            result = get_from_items(id1, 'all')
            if result is not None:
                return True
            else:
                return False
        elif table == "events":
            result = get_from_events(id1, 'date')
            if result is not None:
                return True
            else:
                return False
        elif table == "event_sales":
            i_id = id2[0] #For some reason, the optional value is a tuple. This gets the value from it.
            result = get_from_event_sales(id1, i_id, 'all')
            if result is not None:
                return True
            else:
                return False
        elif table == 'orders':
            result = get_from_orders(id1, 'all')

            if result is not None:
                return True
            else:
                return False
        elif table == 'order_items':
            #c.execute('SELECT * FROM order_items WHERE order_ID=? AND item_ID=?')
            i_id = id2[0]#For some reason, the optional value is a tuple. This gets the value from it.
            result = get_from_order_items(id1, i_id, 'all')
            if result is not None:
                return True
            else:
                return False

    except sqlite3.Error:
        ui.show_message("An error occurred while searching for ID")
        raise MyError('An error occured while searching for ID',traceback.print_exc())


def get_types(table):
    print (table)
    try:
        if table == 'items':
            records = c.execute('SELECT DISTINCT item_Type FROM items')
            c.row_factory = sqlite3.Row
            types = []
            for record in records:
                types.append(record['item_Type'])
            return types
        elif table == 'events':
            records = c.execute('SELECT DISTINCT event_Type FROM events')
            c.row_factory = sqlite3.Row
            types = []
            for record in records:
                types.append(record['event_Type'])
            return types
        else:
            raise MyError('Table does not have type column or table does not exist')
    except sqlite3.Error:
        ui.show_message('An error occured while trying to get types')


def salesTax(price, total):
    """Sales tax owed using home state set in user settings"""
    percent = get_settings('salesTaxPercent')
    if ui.is_Float(percent):
        percent = float(percent)
        return ((price * percent) / 100) * total #percent is global set from database (for MN, percent should be 7.375)
    else:
        ui.show_message('percent must be a float')
        return



def close_database():
    db.close()



def create_tables():
    create_items_table()
    create_organization_table()
    create_orders_table()
    create_events_table()
    create_order_items_table()
    create_event_sales_table()

def delete_table(*table):
    """Used to delete a table.  Only intended for debugging use."""
    '''Have not made and will not make unit test for this.  It is only used for debugging and I don't want to write a 
       function to feed it the name of the table to delete.'''
    try:
        if table is None:
            name = ui.get_table_input()
            if name == 0:
                return
            else:
                c.execute('DROP TABLE IF EXISTS ' + name) #Delete table
                db.commit() #save changes
        else:
            tables = ('items', 'events', 'orders', 'order_items', 'event_sales', 'organizations')
            for table in tables:
                c.execute('DROP TABLE IF EXISTS ' + table)
                db.commit()

    except sqlite3.Error as e:
        ui.show_message('An error occurred.  Changes will be rolled back.')
        traceback.print_exc()
        db.rollback()


class MyError(Exception):
    """ Custom exception class """
    pass


def search_available_inventory_by_item(item):
    sql = 'SELECT items.item_ID, SUM(ordered_Remaining) ' \
          'FROM order_items ' \
          'INNER JOIN items ON items.item_ID=order_items.item_ID ' \
          'WHERE items.item_ID=?' \
          'GROUP BY items.item_ID'
    records = c.execute(sql, (item, ))
    c.row_factory = sqlite3.Row
    r = []
    for record in records:
        r.append(record)
    #display_records(r)
    return r


def search_order_items_by_item(item):
    #item=input('What item Id? ')
    sql = 'SELECT * ' \
          'FROM order_items ' \
          'WHERE item_ID=?'
    records = c.execute(sql, (item,))
    c.row_factory = sqlite3.Row
    r = []
    for record in records:
        r.append(record)
    #display_records(r)
    return r


def auto_update_inventory():
    sql = 'SELECT * ' \
          'FROM event_sales ' \
          'WHERE sales_Profit= 0'
    records = c.execute(sql)
    c.row_factory = sqlite3.Row
    r = []
    for record in records:
        r.append(record)
    #display_records(r)
    for item in r:
        item_ID = item['item_ID']
        a = search_available_inventory_by_item(item_ID)
        available_inventory = a[0][1]
        applicable_order_items = search_order_items_by_item(item_ID)
        #taxable=is_taxable()
        sale_Tax = 0.00
        if is_taxable(item['event_ID'], item['item_ID']):
            sale_Tax = salesTax(item['sales_Price'], item['sales_Total'])

        if available_inventory >= item['sales_Total']: #Enough inventory on hand for sale
            profit = 0
            total = item['sales_Total']
            while total != 0:
                for record in applicable_order_items:
                    # if there is enough in the first order to cover the amount sold
                    if record['ordered_Remaining'] >= item['sales_Total']:

                        if item['sales_Total'] == total:
                            ppitem = item['sales_Price'] - record['ordered_Cost']
                            profit = (ppitem * item['sales_Total']) - sale_Tax
                            remain = record['ordered_Remaining'] - item['sales_Total']
                            aupdate_order_items(record['order_ID'], record['item_ID'], remain)
                            aupdate_event_sales(item['event_ID'], item_ID, sale_Tax, profit)
                            total = 0
                            break

                        elif item['sales_Total'] != total:
                            ppitem = item['sales_Price'] - record['ordered_Cost']
                            profit = profit + (ppitem*total) - sale_Tax
                            remain = record['ordered_Remaining'] - total
                            aupdate_order_items(record['order_ID'], record['item_ID'], remain)
                            aupdate_event_sales(item['event_ID'], item_ID, sale_Tax, profit)
                            total = 0
                            break
                    # if more than one record is used to cover the amount sold
                    elif record['ordered_Remaining'] < item['sales_Total']:
                        for record in applicable_order_items:
                            ppitem = item['sales_Price'] - record['ordered_Cost']
                            profit = profit + (ppitem * record['ordered_Remaining'])
                            aupdate_order_items(record['order_ID'], record['item_ID'], 0)
                            total = total - record['ordered_Remaining']
        else:
            message='There is not enough inventory available to record this transaction.\n' \
                    'Check sales_Total in event_sales table for event_ID'\
                    + str(item['event_ID']) + ', item_ID' + str(item['item_ID']) + ' and try again.'
            ui.show_message(message)
            return


def aupdate_order_items(orderID, itemID, remain):
    """run automatically by auto_update_inventory"""
    sql = 'UPDATE order_items ' \
          'SET ordered_Remaining = ? ' \
          'WHERE order_ID = ? AND item_ID = ? '
    c.execute(sql, (remain, orderID, itemID, ))
    db.commit()


def aupdate_event_sales(eventID, itemID, sale_Tax, profit):
    """run automatically by auto_update_inventory"""
    sql = 'UPDATE event_sales ' \
          'SET sales_Tax = ?, sales_Profit = ? ' \
          'WHERE event_ID = ? AND item_ID = ? '
    c.execute(sql, (sale_Tax, profit, eventID, itemID, ))
    db.commit()
