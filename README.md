# Unlimited Power!

A basic monte carlo simulator for Eternal (https://www.direwolfdigital.com/eternal/).

Most of the simulation happens in deck.py-this handles drawing new cards, power, mulligans, etc.  For an example of how to use it see basic_bot.py.

Full deck import support and gamestate tracking was added thanks to grkles.  I rewrote the rest of the code to work with it, and removed the seek power/diplomatic seal logic from deck.py, as it is more of a simulation decision than basic Eternal gameplay.  I moved it to basic_bot, which shows an example of a bot with simple heuristics.
