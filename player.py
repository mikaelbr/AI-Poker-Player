import cards

# Base class. 
class Player():

  _raise_limit = 30

  def __init__(self, name, money, play_style):
    self.money = money
    self.name = name
    self.sum_pot_in = 0
    self.is_blind = False
    self.last_bet = 0
    self.raise_count = 0
    self.play_style = play_style

  def set_cards(self, cards):
    self.cards = cards

  def show_cards(self):
    return self.cards
  
  def new_round(self, is_small = False, is_big = False):
    self.sum_pot_in = 0
    self.is_blind = is_big or is_small


    if (is_big):
      print("Big blind:", self.name)
      return self.bet_action(self._raise_limit)
    elif (is_small):
      print("Small blind:", self.name)
      return self.bet_action(self._raise_limit/2)
    else:
      return 0

  def fold_action(self):
    print("Player", self.name, "folded")
    self.sum_pot_in = 0
    return False

  def call_action(self, highest_bet):
    deducted = highest_bet - self.sum_pot_in
    self.sum_pot_in += deducted
    # self.sum_pot_in = 0
    self.money -= deducted
    print("Player", self.name, "called" if deducted > 0 else "checked", "with", deducted, "and has a total of", self.sum_pot_in, "in the pot")
    return [0, deducted]

  def raise_action(self, highest_bet):
    print("Player", self.name, "has", self.money, "BEFORE raising")
    self.raise_count += 1
    print("raise_limit: ", self._raise_limit, " highest_bet:", highest_bet, " sum_pot_in:", self.sum_pot_in)
    print("raise_count: ", self.raise_count)
    deducted = self._raise_limit + highest_bet - self.sum_pot_in
    self.sum_pot_in += deducted
    self.money -= deducted
    self.last_bet = self.sum_pot_in
    # Uncomment after testing - self.last_bet = deducted
    # self.sum_pot_in = 0
    print("Player", self.name, "raised  with", deducted, "and has a total of", self.sum_pot_in, "in the pot")
    # Put this between "raised with" and deducted. If needed
    # deducted-self._raise_limit if highest_bet > 0 else
    print("Player", self.name, "has", self.money, "AFTER raising, and last bet is", self.last_bet)
    return [1, deducted]

  def bet_action(self, bet):
    self.sum_pot_in += bet
    self.money -= bet
    self.last_bet = bet
    return bet

  def win(self, pot):
    self.money += float(pot)
    self.sum_pot_in = 0

  def print_info(self, shared_cards):
    print(self.name, "- play style: "+self.play_style, "(", self.money, "credits):", cards.card_names(self.cards), cards.calc_cards_power(self.cards + shared_cards))