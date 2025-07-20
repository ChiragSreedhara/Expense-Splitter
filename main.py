from fastapi import FastAPI, HTTPException, Query, Body
from database import get_connection
from schemas import ExpenseCreate
from dbQueries import create_group, add_user_to_group
import logging #debug, remove later
import traceback #^


app = FastAPI()

@app.post("/expense")
def create_expense(expense: ExpenseCreate):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        query = "INSERT INTO expenses (user_id, amount, description) VALUES (%s, %s, %s)"
        cursor.execute(query, (expense.user_id, expense.amount, expense.description))
        conn.commit()
        return {"message": "Expense created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()


@app.get("/expenses")
def get_expenses(user_id: int = Query(..., description="User ID to fetch expenses for")):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, user_id, amount, description FROM expenses WHERE user_id = %s", (user_id,))
        results = cursor.fetchall()
        expenses = [
            {"id": row[0], "user_id": row[1], "amount": float(row[2]), "description": row[3]} for row in results
        ]
        return expenses
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@app.post("/groups")
def create_new_group(data: dict = Body(...)):
    try:
        group_name = data["name"]
        user_ids = data.get("user_ids", [])

        #creates group AND gets group_id
        group_id = create_group(group_name)  

        # Add users to group
        for uid in user_ids:
            add_user_to_group(uid, group_id)

        return {"message": "Group created", "group_id": group_id}

    except Exception as e:
        traceback.print_exc()
        return {"error": str(e)}
    






#temp debug endpoints,remove later
from dbQueries import run_raw_sql
@app.get("/debug/groups")#displays all groups
def debug_groups():
    rows = run_raw_sql("SELECT * FROM `groups`")
    return {"groups": rows}
@app.post("/debug/reset-db")
def reset_db():
    sql = """
    DROP TABLE IF EXISTS expense_recipients;
    DROP TABLE IF EXISTS expenses;
    DROP TABLE IF EXISTS group_members;
    DROP TABLE IF EXISTS `groups`;

    CREATE TABLE `groups` (
        id INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(255) NOT NULL
    );

    CREATE TABLE group_members (
        group_id INT,
        user_id INT,
        PRIMARY KEY (group_id, user_id),
        FOREIGN KEY (group_id) REFERENCES groups(id),
        FOREIGN KEY (user_id) REFERENCES users(id)
    );

    CREATE TABLE expenses (
        id INT PRIMARY KEY AUTO_INCREMENT,
        group_id INT NOT NULL,
        payer_id INT NOT NULL,
        amount DECIMAL(10, 2) NOT NULL,
        description VARCHAR(255),
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (group_id) REFERENCES groups(id),
        FOREIGN KEY (payer_id) REFERENCES users(id)
    );

    CREATE TABLE expense_recipients (
        expense_id INT NOT NULL,
        user_id INT NOT NULL,
        amount_owed DECIMAL(10, 2) NOT NULL,
        PRIMARY KEY (expense_id, user_id),
        FOREIGN KEY (expense_id) REFERENCES expenses(id) ON DELETE CASCADE,
        FOREIGN KEY (user_id) REFERENCES users(id)
    );
    """
    run_raw_sql(sql)
    return {"message": "Database reset and recreated"}


