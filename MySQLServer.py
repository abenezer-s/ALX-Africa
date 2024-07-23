import mysql.connector
try:
    mydb = mysql.connector.connect(
        host = 'localhost',
        user = 'alx_db_user',
        passwd = 'password',
        collation = 'utf8mb4_general_ci'
    )
except mysql.connector.Error:
    raise Exception("could not connect to DB")

cursor = mydb.cursor()
try:
    cursor.execute("CREATE DATABASE IF NOT EXISTS alx_book_store")
    print('Database alx_book_store created successfully!')
except:
    raise Exception("coudln't create DB") 