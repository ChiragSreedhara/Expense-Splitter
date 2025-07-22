from database import get_connection

#expense logic
def create_expense(group_id, payer_id, amount, description):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # If group_id is falsy (None, 0, ''), store NULL in DB
        group_id_sql = group_id if group_id else None
        cursor.execute("""
            INSERT INTO expenses (group_id, payer_id, amount, description)
            VALUES (%s, %s, %s, %s)
        """, (group_id_sql, payer_id, amount, description))
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        print(f"Error creating expense: {e}")
        conn.rollback()
        return None
    finally:
        cursor.close()
        conn.close()



def add_expense_recipient(expense_id, user_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO expense_recipients (expense_id, user_id) VALUES (%s, %s)",
            (expense_id, user_id)
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()



def get_all_expenses():
    conn = get_connection()
    cursor = conn.cursor()  # No dictionary=True
    try:
        cursor.execute("""
            SELECT e.id, e.group_id, e.payer_id, u.username AS payer_name, e.amount, e.description
            FROM expenses e
            JOIN users u ON e.payer_id = u.id
        """)
        results = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        expenses = [dict(zip(columns, row)) for row in results]
        return expenses
    finally:
        cursor.close()
        conn.close()









#group logic
def create_group(group_name):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO `groups` (name) VALUES (%s)", (group_name,))
        conn.commit()
        group_id = cursor.lastrowid
        print("Last inserted group_id:", group_id)

        return group_id
    except Exception as e:
        print(f"Error creating group: {e}")
        conn.rollback()
        return None
    finally:
        cursor.close()
        conn.close()

def add_user_to_group(user_id, group_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Check if group exists
        cursor.execute("SELECT id FROM `groups` WHERE id = %s", (group_id,))
        if cursor.fetchone() is None:
            raise ValueError(f"Group ID {group_id} does not exist.")

        cursor.execute("INSERT INTO group_members (user_id, group_id) VALUES (%s, %s)", (user_id, group_id))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error adding user to group: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()














#for debugging
def run_raw_sql(query, params=None):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query, params or ())
        result = cursor.fetchall()
        conn.commit()
        return result
    except Exception as e:
        print("SQL Error:", e)
        conn.rollback()
        return None
    finally:
        cursor.close()
        conn.close()



