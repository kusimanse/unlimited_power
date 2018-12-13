import re
from collections import defaultdict
from cards import EternalCard, Power
import pdb
   
# We don't care about setnumber & eternalid right now, but they may be
# relevant in the future. In any case, the json DB has this information
card_parse = re.compile(r"^(?P<count>[0-9]+) (?P<cardname>.+) \(Set(?P<setnumber>[0-9]+) #(?P<eternalid>[0-9]+)\)$")

def read_exported_list(file_name):
    
    with open(file_name) as f:
        export_list = f.read().split('\n')
    export_list = [x for x in export_list if x]
    return parse_export(export_list)

def parse_export(exported_list):
    power_base, nonpower_cards, decklist, market_list = [], [], [], []
    market = False
    for line in exported_list:
        if 'MARKET' in line:
            market = True
            continue
        cardmatch = card_parse.match(line)
        count = int(cardmatch.group('count'))
        name = cardmatch.group('cardname')
        card = EternalCard(name=name, market=market)
        if card.etype == "Power" and not market:
            power = Power(name=name, market=market)
            power_base.extend([power.copy() for _ in range(count)])
            decklist.extend([power.copy() for _ in range(count)])
        elif not market:
            nonpower_cards.extend([card.copy() for _ in range(count)])
            decklist.extend([card.copy() for _ in range(count)])
        else:
            if card.etype == "Power":
                card = Power(name=name, market=market)
            market_list.append(card)

    return power_base, nonpower_cards, decklist, market_list

def tabulate_influence_requirements(decklist):
    """
    Tabulates the most restrictive influence requirement at each turn 
    (indicated by the cost of the card) in each faction.
    """
    
    card_reqs, turn_reqs = defaultdict(list), []
    influence = 'FTJPS'
    for card in decklist:
        if card.etype == "Power" or card.market:
            continue
        card_reqs[card.cost].append(card.influence)
    for turn in range(max(card_reqs.keys())+1):
        cards = card_reqs[turn]
        if turn_reqs:
            reqs = turn_reqs[-1].copy()
        else:
            reqs = {faction: 0 for faction in influence}
        for faction in influence:
            reqs[faction] = max([inf[faction] for inf in cards if faction in inf] + [reqs[faction]])
        turn_reqs.append(reqs)
    return turn_reqs, card_reqs
    
    