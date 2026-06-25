# Functions that add/read/update/delete transactions, using models + database, no UI logic
from datetime import datetime
from decimal import Decimal


from sqlalchemy import between
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from typing import List, Optional

from models import  Transaction, TransactionType



# --- Create the transaction ---
def create_transaction(
        db: Session,
        amount: Decimal,
        trans_type: TransactionType,
        category: str,
        description: Optional[str] = None,
        transaction_date: Optional[datetime] = None,

) -> Transaction:
    try:
        transaction = Transaction(
            amount = amount,
            trans_type = trans_type,
            category = category,
            description = description
        )

        if transaction_date:
            transaction.transaction_date = transaction_date

        db.add(transaction)
        db.commit()
        db.refresh(transaction)

        return transaction

    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Failed to create transaction: {str(e)}")

    except Exception as e:
        db.rollback()
        raise Exception(f"Unexpected error creating transaction: {str(e)}")


# --- Read the transaction ---
def get_transactions(
        db: Session,
        category: Optional[str] = None,
        trans_type: Optional[TransactionType] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,

) -> List[Transaction]:
    try:
        query = db.query(Transaction)

        # Apply filters if provided
        if category is not None:
            query = query.filter(Transaction.category == category)  # type: ignore

        if trans_type is not None:
            query = query.filter(Transaction.trans_type == trans_type)  # type: ignore

        if start_date and end_date:
            query = query.filter(between(Transaction.transaction_date, start_date, end_date))

        elif start_date:
            query = query.filter(Transaction.transaction_date >= start_date)

        elif end_date:
            query = query.filter(Transaction.transaction_date <= end_date)

        # Order by date descending (newest first)
        return query.order_by(Transaction.transaction_date).all()  # type: ignore

    except SQLAlchemyError as e:
        raise Exception(f"Failed to retrieve transactions: {str(e)}")

# --- Update the transaction ---
def update_transaction(
        db: Session,
        trans_id: int,
        **kwargs

) -> Optional[Transaction]:
    try:
        # Get the transaction
        transaction = db.get(Transaction, trans_id)

        if not transaction:
            return None

        # Allowed updatable fields
        allowed_fields = {"amount", "trans_type", "category", "description", "transaction_date"}

        for key, value in kwargs.items():
            if key in allowed_fields and hasattr(transaction, key):
                setattr(transaction, key, value)

        db.commit()
        db.refresh(transaction)
        return transaction  # type: ignore

    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Failed to update transaction {trans_id}: {str(e)}")


# --- Delete the transaction ---
def delete_transaction(
        db: Session,
        trans_id: int

) -> bool:
    try:
        transaction = db.get(Transaction, trans_id)
        if not transaction:
            return False

        db.delete(transaction)
        db.commit()
        return True

    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Failed to delete transaction {trans_id}: {str(e)}")