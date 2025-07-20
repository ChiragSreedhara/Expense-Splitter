from database import get_connection

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



