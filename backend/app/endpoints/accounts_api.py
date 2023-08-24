import app.crud.account_crud as account_crud
from app.database import get_db
from app.schemas.account_schemas import AccountCreate
from app.schemas.account_schemas import AccountResponse
from app.schemas.account_schemas import AccountUpdate
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("", response_model=AccountResponse)
def create_account(account: AccountCreate, db: Session = Depends(get_db)):
    db_account = account_crud.get_account_by_email(db, email=account.email)
    if db_account:
        raise HTTPException(status_code=400, detail="Email already registered")
    return account_crud.create_account(db=db, account=account)


@router.get("", response_model=list[AccountResponse])
def read_accounts(db: Session = Depends(get_db)):
    db_accounts = account_crud.get_accounts(db)
    if db_accounts is None:
        raise HTTPException(status_code=404, detail="Accounts not found")
    return db_accounts


@router.get("/{account_id}", response_model=AccountResponse)
def read_account(account_id: int, db: Session = Depends(get_db)):
    db_account = account_crud.get_account(db, account_id=account_id)
    if db_account is None:
        raise HTTPException(status_code=404, detail=f"Account {account_id} not found")
    return db_account


@router.get("/email/{email}", response_model=AccountResponse)
def get_account_by_email(email: str, db: Session = Depends(get_db)):
    db_account = account_crud.get_account_by_email(db, email=email)
    if db_account is None:
        raise HTTPException(status_code=404, detail=f"Account {email} not found")
    return db_account


@router.delete("/{account_id}", response_model=AccountResponse)
def delete_account(account_id: int, db: Session = Depends(get_db)):
    account = account_crud.get_account(db, account_id)
    if account is None:
        raise HTTPException(
            status_code=404, detail=f"Account with ID: {account_id} not found"
        )
    return account_crud.delete_account(db, account_id=account_id)


@router.patch("/{account_id}", response_model=AccountResponse)
def update_account(
    account_id: int, account: AccountUpdate, db: Session = Depends(get_db)
):
    db_account = account_crud.get_account(db, account_id)
    if db_account is None:
        raise HTTPException(status_code=404, detail=f"Can't update ID: {account_id}")
    update_account = account_crud.update_account(
        db, account_id=db_account.id, account=account
    )
    return update_account