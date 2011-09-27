import cards
import player
import poker
import hand_strength
import pickle
import phase1
import phase2
import db_con


class Phase3(player.Player):

  def take_action(self, highest_bet, pot, players, position, shared_cards, state, total_raises, active_players):
    # generate_context(betting_round, players_remaining, num_raises, pot_odds)
    # get_hand_strength(context, player, action)
    # self.calculated_opponent_models

    pot_odds = (float(highest_bet)/(float(highest_bet)+float(pot)))
    context = player.db.generate_context(state, players, total_raises, pot_odds)

    in_checker = [] # array used to double check that the players haven't dropped out (folded)

    # Now we can use context to check all players 
    # Iterate over the players who has already played their hand this round and overwrite the previous value. 
    for p in active_players[:]:
      if p == None: # continue next iteration if player not active 
        continue

      if p.name == self.name: #check for self if so drop out
        break

      in_checker.append(p.name)
      self.calculated_opponent_models[p.name] = player.db.get_hand_strength(context, p.name, p.last_action)

    # Remove all models of folded players
    for k, v in self.calculated_opponent_models.copy():
      if k not in in_checker:
        del self.calculated_opponent_models[k]

    # Now we can use the self.calculated_opponent_models dictionary to 
    # see if any of the players have a exceptionally good hand

    # Find the highest strength of an opponent. 
    highest_strength = 0
    for k, s in self.calculated_opponent_models:
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
  Phase3("Mikael", 1000, "loose_aggressive"), 
  Phase3("Marius", 1000, "loose_aggressive"),
  Phase3("Martin", 1000, "loose_aggressive"),
  phase2.Phase2("Jostein", 1000, "loose_passive"),
  phase2.Phase2("Emil", 1000, "loose_passive"),
  phase2.Phase2("Steinar", 1000, "loose_passive"),
  phase2.Phase2("Stian", 1000, "loose_passive"),
  phase1.Phase1("Selmer", 1000, "tight_passive"),
  phase1.Phase1("Ole Jorgen", 1000, "tight_passive"),
  phase1.Phase1("Andre the giant", 1000, "tight_aggressive")
]

p = poker.poker(players, 1000, debug_mode = True);

