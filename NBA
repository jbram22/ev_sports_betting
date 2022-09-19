# import necessary packages
import requests
import sys
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import datetime as dt
from datetime import date

# import necessary utils functions (just import all to make things easier)
from utils import *


if __name__ == '__main__':
    # Grab data
    nba_pinnacle_dict, nba_american_dict = nba()

    # Sift thru non-positive EV games
    for game in nba_american_dict:
        print(nba_pinnacle_dict[game].underdog)
        print(f'{int(nba_pinnacle_dict[game].underdog_odds)} & {int(nba_pinnacle_dict[game].favorite_odds)}')
        current = nba_american_dict[game]
        positive = current.loc[current['dog_EV'] > 0]
        print(positive[['book','favorite_odds','dog_odds','dog_EV','fav_EV','dog_kelly']],'\n')

    # Data Mining
    nba_dog_data, nba_fav_data = mine_data(nba_american_dict, nba_pinnacle_dict)
