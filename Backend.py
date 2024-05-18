import mysql.connector


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="nkk789390",
    database="2100031393_backend"
)


mycursor = mydb.cursor()


mycursor.execute("SELECT * FROM Customers")
customers = mycursor.fetchall()
print("List of all customers:")
for customer in customers:
    print(customer)


mycursor.execute("SELECT * FROM Orders WHERE OrderDate BETWEEN '2023-01-01' AND '2023-01-31'")
january_orders = mycursor.fetchall()
print("\nOrders placed in January 2023:")
for order in january_orders:
    print(order)


mycursor.execute("""
    SELECT o.OrderID, o.OrderDate, CONCAT(c.FirstName, ' ', c.LastName) AS CustomerName, c.Email
    FROM Orders o
    JOIN Customers c ON o.CustomerID = c.CustomerID
""")
order_details = mycursor.fetchall()
print("\nDetails of each order (including customer name and email):")
for order in order_details:
    print(order)


mycursor.execute("""
    SELECT p.ProductName, oi.Quantity
    FROM OrderItems oi
    JOIN Products p ON oi.ProductID = p.ProductID
    WHERE oi.OrderID = 1
""")
order_products = mycursor.fetchall()
print("\nProducts purchased in OrderID 1:")
for product in order_products:
    print(product)


mycursor.execute("""
    SELECT c.CustomerID, CONCAT(c.FirstName, ' ', c.LastName) AS CustomerName, c.Email, SUM(p.Price * oi.Quantity) AS TotalSpent
    FROM Customers c
    JOIN Orders o ON c.CustomerID = o.CustomerID
    JOIN OrderItems oi ON o.OrderID = oi.OrderID
    JOIN Products p ON oi.ProductID = p.ProductID
    GROUP BY c.CustomerID, CustomerName, c.Email;
""")
customer_spending = mycursor.fetchall()
print("\nTotal amount spent by each customer:")
for spending in customer_spending:
    print(spending)


mycursor.execute("""
    SELECT p.ProductName, SUM(oi.Quantity) AS TotalOrdered
    FROM OrderItems oi
    JOIN Products p ON oi.ProductID = p.ProductID
    GROUP BY p.ProductName
    ORDER BY TotalOrdered DESC
    LIMIT 1
""")
most_popular_product = mycursor.fetchone()
print("\nThe most popular product:")
print(most_popular_product)


mycursor.execute("""
    SELECT 
        DATE_FORMAT(o.OrderDate, '%Y-%m') AS Month,
        COUNT(o.OrderID) AS TotalOrders,
        SUM(p.Price * oi.Quantity) AS TotalSalesAmount
    FROM Orders o
    JOIN OrderItems oi ON o.OrderID = oi.OrderID
    JOIN Products p ON oi.ProductID = p.ProductID
    WHERE o.OrderDate BETWEEN '2023-01-01' AND '2023-12-31'
    GROUP BY DATE_FORMAT(o.OrderDate, '%Y-%m')
""")
monthly_sales = mycursor.fetchall()
print("\nTotal number of orders and total sales amount for each month in 2023:")
for sales in monthly_sales:
    print(sales)


mycursor.execute("""
    SELECT c.CustomerID, CONCAT(c.FirstName, ' ', c.LastName) AS CustomerName, c.Email, SUM(p.Price * oi.Quantity) AS TotalSpent
    FROM Customers c
    JOIN Orders o ON c.CustomerID = o.CustomerID
    JOIN OrderItems oi ON o.OrderID = oi.OrderID
    JOIN Products p ON oi.ProductID = p.ProductID
    GROUP BY c.CustomerID, CustomerName, c.Email
    HAVING TotalSpent > 1000
""")
big_spenders = mycursor.fetchall()
print("\nCustomers who have spent more than $1000:")
for spender in big_spenders:
    print(spender)


mycursor.close()
mydb.close()