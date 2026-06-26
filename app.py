# The Streamlit UI creation

import streamlit as st
from datetime import datetime

from models import TransactionType
from database import get_db
from crud import create_transaction

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
                                       transaction_date= datetime.combine(transaction_date, datetime.min.time()),  # type: ignore
                                       description=description if description else None
                                       )
                st.session_state["success_message"] = "✅ Transaction added successfully!"

            except Exception as e:
                st.session_state["error_message"] = f"❌ Failed: {str(e)}"

    if "success_message" in st.session_state:
        st.success(st.session_state.pop("success_message"))

    if "error_message" in st.session_state:
        st.error(st.session_state.pop("error_message"))

def main():
    if options == "Add Transaction":
        add_transaction_form()

if __name__ == "__main__":
    main()