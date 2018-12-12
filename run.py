import argparse
from simple_bot import SimpleBot
from run_statistics import calculate_statistics, visualize_statistics
import parse_decklist as pdl
import itertools
import pdb
from collections import Counter

parser = argparse.ArgumentParser(description='A program to simulate Eternal card power bases.  Example usage: python run.py -d decklists/cranky_fjs.txt -m')

parser.add_argument('-d', '--decklist', required=True, help='Path to the decklist')
parser.add_argument('-r', '--runs', default='10000', help='number of times to run the simulation')
parser.add_argument('-i', '--influence', default='', help='The influence target for the deck.  Default is the requirements extracted from the deck.  Enter in the form "4 F 2 S 2 P 1"')
parser.add_argument('-u', '--heuristic', default='', help='A heuristic for ordering of influence for cards like seek power and diplomatic seal.  TODO')
parser.add_argument('-t', '--turns', default='10', help='The number of turns per each run')
parser.add_argument('-m', '--mulligan', action='store_true', help='Calculate for a mulligan?  Choosing multiple of initial hand, mulligan, and second mulligan will result in interleaved output (for easy comparison)')
parser.add_argument('-s', '--second', action='store_true', help='Calculate for second mulligan')
parser.add_argument('-f', '--initial', action='store_true', help='Calculate for initial hand')
parser.add_argument('-7', '--seven', action='store_true', help='Calculate for initial hand as straight drawing 7')
parser.add_argument('-c', '--complex', action='store_true', help='Calculate for initial hand as a complex drawing strategy')
parser.add_argument('-a', '--all', action='store_true', help='Run the program for all hand drawing options, not including drawing seven cards or complex')
args = vars(parser.parse_args())

target_str = args['influence']
if target_str:
	l = args['influence'].split()[1:]
	target = dict(itertools.zip_longest(*[iter(l)] * 2, fillvalue=""))
	target['total'] = target_str[0]
	target = {x: int(target[x]) for x in target}
else:
	power, non_power_list, decklist, market = pdl.read_exported_list(args['decklist'])
	target = pdl.tabulate_influence_requirements(decklist)[0][-1]
	target['total'] = len(pdl.tabulate_influence_requirements(decklist)[0])-1

num_runs = int(args['runs'])
turns_per_run = int(args['turns'])
statistics_dict = {}

if args['mulligan'] or args['all']:
	runs = []
	for i in range(num_runs):
	    bot = SimpleBot(args['decklist'], draw_method='mulligan', target = target)
	    [bot.play_turn() for x in range(turns_per_run)]
	    power_per_turn = bot.power_drawn_per_turn
	    if len(runs) == 0:
	        runs = [[x] for x in power_per_turn]
	    else:
	        [x.append(y) for x,y in zip(runs, power_per_turn)]
	statistics = calculate_statistics(runs, num_runs, target = target)
	statistics_dict['mulligan'] = statistics
if args['second'] or args['all']:
	runs = []
	for i in range(num_runs):
	    bot = SimpleBot(args['decklist'], draw_method='second', target = target)
	    [bot.play_turn() for x in range(turns_per_run)]
	    power_per_turn = bot.power_drawn_per_turn
	    if len(runs) == 0:
	        runs = [[x] for x in power_per_turn]
	    else:
	        [x.append(y) for x,y in zip(runs, power_per_turn)]

	statistics = calculate_statistics(runs, num_runs, target = target)
	statistics_dict['second'] = statistics

if args['initial'] or args['all']:
	runs = []
	for i in range(num_runs):
	    bot = SimpleBot(args['decklist'], draw_method='initial', target = target)
	    [bot.play_turn() for x in range(turns_per_run)]
	    power_per_turn = bot.power_drawn_per_turn
	    if len(runs) == 0:
	        runs = [[x] for x in power_per_turn]
	    else:
	        [x.append(y) for x,y in zip(runs, power_per_turn)]
	statistics = calculate_statistics(runs, num_runs, target = target)
	statistics_dict['initial'] = statistics

if args['complex']:
	runs = []
	for i in range(num_runs):
	    bot = SimpleBot(args['decklist'], draw_method='complex', target = target)
	    [bot.play_turn() for x in range(turns_per_run)]
	    power_per_turn = bot.power_drawn_per_turn
	    if len(runs) == 0:
	        runs = [[x] for x in power_per_turn]
	    else:
	        [x.append(y) for x,y in zip(runs, power_per_turn)]
	statistics = calculate_statistics(runs, num_runs, target = target)
	statistics_dict['complex'] = statistics

if args['seven']:
	runs = []
	for i in range(num_runs):
	    bot = SimpleBot(args['decklist'], draw_method='seven', target = target)
	    [bot.play_turn() for x in range(turns_per_run)]
	    power_per_turn = bot.power_drawn_per_turn
	    if len(runs) == 0:
	        runs = [[x] for x in power_per_turn]
	    else:
	        [x.append(y) for x,y in zip(runs, power_per_turn)]
	statistics = calculate_statistics(runs, num_runs, target = target)
	statistics_dict['seven'] = statistics

# sums = [Counter([x['total'] for x in y]) for y in runs]
# sums = [{x: y[x]/num_runs for x in y} for y in sums]

visualize_statistics(statistics_dict)
