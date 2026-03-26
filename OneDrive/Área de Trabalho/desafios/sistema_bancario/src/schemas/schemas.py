from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from ..models.models import TransactionType

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    class Config:
        from_attributes = True

class AccountBase(BaseModel):
    pass

class AccountCreate(AccountBase):
    pass

class AccountOut(AccountBase):
    id: int
    balance: float
    owner_id: int
    class Config:
        from_attributes = True

class TransactionOut(BaseModel):
    id: int
    account_id: int
    type: TransactionType
    amount: float
    description: Optional[str] = None
    created_at: datetime
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class DepositCreate(BaseModel):
    amount: float
    description: Optional[str] = "Deposit"

class WithdrawCreate(BaseModel):
    amount: float
    description: Optional[str] = "Withdraw"

class TransferCreate(BaseModel):
    to_account_id: int
    amount: float
    description: Optional[str] = "Transfer"

