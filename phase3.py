import cards
import player
import poker
import hand_strength
import pickle
import phase1
import phase2


class Phase3(player.Player):

  def generate_context(self, )

  def take_action(self, highest_bet, pot, players, position, shared_cards):



    
  






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

p = poker.poker(players, 1000, force_log = True);

