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
    nfl_pinnacle_dict, nfl_american_dict = nfl()

    # Sift thru non-positive EV games
    for game in nfl_american_dict:
        print(nfl_pinnacle_dict[game].favorite)
        print(f'{int(nfl_pinnacle_dict[game].underdog_odds)} & {int(nfl_pinnacle_dict[game].favorite_odds)}')
        '''instead of printing this stuf here^^, insert it into amercian dataframe(s)'''
        current = nfl_american_dict[game]
        positive = current.loc[current['fav_EV'] > 0]
        print(positive[['book','favorite_odds','dog_odds','fav_EV','dog_EV']],'\n')

    nfl_dog_data, nfl_fav_data = mine_data(nfl_american_dict, nfl_pinnacle_dict)
    
