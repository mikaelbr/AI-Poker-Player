import cards
import player
import poker

class Phase1(player.Player):
  def take_action(self, highest_bet, pot, players, position, shared_cards):
    if(self.play_style == "tight_passive"):
      return self.take_tight_passive_action(highest_bet, pot, players, position, shared_cards)
    elif self.play_style == "loose_passive":
      #This is what we want...
      #take_loose_passive_action(self, highest_bet, pot, players, position, shared_cards)
      #but for now, we will all be tight-passive :)
      return self.take_tight_passive_action(highest_bet, pot, players, position, shared_cards)
    elif self.play_style == "tight_aggressive":
      #This is what we want...
      #take_tight_aggressive_action(self, highest_bet, pot, players, position, shared_cards)
      #but for now, we will all be tight-passive :)
      return self.take_tight_passive_action(highest_bet, pot, players, position, shared_cards)
    else:
      #This is what we want...
      #take_loose_aggressive_action(self, highest_bet, pot, players, position, shared_cards)
      #but for now, we will all be tight-passive :)
      return self.take_tight_passive_action(highest_bet, pot, players, position, shared_cards)
  
  def take_tight_aggressive_action(self, highest_bet, pot, players, position, shared_cards):
    ranking = cards.calc_cards_power(self.cards + shared_cards) # calculate hand ranking

    if len(shared_cards) < 1: # pre-flop
      pass
    else:
      pass # post-flop

  def take_tight_passive_action(self, highest_bet, pot, players, position, shared_cards):
    ranking = cards.calc_cards_power(self.cards + shared_cards) # calculate hand ranking

    if len(shared_cards) < 1: # pre-flop

      # check for pair, high cards, suited, high card suited. 
      if ranking[0] == 2 and ranking[1] > 9 and self.raise_count < 3:
        # raise if not already committed equally to highest bet
        # check otherwise (call 0)
        if(self.sum_pot_in == highest_bet):
          return self.call_action(highest_bet)
        else:
          return self.raise_action(highest_bet)

      elif ranking[0] == 1 and ranking[1] > 10 and ranking[2] > 10: # high card
        # call
        return self.call_action(highest_bet)

      elif self.cards[0][1] == self.cards[1][1] and ranking[1] > 10 and ranking[2] > 10: # suited high
        # call
        return self.call_action(highest_bet)

      elif self.sum_pot_in == highest_bet:
        # check
        return self.call_action(highest_bet)

      else:
        # fold
        return self.fold_action()

    else: # post-flop
      if ((ranking[0] == 3 and ranking[1] > 10 and ranking[2] > 10) or (ranking[0] == 4 and ranking[1] > 7) or (ranking[0] > 4)) and self.raise_count < 3:
        # raise if not already committed equally to highest bet
        # check otherwise (call 0)
        if(self.sum_pot_in == highest_bet):
          return self.call_action(highest_bet)
        else:
          return self.raise_action(highest_bet)

      elif highest_bet != self.sum_pot_in and ((ranking[0] == 1) or (ranking[0] == 2 and ranking[1] < 12) ):
        # fold
        return self.fold_action()

      else:
        # call/check
        return self.call_action(highest_bet)


# Play styles:
# "tight_passive"
# "tight_aggressive"
# "loose_passive"
# "loose_aggressive"

'''
players = [
  Phase1("Mikael", 1000, "loose_aggressive"), 
  Phase1("Marius", 1000, "loose_aggressive"),
  Phase1("Martin", 1000, "loose_aggressive"),
  Phase1("Jostein", 1000, "loose_passive"),
  Phase1("Emil", 1000, "loose_passive"),
  Phase1("Steinar", 1000, "loose_passive"),
  Phase1("Stian", 1000, "loose_passive"),
  Phase1("Selmer", 1000, "tight_passive"),
  Phase1("Ole Jorgen", 1000, "tight_passive"),
  Phase1("Andre the giant", 1000, "tight_aggressive")
]

p = poker.poker(players, 1000);
'''
