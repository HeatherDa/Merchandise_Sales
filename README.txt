# Merchandise Sales
> Database to track merchandise for sale at events

Features include:
*Track sales of specific items at given event
*Calculate profit on each item for each event
*Track sales tax collected / owed to state
*Track data regarding different events
*Track total sales to date for each category
*Alert user if total remaining inventory for a given category drops below a given amount

DB structure:

merchandise table:
merch_ID: primary key, autoincremented int
merch_Type: text, type of object (T-Shirt, CD, Poster) #Should do something to track different sizes of T-Shirts sold...
merch_Description: text, used to clarify which of several T-Shirts is being described
merch_Total_Ordered: int, total of given item ordered to date #Should really have another value of recieved, so we know how many we've gotten of those that were ordered
merch_Cost: float, how much each item cost when purchased(what should we do if price changes? Make a new item, with description saying 2nd run?)
??merch_Taxable: int (0 or 1 for False or True) could include this (would make program more robust)

event table:
event_ID: primary key, autoincremented int
event_Type: text, type of event (Concert, Signing)
event_Date: text, date event will occur (check how to designate that it is a date and use date and time functions to sort it if necessary)
event_Street: text, street address
event_State:
event_Zip:
event_Contact_Name:
event_Contact_Phone:

event_sales table:
event_ID & merch_ID: combined primary key
sales_Total: int, how many of the merchID item were sold at this event
sales_Price: float, how much was it sold for at that event (price could change due to special discounts or something)
sales_Tax: float, how much sales tax collected? (only collect in home state) Assumes homestate is MN

menu:
1. Show table
    1. merchandise table
    2. event table
    3. event_sales table
2. Update table
    1. merchandise table
        get id of record to change
    2. event table
        get id of record to change
    3. event_sales table
        get item id and event id of record to change
3. Add record
    1. add to merchandise table
        get new information
    2. add to event table
        get new information
    3. add to event_sales table
        get new information
4. Delete record
    1. delete record from merchandise table
        get id of record to delete
    2. delete record from update event table
        get id of record to delete
    3. delete record from update event_sales table
        get item ID and event ID to delete
5. Search
    1. Search for a record by ID
    2. Search for a record by Type
    3. Search for Events by Date
        1. search by exact date
        2. search by month
        3. search by year
    4. Search for Merchandise items
        1.
        2. Current Stock Query
            1. ask about a speicific item
                get item id
            2. ask about items whose current stock is bellow a certain quantity
                get quantity
    5. Sales Tax Query (returns how much sales tax is owed by the band for merchandise sales since the beginning of the year.)
        SUM of sales tax column in event sales table
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

        2. view profit for each item
            SELECT merchandise.merch_ID, merch_Type, merch_Description, SUM(((merch_Price-sales_Cost)*sales_Total)-sales_Tax) AS profit
            FROM event_sales
            INNER JOIN merchandise ON merchandise.merch_ID=event_sales.merch_ID
            GROUP BY
            merchandise.merch_ID
            Order by
            profit ASC
        3. Total profit
            SELECT SUM(((merch_Price-sales_Cost)*sales_Total)-sales_Tax) AS profit
            FROM event_sales
            INNER JOIN merchandise ON merchandise.merch_ID=event_sales.merch_ID
            Order by profit ASC

7. Quit


End cases:
What if some items are stolen?