##############################################################
################## ODDS CONVERSION HELPERS ###################
##############################################################

# decimal to fractional (useful for kelly)
'''fractional = decimal - 1'''
def decimal_to_fractional(decimal_odds):
    frac = decimal_odds-1
    return frac

# american to decimal
def american_to_decimal(american_odds):
    if american_odds > 0:
        dec = (american_odds/100) + 1
    elif american_odds < 0:
        dec = (100/(-1*american_odds)) + 1
    return dec

# decimal to american
def decimal_to_american(decimal_odds):
    if decimal_odds >= 2:
        american = (decimal_odds-1)*100
    elif decimal_odds < 2:
        american = -100/(decimal_odds-1)
    return american

################################################################
####### EXPECTED VALUE, KELLY, AND THRESHOLD HELPERS ###########
################################################################

def expected_value(bet_size,fair_win_prob,decimal_odds):
    win = (bet_size*decimal_odds)-bet_size
    ev = (win*fair_win_prob) - ((1-fair_win_prob)*bet_size)
    return ev

def kelly(p_win,fractional_odds):
  fraction = p_win - (1-p_win)/fractional_odds
  return fraction

def threshold(pinnacle_dawg,pinnacle_fav):
    '''
    @ this function is basically another way to compute no-vig fair odds (for pinnacle) lol
    i.e, it is entirely useless, but an interesting finding all together
    '''
    underdog_prob, fav_prob, no_vig_underdog, no_vig_fav = remove_vig(pinnacle_dawg,pinnacle_fav)
    under_thresh = ((((1-underdog_prob)*100)/underdog_prob) + 100)/100 
    fav_thresh = ((((1-fav_prob)*100)/fav_prob) + 100)/100
    return under_thresh, fav_thresh

################################################################
####################### VIG REMOVAL ############################
#################### MANUAL EV CHECKER #########################
################################################################

def remove_vig(underdog,favorite):
    # convert odds & compute implied probability for underPAWG
    underdog_decimal = american_to_decimal(underdog)
    underdog_implied = (1/underdog_decimal)*100
    # convert odds & compute implied probability for favorite
    favorite_decimal = american_to_decimal(favorite)
    favorite_implied = (1/favorite_decimal)*100
    # wikipedia vig formula
    vig = 100 * (1-((underdog_decimal*favorite_decimal)/(underdog_decimal+favorite_decimal)))
    # random vig formula
    overround = underdog_implied + favorite_implied
    rand_vig = (1-(1/overround)*100)*100
    # no-vig probabilities
    fair_p = underdog_implied/ (underdog_implied + favorite_implied) # for underdog
    fair_q = favorite_implied/ (underdog_implied + favorite_implied) # for favorite
    # no-vig odds
    '''decimal odds'''
    no_vig_p = 1/fair_p # underdog
    no_vig_q = 1/fair_q # favorite
    '''american odds '''
    american_p = (no_vig_p-1)*100 # underdog
    american_q = -100/(no_vig_q-1) # favorite

    return fair_p,fair_q,no_vig_p,no_vig_q
    # return fair_p,fair_q,american_p,american_q

def manual(dawg,fav,pinnacle_dawg,pinnacle_fav): # manually input odds & see expected value and kelly bet size
    underdog_prob, fav_prob, no_vig_underdog, no_vig_fav = remove_vig(pinnacle_dawg,pinnacle_fav)
    under_thresh,fav_thresh = threshold(pinnacle_dawg,pinnacle_fav)
    ### Underdog ###
    under_expectation = expected_value(100,underdog_prob,american_to_decimal(dawg))
    under_kelly = kelly(underdog_prob,decimal_to_fractional(american_to_decimal(dawg)))
    # print(f'Underdog Expectation is {under_expectation} and kelly bet size is {under_kelly}\n')
    # print(f'Underdog Threshold is: {decimal_to_american(under_thresh)}, no-vig underdog is {decimal_to_american(no_vig_underdog)}\n')
    ### Favorite ###
    fav_expectation = expected_value(100,fav_prob,american_to_decimal(fav))
    fav_kelly = kelly(fav_prob, decimal_to_fractional(american_to_decimal(fav)))
    # print(f'Favorite Expectation is {fav_expectation} and kelly bet size is {fav_kelly}')
    # print(f'Favorite Threshold is: {decimal_to_american(fav_thresh)}, no-vig favorite is {decimal_to_american(no_vig_fav)}\n')
    return under_expectation, under_kelly, fav_expectation, fav_kelly

# manual(150,-135,215,-334)

################################################################
###################### API DATA CALL ###########################
################################################################

def sportsbook_data(region,sport, bet_type, API_KEY):
    # An api key is emailed to you when you sign up to a plan
    # Get a free API key at https://api.the-odds-api.com/

    SPORT = 'upcoming' # use the sport_key from the /sports endpoint below, or use 'upcoming' to see the next 8 games across all sports

    REGIONS = region # uk | us | eu | au. Multiple can be specified if comma delimited

    MARKETS = bet_type # h2h | spreads | totals. Multiple can be specified if comma delimited

    ODDS_FORMAT = 'american' # decimal | american

    DATE_FORMAT = 'iso' # iso | unix

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    #
    # First, get a list of live & upcoming games for the sport you want, along with odds for different bookmakers
    # This will deduct from the usage quota
    # The usage quota cost = [number of markets specified] x [number of regions specified]
    # For examples of usage quota costs, see https://the-odds-api.com/liveapi/guides/v4/#usage-quota-costs
    #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

    odds_response = requests.get(
        f'https://api.the-odds-api.com/v4/sports/{sport}/odds',
        params={
            'api_key': API_KEY,
            'regions': REGIONS,
            'markets': MARKETS,
            'oddsFormat': ODDS_FORMAT,
            'dateFormat': DATE_FORMAT,
        }
    )

    if odds_response.status_code != 200:
        print(f'Failed to get odds: status_code {odds_response.status_code}, response body {odds_response.text}')

    else:
        odds_json = odds_response.json()
        print('Number of events:', len(odds_json))
        print(odds_json)

        # Check the usage quota
        print('Remaining requests', odds_response.headers['x-requests-remaining'])
        print('Used requests', odds_response.headers['x-requests-used'])


    data = pd.DataFrame(odds_json)
    return data

################################################################
############## DATA COLLECTION & TRANSFORMATION ################
################################################################

def grab_data(sport,bet_type):
# Pinnacle Book data
    pinnacle_data = sportsbook_data('eu',sport,bet_type)
    pinnacle_dict = {}
    for game in pinnacle_data['id']:
        # Initialize empty dictionary for each game
        game_dict = {}
        # Current Game for EU data (where pinnacle is)
        current_game = pinnacle_data.loc[pinnacle_data.id == game]
        game_dict['home'] = current_game['home_team']
        game_dict['away'] = current_game['away_team']
        for entry in current_game.bookmakers:
            for book in entry:
                if book['key'] == 'pinnacle': # section-off pinnacle data only
                    game_dict['book'] = 'pinnacle'
                    game_dict['bet_type'] = book['markets'][0]['key']
                    # find favorite and underdog
                    sides = {}
                    for team in book['markets'][0]['outcomes']:
                        sides[team['name']] = team['price']
                        favorite = min(sides, key=sides.get)
                        fav_odds = min(sides.values())
                        underdog = max(sides, key=sides.get)
                        dog_odds = max(sides.values())
                    game_dict['favorite'] = favorite
                    game_dict['favorite_odds'] = fav_odds
                    game_dict['underdog'] = underdog
                    game_dict['underdog_odds'] = dog_odds
                    # convert to dataframe & add to dictionary
                    game_df = pd.DataFrame(game_dict)
                    pinnacle_dict[game] = game_df 

# American book data
    american_data = sportsbook_data('us',sport,bet_type)
    american_dict = {}
    for game in american_data['id']:
        # Initialize empty dictionary for each game
        game_dict = {}
        # Current Game for AMERICAN data
        current_game = american_data.loc[american_data.id == game]
        home = current_game['home_team'].iloc[0]
        away = current_game['away_team'].iloc[0]
        # New lists for each game, to append to & create dataframe with    
        for i in ['home','away','book','bet_type','favorite','favorite_odds','fav_EV','fav_kelly','underdog','dog_odds','dog_EV','dog_kelly']:
            game_dict[i] = []
        for entry in current_game.bookmakers:
            for book in entry:
                # print(current_game['home_team'])
                game_dict['home'].append(home) # home team
                game_dict['away'].append(away) # away team
                game_dict['book'].append(book['key'])
                game_dict['bet_type'].append(book['markets'][0]['key'])
                # find favorite and underdog
                sides = {}
                for team in book['markets'][0]['outcomes']:
                    sides[team['name']] = team['price']
                    favorite = min(sides, key=sides.get)
                    fav_odds = min(sides.values())
                    underdog = max(sides, key=sides.get)
                    dog_odds = max(sides.values())
                # gather pinnacle odds for current game & compute EV/Kelly for both sides
                try: # if some games not found and/or listed on pinnacle 
                    pinnacle_dog = pinnacle_dict[game]['underdog_odds']
                    pinnacle_favorite = pinnacle_dict[game]['favorite_odds']
                    under_expectation, under_kelly, fav_expectation, fav_kelly = manual(dog_odds,fav_odds,int(pinnacle_dog),int(pinnacle_favorite))
                    # update lists
                    ## favorite
                    game_dict['favorite'].append(favorite)
                    game_dict['favorite_odds'].append(fav_odds)
                    # game_dict['fav_pinnacle'] = pinnacle_favorite
                    game_dict['fav_EV'].append(fav_expectation)
                    game_dict['fav_kelly'].append(fav_kelly)
                    ## underdog
                    game_dict['underdog'].append(underdog)
                    game_dict['dog_odds'].append(dog_odds)
                    # game_dict['dog_pinnacle'] = pinnacle_dog
                    game_dict['dog_EV'].append(under_expectation)
                    game_dict['dog_kelly'].append(under_kelly)
                except:
                    pass
        # convert to dataframe & add to dictionary
        try:
            game_df = pd.DataFrame(game_dict)
            american_dict[game] = game_df
        except:
            pass
    return pinnacle_dict, american_dict


################################################################
######################## DATA MINING ###########################
################################################################

def mine_helper(relevant,current_pinnacle,side_data,side):
    '''
    @param side is the side we are analyzing (favorite or dog)
    THEREFORE side_data is positive ev data from particular side
    '''
    # EV - specific analysis
    mean_ev = relevant[side].mean()
    range_ev = relevant[side].max() - relevant[side].min()
    stdev_ev = relevant[side].std()
    num_books = len(relevant)
    # Find best book & add pinnacle odds info
    best = relevant.loc[relevant[side].idxmax()]
    best['pinnacle_fav_odds'] = current_pinnacle['favorite_odds'].iloc[0]
    best['pinnacle_dog_odds'] = current_pinnacle['underdog_odds'].iloc[0]
    best['pinnacle_spread'] = abs(abs(best.pinnacle_fav_odds) - abs(best.pinnacle_dog_odds))
    # see if positive EV is listed on fanduel
    if 'fanduel' in set(side_data.book):
        fanduel = 1
    else:
        fanduel = 0
    best['fanduel?'] = fanduel
    best['home?'] = np.where(best.home == best.underdog,1,0)
    return best

###                                                 ###
## Filtering function to filter out irrelevant books ##
###                                                 ###

def filtering(df,irrelevant):
    data = df[df.book.isin(irrelevant) == False]
    return data

# Actual Mining of Data
def mine_data(american_dict, pinnacle_dict):
    dog_list = []
    fav_list = []
    for game in american_dict:
        # current game pin & american
        current_game = american_dict[game]
        current_pinnacle = pinnacle_dict[game]
        # Positive EV for Dog & Favorite
        dog_ev = current_game.loc[current_game.dog_EV > 0]
        favorite_ev = current_game.loc[current_game.fav_EV > 0]
        # Filter out irrelevant books (betfair,bovada,etc.)
        irrelevant = ['bovada','betfair','williamhill_us'] ## CAN PURPOSELY EXCLUDE PARTICULAR BOOKS HERE ##
        relevant_dogs = filtering(dog_ev,irrelevant)
        relevant_favs = filtering(favorite_ev,irrelevant)
        # DAWG
        if relevant_dogs.empty == False:
            dog_best = mine_helper(relevant_dogs,current_pinnacle,dog_ev,'dog_EV')
            dog_list.append(dog_best)
        # FAV
        if relevant_favs.empty == False:
            fav_best = mine_helper(relevant_favs,current_pinnacle,favorite_ev,'fav_EV')
            fav_list.append(fav_best)
    # Concatenate
    dog_data = pd.DataFrame(dog_list)
    fav_data = pd.DataFrame(fav_list)

    return dog_data,fav_data

################################################################
######################## BASKETBALL ############################
################################################################

## NBA ##
def nba():
    pinnacle_dict, american_dict = grab_data('basketball_nba', 'h2h')
    return pinnacle_dict, american_dict

## NCAABB ##
def ncaa_bb():
    pinnacle_dict, american_dict = grab_data('basketball_ncaab', 'h2h')
    return pinnacle_dict, american_dict

################################################################
######################### FOOTBALL #############################
################################################################

def nfl():
    pinnacle_dict, american_dict = grab_data('americanfootball_nfl', 'h2h')
    return pinnacle_dict,american_dict
