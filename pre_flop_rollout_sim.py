import cards
  

class PreFlopSim:

    def __init__(self):
        self.unsuited = []
        self.unsuited2 = []
        self.suited = []
        self.pairs = []
        pass

    def generateEquivLists(self):

        # fill out a list of cards. 
        card_list = cards.gen_52_cards();
            
        for i in range(13): # Check with the first suit
            for j in range(13, 26): # Check with the rest of the suits
                if cards.card_value(card_list[i]) != cards.card_value(card_list[j]):
                    is_in_list = False
                    for c in self.unsuited:
                        is_in_list = cards.card_value(card_list[j]) == cards.card_value(c)
                        if not is_in_list:
                            break

                    if not is_in_list:                    
                        self.unsuited.append([card_list[i], card_list[j]])
        
        for i in range(13):
            for j in range(13,13+13):
                if cards.card_value(card_list[i]) != cards.card_value(card_list[j]):
                    exists = False
                    for k in range(len(self.unsuited2)):
                        if cards.card_value(card_list[j]) == cards.card_value(self.unsuited2[k][0]):
                            exists = True
                    if not exists:                    
                        self.unsuited2.append([card_list[i], card_list[j]])

        print(len(self.unsuited))
        print(self.unsuited)


preflopsim = PreFlopSim()
preflopsim.generateEquivLists()


'''
    #generate the three equivelence classes.
    def generateEquivLists(self):
        sortedCardList = []
        
        #fill out a list of cards. 
        for i in range(len(self.suits)):
            for j in range(len(self.values)):
                sortedCardList.append(cards.create_card(self.values[j], self.suits[i]))
            
        #fill out eclassListUnsuited list with all unsuited EClasses.
        for i in range(13):
            for j in range(13,13+13):
                if cards.card_value(sortedCardList[i]) != cards.card_value(sortedCardList[j]):
                    exists = False
                    for k in range(len(self.eclassListUnsuited)):
                        if cards.card_value(sortedCardList[j]) == cards.card_value(self.eclassListUnsuited[k].c1):
                            exists = True
                    if not exists:                    
                        self.eclassListUnsuited.append(EClass.EClass(sortedCardList[i], sortedCardList[j]))
                        
#        print ( len (self.eclassListUnsuited))
#        for e in self.eclassListUnsuited:
#            print (str(e.c1 ) +" " + str(e.c2))
#        print self.eclassListUnsuited
        
        #fill out eclassListSuited list with all suited EClasses.
        for i in range(13):
            for j in range(13):
                if cards.card_value(sortedCardList[i]) != cards.card_value(sortedCardList[j]):
                    exists = False
                    for k in range(len(self.eclassListSuited)):
                        if cards.card_value(sortedCardList[j]) == cards.card_value(self.eclassListSuited[k].c1):
                            exists = True
                    if not exists:                    
                        self.eclassListSuited.append(EClass.EClass(sortedCardList[i], sortedCardList[j]))
        
#        print(len(self.eclassListSuited))
#        for e in self.eclassListSuited:
#            print (str(e.c1 ) +" " + str(e.c2))
#        print self.eclassListSuited
        
        for i in range(13):
            self.eclassListPairs.append(EClass.EClass(sortedCardList[i],sortedCardList[i+13]))
#        print(len(self.eclassListPairs))
#        for e in self.eclassListPairs:
#            print (str(e.c1 ) +" " + str(e.c2))
#        print self.eclassListPairs       
        

'''