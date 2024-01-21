# import necessary utils functions (just import all to make things easier)
from utils import nfl, mine_data

if __name__ == "__main__":
    # Grab data
    nfl_pinnacle_dict, nfl_american_dict = nfl()

    # Sift thru games
    for game in nfl_american_dict:

        current = nfl_american_dict[game]
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

    nfl_dog_data, nfl_fav_data = mine_data(nfl_american_dict, nfl_pinnacle_dict)
