from deck import Deck
from cards import EternalCard, Power
import pdb 
from gamestate import Gamestate
import numpy as np
import parse_decklist as pdl
from run_statistics import calculate_statistics



class SimpleBot:
    def __init__(self, deck_path, draw_method='mulligan', mulligan_power=0, target={}):
        power, non_power_list, decklist, market = pdl.read_exported_list(deck_path)
        self.deck = Deck(power, non_power_list, market=market, target = target)
        self.power_drawn_per_turn = []
        self.target = target
        self.turn_number = 0
        self.draw_opening_hand(draw_method=draw_method, mulligan_power=0)
        self.power_drawn_per_turn.append(dict(self.deck.gamestate.drawn_power))
    def draw_opening_hand(self,draw_method='mulligan', mulligan_power=0):
        if draw_method == 'mulligan':
            self.deck.draw_mulligan(num_power=mulligan_power)
        elif draw_method == 'complex':
            self.deck.draw_initial_7()
            total_power = self.deck.gamestate.drawn_power['total']
            complex_target = {x:min(self.target[x],1) for x in self.target}
            hit_complex_target = True
            if complex_target:
                for key in complex_target:
                    if (total_power < 2 or total_power > 4) or self.deck.gamestate.drawn_power[key] < complex_target[key]:
                        hit_complex_target = False
            if not hit_complex_target:
                self.deck.reset()
                self.deck.draw_mulligan()
                hit_complex_target = True
                if complex_target:
                    for key in complex_target:
                        if self.deck.gamestate.drawn_power[key] < complex_target[key]:
                            hit_complex_target = False
                if not hit_complex_target:
                    self.deck.reset()
                    self.deck.draw_second_mulligan()

        elif draw_method == 'initial':
            self.deck.draw_initial_7()
        elif draw_method == 'second':
            self.deck.draw_second_mulligan()
        elif draw_method == 'seven':
            self.deck.draw_7()
    #a basic step towards more complicated play-at the moment it just handles diplo seal stupidly.
    def play_turn(self):
        self.turn_number += 1
        self.deck.draw()
        if 'Privilege of Rank' in [x.name for x in self.deck.gamestate.hand]:
            if self.deck.play_card('Privilege of Rank'):
                self.deck.play_seek('J')
                self.deck.play_seek('J')
        if 'Vara\'s Favor' in [x.name for x in self.deck.gamestate.hand]:
            if self.deck.play_card('Vara\'s Favor'):
                self.deck.play_seek('S')

        if 'Diplomatic Seal' in [x.name for x in self.deck.gamestate.hand]:
            idx = np.random.choice([i for i, x in enumerate(self.deck.gamestate.hand) if x.name == 'Diplomatic Seal'])
            card = self.deck.gamestate.hand[idx]
            #check if we aquire influence when playing it
            if card.acquire_influence(self.deck.gamestate):
                (max_key, total_difference) = self.distance_from_target()
                #max_key = self.manus_heuristic()
                self.deck.play_card('Diplomatic Seal', influence=max_key)
        elif any(['pledge' in y for y  in [x.text for x in self.deck.gamestate.hand]]) and self.turn_number == 1:
            text = [x.text for x in self.deck.gamestate.hand]
            idxs = [i for i, x in enumerate(text) if 'pledge' in x]
            options = []

            pledge_cards = []
            #we need to collect the possible influence options that we have available.  This is nice because it should handle multi-color cards just fine
            for idx in idxs:
                pledge_cards.append(self.deck.gamestate.hand[idx])
                influence = pledge_cards[-1].influence
                for i in influence:
                    if i not in options:
                        options.append(i)
            (max_key, total_difference) = self.distance_from_target(available_influence=options)
            for card in pledge_cards:
                if max_key in card.influence:
                    self.deck.play_card(card.name, free=True)
                    self.deck.gamestate.drawn_power[max_key] += 1
                    self.deck.gamestate.drawn_power['total'] += 1
                    break
        else:
            #play a random power for now
            if np.any([isinstance(x, Power) for x in self.deck.gamestate.hand]):
                idx = np.random.choice([i for i, x in enumerate(self.deck.gamestate.hand) if isinstance(x, Power)])
                card = self.deck.gamestate.hand[idx]
                self.deck.play_card(card.name)
        if 'Seek Power' in [x.name for x in self.deck.gamestate.hand]:
            (max_key, total_difference) = self.distance_from_target(seek=True)
            #if total_difference <= 1:
            self.deck.play_seek(max_key)
            self.deck.play_card('Seek Power')
        self.power_drawn_per_turn.append(dict(self.deck.gamestate.drawn_power))

    #a simple method of choosing which influence is missings
    #available influence-if only a subset of influence is available (say, due to pledge)
    def distance_from_target(self, seek=False, available_influence=['F','J','S','P','T']):
        max_difference = -1000
        total_difference= 0
        max_key = ''
        for key in self.target:
            if key not in available_influence:
                continue
            if self.target[key] == 0:
                continue
            if seek:
                if not [x for x in self.deck.gamestate.power if x.influence == {key:1} and 'Sigil' in x.name]:
                    continue
            dif = self.target[key] - self.deck.gamestate.drawn_power[key]
            if (dif > 0):
                total_difference += dif
            if dif > max_difference:
                max_difference = dif
                max_key = key
        return (max_key, total_difference)

    #an example of how to write a heuristic
    def manus_heuristic(self):
        max_difference = 0     
        max_key = ''
        self.target = {'F':1, 'P':1, 'S':1}
        for key in self.target:
            dif = self.target[key] - self.deck.gamestate.drawn_power[key]
            if dif > max_difference and max_difference == 0:
                max_difference = dif
                max_key = key
        if max_difference == 0:
            self.target = {'F':2, 'S':2, 'P':2}
            max_difference = -1000     
            for key in self.target:
                dif = self.target[key] - self.deck.gamestate.drawn_power[key]
                if dif > max_difference:
                    max_difference = dif
                    max_key = key
        return max_key
