import numpy as np 
from deck import Deck
import pdb
import matplotlib.pyplot as plt
from read_list import read_exported_list
from run_statistics import calculate_statistics

def power_run(power_list='ghp_haunted.txt', draw_method='mulligan', mulligan_power=0, seek_power=0, complex_target={}, influence_target={}):
    power = read_exported_list(power_list)
    deck = Deck(total_cards=75, power_list=power, seek_power=seek_power, target=influence_target)

    if draw_method == 'mulligan':
        deck.draw_mulligan(num_power=mulligan_power)
    elif draw_method == 'complex':
        deck.draw_7()
        total_power = deck.drawn_power['total']
        hit_complex_target = True
        if complex_target:
            for key in complex_target:
                if (total_power < 2 or total_power > 4) or deck.drawn_power[key] < complex_target[key]:
                    hit_complex_target = False
        if not hit_complex_target:
            power = read_exported_list(power_list)
            deck = Deck(total_cards=75, power_list=power, seek_power=seek_power, target=influence_target)
            deck.draw_mulligan()
    else:
        deck.draw_7()
    power_drawn = dict(deck.drawn_power)
    power_per_turn = [power_drawn]
    for i in range(10):
        deck.play_turn()
        power_drawn = dict(deck.drawn_power)
        power_per_turn.append(power_drawn)
    return power_per_turn


num_runs = 100000
runs = []
for i in range(num_runs):
    power_per_turn = power_run(power_list='manus_haunted.txt', draw_method='mulligan', seek_power=0, influence_target = {'f':2, 's':2, 'p':1})
    #power_per_turn = power_run(draw_method='complex', seek_power=0, complex_target={'s':1, 'f':1, 'p':1})
    if len(runs) == 0:
        runs = [[x] for x in power_per_turn]
    else:
        [x.append(y) for x,y in zip(runs, power_per_turn)]

statistics = calculate_statistics(runs, num_runs, target = {'s':2, 'f':2, 'total': 4})
#statistics = calculate_statistics(runs, num_runs, target = {'f':1, 'p':2, 's':2, 'total': 5})

print()
for s in statistics:
    print(s)
    print()


