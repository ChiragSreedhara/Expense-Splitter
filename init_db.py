from database import get_connection

def execute_sql_file(filename):
    conn = get_connection()
    cursor = conn.cursor()
    
    with open(filename, 'r') as f:
        sql = f.read()

    try:
        for statement in sql.strip().split(';'):
            stmt = statement.strip()
            if stmt:
                cursor.execute(stmt)
        conn.commit()
        print(" Tables created successfully.")
    except Exception as e:
        print(" Error:", e)
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    execute_sql_file("tables.sql")
