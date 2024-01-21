# import necessary utils functions (just import all to make things easier)
from utils import ncaa_bb, mine_data

if __name__ == "__main__":
    # Grab data
    ncaabb_pinnacle_dict, ncaabb_american_dict = ncaa_bb()

    # Sift thru games
    for game in ncaabb_american_dict:
        
        current = ncaabb_american_dict[game]
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

    ncaabb_dog_data, ncaabb_fav_data = mine_data(
        ncaabb_american_dict, ncaabb_pinnacle_dict
    )
