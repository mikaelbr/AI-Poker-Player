import cards
import pickle

class PreFlopSim:

    def __init__(self, players, R):

        self.num_players = players
        self.R = R

        self.unsuited = []
        self.suited = []
        self.pairs = []

        self.generated_eqv_table = {}
        
    
    def remove_card_from_deck (self, deck, card):

        for c in deck[:]:
            if c == card:
                deck.remove(c)
        

    def generate_lists(self):

        # fill out a list of cards. 
        card_list = cards.gen_52_cards();
            
        for i in range(13): # Check with the first suit
            for j in range(13, 26): # Check with the rest of the suits
                if cards.card_value(card_list[i]) == cards.card_value(card_list[j]):
                    continue

                is_in_list = False
                for k in self.unsuited:
                    if cards.card_value(card_list[j]) == cards.card_value(k[0]):
                        is_in_list = True
                        break

                if not is_in_list: 
                    self.unsuited.append([card_list[i], card_list[j]])

            for j in range(13):
                if cards.card_value(card_list[i]) == cards.card_value(card_list[j]):
                    continue
                
                is_in_list = False
                for k in self.suited:
                    if cards.card_value(card_list[j]) == cards.card_value(k[0]):
                        is_in_list = True
                        break

                if not is_in_list: 
                    self.suited.append([card_list[i], card_list[j]])

            self.pairs.append([card_list[i], card_list[i+13]])

    def calculate_results(self, player, opponents, shared_cards):
        loss = False
        tie = False

        pl = cards.calc_cards_power(player + shared_cards)
        for p in opponents:

            o = cards.calc_cards_power(p + shared_cards)
            if o[0] > pl[0]:
              loss = True
            elif o[0] == pl[0]:
              if o == pl:
                tie = True
              else:
                for j in range(1, len(o)):
                    if o[j] > pl[j]:
                        loss = True
                        break

        # Return win tables. 
        return {"win": int(not(loss or tie)), "loss": int(loss), "tie": int(tie and not(loss))}



    def simulate_game(self, player_cards, p):
        deck = cards.card_deck()

        final_results = {"win": 0, "loss":0, "tie": 0}

        for j in range(self.R):

            self.remove_card_from_deck(deck.cards, player_cards)

            # deal cards to opponents
            opponents = []
            for i in range(p):
                opponents.append(deck.deal_n_cards(2))

            # play and calculate wins/loss/ties
            shared_cards = deck.deal_n_cards(5)

            temp_results = self.calculate_results(player_cards, opponents, shared_cards)

            final_results['win'] += temp_results['win']
            final_results['loss'] += temp_results['loss']
            final_results['tie'] += temp_results['tie']

            deck.reset()
        

        return final_results

    def isset(self, var, v):
        try:
            var[v]
            return True
        except KeyError:
            return False

    def simulate(self):

        

        self.generate_lists()

        for p in range(2, self.num_players+1):
            print("Player #", p)

            self.generated_eqv_table[p] = {}

            # Check for both suited and unsuited. 
            for i in range(len(self.unsuited)):

                cards_unsuited = self.unsuited[i]
                results_unsuited = self.simulate_game(cards_unsuited, p)

                un_key = "%s,%s" % (cards_unsuited[0][0], cards_unsuited[1][0])
                if not self.isset(self.generated_eqv_table[p], un_key):
                    self.generated_eqv_table[p][un_key] = {"unsuited": "", "suited": ""}

                self.generated_eqv_table[p][un_key]["unsuited"] = float(results_unsuited["win"]) / float(self.R)

                cards_suited = self.suited[i]
                results_suited = self.simulate_game(cards_suited, p)    
                
                su_key = "%s,%s" % (cards_suited[0][0], cards_suited[1][0])
                if not self.isset(self.generated_eqv_table[p], su_key):
                    self.generated_eqv_table[p][su_key] = {"unsuited": "", "suited": ""}

                self.generated_eqv_table[p][su_key]["suited"] = float(results_suited["win"]) / float(self.R)            

            # Check for pairs. 
            for i in range(len(self.pairs)):
                cards_pairs = self.pairs[i]
                results_pairs = self.simulate_game(cards_pairs, p)

                key = "%s,%s" % (cards_pairs[0][0], cards_pairs[1][0])
                if not self.isset(self.generated_eqv_table[p], key):
                    self.generated_eqv_table[p][key] = {"unsuited": "", "suited": ""}

                self.generated_eqv_table[p][key]["unsuited"] = float(results_pairs["win"]) / float(self.R)  

            
        return self.generated_eqv_table
            


preflopsim = PreFlopSim(10, 1200)
table = preflopsim.simulate()

print(table)

fileObj = open("dataset_huge","w")
pickle.dump(table, fileObj)
fileObj.close()


fileRead = open("dataset_huge","r")
table2 = pickle.load(fileRead)

print(table2)


