import cards
import player
import poker
import hand_strength
import pickle
import phase1
import phase2
import db_con


class Phase3(player.Player):

  def opponent_model_update_array (self, highest_bet, pot, players, position, shared_cards, state, total_raises, active_players):

    pot_odds = (float(highest_bet)/(float(highest_bet)+float(pot)))
    context = player.db.generate_context(state, players, total_raises, pot_odds)

    in_checker = [] # array used to double check that the players haven't dropped out (folded)

    # Now we can use context to check all players 
    # Iterate over the players who has already played their hand this round and overwrite the previous value. 
    for p in active_players:
      if p == None or p.name == self.name: # continue next iteration if player not active 
        continue

      in_checker.append(p.name)
      self.calculated_opponent_models[p.name] = player.db.get_hand_strength(context, p.name, p.last_action)


    # Remove all models of folded players
    for k, v in self.calculated_opponent_models.copy().items():
      if k not in in_checker:
        del self.calculated_opponent_models[k]


  def take_action(self, highest_bet, pot, players, position, shared_cards, state, total_raises, active_players):
    # generate_context(betting_round, players_remaining, num_raises, pot_odds)
    # get_hand_strength(context, player, action)
    # self.calculated_opponent_models

    pot_odds = (float(highest_bet)/(float(highest_bet)+float(pot)))
    context = player.db.generate_context(state, players, total_raises, pot_odds)

    in_checker = [] # array used to double check that the players haven't dropped out (folded)

    # Now we can use context to check all players 
    # Iterate over the players who has already played their hand this round and overwrite the previous value. 
    for p in active_players:
      if p == None: # continue next iteration if player not active 
        continue

      if p.name == self.name: #check for self if so drop out
        break

      in_checker.append(p.name)
      self.calculated_opponent_models[p.name] = player.db.get_hand_strength(context, p.name, p.last_action)

    # Remove all models of folded players
    for k, v in self.calculated_opponent_models.copy().items():
      if k not in in_checker:
        del self.calculated_opponent_models[k]

    # Now we can use the self.calculated_opponent_models dictionary to 
    # see if any of the players have a exceptionally good hand

    # Find the highest strength of an opponent. 
    highest_strength = 0
    for k, s in self.calculated_opponent_models.items():
      if s > highest_strength and k != self.name:
        highest_strength = s


    # Begin intelligent behaviour....
    if state == 1: # Pre-flop
      # Take hand strength into account?
      # Fetch information from stored data for rollout simulations.

      strength = phase2.fetch_rollout_data(players, self.cards)

    else: # post-flop
      # Use hand strength calculations

      hand = hand_strength.HandStrength(players)
      strength = hand.calculate(self.cards, shared_cards)

    
    # We now have strength. Use this to take actions. 
    if not strength:
      strength = 0

    if(self.play_style == "loose_aggressive"):
      return self.take_loose_aggressive_action(highest_bet, pot, players, position, shared_cards, state, total_raises, strength, highest_strength)
    else:
      return self.take_tight_passive_action(highest_bet, pot, players, position, shared_cards, state, total_raises, strength, highest_strength)
    
    
  def take_loose_aggressive_action(self, highest_bet, pot, players, position, shared_cards, state, total_raises, strength, highest_strength):
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
      if (ranking[0] == 1 and ranking[1] > 12) or (ranking[0] == 2) or (strength > 0.30 and highest_strength != 0 and strength > (highest_strength - 0.2)): #High card and highest card is above 10 or pair or strength > 30%
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
      else:
        if(self.sum_pot_in == highest_bet):
          self.last_action = "check"
          ret = self.call_action(highest_bet)
        else:
          return self.fold_action()
    elif state >= 2:
      # Post-flop
      if(self.raise_count > 5):
        self.last_action = "call"
        ret = self.call_action(highest_bet)
      else:
        if (ranking[0] == 2 and players < 4 and self.sum_pot_in != highest_bet) or (strength > 0.30 and highest_strength != 0 and strength > (highest_strength - 0.2)) or (ranking[0] > 3 and self.sum_pot_in != highest_bet):
          self.last_action = "raise"
          ret = self.raise_action(highest_bet)
        elif self.sum_pot_in == highest_bet:
          self.last_action = "check"
          ret = self.call_action(highest_bet)
        else:
          return self.fold_action()        
    else:
      return self.fold_action()
    
    if self.last_action != "":
      self.take_action_super(highest_bet, pot, players, position, shared_cards, state, total_raises, self.last_action)

    print("DEBUG RET FROM AGGRESSIVE ===================== ", ret)
    return ret

  def take_tight_passive_action(self, highest_bet, pot, players, position, shared_cards, state, total_raises, strength, highest_strength):
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

    self.last_action = ""

    if len(shared_cards) < 1: # pre-flop
      # check for pair, high cards, suited, high card suited. 
      if (ranking[0] == 2 and ranking[1] > 9 and self.raise_count < 3) or (strength > 0.7 and highest_strength != 0 and strength > (highest_strength)):
        # raise if not already committed equally to highest bet
        # check otherwise (call 0)
        if(self.sum_pot_in == highest_bet):
          self.last_action = "check"
          ret = self.call_action(highest_bet)
        else:
          self.last_action = "raise"
          ret = self.raise_action(highest_bet)

      elif (ranking[0] == 1 and ranking[1] > 10 and ranking[2] > 10) or (strength > 0.5 and highest_strength != 0 and strength > (highest_strength-0.1)): # high card
        # call
        self.last_action = "call"
        ret = self.call_action(highest_bet)

      elif self.cards[0][1] == self.cards[1][1] and ranking[1] > 10 and ranking[2] > 10: # suited high
        # call
        self.last_action = "call"
        ret = self.call_action(highest_bet)

      elif self.sum_pot_in == highest_bet:
        # check, we use call for this purpose(calls 0)
        self.last_action = "check"
        ret = self.call_action(highest_bet)

      else:
        # fold
        return self.fold_action()

    else: # post-flop
      if ((ranking[0] == 3 and ranking[1] > 10 and ranking[2] > 10) or (ranking[0] == 4 and ranking[1] > 7) or (ranking[0] > 4) or (strength > 0.7 and highest_strength != 0 and strength > (highest_strength))) and self.raise_count < 3:
        # raise if not already committed equally to highest bet
        # check otherwise (call 0)
        if(self.sum_pot_in == highest_bet):
          self.last_action = "check"
          ret = self.call_action(highest_bet)
        else:
          self.last_action = "raise"
          ret = self.raise_action(highest_bet)

      elif (highest_bet != self.sum_pot_in and ((ranking[0] == 1) or (ranking[0] == 2 and ranking[1] < 12) )) or strength < 0.3 or (highest_strength != 0 and highest_strength-0.1 > strength):
        # fold
        return self.fold_action()

      else:
        # call/check
        self.last_action = "call" if highest_bet != self.sum_pot_in else "check"
        ret = self.call_action(highest_bet)
    
    if self.last_action != "":
      self.take_action_super(highest_bet, pot, players, position, shared_cards, state, total_raises, self.last_action)

    return ret


# Play styles:
# "tight_passive"
# "loose_aggressive"

players = [
  Phase3("Mikael", 1000, "loose_aggressive"), 
  phase2.Phase2("Marius", 1000, "loose_aggressive"),
  Phase3("Martin", 1000, "tight_passive"),
  phase2.Phase2("Jostein", 1000, "tight_passive"),
  #Phase2("Emil", 1000, "loose_passive"),
  phase1.Phase1("Steinar", 1000, "tight_passive"),
  #phase1.Phase1("Stian", 1000, "tight_passive"),
  #phase1.Phase1("Selmer", 1000, "loose_aggressive"),
  #phase1.Phase1("Ole Jorgen", 1000, "tight_passive"),
  phase1.Phase1("Andre the giant", 1000, "loose_aggressive")
]


p = poker.poker(players, 200, debug_mode = True);

