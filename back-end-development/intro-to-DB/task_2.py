import mysql.connector
try:
    mydb = mysql.connector.connect(
        host = 'localhost',
        user = 'alx_db_user',
        passwd = 'password',
        collation = 'utf8mb4_general_ci',
        database = 'alx_book_store'
    )

except mysql.connector.Error:
    raise Exception("could not connect to DB")

cursor = mydb.cursor()
try:
    cursor.execute("CREATE DATABASE IF NOT EXISTS alx_book_store")
    print('Database alx_book_store created successfully!')
except:
    raise Exception("coudln't create DB") 

cursor.execute("""
    CREATE TABLE Boooks (
    book_id INT PRIMARY KEY,
    title VARCHAR(130),
    author_id INT,
    price DOUBLE,
    publication_date DATE,
    FOREIGN KEY (author_id) REFERENCES Authors(author_id)
    )
""")

cursor.execute("""
    CREATE TABLE Authors (
    author_id INT PRIMARY KEY,
    author_name VARCHAR(215)
)
""")
cursor.execute("""
CREATE TABLE Customers (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(215),
    email VARCHAR(215),
    address TEXT
) """)


cursor.execute(""" 
CREATE TABLE Orders ( 
    order_id INT PRIMARY KEY,
    customer_id INT,
    order_date DATE,
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
)""")


cursor.execute(""" 
CREATE TABLE Order_Details (
    orderdetailid INT PRIMARY KEY,
    order_id INT,
    book_id INT,
    quantity DOUBLE,
    FOREIGN KEY (order_id) REFERENCES Orders(order_id),
    FOREIGN KEY (book_id) REFERENCES Books(book_id)
)""")

