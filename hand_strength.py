import cards

class HandStrength:

    def __init__(self, players):

        self.num_players = players
        
        
    
    def remove_card_from_deck (self, deck, card):

        for c in deck[:]:
            if c == card:
                deck.remove(c)
        


    def calculate_results(self, player, opponents, shared_cards):

        result = {"win": 0, "loss": 0, "tie": 0}

        pl = cards.calc_cards_power(player + shared_cards)
        i = 0
        for p in opponents:
            i += 1
            o = cards.calc_cards_power(p + shared_cards)
            if o[0] > pl[0]:
              result['loss'] += 1
            elif o[0] == pl[0]:
              if o == pl:
                result['tie'] += 1
              else:
                loss = False
                for j in range(1, len(o)):
                    if o[j] > pl[j]:
                        loss = True
                        break
                if loss: 
                    result['loss'] += 1
                else:
                    result['win'] += 1
            else: 
                result['win'] += 1

        print(i)

        # Return win tables. 
        return result

    def calculate(self, player_cards, shared_cards):

        # calculate a table of all different combinations of hole cards except player_cards and shared cards
        card_list = cards.gen_52_cards();

        # Remove cards in use. 
        for c in player_cards + shared_cards:
            self.remove_card_from_deck(card_list, c)


        # Generate a list of all combinations of hole cards (permutations of the deck)
        opponents = []

        for c1 in card_list: # Check with the first suit
            for c2 in card_list: # Check with the rest of the suits
                if c1 != c2 and not [c2, c1] in opponents and not [c1, c2] in opponents:
                    opponents.append([c1, c2]);

        results = self.calculate_results(player_cards, opponents, shared_cards)
        hand_ranking = pow(((results["win"]+0.5*results["tie"])/(results["win"]+results["tie"]+results["loss"])), self.num_players)

        print(len(opponents))
        print(results)
        print(hand_ranking)
        return hand_ranking



'''
deck = cards.card_deck()
H = deck.deal_n_cards(2)
S = deck.deal_n_cards(5)

print(H)
print(S)
print(cards.calc_cards_power(H + S))

hand_strength = HandStrength(2)
hand_strength.calculate(H, S)
'''




