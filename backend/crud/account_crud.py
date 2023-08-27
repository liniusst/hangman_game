from logs.logger import logger
from datetime import datetime
from typing import List
from typing import Optional
import schemas.account_schemas as account_schemas
from models.account import Account
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound


def get_account(db: Session, account_id: int) -> Account:
    try:
        account = db.query(Account).filter(Account.id == account_id).first()
    except NoResultFound as error:
        logger.exception(f"NoResultFound {error}")
        return None
    except Exception as error:
        logger.exception(error)
        return None
    return account


def get_account_by_email(db: Session, email: str) -> Optional[Account]:
    try:
        account = db.query(Account).filter(Account.email == email).first()
        logger.debug("get_account_by_email returned")
    except NoResultFound as error:
        logger.exception(error)
        return None
    except Exception as error:
        logger.exception(error)
        return None
    return account


def get_accounts(db: Session) -> List[Account]:
    try:
        accounts = db.query(Account).all()
        logger.debug("get_accounts returned")
    except Exception as error:
        logger.exception(error)
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
        logger.debug(f"{db_account.id} Account created")
    except Exception as error:
        logger.exception(error)
        db.rollback()
        return None
    return db_account


def delete_account(db: Session, account_id: int) -> Optional[Account]:
    try:
        account = get_account(db, account_id)
        logger.debug("account for deletion found")
        if account:
            db.delete(account)
            db.commit()
            logger.debug(f"{account.id} Account deleted")
        else:
            raise NoResultFound("Account not found for deletion")
    except NoResultFound as error:
        logger.exception(error)
        return None
    except Exception as error:
        logger.exception(error)
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
        logger.debug("Account found for update")
        if db_account:
            account_data = account.model_dump(exclude_unset=True)
            for key, value in account_data.items():
                setattr(db_account, key, value)
            db.commit()
            logger.debug(f"Acount {db_account.id} updated")
            return db_account
        else:
            logger.error(NoResultFound)
            raise NoResultFound("Account not found for update")
    except NoResultFound as error:
        logger.exception(error)
        return None

    except Exception as error:
        logger.exception(error)
        db.rollback()
        return None
