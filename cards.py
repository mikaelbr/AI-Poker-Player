#!/usr/bin/env python3

# Primitives for card-playing, particularly poker.

import random
import math

# A few global variables
_card_value_names_ = [2,3,4,5,6,7,8,9,10,'jack','queen','king','ace']
_card_suits_ = {'S':'Spade','H':'Heart','C':'Club','D':'Diamond'} # A dictionary

# The basic card data structure: a 2-element list

def create_card (value, suit): return [value, suit]

def card_value(card): return card[0]
def card_suit(card): return card[1]

def card_value_name(card): return card_value_to_name(card_value(card))
def card_value_to_name(val): return _card_value_names_[val-2]

def card_suit_name(card): return _card_suits_[card_suit(card)]
def get_all_suits(): return _card_suits_.keys()

def card_name(card): return [card_value_name(card), card_suit_name(card)]
def card_names(cards): return [card_name(c) for c in cards]

def quick_cards (name_suit_list):
   return [create_card(spec[0],spec[1]) for spec in name_suit_list]

def is_jack (card): return card_value(card) == 11
def is_queen (card): return card_value(card) == 12
def is_king (card): return card_value(card) == 13
def is_ace (card): return card_value(card) == 14

def card_eq (c1, c2):
    return card_value(c1) == card_value(c2) and card_suit(c1) == card_suit(c2)

def copy_card(c): return create_card(card_value(c),card_suit(c))
def copy_cards(cards): return [copy_card(c) for c in cards]

# Create a list of 52 standard playing cards
def gen_52_cards():
    deck = []
    for suit in get_all_suits():
       for v in range(2,15):
         deck.append(create_card(v,suit))
    return deck

# Shuffle a set of cards 'reps number of times
def shuffle_cards(cards, reps = 1):
  for rep in range(reps):
    new_cards = []
    for i in range(len(cards)-1,-1,-1):
      index =random.randint(0,i)
      new_cards.append(cards[index])
      cards[index:index+1] = [] # Removing the indexed item
    cards = new_cards
  return cards

def gen_52_shuffled_cards(reps = 5):
    d = gen_52_cards()
    return shuffle_cards(d,reps=reps)

def gen_random_cards(count, reps = 5):
    d = gen_52_shuffled_cards(reps = reps)
    return d[0:count]

# Sorting cards

# Auxiliary funcs copied from prims/prims1.py

def find_list_item(L,item,key=(lambda x: x)):
    for x in L:
      if item == key(x):
        return x

def kd_sort(elems, prop_func = (lambda x: x), dir = 'increase'): 
    elems.sort(key=prop_func) # default of the sort func is increasing order
    if dir =='decrease' or dir =='decr':
      elems.reverse()

# This groups a set of elements by shared values of a specified property (which is determined by
# prop_func), where the equality of two values is determined by eq_func.  For example, this might
# be used to group a set of cards by card-value.  Then all the 5's would be returned as one group, all
# the queens as another, etc.

def partition(elems, prop_func = (lambda x:x), eq_func = (lambda x,y: x == y)):
    kd_sort(elems,prop_func=prop_func)
    partition = []
    subset = False
    last_key = False
    counter = 0
    for elem in elems:
      new_key = prop_func(*[elem])
      if not(subset) or not(eq_func(*[last_key,new_key])):
        if subset: partition.append(subset)
        subset = [elem]
        last_key = new_key
      else: subset.append(elem)
    if subset: partition.append(subset)
    return partition

# This partitions elements and then sorts the groups by the subset_prop function, which defaults to group size.
# Thus, using the defaults, the largest groups would be at the beginning of the sorted partition.

def sorted_partition(elems,elem_prop = (lambda x:x), subset_prop = (lambda ss: len(ss)), eq_func = (lambda x,y: x ==y), dir = "decrease"):
    p = partition(elems,prop_func = elem_prop, eq_func = eq_func)
    kd_sort(p,prop_func = subset_prop,dir = dir)
    return p

def sort_cards(cards, prop_func = (lambda c: card_value(c)), dir = 'decrease'):
    kd_sort(cards,prop_func=prop_func,dir=dir)

# Group a set of cards by suit
def gen_suit_groups(cards):
    new_cards = copy_cards(cards)
    return sorted_partition(new_cards,elem_prop = (lambda c: card_suit(c)))

# Group a set of cards by value
def gen_value_groups(cards):
    new_cards = copy_cards(cards)
    return sorted_partition(new_cards,elem_prop = (lambda c: card_value(c)))

# Sort a set of cards in ascending or descending order, based on the card value (e.g. 3,7,queen,ace, etc.)
def gen_ordered_cards(cards, dir = 'increase'):
    new_cards = copy_cards(cards)
    kd_sort(new_cards,prop_func=(lambda c: card_value(c)),dir = dir)
    return new_cards

# This is the most important function in this file.  It takes a set of cards and computes
# their power rating, which is a list of integers, the first of which indicates the type of
# hand: 9 - straight flush, 8 - 4 of a kind, 7 - full house, 6 - flush, 5 - straight, 4 - 3 of  kind
# 3 - two pair, 2 - one pair, 1 - high card.  The remaining integers are tie-breaker information
# required in cases where, for example, two players both have a full house.

def calc_cards_power (cards, target_len = 5):

    def has_len (length, items): return length == len(items)

    vgroups = gen_value_groups(cards)
    flush = find_flush(cards, target_len = target_len)
    if flush:
      str_in_flush = find_straight(flush,target_len = target_len)
    if flush and str_in_flush:
      return calc_straight_flush_power(str_in_flush)
    elif has_len(4, vgroups[0]):
      return calc_4_kind_power(vgroups)
    elif has_len(3, vgroups[0]) and len(vgroups) > 1 and len(vgroups[1]) >= 2: 
        return calc_full_house_power(vgroups)
    elif flush:
      return calc_simple_flush_power(flush)
    else:
      straight = find_straight(cards)
      if straight:
        return calc_straight_power(straight)
      elif has_len(3,vgroups[0]):
        return calc_3_kind_power(vgroups)
      elif has_len(2,vgroups[0]):
        if len(vgroups) > 1 and has_len(2,vgroups[1]):
          return calc_2_pair_power(vgroups)
        else: return calc_pair_power(vgroups)
      else: return calc_high_card_power(cards)

def card_power_greater(p1,p2): # Both are power ratings = lists of power integers returned by calc_cards_power
    if not(p1) or not(p2):
      return False
    elif p1[0] == p2[0]:
      return card_power_greater(p1[1:],p2[1:])
    elif p1[0] > p2[0]:
      return True
    else: return False

# Functions for finding flushes and straights in a set of cards (of any length)

def find_flush(cards, target_len = 5):
  sgroups = gen_suit_groups(cards)
  if len(sgroups[0]) >= target_len:
      return sgroups[0]
  else: return False

def find_straight(cards, target_len = 5):
    ace = find_list_item(cards,14,key=(lambda c: card_value(c)))
    scards = gen_ordered_cards(cards, dir = 'decrease')

    def scan(cards, straight):
      if len(straight) == target_len:
        return straight
      elif ace and 2 == card_value(straight[0]) and len(straight) == target_len - 1:
        return [ace] + straight
      elif not(cards):
        return False # null check is late since variable 'cards not involved in 1st 2 cases
  
      c = cards.pop(0)
      if card_value(c) == card_value(straight[0]) - 1:
        return scan(cards,[c] + straight)
      elif card_value(c) == card_value(straight[0]):
        return scan(cards,straight)
      else: # Broken straight, so start again with the current card
        return scan(cards,[c])

    top_card = scards.pop(0)
    return scan(scards,[top_card])

# Simple auxiliary function for finding and sorting all card values in a set of card groups, and then returning
# the largest 'count of them.
def max_group_vals(groups,count):
   vals = [card_value(g[0]) for g in groups]
   kd_sort(vals,dir='decrease')
   return vals[0:count]
   

# Straights are presumably sorted in ASCENDING order
def calc_straight_flush_power(straight):
    return [9,card_value(straight[-1])]

def calc_4_kind_power(value_groups):
    return [8,card_value(value_groups[0][0])] + max_group_vals(value_groups[1:],1)

def calc_full_house_power(value_groups):
    return [7] + [card_value(vg[0]) for vg in value_groups[0:2]]

def calc_simple_flush_power(flush, target_len = 5):
  new_flush = copy_cards(flush)
  sort_cards(new_flush)
  return [6] + [card_value(c) for c in new_flush[0:target_len]]

def calc_straight_power(straight):
    return [5,card_value(straight[-1])]

def calc_3_kind_power(value_groups):
    return [4,card_value(value_groups[0][0])] + max_group_vals(value_groups[1:],2)


def calc_2_pair_power(value_groups):
    return [3,card_value(value_groups[0][0]),card_value(value_groups[1][0])] + max_group_vals(value_groups[2:],1)

def calc_pair_power(value_groups):
    return [2,card_value(value_groups[0][0])] + max_group_vals(value_groups[1:],3)

def calc_high_card_power(cards):
    ocards = gen_ordered_cards(cards,dir='decrease')
    return [1] + [card_value(c) for c in ocards][0:5]

# A simple card-deck class
class card_deck():

  def __init__(self, shuffles = 10):
    self.shuffle_reps = shuffles
    self.cards = []
    self.reset()

  def reset(self):
    self.cards =  gen_52_shuffled_cards(reps = self.shuffle_reps)

  def deal_one_card(self):
    if self.cards:
      return self.cards.pop(0)
    else:
      print("The deck is empty")
      return False

  def deal_n_cards(self,n):
    cards = []
    for i in range(n):
      card = self.deal_one_card()
      if card:
        cards.append(card)
      else:
        print("Not enough cards in the deck")
        return False
    return cards
    
  def num_cards(self):
    return len(self.cards)

# Main routine for testing the generation and classification (via power ratings) of many poker hands.
def power_test(hands, hand_size = 7):
    for i in range(hands):
      deck = card_deck()
      cards = deck.deal_n_cards(hand_size)
      print("Hand: " , card_names(cards), '  Power: ', calc_cards_power(cards))
    

class poker():

  def __init__(self, players, n_rounds = 1, n_games = 1, force_log = False):
    self.n_games = n_games
    self.n_rounds = n_rounds
    self.show_data = n_games < 2 or force_log
    self.players = players
    self.start_game()
    self.last_raise = 0


  def start_game(self):
    self.deck = card_deck()
    self.pot = 0
    
    # Main game loop/structure. Based on Texas Hold 'Em rules
    for i in range(self.n_rounds):

      self.round = i
      self.log("---- Round #", self.round, "----")

      # Suffle for big blind/small blind
      if(i != 0):
        self.players.append(self.active_players.pop(0))
        self.players.append(self.active_players.pop(0))

      # Reset info.
      self.flop = []
      self.turn = []
      self.river = []
      self.shared_cards = []
      self.active_players = self.players

      
      
      self.log("Small blind:", self.active_players[1].name)
      self.log("Big blind:", self.active_players[2].name)

      self.active_raise = 0

      # Deal hole cards
      j = 0
      for p in self.active_players:
        j += 1 
        p.new_round((j==1), (j==2))
        p.set_cards(self.deck.deal_n_cards(2))

      self.show_player_stats()

      

      self.do_betting_round()
      self.deal_flop()
      self.do_betting_round()
      self.deal_turn()
      self.do_betting_round()
      self.deal_river()
      self.do_betting_round()
      self.calculate_win()

      # Serve a fresh deck
      self.deck.reset()
      



  def deal_flop(self):
    self.flop = self.deck.deal_n_cards(3)
    self.shared_cards = self.flop
    self.log("Round #", self.round, ", Flop:", card_names(self.flop))
    self.show_shared_cards()
    self.show_player_stats()

  def deal_turn(self):
    self.turn = self.deck.deal_one_card()

    self.log("Round #", self.round, "- Turn:", card_name(self.turn))
    
    self.shared_cards += [self.turn]
    self.show_shared_cards()
    self.show_player_stats()

  def deal_river(self):
    self.river = self.deck.deal_one_card()

    self.log ("Round #", self.round, "- River:", card_name(self.river))

    self.shared_cards += [self.river]
    self.show_shared_cards()
    self.show_player_stats()

  def do_betting_round(self):
    for p in self.active_players:
      p.take_action(self.active_raise)
    


  def calculate_win(self):
    # Winning calcs 
    pass

  def show_shared_cards(self):
    self.log("Shared cards:", card_names(self.shared_cards))

  def show_player_stats(self):
    self.log("------ Player stats -----")
    for p in self.players:
      p.print_info(self.shared_cards)
    self.log("---- END Player stats ---")

  def log(self, *message, **argv):
    if (self.show_data): 
      # print(*message, sep=" ", end=".\n") # Python 3.0 syntax
      print message # python 2 syntax




# Base class. 
class Player():

  _raise_limit = 30

  def __init__(self, name, money):
    self.money = money
    self.name = name
    self.sum_pot_in = 0
    self.is_blind = False

  def set_cards(self, cards):
    self.cards = cards

  def show_cards(self):
    return self.cards
  
  def new_round(self, is_small = False, is_big = False):
    self.sum_pot_in = 0
    self.is_blind = is_big or is_small

    if (is_big):
      return self.call_action(self._raise_limit)
    elif (is_small):
      return self.call_action(self._raise_limit/2)

  def fold_action(self):
    self.sum_pot_in = 0
    return False

  def call_action(self, last_opponent_raise):
    deducted = last_opponent_raise
    self.sum_pot_in += deducted
    self.money -= deducted
    return deducted

  def raise_action(self, last_opponent_raise):
    deducted = self._raise_limit + last_opponent_raise
    self.sum_pot_in += deducted
    self.money -= deducted
    return deducted

  def win(self, pot):
    self.money += pot

  def print_info(self, shared_cards):
    print(self.name, " (", self.money, "credits):", card_names(self.cards), calc_cards_power(self.cards + shared_cards))


class Phase1(Player):

  def take_action(self, last_opponent_raise):
    if (self.is_blind):
      print("Her")



players = [
  Phase1("Mikael", 1000), 
  Phase1("Marius", 1000),
  Phase1("Martin", 1000)
]

p = poker(players, 10);



  