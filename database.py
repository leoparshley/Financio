# database.py
import sqlite3
import pandas as pd
from datetime import datetime

DATABASE_NAME = 'expenses.db'

def init_db():
    """Initializes the SQLite database and creates the transactions table if it doesn't exist."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL, CHECK(type IN ('Income', 'Expense')),
            date TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            description TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_transaction(trans_type, date, category, amount, description):
    """Adds a new transaction to the database."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO transactions (type, date, category, amount, description)
            VALUES (?, ?, ?, ?, ?)
        ''', (trans_type, date.isoformat(), category, amount, description))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}") # Basic error handling
    finally:
        conn.close()

def get_transactions():
    """Retrieves all transactions from the database as a Pandas DataFrame."""
    conn = sqlite3.connect(DATABASE_NAME)
    try:
        # Use pandas to read directly from SQL query for convenience
        df = pd.read_sql_query("SELECT * FROM transactions ORDER BY date DESC", conn)
        # Convert date column back to datetime objects after reading
        if not df.empty and 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
        return df
    except Exception as e:
        print(f"Error reading database: {e}")
        # Return an empty DataFrame with expected columns if error occurs or table is empty
        return pd.DataFrame(columns=['id', 'type', 'date', 'category', 'amount', 'description'])
    finally:
        conn.close()

def delete_transaction(transaction_id):
    """Deletes a specific transaction by its ID."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
        conn.commit()
        return True # Indicate success
    except sqlite3.Error as e:
        print(f"Database error during delete: {e}")
        return False # Indicate failure
    finally:
        conn.close()

# Initialize the database when this module is imported
init_db()