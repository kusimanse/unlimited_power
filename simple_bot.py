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
        self.draw_opening_hand(draw_method=draw_method, mulligan_power=0)
        self.power_drawn_per_turn.append(dict(self.deck.gamestate.drawn_power))
        self.target = target
    def draw_opening_hand(self,draw_method='mulligan', mulligan_power=0):
        if draw_method == 'mulligan':
            self.deck.draw_mulligan(num_power=mulligan_power)
        elif draw_method == 'complex':
            self.deck.draw_7()
            total_power = self.deck.gamestate.drawn_power['total']
            complex_target = {x:1 for x in self.target}
            hit_complex_target = True
            if complex_target:
                for key in complex_target:
                    if (total_power < 2 or total_power > 4) or self.deck.gamestate.drawn_power[key] < complex_target[key]:
                        hit_complex_target = False
            if not hit_complex_target:
                self.deck.reset()
                self.deck.draw_mulligan()
        else:
            self.deck.draw_7()

    #a basic step towards more complicated play-at the moment it just handles diplo seal stupidly.
    def play_turn(self):
        self.deck.draw()
        if 'Diplomatic Seal' in [x.name for x in self.deck.gamestate.hand]:
            idx = np.random.choice([i for i, x in enumerate(self.deck.gamestate.hand) if x.name == 'Diplomatic Seal'])
            card = self.deck.gamestate.hand[idx]
            #check if we aquire influence when playing it
            if card.acquire_influence(self.deck.gamestate):
                (max_key, total_difference) = self.distance_from_target()
                self.deck.play_card('Diplomatic Seal', influence=max_key)
        else:
            #play a random power for now
            if np.any([isinstance(x, Power) for x in self.deck.gamestate.hand]):
                idx = np.random.choice([i for i, x in enumerate(self.deck.gamestate.hand) if isinstance(x, Power)])
                card = self.deck.gamestate.hand[idx]
                self.deck.play_card(card.name)
        if 'Seek Power' in [x.name for x in self.deck.gamestate.hand]:
            (max_key, total_difference) = self.distance_from_target(seek=True)
            if total_difference <= 1:
                self.deck.play_seek(max_key)
                self.deck.play_card('Seek Power')
        self.power_drawn_per_turn.append(dict(self.deck.gamestate.drawn_power))



    #a simple method of choosing which influence is missing
    def distance_from_target(self, seek=False):
        max_difference = -1000
        total_difference= 0
        max_key = ''
        for key in self.target:
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


num_runs = 100000
turns_per_run = 10
runs = []
for i in range(num_runs):
    bot = SimpleBot('decklists/wind_herald_seek.txt', draw_method='mulligan', target = {'F':1, 'P':2, 'S':2})
    [bot.play_turn() for x in range(turns_per_run)]
    power_per_turn = bot.power_drawn_per_turn
    if len(runs) == 0:
        runs = [[x] for x in power_per_turn]
    else:
        [x.append(y) for x,y in zip(runs, power_per_turn)]

statistics = calculate_statistics(runs, num_runs, target = {'F':1, 'S':2, 'P':2, 'total': 6})

print()
for s in statistics:
    print(s)
    print()
