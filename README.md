# Unlimited Power!

A basic monte carlo simulator for Eternal (https://www.direwolfdigital.com/eternal/).

How to run:
Prerequisites:
Download the card base json from: https://eternalwarcry.com/cards/download and move it to this folder
Python 3.x with numpy (it should run with python 2, but you need to change the print statements)

If you aren't familiar with python, I recommend using anaconda (https://www.anaconda.com/download/)-it makes it super easy to install numpy and anything else.  Once anaconda is installed, open terminal or command prompt and run:

conda install numpy 

Then, cd to the folder where unlimited power is:
cd /path/to/unlimited_power

From here, you can run simulations using run.py.  To see how to run it, run python run.py -h

For example:

python.run.py -r 100000  -d decklists/cranky_fjs.txt -m

Runs a simulation with the given decklist with 100,000 runs per simulation, testing mulligans only.  The output is in csv format, which makes it easy to copy and paste into spreadsheets.  


Most of the simulation happens in deck.py-this handles drawing new cards, power, mulligans, etc.  For an example of how to make a basic simulation, see basic_bot.py and run.py.

Full deck import support and gamestate tracking was added thanks to grkles.  I rewrote the rest of the code to work with it, and removed the seek power/diplomatic seal logic from deck.py, as it is more of a simulation decision than basic Eternal gameplay.  I moved it to basic_bot, which shows an example of a bot with simple heuristics.  I added better seek power handeling thanks to mathmauney.
