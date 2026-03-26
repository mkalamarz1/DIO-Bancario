from fastapi import HTTPException

class AccountNotFoundError(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Account not found")

class NotEnoughFundsError(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Not enough funds")

class UserNotFoundError(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="User not found")

class InvalidCredentialsError(HTTPException):
    def __init__(self):
        super().__init__(status_code=401, detail="Invalid credentials")

