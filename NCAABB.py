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
    ncaabb_pinnacle_dict, ncaabb_american_dict = ncaa_bb()

    # Sift thru non-positive EV games
    for game in ncaabb_american_dict:
        print(ncaabb_pinnacle_dict[game].underdog)
        print(f'{int(ncaabb_pinnacle_dict[game].underdog_odds)} & {int(ncaabb_pinnacle_dict[game].favorite_odds)}')
        '''instead of printing this stuf here^^, insert it into amercian dataframe(s)'''
        current = ncaabb_american_dict[game]
        positive = current.loc[current['dog_EV'] > 0]
        print(positive[['book','favorite_odds','dog_odds','dog_EV','fav_EV','dog_kelly']],'\n')
  
