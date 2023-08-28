import unittest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session

from crud.game_crud import Game
from crud.game_crud import get_game, get_user_last_five_games, get_games_by_user_id
from crud.account_crud import Account


class TestGame(unittest.TestCase):
    @patch("logs.logger")
    def test_get_account(self, mock_logger):
        mock_db = MagicMock(spec=Session)
        mock_game = MagicMock(spec=Game)
        mock_db.query.return_value.filter.return_value.first.return_value = mock_game

        game_id = 1
        result = get_game(mock_db, game_id)

        self.assertEqual(result, mock_game)

    @patch("logs.logger")
    def test_get_user_last_five_games(self, mock_logger):
        mock_db = MagicMock(spec=Session)
        mock_games = [MagicMock(), MagicMock()]
        mock_account = MagicMock(spec=Account)

        mock_db.query.return_value.filter.return_value.first.return_value = mock_account
        mock_db.query.return_value.filter.return_value.order_by.return_value.limit.return_value.all.return_value = (
            mock_games
        )

        account_id = 1
        result = get_user_last_five_games(mock_db, account_id)

        self.assertEqual(result, mock_games)

    @patch("logs.logger")
    def test_get_games_by_user_id(self, mock_logger):
        mock_db = MagicMock(spec=Session)
        mock_games = [MagicMock(), MagicMock()]
        mock_account = MagicMock(spec=Account)

        mock_db.query.return_value.filter.return_value.first.return_value = mock_account
        mock_db.query.return_value.filter.return_value.order_by.return_value.all.return_value = (
            mock_games
        )

        account_id = 1
        result = get_games_by_user_id(mock_db, account_id)

        self.assertEqual(result, mock_games)
