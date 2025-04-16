# database.py
import sqlite3
import pandas as pd
from datetime import datetime

DATABASE_NAME = 'expenses.db'

def init_db():
    """Initializes the SQLite database and creates the transactions table if it doesn't exist."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    # --- MODIFIED CREATE TABLE STATEMENT ---
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            date TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            description TEXT,
            CHECK(type IN ('Income', 'Expense')) -- Moved CHECK constraint here
        )
    ''')
    # --- END OF MODIFICATION ---
    conn.commit()
    conn.close()

def add_transaction(trans_type, date, category, amount, description):
    """Adds a new transaction to the database."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    try:
        # Store date as ISO format string (YYYY-MM-DD HH:MM:SS.ffffff or YYYY-MM-DD)
        # Using just the date part is fine if you don't need time
        date_str = date.strftime('%Y-%m-%d')
        cursor.execute('''
            INSERT INTO transactions (type, date, category, amount, description)
            VALUES (?, ?, ?, ?, ?)
        ''', (trans_type, date_str, category, amount, description))
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
        # Specify parse_dates to let pandas handle conversion
        df = pd.read_sql_query("SELECT * FROM transactions ORDER BY date DESC, id DESC", conn, parse_dates=['date'])
        # Convert date column back to datetime objects after reading (if parse_dates fails or isn't used)
        # if not df.empty and 'date' in df.columns:
        #     df['date'] = pd.to_datetime(df['date']) # Already handled by parse_dates usually
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
        # Check if any row was actually deleted
        return cursor.rowcount > 0 # Indicate success if rows were affected
    except sqlite3.Error as e:
        print(f"Database error during delete: {e}")
        return False # Indicate failure
    finally:
        conn.close()


# --- IMPORTANT ---
# Initialize the database when this module is imported
# Make sure any existing 'expenses.db' file is compatible or delete it
# if you change the schema significantly.
try:
    init_db()
except sqlite3.Error as e:
    print(f"FATAL: Could not initialize database '{DATABASE_NAME}': {e}")
    # You might want to exit or raise the exception here depending on desired behavior
    # raise e
# --- END OF IMPORTANT SECTION ---