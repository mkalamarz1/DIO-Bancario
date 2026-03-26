from sqlalchemy.orm import Session, SessionTransaction
from sqlalchemy.exc import IntegrityError
from typing import Optional, List
from ..database import get_db
from ..models.models import User, Account, Transaction, TransactionType
from ..schemas.schemas import AccountCreate, AccountOut, DepositCreate, WithdrawCreate, TransferCreate, TransactionOut
from ..exceptions import AccountNotFoundError, NotEnoughFundsError, UserNotFoundError
from ..services.user_service import get_user_by_username
from fastapi import Depends

def get_account(db: Session, account_id: int) -> Optional[Account]:
    return db.query(Account).filter(Account.id == account_id).first()

def get_accounts_by_user(db: Session, user_id: int) -> List[Account]:
    return db.query(Account).filter(Account.user_id == user_id).all()

def create_account(db: Session, user_id: int) -> Account:
    db_account = Account(user_id=user_id, balance=0.0)
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

def deposit(db: Session, account_id: int, deposit: DepositCreate) -> Account:
    account = get_account(db, account_id)
    if not account:
        raise AccountNotFoundError()
    account.balance += deposit.amount
    transaction = Transaction(account_id=account_id, type=TransactionType.deposit, amount=deposit.amount, description=deposit.description)
    db.add(transaction)
    db.commit()
    db.refresh(account)
    return account

def withdraw(db: Session, account_id: int, withdraw: WithdrawCreate) -> Account:
    account = get_account(db, account_id)
    if not account:
        raise AccountNotFoundError()
    if account.balance < withdraw.amount:
        raise NotEnoughFundsError()
    account.balance -= withdraw.amount
    transaction = Transaction(account_id=account_id, type=TransactionType.withdraw, amount=-withdraw.amount, description=withdraw.description)
    db.add(transaction)
    db.commit()
    db.refresh(account)
    return account

def transfer(db: Session, from_account_id: int, to_account_id: int, transfer: TransferCreate) -> List[Account]:
    from_account = get_account(db, from_account_id)
    to_account = get_account(db, to_account_id)
    if not from_account or not to_account:
        raise AccountNotFoundError()
    if from_account.balance < transfer.amount:
        raise NotEnoughFundsError()
    
    from_account.balance -= transfer.amount
    to_account.balance += transfer.amount
    
    from_tx = Transaction(account_id=from_account_id, type=TransactionType.transfer, amount=-transfer.amount, description=f"Transfer to {to_account_id}: {transfer.description}")
    to_tx = Transaction(account_id=to_account_id, type=TransactionType.transfer, amount=transfer.amount, description=f"Transfer from {from_account_id}: {transfer.description}")
    
    db.add(from_tx)
    db.add(to_tx)
    db.commit()
    db.refresh(from_account)
    db.refresh(to_account)
    return [from_account, to_account]

def get_transactions(db: Session, account_id: int) -> List[Transaction]:
    return db.query(Transaction).filter(Transaction.account_id == account_id).order_by(Transaction.created_at.desc()).all()

