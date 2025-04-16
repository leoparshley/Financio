# app.py
import streamlit as st
import pandas as pd
from datetime import datetime
import database as db # Import our database functions

# --- Page Configuration ---
st.set_page_config(
    page_title="Expense Tracker",
    page_icon="💰",
    layout="centered" # Can be "wide" or "centered"
)

# --- Predefined Categories ---
# (You can customize or load these from a file/db later)
INCOME_CATEGORIES = ["Salary", "Freelance", "Investment", "Gift", "Other"]
EXPENSE_CATEGORIES = ["Food", "Transport", "Rent", "Utilities", "Entertainment", "Shopping", "Health", "Education", "Other"]

# --- App Title ---
st.title("💰 Personal Expense Tracker")
st.markdown("Track your income and expenses efficiently.")

# --- Input Form ---
st.header("Add New Transaction")

# Use columns for layout
col1, col2 = st.columns(2)

with col1:
    trans_type = st.selectbox("Type", ["Expense", "Income"], key="trans_type_input")
    if trans_type == "Income":
        category = st.selectbox("Category", INCOME_CATEGORIES, key="income_cat_input")
    else:
        category = st.selectbox("Category", EXPENSE_CATEGORIES, key="expense_cat_input")

with col2:
    amount = st.number_input("Amount", min_value=0.01, format="%.2f", key="amount_input")
    trans_date = st.date_input("Date", datetime.now(), key="date_input")

description = st.text_area("Description (Optional)", key="desc_input")

if st.button("Add Transaction", key="add_button"):
    if not category:
        st.warning("Please select a category.")
    elif amount <= 0:
        st.warning("Amount must be positive.")
    else:
        db.add_transaction(trans_type, trans_date, category, amount, description)
        st.success(f"{trans_type} of {amount:.2f} added successfully!")
        # Clear inputs after adding (optional, requires rerunning or more complex state management)
        # Consider using st.form for better input handling if needed

# --- Display Transactions ---
st.header("Transaction History")

transactions_df = db.get_transactions()

if not transactions_df.empty:
    # Format date for display (optional)
    transactions_df_display = transactions_df.copy()
    transactions_df_display['date'] = transactions_df_display['date'].dt.strftime('%Y-%m-%d')

    # Basic filtering (Example)
    st.sidebar.header("Filter Transactions")
    filter_type = st.sidebar.multiselect("Filter by Type", options=transactions_df['type'].unique(), default=transactions_df['type'].unique())
    filter_category = st.sidebar.multiselect("Filter by Category", options=transactions_df['category'].unique(), default=transactions_df['category'].unique())

    # Apply filters
    filtered_df = transactions_df_display[
        (transactions_df_display['type'].isin(filter_type)) &
        (transactions_df_display['category'].isin(filter_category))
    ]

    st.dataframe(filtered_df, use_container_width=True, hide_index=True) # Display the filtered table

    # --- Summary ---
    st.header("Summary")
    total_income = transactions_df[transactions_df['type'] == 'Income']['amount'].sum()
    total_expense = transactions_df[transactions_df['type'] == 'Expense']['amount'].sum()
    balance = total_income - total_expense

    col_summary1, col_summary2, col_summary3 = st.columns(3)
    col_summary1.metric("Total Income", f"{total_income:,.2f}")
    col_summary2.metric("Total Expenses", f"{total_expense:,.2f}")
    col_summary3.metric("Balance", f"{balance:,.2f}")

    # --- Delete Transaction ---
    st.sidebar.header("Delete Transaction")
    if not transactions_df.empty:
        # Create a list of strings for the selectbox: "ID: Date - Type - Category - Amount"
        transaction_options = [
            f"{row['id']}: {row['date'].strftime('%Y-%m-%d')} - {row['type']} - {row['category']} - {row['amount']:.2f}"
            for index, row in transactions_df.iterrows()
        ]
        trans_to_delete_display = st.sidebar.selectbox("Select Transaction to Delete", options=[""] + transaction_options)

        if trans_to_delete_display:
            # Extract the ID from the selected string
            trans_id_to_delete = int(trans_to_delete_display.split(":")[0])

            if st.sidebar.button("Delete Selected Transaction", type="primary"):
                if db.delete_transaction(trans_id_to_delete):
                    st.sidebar.success("Transaction deleted successfully!")
                    st.experimental_rerun() # Rerun the app to refresh the data
                else:
                    st.sidebar.error("Failed to delete transaction.")
    else:
        st.sidebar.write("No transactions to delete.")


else:
    st.info("No transactions recorded yet. Add some using the form above!")

# --- Simple Plot (Example) ---
if not transactions_df.empty and total_expense > 0:
    st.header("Expense Breakdown by Category")
    expense_df = transactions_df[transactions_df['type'] == 'Expense']
    category_expenses = expense_df.groupby('category')['amount'].sum()

    if not category_expenses.empty:
        st.bar_chart(category_expenses)
        # For a pie chart (requires plotly usually, but basic altair/vega-lite might work)
        # import altair as alt
        # chart = alt.Chart(category_expenses.reset_index()).mark_arc().encode(
        #     theta=alt.Theta(field="amount", type="quantitative"),
        #     color=alt.Color(field="category", type="nominal")
        # )
        # st.altair_chart(chart, use_container_width=True)
    else:
        st.write("No expenses to plot yet.")