# Merchandise Sales
> Database to track merchandise for sale at events

Features include:
*Track sales and profit for each item sold at each event
*Track sales tax collected / owed to state
*Track data regarding different events
*Track total sales to date for each type of item or event
*Alert user if total remaining inventory for a given category drops below a given amount

DB structure:

items table:
item_ID: primary key, autoincremented int
item_Type: text, type of object (T-Shirt, CD, Poster) #Should do something to track different sizes of T-Shirts sold...
item_Description: text, used to clarify which of several T-Shirts is being described
item_Taxable: int (0 or 1 for False or True) could include this (would make program more robust)

event table:
event_ID: primary key, autoincremented int
event_Type: text, type of event (Concert, Signing)
event_Date: text, date event will occur (check how to designate that it is a date and use date and time functions to sort it if necessary)
event_Street: text, street address
event_State: text, state code
event_Zip: text, 5 digit number
event_Contact_Name: text, name
event_Contact_Phone: text, phone number, seperated with -

orders table:
order_ID: primary key, autoincremented int
vendor_ID: integer foreign key to table that doesn't exist yet.  Could add later
order_Date: Date, date order was placed
order_Received: Date, date order was received. Automatically updated when order_items with that order_ID are added.

event_sales table:
event_ID & merch_ID: combined primary key
sales_Total: int, how many of the merchID item were sold at this event
sales_Price: float, how much was it sold for at that event (price could change due to special discounts or something)
sales_Tax: float, sales tax collected at event for this item.
sales_Profit: float, profit on this item for this event ((sales_Price-ordered_Cost)*sales_Total)-sales_Tax.
    sales_Tax and sales_Profit are calculated and updated automatically after other values have been added, but can be updated later.

order_items table:
order_ID & item_ID: combined primary key
ordered_Total: int, total of given item ordered
ordered_Cost: float, how much each item cost
ordered_Memo: note about purchase, such as discount
ordered_Remaining: how many items still in inventory from this order.  Automatically updated when event_sales records are added


menu:
1. Show table
2. Update table
3. Add record
4. Delete record
5. Search
    1. Search for a record by ID
    2. Search for records by Type
    3. Search for Event by Date
        1. search by exact date
        2. search by month
        3. search by year
    4. Search for Items
        1.
        2. Current Stock Query
            1. get current stock for an item
            2. get items whose current stock is bellow a certain quantity
    5. Sales Tax Query (returns how much sales tax is owed by the band for merchandise sales since the beginning of the year.)
        1. get sales tax due for current year to date
        2. get sales tax due for some other period of time, using provided dates
    6. Profit Query
        1. get items with above average profit margin
            SELECT merchandise.merch_ID, merch_Type, merch_Description, SUM(((merch_Price-sales_Cost)*sales_Total)-sales_Tax) AS actual_profit, AVG(((merch_Price-sales_Cost)*sales_Total)-sales_Tax) AS average_profit
            FROM event_sales
            INNER JOIN merchandise ON merchandise.merch_ID=event_sales.merch_ID
            WHERE SUM(((merch_Price-sales_Cost)*sales_Total)-sales_Tax)>(Select AVG(((merch_Price-sales_Cost)*sales_Total)-sales_Tax)FROM event_sales INNER JOIN merchandise on merchandise.merch_ID=event_sales.merch_ID)
            GROUP BY
            merchandise.merch_ID
            Having
            actual_profit>average_profit
            Order by
            profit ASC;
        2. view total profit for each item
        3. Total profit
            1. year to date
            2. period of time between two dates

7. Quit


End cases:
What if some items are stolen?