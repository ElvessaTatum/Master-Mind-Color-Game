from enum import Enum
from collections import Counter
import random

class Color(Enum):
    RED = 1
    BLUE = 2
    GREEN = 3
    YELLOW = 4
    ORANGE = 5
    PURPLE = 6
    CYAN = 7
    VIOLET = 8
    WHITE = 9
    BLACK = 10

class Match(Enum):
    EXACT = "Exact Match"
    PARTIAL = "Partial Match"
    NOT_FOUND = "Mismatch"

class GameStatus(Enum):
   WON = "Won"
   IN_PROGRESS = "In Progress"
   LOST = "Lost"

def guess(user_provided_colors, selected_colors):
  def match_for_position(position):
    candicate_color = user_provided_colors[position]

    if candicate_color == selected_colors[position]:
      return Match.EXACT

    index = selected_colors.index(candicate_color) if candicate_color in selected_colors else -1
     
    if index > -1 and selected_colors[index] != user_provided_colors[index]:
      return Match.PARTIAL
 
    return Match.NOT_FOUND

  return {**{Match.EXACT: 0, Match.PARTIAL: 0, Match.NOT_FOUND: 0}, **Counter(map(match_for_position, range(0, len(selected_colors))))}

def play(selected_colors, user_provided_colors, number_of_attempts):
  response = guess(selected_colors, user_provided_colors)
  MAX_ATTEMPTS = 20

  if number_of_attempts >= MAX_ATTEMPTS:
    raise Exception("Maximum number of attempts exceeded.")
  
  status = GameStatus.IN_PROGRESS

  if response[Match.EXACT] == len(selected_colors):
    status = GameStatus.WON
    
  if response[Match.EXACT] != len(selected_colors) and number_of_attempts == MAX_ATTEMPTS - 1:
    status = GameStatus.LOST
 
  return response, number_of_attempts + 1, status

def select_colors(random_seed):
    random.seed(random_seed)
    ANSWER_LENGTH = 6
    
    return random.sample(list(Color), ANSWER_LENGTH)
