# The Streamlit UI creation

import streamlit as st
from datetime import datetime

from models import TransactionType
from database import get_db
from crud import create_transaction, get_transactions

st.set_page_config(
    page_title="Personal Expense Tracker",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Expense Tracker")

st.sidebar.title("Menu")
options = st.sidebar.selectbox(
    "Select an option",
    ["Add Transaction","Transaction History", "Summary"]
)


# === PAGE 1 : ADD TRANSACTION ===
def add_transaction_form():
    with st.form("Add Transaction", clear_on_submit=True):
        st.subheader("➕ Add Transaction")

        # Form fields
        amount = st.number_input("**Amount**",
                                 min_value = 0.01,
                                 step = 0.01,
                                 format = "%.2f"
                                 )

        category = st.text_input("**Category**",
                                 placeholder="e.g. Food, Groceries, Salary, Transport"
                                 )

        trans_type = st.selectbox("**Type**",
                                  options = [TransactionType.INCOME, TransactionType.EXPENSE],
                                  format_func= lambda x: x.value.capitalize(),
                                  help="Is this Income or Expense?"
                                  )

        transaction_date = st.date_input("**Date**",
                                         value=(datetime.now()),
                                         help="When did this transaction occur?"
                                         )

        description = st.text_area("**Description (Optional)**",
                                   placeholder="Add any additional details about this transaction...",
                                   height=100
                                   )
        # Submit button
        submitted = st.form_submit_button("💾 Add Transaction",
                                          type="primary",
                                          use_container_width=True
                                          )
        # Validation
        if submitted:
            if amount <= 0:  # type: ignore
                st.error("Amount must be greater than 0")
                return

            if not category or category.strip() == "":
                st.error("Category is required")
                return

            # Create the transaction
            try:
                with get_db() as db:
                    create_transaction(db,
                                       amount=amount,    # type: ignore
                                       category=category,
                                       trans_type=trans_type,
                                       transaction_date = datetime.combine(transaction_date, datetime.now().time()),  # type: ignore
                                       description=description if description else None
                                       )
                st.session_state["success_message"] = "✅ Transaction added successfully!"

            except Exception as e:
                st.session_state["error_message"] = f"❌ Failed: {str(e)}"

    if "success_message" in st.session_state:
        st.success(st.session_state.pop("success_message"))

    if "error_message" in st.session_state:
        st.error(st.session_state.pop("error_message"))


# ==== Transaction History ====
def transaction_history():
    st.subheader("📊 Transaction History")

    # Filter controls outside any form
    col1, col2, col3 = st.columns([2, 2, 3])

    # Type filter - All/Income/Expense
    with col1:
        type_filter = st.selectbox("**Transaction Type**",
                             options=["All", "Income", "Expense"],
                             index=0,
                             )

    # Category filter - text input
    with col2:
        category_filter = st.text_input("**Category**",
                                       placeholder="e.g. Food",
                                        help="Filter by category name?"
                                        )

    # Date range - two date inputs
    with col3:
        st.write("**Date Range**")
        date_col1, date_col2 = st.columns(2)
        with date_col1:
            start_date = st.date_input("From", value=None)
        with date_col2:
            end_date = st.date_input("To", value=None)


    # Convert type filter to TransactionType enum or None
    trans_type = None
    if type_filter == "Income":
        trans_type = TransactionType.INCOME
    elif type_filter == "Expense":
        trans_type = TransactionType.EXPENSE

    # Convert category filter (empty means none)
    category = category_filter.strip() if category_filter else None

    # Only apply date filter when BOTH dates exist
    start = None
    end = None

    if start_date and end_date:
        start = datetime.combine(start_date, datetime.min.time())  # type: ignore
        end = datetime.combine(end_date, datetime.max.time())    # type: ignore

    elif start_date and not end_date:
        st.info("ℹ️ Please select both start and end dates for date filtering")

    elif end_date and not start_date:
        st.info("ℹ️ Please select both start and end dates for date filtering")

    # Get transactions with filters
    try:
        with get_db() as db:
            transactions = get_transactions(
                db,
                category=category,
                trans_type=trans_type,
                start_date= start,
                end_date= end
            )

        # Handle empty case
        if not transactions:
            st.info("📭 No transactions found")
            return

        st.caption(f"Showing {len(transactions)} transactions")

        # Convert to list of dicts for display
        data = []
        for transaction in transactions:
            data.append({
                "Transaction ID": transaction.trans_id,
                "Amount": round(float(transaction.amount),2),
                "Category": transaction.category,
                "Type": transaction.trans_type.value.capitalize(),
                "Date": transaction.transaction_date.strftime("%Y-%m-%d"),
                "Description": transaction.description or "",

            })

        # Display as dataframe
        st.dataframe(data=data,
                     use_container_width=True,
                     column_config={
                         "Transaction ID": st.column_config.NumberColumn("ID", format="%d"),
                         "Amount": st.column_config.NumberColumn("Amount", format="%.2f"),
                         "Type": st.column_config.Column("Type", width="small"),
                         "Category": st.column_config.Column("Category", width="medium"),
                         "Date": st.column_config.Column("Date", width="medium"),
                         "Description": st.column_config.Column("Description", width="large")
                     }
                     )
    except Exception as e:
        st.error(f"❌ Failed to load transactions: {str(e)}")


def main():
    if options == "Add Transaction":
        add_transaction_form()
    elif options == "Transaction History":
        transaction_history()

if __name__ == "__main__":
    main()