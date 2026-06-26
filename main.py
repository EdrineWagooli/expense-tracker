# The entry point that calls crud functions and handles input/output, no direct database code
from datetime import datetime

from database import  get_db
from crud import create_transaction, get_transactions, update_transaction, delete_transaction
from models import  TransactionType, Transaction


def main():
    # Getting a session from the generator
    with get_db() as db:
        try:
            # Cleanup part
            db.query(Transaction).delete()
            db.commit()

            print("=" * 50)
            print("    🧪 Expense Tracker \n")
            print("=" * 50)

           # ---- CREATE ---
            print("=" * 50)
            print("\n📝 Creating an income transaction")
            income = create_transaction(
                db= db,
                amount = 3000.00,    # type: ignore
                category = "Salary",
                trans_type = TransactionType.INCOME,
                transaction_date = datetime(2026, 6, 23, 9,45, 12),
                description = "June salary  deposit"
            )
            print(f"   ✅ Created: {income}")

            # Creating expenses
            print("\n📝 Creating expense transaction")
            expense1 = create_transaction(
                db= db,
                amount = 33.99,    # type: ignore
                category = "Groceries",
                trans_type = TransactionType.EXPENSE,
                transaction_date=datetime(2026, 6, 5, 14, 30, 59),
                description = "Weekly grocery shopping"
            )
            print(f"   ✅ Created: {expense1}")

            # Another test expense
            print("\n📝 Create another expense transaction")
            expense2 = create_transaction(
                db= db,
                amount = 15.50,    # type: ignore
                category = "Transportation",
                trans_type = TransactionType.EXPENSE,
                transaction_date=datetime.now(),
                description = "Uber ride to airport"
            )
            print(f"   ✅ Created: {expense2}")

            # Creating an expense with no description
            print("\n📝 Creating an expense with no description")
            expense3 = create_transaction(
                db = db,
                amount = 89.99,     # type: ignore
                category="Electronics",
                trans_type=TransactionType.EXPENSE,
                transaction_date=datetime(2026, 6, 15, 10, 0, 22)
            )
            print(f"   ✅ Created: {expense3}")


            # --- READ ---
            # Getting all transactions
            print("\n📊 Get all transactions")
            all_transactions = get_transactions(db = db)
            print(f"   Found {len(all_transactions)} transactions:")

            for index, transaction in enumerate(all_transactions, start=1):
                print(f" {index}. {transaction}")


            # Getting filtered transactions (expenses only)
            print("\n📊 Getting expense transactions only")
            expenses = get_transactions(
                db= db,
                trans_type = TransactionType.EXPENSE,
            )
            print(f"   Found {len(expenses)} expenses transactions:")

            for index, expense in enumerate(expenses, start=1):
                 print(f" {index}. {expense}")


            # --- UPDATE ---
            print("\n📝 Updating transaction description only")
            updated = update_transaction(
                db = db,
                trans_id = expense1.trans_id,
                description = "Updated: Weekly grocery run at Trader Joe's"
            )
            if updated:
                print(f"   ✅ Updated: {updated}")
            else:
                print("   ❌ Transaction not found")


            # --- DELETE ---
            print("\n🗑️ Deleting a transaction")
            deleted = delete_transaction(
                db = db,
                trans_id = expense2.trans_id,
            )
            if deleted:
                print(f"   ✅ Deleted transaction #{expense2.trans_id}")
            else:
                print("   ❌ Transaction not found")

            # Verify deletion(get all again)
            after_delete = get_transactions(db = db)
            print(f"   {len(after_delete)} transactions remaining:")

            for index, transaction in enumerate(after_delete, start=1):
                print(f"   {index}. {transaction}")

            # Trying to delete non-existent transaction
            print("\n🗑️ Try to delete non-existent transaction")
            deleted = delete_transaction(db = db, trans_id = 678)
            print(f"   Deleted: {deleted} (False means not found)")

            print("\n" + "=" * 60)
            print("     ✅ TESTING COMPLETE")
            print("=" * 60)
            print("\n🔒 Database session closed.")

        except Exception as e:
            print(f"\n❌ ERROR: {e}")
            db.rollback()

        # finally:
        #     print("\n🔒 Database session closed.")


if __name__ == "__main__":
    main()