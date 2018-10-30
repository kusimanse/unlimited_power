import numpy as np
from power import Power
import pdb 

class Deck:
    def __init__(self, power_list = [], num_power=25, total_cards=75, seek_power=0, target = {}):
        #need to have a target to seek
        assert(seek_power == 0 or target)
        if power_list:
            self.power = power_list
            self.non_power = [0]*(total_cards-len(power_list)-seek_power) + ['seek']*seek_power
        else:
            self.power = ['c']*num_power
            self.non_power = [0]*(total_cards-num_power-seek_power) + ['seek']*seek_power

        self.deck = self.power + self.non_power
        self.target = target

        self.drawn_power = {'p':0, 'f': 0, 'j': 0, 's': 0, 't': 0, 'total': 0}
        self.played_power = {'p':0, 'f': 0, 'j': 0, 's': 0, 't': 0, 'total': 0}

        #drawn power, not power
        self.power_in_hand = []

        np.random.shuffle(self.deck)
        np.random.shuffle(self.power)
        np.random.shuffle(self.non_power)

    def add_card(self, card):
        self.non_power.append(card)
        self.deck.append(card)
        np.random.shuffle(self.non_power)
        np.random.shuffle(self.deck)

    #basic logic-find power to bring us closer to ideal, if not choose arbitrary power
    def play_seek(self):
        #basically -inf
        max_difference = -1000     
        max_key = ''
        for key in self.target:
            #if the power type isn't in the deck
            if not [x for x in self.power if x.color == [key] and x.type == 'sigil']:
                continue
            dif = self.target[key] - self.drawn_power[key]
            if dif > max_difference:
                max_difference = dif
                max_key = key
        #all available power is gone
        if max_key == '':
            return
        #choose a random index of a sigil matching the influence requirement
        #using isinstance is bad but it works and I'm lazy
        idxs = [i for i, x in enumerate(self.deck) if isinstance(x, Power) and (x.color == [max_key] and x.type == 'sigil')]
        if idxs:
            idx = np.random.choice(idxs)
            number_power = len(self.power)
            card = self.deck[idx]
            self.power_in_hand.append(card)
            self.power.remove(self.deck[idx])
            del(self.deck[idx])
            assert(len(self.power)+1 == number_power)
            self.drawn_power[max_key] += 1
            self.drawn_power['total'] += 1

    def draw(self):
        card = self.deck.pop()
        if card in self.non_power:
            self.non_power.remove(card)
        else:
            self.power.remove(card)
            self.power_in_hand.append(card)
            for c in card.color:
                if c != 'c':
                    self.drawn_power[c] += 1
            self.drawn_power['total'] += 1                    
        if card == 'seek':
            self.play_seek()
        return card
    def draw_n(self, n):
        cards = []
        for i in range(n):
            cards.append(self.draw())
        return cards
    def draw_7(self):
        return self.draw_n(7)

    def draw_power(self):
        card = self.power.pop()
        self.deck.remove(card)
        for c in card.color:
            if c != 'c':
                self.drawn_power[c] += 1
        self.drawn_power['total'] += 1
        self.power_in_hand.append(card)
        return card

    def draw_non_power(self):
        card = self.non_power.pop()
        self.deck.remove(card)
        if card == 'seek':
            self.play_seek()
        return card

    def draw_mulligan(self, num_power=0):
        if num_power == 0:
            num_power = np.random.randint(2,5)
        for i in range(num_power):
            card = self.draw_power()
        for i in range(7-num_power):
            self.draw_non_power()

    #a basic step towards more complicated play-at the moment it just handles diplo seal stupidly.
    def play_turn(self):
        self.draw()
        if (sum(self.played_power.values()) - self.played_power['total']) < 3 and 'Diplomatic Seal' in [x.name for x in self.power_in_hand]:
            idx = [0 if x.name == 'Diplomatic Seal' else 1 for x in self.power_in_hand].index(0)
            del(self.power_in_hand[idx])
            max_difference = -1000     
            max_key = ''
            for key in self.target:
                dif = self.target[key] - self.drawn_power[key]
                if dif > max_difference:
                    max_difference = dif
                    max_key = key
            self.drawn_power[max_key] += 1
            self.played_power[max_key] += 1
            self.played_power['total'] += 1
        else:
            #play a random power for now
            if self.power_in_hand:
                idx = np.random.choice(len(self.power_in_hand))
                card = self.power_in_hand[idx]
                for c in card.color:
                    if c != 'c':
                        self.played_power[c] += 1
                        self.played_power['total'] += 1
                del(self.power_in_hand[idx])


    def stats(self):
        print(len(self.deck))
        print(len(self.power))
        print(len(self.non_power))