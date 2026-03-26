from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..schemas.schemas import (
    AccountOut, AccountCreate, DepositCreate, WithdrawCreate, TransferCreate, TransactionOut
)
from ..core.security import get_current_user
from ..services.user_service import get_user_by_username
from ..services.account_service import (
    get_account, get_accounts_by_user, create_account, deposit, withdraw, transfer, get_transactions
)
from ..exceptions import AccountNotFoundError, NotEnoughFundsError

router = APIRouter(prefix="/accounts", tags=["accounts"])

@router.get("/", response_model=List[AccountOut])
def list_accounts(current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    user = get_user_by_username(db, current_user)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return get_accounts_by_user(db, user.id)

@router.post("/", response_model=AccountOut)
def create_new_account(current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    user = get_user_by_username(db, current_user)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return create_account(db, user.id)

@router.get("/{account_id}", response_model=AccountOut)
def get_account_detail(account_id: int, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    acc = get_account(db, account_id)
    if not acc or acc.user_id != get_user_by_username(db, current_user).id:
        raise AccountNotFoundError()
    return acc

@router.post("/{account_id}/deposit", response_model=AccountOut)
def do_deposit(account_id: int, deposit: DepositCreate, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    acc = get_account(db, account_id)
    if not acc or acc.user_id != get_user_by_username(db, current_user).id:
        raise AccountNotFoundError()
    return deposit(db, account_id, deposit)

@router.post("/{account_id}/withdraw", response_model=AccountOut)
def do_withdraw(account_id: int, withdraw: WithdrawCreate, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    acc = get_account(db, account_id)
    if not acc or acc.user_id != get_user_by_username(db, current_user).id:
        raise AccountNotFoundError()
    return withdraw(db, account_id, withdraw)

@router.post("/{account_id}/transfer", response_model=List[AccountOut])
def do_transfer(account_id: int, transfer: TransferCreate, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    from_user = get_user_by_username(db, current_user)
    from_acc = get_account(db, account_id)
    if not from_acc or from_acc.user_id != from_user.id:
        raise AccountNotFoundError()
    if transfer.to_account_id == account_id:
        raise HTTPException(status_code=400, detail="Cannot transfer to same account")
    return transfer(db, account_id, transfer.to_account_id, transfer)

@router.get("/{account_id}/transactions", response_model=List[TransactionOut])
def list_transactions(account_id: int, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    acc = get_account(db, account_id)
    if not acc or acc.user_id != get_user_by_username(db, current_user).id:
        raise AccountNotFoundError()
    return get_transactions(db, account_id)

