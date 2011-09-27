import player
import cards

# Class for running a poker-game
class poker():

  def __init__(self, players, n_rounds = 1, n_games = 1, debug_mode = False):
    self.n_games = n_games
    self.n_rounds = n_rounds
    self.debug_mode = debug_mode
    self.players = players
    self.last_raise = 0
    self.state = 0;

    for i in range(n_games):
      self.start_game()


  def start_game(self):
    self.deck = cards.card_deck()
    
    # Main game loop/structure. Based on Texas Hold 'Em rules
    for i in range(self.n_rounds):
      # Reset info
      self.deck.reset()
      self.state = 1 # 1 = Pre-flop
      self.round = i
      print('\n')
      print("================================== Round #", self.round, "State: ",self.state," ========================================")

      # Shuffle for big blind/small blind
      if(i != 0):
        self.players.append(self.players.pop(0))

      # Reset info.
      self.pot = 0
      self.flop = []
      self.turn = []
      self.river = []
      self.shared_cards = []
      self.active_players = self.players[:]

      # Deal hole cards 
      j = 0
      for p in self.active_players:
        if p == None:
          continue
                
        small_blind_player = j == len(self.players)-2
        big_blind_player = j == len(self.players)-1
        self.pot += p.new_round(small_blind_player, big_blind_player)
        p.set_cards(self.deck.deal_n_cards(2))

        j += 1 

      self.log("Pot:", self.pot)
      #self.show_active_player_stats()      

      self.do_betting_round(False)

      p = self.calculate_win()
      if p:
        self.log("Winner:")
        p[0][0].print_info(self.shared_cards)
        continue

      print("====== FLOP ======")
      self.deal_flop()
      self.do_betting_round()
      print("====== END FLOP ======")

      p = self.calculate_win()
      if p:
        self.log("Winner:")
        p[0][0].print_info(self.shared_cards)
        continue

      print("====== TURN ======")
      self.deal_turn()
      self.do_betting_round()
      print("====== END TURN ======")

      p = self.calculate_win()
      if p:
        print("Winner:")
        p[0][0].print_info(self.shared_cards)
        continue

      print("====== RIVER ======")
      self.deal_river()
      self.do_betting_round()
      print("====== END RIVER ======")

      p = self.calculate_win(True)
      if p:
        print("Winner(s) with hand ranking:", p[1])
        for winner in p[0]:
          winner.print_info(self.shared_cards)
        continue
      
      # Serve a fresh deck
    print("\n\n\n\n=========== THE POKER GAME IS FINISHED ===============")
    self.show_all_player_stats()



  def deal_flop(self):
    self.flop = self.deck.deal_n_cards(3)
    self.shared_cards = self.flop
    self.state += 1 # State should be 2 = post-flop
    self.log("Round #", self.round, ", Flop:", cards.card_names(self.flop), "- State:", self.state)
    self.show_shared_cards()
    if(self.debug_mode): self.show_active_player_stats()

  def deal_turn(self):
    self.turn = self.deck.deal_one_card()
    self.state += 1 # State should be 3 = post-turn
    self.log("Round #", self.round, "- Turn:", cards.card_name(self.turn), "- State:", self.state)
    self.shared_cards += [self.turn]
    self.show_shared_cards()
    if(self.debug_mode): self.show_active_player_stats()

  def deal_river(self):
    self.river = self.deck.deal_one_card()
    self.state += 1 # State should be 4 = post-river
    self.log ("Round #", self.round, "- River:", cards.card_name(self.river), "- State:", self.state)
    self.shared_cards += [self.river]
    self.show_shared_cards()
    if(self.debug_mode): self.show_active_player_stats()

  def do_betting_round(self, do_reset_bets = True):
    print("====== START BETTING ROUND ======")
    self.show_table_status()
    self.log("Pot:", self.pot)

    if self.calculate_win():
      return

    i = -1

    for p in self.active_players:
      i += 1

      if p == None:
        continue

      if do_reset_bets:
        p.sum_pot_in = 0

      highest_bet = 0 if self.active_players[-1] == None else self.active_players[-1].last_bet
      if do_reset_bets:
        highest_bet = 0
      self.log("Highest bet before take action :", highest_bet)
      action = p.take_action(highest_bet, self.pot, self.count_active_players(self.active_players), i, self.shared_cards)
      self.log("Highest bet after take action :", highest_bet)

      # Action returns a list [<0|1|2>, amount] 0 = Call, 1 = raise, 2 = check

      if not(action): # Fold
        self.active_players[i] = None
      else:
        # The player called, checked or raised, add the amount to the pot
        self.pot += action[1]
        print("Total pot: ", self.pot)
        if action[0] == 1:
          # Player raised; put the player that raised on the bottom of the turn-list
          # continue the betting round
          self.active_players = self.active_players[(i+1):] + self.active_players[:(i+1)]
          if i != len(self.active_players):
            return self.do_betting_round(False)
        
    print("====== END BETTING ROUND ======")
    
    
  def count_active_players(self, player_list):
    i = 0;
    for p in player_list:
      if p != None:
        i += 1
    return i

  def calculate_win(self, is_last_round = False):
    # Winning calcs 
    if self.count_active_players(self.active_players) < 2:
      for p in self.active_players:
        if p != None:
          print("Pot is added to winner", p.name)
          p.win(self.pot)
          return [[p], cards.calc_cards_power(p.cards + self.shared_cards)]
    
    if is_last_round:

      count_active = self.count_active_players(self.active_players)

      winner = [None, [0, 0, 0, 0, 0]]
      for p in self.active_players:
        if p == None:
          continue
        
        ranking = cards.calc_cards_power(p.cards + self.shared_cards)
        #If the players cards are better than the current winner,
        #the player is set as the current winner
        if ranking[0] > winner[1][0]:
          winner = [[p], ranking]
        elif ranking[0] == winner[1][0]:
          #If the player has the same cards as the current winner,
          #they will share the pot, so we add the player to the winner-table
          if ranking == winner[1]:
            winner[0].append(p)
          else:
            for j in range(1, len(ranking)):
              if ranking[j] > winner[1][j]:
                winner = [[p], ranking]
                break
      
      for p in winner[0]:
        print("Pot is added to winner after last round")
        #p.win(self.pot/len(winner[0]))
        winners = len(winner[0])
        if(winners > 1): 
          # It's a tie, register it, and split the money
          p.showdown_tie(self.pot/winners)
        else:
          # Only one winner, give him the money!
          p.showdown_win(self.pot/winners)
      
      #Check who lost the showdown
      for p in self.active_players:
        if p != None:
          p.save_modeling(count_active, self.shared_cards)
          if not p in winner[0]:
            # Register loss on the players
            p.showdown_loss()

      return winner
    
    return False

  def show_shared_cards(self):
    self.log("Shared cards:", cards.card_names(self.shared_cards))

  def show_table_status(self):
    print('====== TABLE STATUS ======')
    print('Pot: '+str(self.pot))
    print('Shared cards: '+str(self.shared_cards))
    print('Players left, with credits and hole cards :')
    self.show_active_player_stats()
    print('====== END TABLE STATUS ======')

  def show_active_player_stats(self):
    sum = 0
    self.log("====== Active player stats ======")
    for p in self.active_players:
      if p != None:
        p.print_info(self.shared_cards)
        sum += p.money
    self.log("Total sum : ", sum+self.pot)
    self.log("====== END Active player stats ======")

  def show_all_player_stats(self):
    sum = 0
    nr_of_players = 0
    best_player = None
    max_money = 0
    print('\n')
    print("====== TOTAL PLAYER STATS ======")
    for p in self.players:
      p.print_info(self.shared_cards)
      sum += p.money
      nr_of_players+=1
      if (p.money > max_money):
        best_player = p
        max_money = p.money
    print("Number of players : ", nr_of_players)
    print("Best player was ", best_player.name, "with", best_player.money, "credits")
    print("Total sum : ", sum)
    print("====== END TOTAL PLAYER STATS ======")
    print('\n')

  def log(self, *message, **argv):
    if (self.debug_mode): 
      print(*message, sep=" ", end="\n") # Python 3.0 syntax
      #print message # python 2 syntax
