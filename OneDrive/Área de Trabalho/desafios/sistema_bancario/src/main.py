from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from .database import engine, Base, get_db
from .exceptions import AccountNotFoundError, NotEnoughFundsError, UserNotFoundError, InvalidCredentialsError
from .controllers import auth_controller, account_controller

app = FastAPI(title="Sistema Bancário", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_controller.router)
app.include_router(account_controller.router)

# Create tables
Base.metadata.create_all(bind=engine)

@app.exception_handler(AccountNotFoundError)
async def account_not_found_handler(request, exc: AccountNotFoundError):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

@app.exception_handler(NotEnoughFundsError)
async def not_enough_funds_handler(request, exc: NotEnoughFundsError):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

@app.exception_handler(UserNotFoundError)
async def user_not_found_handler(request, exc: UserNotFoundError):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

@app.exception_handler(InvalidCredentialsError)
async def invalid_credentials_handler(request, exc: InvalidCredentialsError):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

@app.get("/")
def read_root():
    return {"message": "Sistema Bancário API - Acesse /docs"}

@app.on_event("startup")
async def startup():
    pass  # Tables already created

