from json import load
from gamestate import Gamestate
from collections import Counter
import pdb

with open('eternal-cards.json') as f:
    cardlist = load(f)
    ETERNAL_DB = {card["Name"]: card for card in cardlist}
    
NONUNIT_TYPES = ["Power", "Spell", "Fast Spell", "Weapon", "Relic Weapon",
                 "Relic", "Cursed Relic", "Curse"]

with open('power_dict.json') as f:
    POWER_DICT = load(f)

INFLUENCE_NAMES = ['F','J','S','P','T']

#converts influence requirements from '{F}{F}{S}' form to a dict-makes later handling much easier
def convert_influence(influence_string):
    influences = [x for x in influence_string if x in INFLUENCE_NAMES]
    if not influences:
        return {"C": 1}
    return dict(Counter(influences))


class EternalCard(object):
    """
    This can be expanded later if we want, to include things like 
    attack/health, etc."
    """
    
    def __init__(self, name="", market=False):
        self.entry = ETERNAL_DB[name]
        
        self.name = self.entry["Name"]
        cardtype = self.entry["Type"]
        if cardtype not in NONUNIT_TYPES:
            self.etype = "Unit"
            self.subtype = cardtype
        else:
            self.etype = cardtype
            self.subtype = ""
        self.cost = self.entry["Cost"]
        self.influence = convert_influence(self.entry["Influence"])
        self.market = market
        self.text = self.entry['CardText'].lower()
    def copy(self):
        return EternalCard(name=self.name)
    
    def __repr__(self):
        return '<EternalCard: "{}">'.format(self.name)
    

class Power(EternalCard):
    def __init__(self, name="", **kw):
        super().__init__(name=name, **kw)
        self._influence = convert_influence(POWER_DICT[name])
        self._depleted = None
   
    #copy was returning EternalCard objects, not power objects
    def copy(self):
        return Power(name=self.name)

    def depleted(self, gamestate=None):
        """
        Determine whether the power is depleted or not.
        """
        if self._depleted:
            return self._depleted
        
        if any([cat in self.name for cat in ["Sigil", "Waystone"]]):
            return False
        if any([cat in self.name for cat in ["Monument", "Crest", "Standard"]]):
            return True
        
        if not gamestate:
            return True
        
        if "Seal" in self.name:
            return not any([card for card in gamestate.hand 
                                  if 'Sigil' in card.name.lower()])
        if "Banner" in self.name:
            return not any([card for card in gamestate.board
                                  if card.etype == "Unit"])
    
    def deplete(self):
        """
        Utility function to allow cards like Find the Way to deplete the power.
        """
        self._depleted = True
    
    def acquire_influence(self, gamestate=None):
        """
        Get influence from the power. Allows for handling of Diplomatic Seal
        or Common Cause.
        """
        
        if not gamestate:
            return self._influence
        
        if self.name == "Diplomatic Seal":
            test_number = sum([gamestate.played_power[x] for x in gamestate.played_power if x in INFLUENCE_NAMES]) 
            if test_number < 3:
                return self._influence
            else:
                return []
        
        if self.name == "Common Cause":
            unit_subtypes = [card.subtype for card in gamestate.hand 
                                 if card.etype == "Unit"]
            if len(set(unit_subtypes)) < len(unit_subtypes):
                return self._influence
            else:
                return []
        
        return self._influence

