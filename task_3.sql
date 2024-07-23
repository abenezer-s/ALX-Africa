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

cursor.execute("""
    SHOW TABLES
""")