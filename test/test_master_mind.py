import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.master_mind import Match, guess, Color, play, GameStatus, select_colors

EXACT = Match.EXACT
PARTIAL = Match.PARTIAL
NOT_FOUND = Match.NOT_FOUND

WON = GameStatus.WON
IN_PROGRESS = GameStatus.IN_PROGRESS
LOST = GameStatus.LOST

EXCEPTION_MESSAGE = "Maximum number of attempts exceeded."

class MasterMindTests(unittest.TestCase):
  def test_canary(self):
    self.assertTrue(True)

  def test_guess_with_all_colors_match_in_position(self):
    selected_colors = [Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW, Color.ORANGE, Color.PURPLE]
    user_provided_colors = selected_colors

    response = guess(selected_colors, user_provided_colors)

    self.assertEqual(response[EXACT], 6)

  def test_guess_with_all_colors_mismatch(self):
    selected_colors = [Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW, Color.ORANGE, Color.PURPLE]
    user_provided_colors = [Color.WHITE, Color.BLACK, Color.CYAN, Color.VIOLET, Color.WHITE, Color.BLACK]

    response = guess(selected_colors, user_provided_colors)

    self.assertEqual(response[NOT_FOUND], 6)

  def test_guess_with_all_colors_match_out_of_position(self):
    selected_colors = [Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW, Color.ORANGE, Color.PURPLE]
    user_provided_colors = [Color.PURPLE, Color.ORANGE, Color.YELLOW, Color.GREEN, Color.BLUE, Color.RED]

    response = guess(selected_colors, user_provided_colors)

    self.assertEqual(response[PARTIAL], 6)

  def test_guess_with_first_four_colors_match_in_position(self):
    selected_colors = [Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW, Color.ORANGE, Color.PURPLE]
    user_provided_colors = [Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW, Color.WHITE, Color.BLACK]

    response = guess(selected_colors, user_provided_colors)

    self.assertEqual(response, {EXACT: 4, PARTIAL: 0, NOT_FOUND: 2})

  def test_guess_with_last_four_colors_match_in_position(self):
    selected_colors = [Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW, Color.ORANGE, Color.PURPLE]
    user_provided_colors = [Color.WHITE, Color.BLACK, Color.GREEN, Color.YELLOW, Color.ORANGE, Color.PURPLE]

    response = guess(selected_colors, user_provided_colors)

    self.assertEqual(response, {EXACT: 4, PARTIAL: 0, NOT_FOUND: 2})

  def test_guess_with_first_three_colors_match_in_position_and_the_last_three_match_out_of_position(self):
    selected_colors = [Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW, Color.ORANGE, Color.PURPLE]
    user_provided_colors = [Color.RED, Color.BLUE, Color.GREEN, Color.PURPLE, Color.YELLOW, Color.ORANGE]

    response = guess(selected_colors, user_provided_colors)

    self.assertEqual(response, {EXACT: 3, PARTIAL: 3, NOT_FOUND: 0})
    
  def test_guess_with_first_and_third_color_mismatch_second_in_position_and_the_others_match_out_of_position(self):
    selected_colors = [Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW, Color.ORANGE, Color.PURPLE]
    user_provided_colors = [Color.WHITE, Color.BLUE, Color.BLACK, Color.PURPLE, Color.YELLOW, Color.ORANGE]

    response = guess(selected_colors, user_provided_colors)

    self.assertEqual(response, {EXACT: 1, PARTIAL: 3, NOT_FOUND: 2})

  def test_guess_with_first_color_in_the_selected_colors_repeated_five_times(self):
    selected_colors = [Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW, Color.ORANGE, Color.PURPLE]
    user_provided_colors = [Color.RED, Color.RED, Color.RED, Color.RED, Color.RED, Color.RED]

    response = guess(selected_colors, user_provided_colors)

    self.assertEqual(response, {EXACT: 1, PARTIAL: 0, NOT_FOUND: 5})

  def test_guess_with_last_color_in_the_selected_colors_repeated(self):
    selected_colors = [Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW, Color.ORANGE, Color.PURPLE]
    user_provided_colors = [Color.PURPLE, Color.PURPLE, Color.PURPLE, Color.PURPLE, Color.PURPLE, Color.PURPLE]

    response = guess(selected_colors, user_provided_colors)

    self.assertEqual(response, {EXACT: 1, PARTIAL: 0, NOT_FOUND: 5})

  def test_guess_with_the_first_color_in_the_selected_colors_repeated_from_position_two_to_six_with_first_position_in_the_guess_having_the_second_color_in_selection(self):
    selected_colors = [Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW, Color.ORANGE, Color.PURPLE]
    user_provided_colors = [Color.BLUE, Color.RED, Color.RED, Color.RED, Color.RED, Color.RED]

    response = guess(selected_colors, user_provided_colors)

    self.assertEqual(response, {EXACT: 0, PARTIAL: 2, NOT_FOUND: 4})

  def test_guess_with_the_first_color_in_the_selected_colors_repeated_from_position_two_to_six_with_first_position_in_the_guess_having_no_match(self):
    selected_colors = [Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW, Color.ORANGE, Color.PURPLE]
    user_provided_colors = [Color.WHITE, Color.RED, Color.RED, Color.RED, Color.RED, Color.RED]

    response = guess(selected_colors, user_provided_colors)

    self.assertEqual(response, {EXACT: 0, PARTIAL: 1, NOT_FOUND: 5})

  def test_play_for_the_1st_attempt_with_exact_match(self):
    selected_colors = [Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW, Color.ORANGE, Color.PURPLE]
    user_provided_colors = selected_colors

    response, attempts_count, status = play(selected_colors, user_provided_colors, 0)

    self.assertEqual(status, GameStatus.WON) 
    self.assertEqual(attempts_count, 1)
    self.assertEqual(response, {EXACT: 6, PARTIAL: 0, NOT_FOUND: 0})

  def test_play_for_the_1st_attempt_with_no_match(self):
    selected_colors = [Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW, Color.ORANGE, Color.PURPLE]
    user_provided_colors = [Color.WHITE, Color.BLACK, Color.CYAN, Color.VIOLET, Color.WHITE, Color.BLACK]

    response, attempts_count, status = play(selected_colors, user_provided_colors, 0)

    self.assertEqual(status, GameStatus.IN_PROGRESS)
    self.assertEqual(attempts_count, 1)
    self.assertEqual(response, {EXACT: 0, PARTIAL: 0, NOT_FOUND: 6})

  def test_play_for_the_1st_attempt_with_some_exact_and_some_non_exact_match(self):
    selected_colors = [Color.RED, Color.BLUE, Color.GREEN, Color.WHITE, Color.VIOLET, Color.BLACK]
    user_provided_colors = [Color.RED, Color.BLUE, Color.GREEN, Color.VIOLET, Color.WHITE, Color.BLACK]

    response, attempts_count, status = play(selected_colors, user_provided_colors, 0)

    self.assertEqual(status, GameStatus.IN_PROGRESS)
    self.assertEqual(attempts_count, 1)
    self.assertEqual(response, {EXACT: 4, PARTIAL: 2, NOT_FOUND: 0})

  def test_play_for_the_2nd_attempt_with_exact_match(self):
    selected_colors = [Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW, Color.ORANGE, Color.PURPLE]
    user_provided_colors = selected_colors

    response, attempts_count, status = play(selected_colors, user_provided_colors, 1)

    self.assertEqual(status, GameStatus.WON) 
    self.assertEqual(attempts_count, 2)
    self.assertEqual(response, {EXACT: 6, PARTIAL: 0, NOT_FOUND: 0})

  def test_play_for_the_2nd_attempt_with_no_match(self):
    selected_colors = [Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW, Color.ORANGE, Color.PURPLE]
    user_provided_colors = [Color.WHITE, Color.BLACK, Color.CYAN, Color.VIOLET, Color.WHITE, Color.BLACK]

    response, attempts_count, status = play(selected_colors, user_provided_colors, 1)

    self.assertEqual(status, GameStatus.IN_PROGRESS)
    self.assertEqual(attempts_count, 2)
    self.assertEqual(response, {EXACT: 0, PARTIAL: 0, NOT_FOUND: 6})

  def test_play_for_the_20th_attempt_with_exact_match(self):
    selected_colors = [Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW, Color.ORANGE, Color.PURPLE]
    user_provided_colors = selected_colors

    response, attempts_count, status = play(selected_colors, user_provided_colors, 19)

    self.assertEqual(status, GameStatus.WON) 
    self.assertEqual(attempts_count, 20)
    self.assertEqual(response, {EXACT: 6, PARTIAL: 0, NOT_FOUND: 0})

  def test_play_for_the_20th_attempt_with_no_match(self):
    selected_colors = [Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW, Color.ORANGE, Color.PURPLE]
    user_provided_colors = [Color.WHITE, Color.BLACK, Color.CYAN, Color.VIOLET, Color.WHITE, Color.BLACK]

    response, attempts_count, status = play(selected_colors, user_provided_colors, 19)

    self.assertEqual(attempts_count, 20)
    self.assertEqual(status, GameStatus.LOST)
    self.assertEqual(response, {EXACT: 0, PARTIAL: 0, NOT_FOUND: 6})

  def test_play_for_the_21st_attempt_with_exact_match(self):
    selected_colors = [Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW, Color.ORANGE, Color.PURPLE]
    user_provided_colors = selected_colors

    with self.assertRaises(Exception) as message: play(selected_colors, user_provided_colors, 20)
    self.assertEqual(str(message.exception), EXCEPTION_MESSAGE)

  def test_play_for_the_21th_attempt_with_no_match(self):
    selected_colors = [Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW, Color.ORANGE, Color.PURPLE]
    user_provided_colors = [Color.WHITE, Color.BLACK, Color.CYAN, Color.VIOLET, Color.WHITE, Color.BLACK]

    with self.assertRaises(Exception) as message: play(selected_colors, user_provided_colors, 20)
    self.assertEqual(str(message.exception), EXCEPTION_MESSAGE)

  def test_randomize_selected_colors_given(self):
    selected_colors = select_colors(10)

    self.assertEqual(len(selected_colors), 6)
    self.assertTrue(all(color in Color for color in selected_colors))
    
  def test_randomize_selected_colors_is_different_when_called_twice(self):
    selected_colors_1 = select_colors(10)
    selected_colors_2 = select_colors(20)

    self.assertNotEqual(selected_colors_1, selected_colors_2)

if __name__ == '__main__': 
  unittest.main()
