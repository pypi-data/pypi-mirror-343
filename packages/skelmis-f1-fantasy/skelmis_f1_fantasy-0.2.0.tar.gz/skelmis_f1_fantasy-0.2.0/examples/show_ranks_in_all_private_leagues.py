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
