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