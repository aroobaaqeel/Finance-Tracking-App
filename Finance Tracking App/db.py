import mysql.connector
from datetime import datetime, timedelta

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Pass357781/2111",
        database="finance_db"
    )

def insert_transaction(date, description, amount, t_type):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO transactions (date, description, amount, type) VALUES (%s, %s, %s, %s)",
                (date, description, amount, t_type))
    conn.commit()
    conn.close()

def delete_transaction(tid):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM transactions WHERE id = %s", (tid,))
    conn.commit()
    conn.close()

def get_transactions():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM transactions ORDER BY date DESC")
    rows = cur.fetchall()
    conn.close()
    return rows

def get_summary(period):
    conn = get_connection()
    cur = conn.cursor()
    now = datetime.now()

    if period == 'daily':
        since = now.strftime("%Y-%m-%d")
    elif period == 'weekly':
        since = (now - timedelta(days=7)).strftime("%Y-%m-%d")
    elif period == 'monthly':
        since = (now - timedelta(days=30)).strftime("%Y-%m-%d")
    else:
        since = '1970-01-01'

    cur.execute("SELECT type, SUM(amount) FROM transactions WHERE date >= %s GROUP BY type", (since,))
    data = {"income": 0, "expense": 0}
    for row in cur.fetchall():
        data[row[0]] = float(row[1])
    conn.close()
    return data

def init_db():
    pass  # No need to create tables from Python for now
