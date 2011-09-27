import cards
import player
import poker

class Phase1(player.Player):
  def take_action(self, highest_bet, pot, players, position, shared_cards, state, total_raises):
    if(self.play_style == "tight_passive"):
      return self.take_tight_passive_action(highest_bet, pot, players, position, shared_cards, state, total_raises)
    elif self.play_style == "loose_passive":
      #This is what we want...
      #take_loose_passive_action(self, highest_bet, pot, players, position, shared_cards)
      #but for now, we will all be tight-passive :)
      return self.take_tight_passive_action(highest_bet, pot, players, position, shared_cards, state, total_raises)
    elif self.play_style == "tight_aggressive":
      #This is what we want...
      #take_tight_aggressive_action(self, highest_bet, pot, players, position, shared_cards)
      #but for now, we will all be tight-passive :)
      return self.take_tight_passive_action(highest_bet, pot, players, position, shared_cards, state, total_raises)
    else:
      #This is what we want...
      return self.take_loose_aggressive_action(highest_bet, pot, players, position, shared_cards, state, total_raises)
      #but for now, we will all be tight-passive :)
      #return self.take_tight_passive_action(highest_bet, pot, players, position, shared_cards, state, total_raises)
  
  def take_loose_aggressive_action(self, highest_bet, pot, players, position, shared_cards, state, total_raises):
    #1. Highest card
    #2. One pair
    #3. Two pair
    #4. 3 of a kind
    #5. Straight
    #6. Flush
    #7. Full House
    #8. 4 of a kind
    #9. Straight Flush - with Royal Flush being the highest of these

    ranking = cards.calc_cards_power(self.cards + shared_cards) # calculate hand ranking
    action = ""
    ret = None

    if state == 1:
      # Pre-flop
      if ranking[0] == 1 and ranking[1] > 12: #High card and highest card is above 10
        # Raise
        if(self.raise_count > 5):
          self.last_action = "call"
          ret = self.call_action(highest_bet)
        else:
          if(self.sum_pot_in == highest_bet):
            self.last_action = "check"
            ret = self.call_action(highest_bet)
          else:
            self.last_action = "raise"
            ret = self.raise_action(highest_bet)
      elif ranking[0] == 2: # Hole pair.. RAISE!
        if(self.raise_count > 5):
          self.last_action = "call"
          ret = self.call_action(highest_bet)
        else:
          if(self.sum_pot_in == highest_bet):
            self.last_action = "check"
            ret = self.call_action(highest_bet)
          else:
            self.last_action = "raise"
            ret = self.raise_action(highest_bet)
      else:
        if(self.sum_pot_in == highest_bet):
          self.last_action = "check"
          ret = self.call_action(highest_bet)
        else:
          ret = self.fold_action()
    elif state >= 2:
      # Post-flop
      if(self.raise_count > 5):
        self.last_action = "call"
        ret = self.call_action(highest_bet)
      else:
        if ranking[0] == 2 and players < 4 and self.sum_pot_in != highest_bet:
          self.last_action = "raise"
          ret = self.raise_action(highest_bet)
        elif ranking[0] > 3 and self.sum_pot_in != highest_bet:
          self.last_action = "raise"
          ret = self.raise_action(highest_bet)
        elif self.sum_pot_in == highest_bet:
          self.last_action = "check"
          ret = self.call_action(highest_bet)
        else:
          ret = self.fold_action()        
    else:
      ret = self.fold_action()
    
    if action != "":
      self.take_action_super(highest_bet, pot, players, position, shared_cards, state, total_raises, self.last_action)

    #print("DEBUG RET FROM AGGRESSIVE ===================== ", ret)
    return ret

  def take_tight_passive_action(self, highest_bet, pot, players, position, shared_cards, state, total_raises):
    #1. Highest card
    #2. One pair
    #3. Two pair
    #4. 3 of a kind
    #5. Straight
    #6. Flush
    #7. Full House
    #8. 4 of a kind
    #9. Straight Flush - with Royal Flush being the highest of these

    ranking = cards.calc_cards_power(self.cards + shared_cards) # calculate hand ranking

    action = ""

    if len(shared_cards) < 1: # pre-flop
      # check for pair, high cards, suited, high card suited. 
      if ranking[0] == 2 and ranking[1] > 9 and self.raise_count < 3:
        # raise if not already committed equally to highest bet
        # check otherwise (call 0)
        if(self.sum_pot_in == highest_bet):
          action = "check"
          ret = self.call_action(highest_bet)
        else:
          action = "raise"
          ret = self.raise_action(highest_bet)

      elif ranking[0] == 1 and ranking[1] > 10 and ranking[2] > 10: # high card
        # call
        action = "call"
        ret = self.call_action(highest_bet)

      elif self.cards[0][1] == self.cards[1][1] and ranking[1] > 10 and ranking[2] > 10: # suited high
        # call
        action = "call"
        ret = self.call_action(highest_bet)

      elif self.sum_pot_in == highest_bet:
        # check, we use call for this purpose(calls 0)
        action = "check"
        ret = self.call_action(highest_bet)

      else:
        # fold
        return self.fold_action()

    else: # post-flop
      if ((ranking[0] == 3 and ranking[1] > 10 and ranking[2] > 10) or (ranking[0] == 4 and ranking[1] > 7) or (ranking[0] > 4)) and self.raise_count < 3:
        # raise if not already committed equally to highest bet
        # check otherwise (call 0)
        if(self.sum_pot_in == highest_bet):
          action = "check"
          ret = self.call_action(highest_bet)
        else:
          action = "raise"
          ret = self.raise_action(highest_bet)

      elif highest_bet != self.sum_pot_in and ((ranking[0] == 1) or (ranking[0] == 2 and ranking[1] < 12) ):
        # fold
        return self.fold_action()

      else:
        # call/check
        action = "call" if highest_bet != self.sum_pot_in else "check"
        ret = self.call_action(highest_bet)
    
    if action != "":
      self.take_action_super(highest_bet, pot, players, position, shared_cards, state, total_raises, self.last_action)

    return ret


# Play styles:
# "tight_passive"
# "loose_aggressive"

players = [
  Phase1("Mikael", 1000, "loose_aggressive"),
  Phase1("Marius", 1000, "tight_passive"),
  Phase1("Martin", 1000, "loose_agressive"),
  Phase1("Jostein", 1000, "tight_passive"),
  Phase1("Emil", 1000, "tight_passive"),
  Phase1("Steinar", 1000, "tight_passive"),
  Phase1("Stian", 1000, "tight_passive"),
  #Phase1("Selmer", 1000, "tight_passive"),
  #Phase1("Ole Jorgen", 1000, "tight_passive"),
  #Phase1("Andre the giant", 1000, "tight_aggressive")
]

#p = poker.poker(players, 250, debug_mode=False);
p = poker.poker(players, 1000, debug_mode=True);
