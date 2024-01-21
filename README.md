# ev_sports_betting
This repo contains various scripts and functionality to scan numerous american sportbooks and return positive expected value bets, along with the corresponding appropriate bet size, according to the Kelly Criterion https://en.wikipedia.org/wiki/Kelly_criterion#Gambling_formula

This is more of a repo so I am able to keep track of changes, but I am open to all questions and/or potential improvements, so feel free to reach out


# Conact Info
If at any point, you have any issues, comments, concerns, or questions, feel free to reach out to me, Jason Bram, either via the `issues` tab on this repo, or via pull request. I am also happy to provide tutorials on usage via Zoom, if need be.


# Functionality
* `nba()`
* `ncaa_bb()`
* `nfl()`


# Installation
After cloning this repo, you will need to insert your api key in the config.py file, and
you will need to install the neccessary packages via the following command:
```
pip install -r requirements.txt
```
## Example
First, you want to clone the repo,
```
git clone https://github.com/jbram22/ev_sports_betting.git

```
Then, you want to cd into it (ie make the directory containing this repo your current working directory)
```
cd ev_sports_betting
```
AFTER inserting you api key into the `config.py` file, all thats left is to install the required packages!
```
pip install -r requirements.txt
```
Note: It is recommended to use a virutal environment whenever developing code, see `https://docs.python.org/3/library/venv.html` for more details


# Prefered Usage
The prefered usage is very simple, just executing the pre-made scripts via your command line. It is important to remember that during certain times in the season, one example is during playoffs, there may be no positive EV games returned for a particular sport, which will be reflected as an empty dataframe in your output.

## Obtaining Positive EV NBA Games
```
python NBA.py
```

## Obtaining Positive EV NCAABB Games
```
python NCAABB.py
```

## Obtaining Positive EV NFL Games
```
python NFL.py
```
