import cards
import player
import poker
import hand_strength
import pickle
import phase1


with open('dataset_huge', 'rb') as f:
  dataset = pickle.load(f)   
   
#data = open("dataset_huge","r")
# dataset = pickle.load(data)
#data.close()

def isset(var, v):
  try:
      var[v]
      return True
  except KeyError:
      return False

# Takes two cards c1 and c2. 
def fetch_rollout_data(players, hole_cards):
  val1 = "%s,%s" % (hole_cards[0][0], hole_cards[1][0])
  val2 = "%s,%s" % (hole_cards[1][0], hole_cards[0][0])

  suits = "suited" if cards.card_suit(hole_cards[0]) == cards.card_suit(hole_cards[1]) else "unsuited"

  if players < 2:
    return 1

  if isset(dataset[players], val1):
    return dataset[players][val1][suits]
  
  if isset(dataset[players], val2):
    return dataset[players][val2][suits]

  return 0



class Phase2(player.Player):

  def opponent_model_update_array (self, highest_bet, pot, players, position, shared_cards, state, total_raises, active_players):
    pass

  def take_action(self, highest_bet, pot, players, position, shared_cards, state, total_raises, active_players):
    if len(shared_cards) < 1: # pre-flop
      
      # Fetch information from stored data for rollout simulations.

      strength = fetch_rollout_data(players, self.cards)

    else:
      # Use hand strength calculations
      hand = hand_strength.HandStrength(players)
      strength = hand.calculate(self.cards, shared_cards)


    # We now have strength. Use this to take actions. 

    if not strength:
      strength = 0

    if(self.play_style == "loose_aggressive"):
      return self.take_loose_aggressive_action(highest_bet, pot, players, position, shared_cards, state, total_raises, strength)
    else:
      return self.take_tight_passive_action(highest_bet, pot, players, position, shared_cards, state, total_raises, strength)


  def take_loose_aggressive_action(self, highest_bet, pot, players, position, shared_cards, state, total_raises, strength):
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

    if state == 1:
      # Pre-flop
      if (ranking[0] == 1 and ranking[1] > 12) or (ranking[0] == 2) or (strength > 0.30): #High card and highest card is above 10 or pair or strength > 30%
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
        if (ranking[0] == 2 and players < 4 and self.sum_pot_in != highest_bet) or (strength > 0.30) or (ranking[0] > 3 and self.sum_pot_in != highest_bet):
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

  def take_tight_passive_action(self, highest_bet, pot, players, position, shared_cards, state, total_raises, strength):
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
      if (ranking[0] == 2 and ranking[1] > 9 and self.raise_count < 3) or strength > 0.7:
        # raise if not already committed equally to highest bet
        # check otherwise (call 0)
        if(self.sum_pot_in == highest_bet):
          self.last_action = "check"
          ret = self.call_action(highest_bet)
        else:
          self.last_action = "raise"
          ret = self.raise_action(highest_bet)

      elif (ranking[0] == 1 and ranking[1] > 10 and ranking[2] > 10) or strength > 0.5: # high card
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
      if ((ranking[0] == 3 and ranking[1] > 10 and ranking[2] > 10) or (ranking[0] == 4 and ranking[1] > 7) or (ranking[0] > 4) or strength > 0.70) and self.raise_count < 3:
        # raise if not already committed equally to highest bet
        # check otherwise (call 0)
        if(self.sum_pot_in == highest_bet):
          self.last_action = "check"
          ret = self.call_action(highest_bet)
        else:
          self.last_action = "raise"
          ret = self.raise_action(highest_bet)

      elif (highest_bet != self.sum_pot_in and ((ranking[0] == 1) or (ranking[0] == 2 and ranking[1] < 12) )) or strength < 0.3:
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

'''
players = [
  #Phase2("Mikael", 1000, "loose_aggressive"), 
  Phase2("Marius", 1000, "loose_aggressive"),
  #Phase2("Martin", 1000, "loose_aggressive"),
  Phase2("Jostein", 1000, "tight_passive"),
  #Phase2("Emil", 1000, "loose_passive"),
  phase1.Phase1("Steinar", 1000, "tight_passive"),
  #phase1.Phase1("Stian", 1000, "tight_passive"),
  #phase1.Phase1("Selmer", 1000, "loose_aggressive"),
  #phase1.Phase1("Ole Jorgen", 1000, "tight_passive"),
  phase1.Phase1("Andre the giant", 1000, "loose_aggressive")
]

p = poker.poker(players, 1000, debug_mode = True);
'''
