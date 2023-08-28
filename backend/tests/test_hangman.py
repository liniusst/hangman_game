import unittest
from unittest.mock import MagicMock, patch

from utils.hangman_game import Hangman


class TestGetRandomWord(unittest.TestCase):
    def setUp(self):
        self.hangman = Hangman()
        self.game_word = "success"
        self.game_display = ""
        self.game_blanks = 8

    @patch("utils.hangman_game.RandomWords")
    def test_get_random_word(self, mock_random_words):
        mock_hangman = MagicMock()
        mock_hangman.get_random_word.return_value = self.game_word
        mock_random_words.return_value = mock_hangman

        result = self.hangman.get_random_word()

        self.assertEqual(result, self.game_word)
        self.assertNotEqual(result, "unsuccess")

    def test_get_game_word_display(self):
        self.hangman.game_word = self.game_word
        result = self.hangman.get_game_word_display()

        self.assertEqual(result, "_______")
        self.assertNotEqual(result, "__")

    def test_get_game_word_blanks(self):
        self.hangman.game_word = self.game_word
        result = self.hangman.get_game_word_blanks()

        self.assertEqual(result, 7)
        self.assertNotEqual(result, 8)


if __name__ == "__main__":
    unittest.main()
