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
  def take_action(self, highest_bet, pot, players, position, shared_cards, state, total_raises):
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

    # Simple solutions for testing (don't take pre/post flop into account)
    action = ""
    if strength > 0.7 and self.raise_count < 3: # raise
      if(self.sum_pot_in == highest_bet):
        # Check
        action = "check"
        ret = self.call_action(highest_bet)
      else:
        action = "raise"
        ret = self.raise_action(highest_bet)
    elif strength > 0.3: # call
      action = "call"
      ret = self.call_action(highest_bet)
    else: #fold
      if self.sum_pot_in == highest_bet:
        action = "check"
        ret = self.call_action(highest_bet)
      else:
        return self.fold_action()

    if action != "":
      self.take_action_super(highest_bet, pot, players, position, shared_cards, state, total_raises, action)

    return ret





  
  


# Play styles:
# "tight_passive"
# "tight_aggressive"
# "loose_passive"
# "loose_aggressive"


players = [
  Phase2("Mikael", 1000, "loose_aggressive"), 
  Phase2("Marius", 1000, "loose_aggressive"),
  Phase2("Martin", 1000, "loose_aggressive"),
  Phase2("Jostein", 1000, "loose_passive"),
  Phase2("Emil", 1000, "loose_passive"),
  phase1.Phase1("Steinar", 1000, "loose_passive"),
  phase1.Phase1("Stian", 1000, "loose_passive"),
  phase1.Phase1("Selmer", 1000, "tight_passive"),
  phase1.Phase1("Ole Jorgen", 1000, "tight_passive"),
  phase1.Phase1("Andre the giant", 1000, "tight_aggressive")
]

p = poker.poker(players, 1000, debug_mode = True);

