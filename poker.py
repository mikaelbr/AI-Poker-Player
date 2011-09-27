import player
import cards

# Class for running a poker-game
class poker():

  def __init__(self, players, n_rounds = 1, n_games = 1, force_log = False):
    self.n_games = n_games
    self.n_rounds = n_rounds
    self.show_data = n_games < 2 or force_log
    self.players = players
    self.last_raise = 0

    for i in range(n_games):
      self.start_game()


  def start_game(self):
    self.deck = cards.card_deck()
    
    # Main game loop/structure. Based on Texas Hold 'Em rules
    for i in range(self.n_rounds):

      self.deck.reset()

      self.round = i
      print('\n')
      self.log("------------------------------- Round #", self.round, "-----------------------------------")

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
      self.show_active_player_stats()      

      
      self.do_betting_round(False)

      p = self.calculate_win()
      if p:
        self.log("Winner:")
        p[0][0].print_info(self.shared_cards)
        continue

      self.log("----- FLOP ------")
      self.deal_flop()
      self.do_betting_round()
      self.log("----- END FLOP ------")

      p = self.calculate_win()
      if p:
        self.log("Winner:")
        p[0][0].print_info(self.shared_cards)
        continue

      self.log("----- TURN ------")
      self.deal_turn()
      self.do_betting_round()
      self.log("----- END TURN ------")

      p = self.calculate_win()
      if p:
        self.log("Winner:")
        p[0][0].print_info(self.shared_cards)
        continue

      self.log("----- RIVER ------")
      self.deal_river()
      self.do_betting_round()
      self.log("----- END RIVER ------")

      p = self.calculate_win(True)
      if p:
        self.log("Winner(s) with hand ranking:", p[1])
        for winner in p[0]:
          winner.print_info(self.shared_cards)
        continue

      # Serve a fresh deck
    self.log("\n\n\n\n=========== THE POKER GAME IS FINISHED ===============")
    self.show_all_player_stats()



  def deal_flop(self):
    self.flop = self.deck.deal_n_cards(3)
    self.shared_cards = self.flop
    self.log("Round #", self.round, ", Flop:", cards.card_names(self.flop))
    self.show_shared_cards()
    self.show_active_player_stats()

  def deal_turn(self):
    self.turn = self.deck.deal_one_card()

    self.log("Round #", self.round, "- Turn:", cards.card_name(self.turn))
    
    self.shared_cards += [self.turn]
    self.show_shared_cards()
    self.show_active_player_stats()

  def deal_river(self):
    self.river = self.deck.deal_one_card()

    self.log ("Round #", self.round, "- River:", cards.card_name(self.river))

    self.shared_cards += [self.river]
    self.show_shared_cards()
    self.show_active_player_stats()

  def do_betting_round(self, do_reset_bets = True):
    self.log("------ START BETTING ROUND -------")
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
      print("Highest bet before take action :", highest_bet)
      action = p.take_action(highest_bet, self.pot, self.active_players, i, self.shared_cards)
      print("Highest bet after take action :", highest_bet)

      # Action returns a list [<0|1>, amount] 0 = Call, 1 = raise

      if not(action): # Fold
        self.active_players[i] = None
      else:
        self.pot += action[1]
        self.log("Total pot: ", self.pot)
        if action[0] == 1:
          self.active_players = self.active_players[(i+1):] + self.active_players[:(i+1)]
          if i != len(self.active_players):
            return self.do_betting_round(False)
        
    self.log("------ END BETTING ROUND -------")
    
    
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
      winner = [None, [0, 0, 0, 0, 0]]
      for p in self.active_players:
        if p == None:
          continue
        
        ranking = cards.calc_cards_power(p.cards + self.shared_cards)
        if ranking[0] > winner[1][0]:
          winner = [[p], ranking]
        elif ranking[0] == winner[1][0]:
          if ranking == winner[1]:
            winner[0].append(p)
          else:
            for j in range(1, len(ranking)):
              if ranking[j] > winner[1][j]:
                winner = [[p], ranking]
                break
      
      for p in winner[0]:
        print("Pot is added to winner after last round")
        p.win(self.pot/len(winner[0]))

      return winner
    
    return False

  def show_shared_cards(self):
    self.log("Shared cards:", cards.card_names(self.shared_cards))

  def show_active_player_stats(self):
    sum = 0
    print('\n')
    self.log("------ Active player stats -----")
    for p in self.active_players:
      if p != None:
        p.print_info(self.shared_cards)
        sum += p.money
    self.log("Total sum : ", sum+self.pot)
    self.log("---- END active player stats ---")
    print('\n')

  def show_all_player_stats(self):
    sum = 0
    nrOfPlayers = 0
    bestPlayer = None
    maxMoney = 0
    print('\n')
    self.log("------ TOTAL PLAYER STATS ------")
    for p in self.players:
      p.print_info(self.shared_cards)
      sum += p.money
      nrOfPlayers+=1
      if (p.money > maxMoney):
        bestPlayer = p
        maxMoney = p.money
    self.log("Number of players : ", nrOfPlayers)
    self.log("Best player was ", bestPlayer.name, "with", bestPlayer.money, "money")
    self.log("Total sum : ", sum)
    self.log("----- END TOTAL PLAYER STATS ------")
    print('\n')

  def log(self, *message, **argv):
    if (self.show_data): 
      print(*message, sep=" ", end=".\n") # Python 3.0 syntax
      #print message # python 2 syntax