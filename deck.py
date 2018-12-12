import numpy as np
from cards import EternalCard, Power
import pdb 
from gamestate import Gamestate

class Deck:
    def __init__(self, power_list, non_power_list, market={}, num_power=25, total_cards=75, seek_power=0, target = {}):
        #need to have a target to seek
        assert(seek_power == 0 or target)
        if power_list:
            self.initial_power = power_list
            self.initial_non_power = non_power_list
        else:
            self.initial_power = ['c']*num_power
            self.initial_non_power = [0]*(total_cards-num_power-seek_power) + ['Seek Power']*seek_power
        assert(self.initial_power)
        assert(self.initial_non_power)
        self.initial_deck = self.initial_power + self.initial_non_power
        self.initial_market = market
        self.target = target

        self.reset()

    def reset(self):
        #drawn power, not power
        self.gamestate = Gamestate(self.initial_deck, self.initial_power, self.initial_non_power, self.initial_market)
        np.random.shuffle(self.gamestate.deck)
        np.random.shuffle(self.gamestate.power)
        np.random.shuffle(self.gamestate.non_power)


    #this isn't what actually happens, but until we start tracking postitions in the deck-say by tracking scouts with crests, it works
    #it should add to a random point in the deck
    def add_card(self, card):
        self.gamestate.non_power.append(card)
        self.gamestate.deck.append(card)
        np.random.shuffle(self.gamestate.non_power)
        np.random.shuffle(self.gamestate.deck)

    #plays a seek power fetching a targeted power-can also be used for other fetching cards
    def play_seek(self, target_power):
        #choose a random index of a sigil matching the influence requirement
        #using isinstance is bad but it works and I'm lazy
        idxs = [i for i, x in enumerate(self.gamestate.deck) if isinstance(x, Power) and (x.influence == {target_power:1} and  'Sigil' in x.name)]
        if idxs:
            idx = np.random.choice(idxs)
            number_power = len(self.gamestate.power)
            card = self.gamestate.deck[idx]
            self.gamestate.hand.append(card)
            self.gamestate.power.remove(self.gamestate.deck[idx])
            del(self.gamestate.deck[idx])
            assert(len(self.gamestate.power)+1 == number_power)
            self.gamestate.drawn_power[target_power] += 1
            self.gamestate.drawn_power['total'] += 1

    def draw(self):
        card = self.gamestate.deck.pop()
        if card in self.gamestate.non_power:
            self.gamestate.non_power.remove(card)
        else:
            self.gamestate.power.remove(card)
            for c in card.influence:
                if c != 'C':
                    self.gamestate.drawn_power[c] += 1
            self.gamestate.drawn_power['total'] += 1    
        self.gamestate.hand.append(card)
        return card
    def draw_n(self, n):
        cards = []
        for i in range(n):
            cards.append(self.draw())
        return cards
    def draw_7(self):
        return self.draw_n(7)

    def draw_power(self):
        card = self.gamestate.power.pop()
        self.gamestate.deck.remove(card)
        for c in card.influence:
            if c != 'C':
                self.gamestate.drawn_power[c] += 1
        self.gamestate.drawn_power['total'] += 1
        self.gamestate.hand.append(card)
        return card

    def draw_non_power(self):
        card = self.gamestate.non_power.pop()
        self.gamestate.deck.remove(card)
        self.gamestate.hand.append(card)                
        return card
    def draw_initial_7(self):
        hand = self.draw_7()
        while(self.gamestate.drawn_power['total'] < 1 or self.gamestate.drawn_power['total'] > 6):
            self.reset()
            hand = self.draw_7()
        return hand

    def draw_mulligan(self, num_power=0):
        hand = []
        if num_power == 0:
            num_power = np.random.randint(2,5)
        for i in range(num_power):
            card = self.draw_power()
            hand.append(card)
        for i in range(7-num_power):
            self.draw_non_power()
            hand.append(card)
        return hand

    def draw_second_mulligan(self, num_power=0):
        hand = []
        if num_power == 0:
            num_power = np.random.randint(2,5)
        for i in range(num_power):
            card = self.draw_power()
            hand.append(card)
        for i in range(6-num_power):
            self.draw_non_power()
            hand.append(card)
        return hand


    #checks to see if we can play a card's influence
    def check_influence(self, card):
        if isinstance(card, Power):
            return True            
        influence_reqs = card.influence
        power_reqs = card.cost

        if power_reqs > self.gamestate.played_power['total']:
            return False
        for key in card.influence:
            if key != 'C':
                if card.influence[key] > self.gamestate.played_power[key]:
                    return False
        return True
    #plays a given card from hand, returns true if sucessful, false otherwise
    #the influence is for cards that let you choose an influence to add-say Diplomatic Seal
    #need to define where the card goes-units to board, relics to relic, etc.
    def play_card(self, card_name, influence='C', free=False):
        idxs = [1 if x.name == card_name else 0 for x in self.gamestate.hand]

        if np.any(idxs):
            idx = idxs.index(1)
            card = self.gamestate.hand[idx]

            if not self.check_influence(card) and not free:
                return False
            del(self.gamestate.hand[idx])

            if isinstance(card, Power):
                for c in card.influence:
                    if c != 'C':
                        self.gamestate.played_power[c] += 1
                self.gamestate.played_power['total'] += 1
                if influence != 'C':
                    self.gamestate.drawn_power[influence] += 1
                    
            return True
        return False

    #for debugging
    def stats(self):
        print(len(self.deck))
        print(len(self.power))
        print(len(self.non_power))