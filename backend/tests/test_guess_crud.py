import unittest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session

from crud.game_crud import Game
from crud.guess_crud import get_guesses_by_game_id


class TestGuess(unittest.TestCase):
    @patch("logs.logger")
    def test_get_guesses_by_game_id(self, mock_logger):
        mock_db = MagicMock(spec=Session)
        mock_guesses = [MagicMock(), MagicMock()]

        mock_game = MagicMock(spec=Game)
        mock_game.guesses = mock_guesses

        mock_db.query.return_value.filter.return_value.first.return_value = mock_game

        game_id = 1
        result = get_guesses_by_game_id(mock_db, game_id)

        self.assertEqual(result, mock_guesses)
