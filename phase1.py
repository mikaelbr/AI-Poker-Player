import cards

class Phase1(cards.Player):

  def take_action(self, highest_bet, pot, players, position, shared_cards):
    ranking = cards.calc_cards_power(self.cards + shared_cards) # calculate hand ranking
    

    if len(shared_cards) < 1: # pre-flop

      # check for pair, high cards, suited, high card suited. 
      if ranking[0] == 2 and ranking[1] > 9 and self.raise_count < 3:
        # raise
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
        # raise
        return self.raise_action(highest_bet)

      elif highest_bet != self.sum_pot_in and ((ranking[0] == 1) or (ranking[0] == 2 and ranking[1] < 12) ):
        # fold
        return self.fold_action()

      else:
        # call/check
        return self.call_action(highest_bet)





players = [
  Phase1("Mikael", 1000), 
  Phase1("Marius", 1000),
  Phase1("Martin", 1000),
  Phase1("Jostein", 1000),
  Phase1("Emil", 1000)
]

p = cards.poker(players, 20);

