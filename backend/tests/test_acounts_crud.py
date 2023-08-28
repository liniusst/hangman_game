import unittest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session

from crud.account_crud import get_account, get_account_by_email, get_accounts, Account


class TestAccount(unittest.TestCase):
    @patch("logs.logger")
    def test_get_account(self, mock_logger):
        mock_db = MagicMock(spec=Session)
        mock_account = MagicMock(spec=Account)

        mock_db.query.return_value.filter.return_value.first.return_value = mock_account
        account_id = 1
        result = get_account(mock_db, account_id)

        self.assertEqual(result, mock_account)

    @patch("logs.logger")
    def test_get_account_by_email(self, mock_logger):
        mock_db = MagicMock(spec=Session)
        mock_account = MagicMock(spec=Account)

        mock_db.query.return_value.filter.return_value.first.return_value = mock_account
        email = "demo@demo.com"
        result = get_account_by_email(mock_db, email)

        self.assertEqual(result, mock_account)

    @patch("logs.logger")
    def test_get_accounts(self, mock_logger):
        mock_db = MagicMock(spec=Session)
        mock_accounts = [MagicMock(), MagicMock()]

        mock_db.query.return_value.all.return_value = mock_accounts

        result = get_accounts(mock_db)

        self.assertEqual(result, mock_accounts)


if __name__ == "__main__":
    unittest.main()
