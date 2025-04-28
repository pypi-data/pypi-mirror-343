F1 Fantasy API Client
---

A mildy janky implementation letting you browser the F1 fantasy data set. Certain values are guaranteed to be wrong and methods missing due to a lack of public methods. This is a best guess implementation, and I'd love any feedback.


### Basic Usage

- Navigate to https://fantasy.formula1.com
- Open dev tools for your browser (typically F12)
- Click `Network`
- Login
- Look for a request to `/services/session/login`
- Click `Response`
- Copy the value of `GUID` and `Token`.
- See below example.

```python
import os
import asyncio

from fantasy import Client, APIClient


async def main():
    """Shows your highest place in all your private leagues."""
    client = Client(
        APIClient(
            user_guid=os.environ["USER_GUID"],
            token=os.environ["TOKEN"],
        )
    )

    user_leagues = await client.get_user_leagues()
    for league in user_leagues.leagues:
        leaderboard = await client.get_private_league_leaderboard(league.league_id)
        ranks = [i.rank_in_league for i in league.teams_in_league]
        print(f"League: {leaderboard.league_name}\n\tBest rank: {max(ranks)}")


if __name__ == "__main__":
    asyncio.run(main())
```

### Further Usage

The class `fantasy.Client` exposes all the nice data models, however many are missing.

If you want full access, use `fantasy.APIClient` which implements significantly more but provides the data as the API does which is hard to work with.