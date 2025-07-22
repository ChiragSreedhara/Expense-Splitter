from fastapi import FastAPI, HTTPException, Query, Body
from database import get_connection
from schemas import ExpenseCreate
from dbQueries import *
import logging #debug, remove later
import traceback #^


app = FastAPI()

#expense endpoints
@app.post("/expenses")
@app.post("/expenses")
def create_expense_endpoint(data: dict = Body(...)):
    try:
        group_id = data.get("group_id")  # Optional
        payer_id = data["payer_id"]
        amount = data["amount"]
        description = data.get("description", "")
        recipient_ids = data.get("recipient_ids", [])

        # Create the expense
        expense_id = create_expense(group_id, payer_id, amount, description)
        if expense_id is None:
            return {"error": "Failed to create expense"}

        # Add recipients
        for rid in recipient_ids:
            add_expense_recipient(expense_id, rid)

        return {"message": "Expense created", "expense_id": expense_id}
    except Exception as e:
        return {"error": str(e)}



@app.get("/expenses")
def get_expenses():
    try:
        expenses = get_all_expenses()
        return {"expenses": expenses}
    except Exception as e:
        return {"error": str(e)}




#group endpoints
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
        group_id INT,
        payer_id INT NOT NULL,
        amount DECIMAL(10, 2) NOT NULL,
        description VARCHAR(255),
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (group_id) REFERENCES `groups`(id),
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


