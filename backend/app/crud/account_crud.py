import logging
from datetime import datetime
from typing import List
from typing import Optional

import app.schemas.account_schemas as account_schemas
from app.models.account import Account
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound


def get_account(db: Session, account_id: int) -> Account:
    try:
        account = db.query(Account).filter(Account.id == account_id).first()
    except NoResultFound:
        return None
    except Exception as error:
        logging.error(error)
        return None
    return account


def get_account_by_email(db: Session, email: str) -> Optional[Account]:
    try:
        account = db.query(Account).filter(Account.email == email).first()
    except NoResultFound:
        return None
    except Exception as error:
        logging.error(error)
        return None
    return account


def get_accounts(db: Session) -> List[Account]:
    try:
        accounts = db.query(Account).all()
    except Exception as error:
        logging.error(error)
        return []
    return accounts


def create_account(db: Session, account: account_schemas.AccountCreate) -> Account:
    try:
        now = datetime.now()
        db_account = Account(
            username=account.username,
            email=account.email,
            password=account.password,
            created=now,
        )
        db.add(db_account)
        db.commit()
        db.refresh(db_account)
    except Exception as error:
        logging.error(error)
        db.rollback()
        return None
    return db_account


def delete_account(db: Session, account_id: int) -> Optional[Account]:
    try:
        account = get_account(db, account_id)
        if account:
            db.delete(account)
            db.commit()
        else:
            raise NoResultFound("Account not found for deletion")
    except NoResultFound:
        return None
    except Exception as error:
        logging.error(error)
        db.rollback()
        return None
    return account


def update_account(
    db: Session,
    account_id: int,
    account: account_schemas.AccountUpdate,
) -> Optional[Account]:
    try:
        db_account = get_account(db, account_id)
        if db_account:
            account_data = account.model_dump(exclude_unset=True)
            for key, value in account_data.items():
                setattr(db_account, key, value)
            db.commit()
            return db_account
        else:
            raise NoResultFound("Account not found for update")
    except NoResultFound:
        return None

    except Exception as error:
        logging.error(error)
        db.rollback()
        return None