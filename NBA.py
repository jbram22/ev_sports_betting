# import necessary utils functions (just import all to make things easier)
from utils import nba, mine_data

if __name__ == "__main__":
    # Grab data
    nba_pinnacle_dict, nba_american_dict = nba()

    # Sift thru games
    for game in nba_american_dict:
        
        current = nba_american_dict[game]
        positive = current.loc[(current["fav_EV"] > 0) | (current["dog_EV"] > 0)]

        if not positive.empty:
            print(
                positive[
                    [
                        "book",
                        "home",
                        "away",
                        "favorite_odds",
                        "dog_odds",
                        "fav_EV",
                        "fav_kelly",
                        "dog_EV",
                        "dog_kelly"
                    ]
                ],
                "\n",
            )
    # Data Mining
    nba_dog_data, nba_fav_data = mine_data(nba_american_dict, nba_pinnacle_dict)
