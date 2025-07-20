from fastapi import FastAPI
from database import get_connection

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Expense Splitter API is up and running!"}

@app.get("/databases")
def list_databases():
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SHOW DATABASES;")
        dbs = cursor.fetchall()
    conn.close()
    return {"databases": [db[0] for db in dbs]}
