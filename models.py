#  Defines the data shape (what a Transaction is), nothing about how it's saved or shown
from datetime import datetime
import enum
from decimal import Decimal

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Numeric, String, Enum
from  sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
from sqlalchemy import DateTime



class Base(DeclarativeBase):
    pass


class TransactionType(str, enum.Enum):
    INCOME = "income"
    EXPENSE = "expense"


class Transaction(Base):
    __tablename__ = 'transaction'
    trans_id: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    category: Mapped[str] = mapped_column(String(50))
    description: Mapped[Optional[str]] = mapped_column(String(255))
    transaction_date: Mapped[datetime] = mapped_column(DateTime,default=datetime.now)
    trans_type: Mapped[TransactionType] = mapped_column(Enum(TransactionType), nullable=False)

