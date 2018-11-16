class Gamestate(object):
    def __init__(self, deck, power, non_power, market):
        self.power = power
        self.non_power = non_power
        self.deck = deck
        self.hand = []
        self.void = []
        self.influence = []
        self.board = []
        self.relics = []
        self.market = market
        self.drawn_power = {'P':0, 'F': 0, 'J': 0, 'S': 0, 'T': 0, 'total': 0}
        self.played_power = {'P':0, 'F': 0, 'J': 0, 'S': 0, 'T': 0, 'total': 0}
        self.undepleted_power = 0

    #zone is a string=hand, board, relics, etc.
    def number_of_card_in_zone(card, zone):
        if zone == 'hand':
            return sum([1 for x in self.hand if x.name == card.name])
        if zone == 'board':
            return sum([1 for x in self.board if x.name == card.name])
        if zone == 'void':
            return sum([1 for x in self.void if x.name == card.name])
        if zone == 'relics':
            return sum([1 for x in self.relics if x.name == card.name])

