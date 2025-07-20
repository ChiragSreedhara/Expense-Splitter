import os
from dotenv import load_dotenv
import pymysql

load_dotenv()  # loads .env file variables into environment

def get_connection():
    return pymysql.connect(
        host=os.getenv('DB_HOST'),
        port=int(os.getenv('DB_PORT')),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )

# connection = get_connection()
# with connection.cursor() as cursor:
#     cursor.execute("DESCRIBE users;")
#     for row in cursor.fetchall():
#         print(row)

# try:
#     with connection.cursor() as cursor:
#         cursor.execute("INSERT INTO users (id, username) VALUES (1, 'Test User')")
#     connection.commit()
#     print("Test user inserted successfully.")
# except Exception as e:
#     print("Error inserting test user:", e)
# finally:
#     connection.close()

