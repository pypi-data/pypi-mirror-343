from __future__ import annotations

import typing

import commons

from fantasy import models
from fantasy.models import leagues

if typing.TYPE_CHECKING:
    from fantasy import APIClient


class Client:
    def __init__(self, api_client: APIClient):
        self.api: APIClient = api_client

    async def get_private_league_leaderboard(
        self, league_id: int
    ) -> leagues.PrivateLeaderboard:
        """Fetch the leaderboard for your league!

        Parameters
        ----------
        league_id: int
            The league id we want a leaderboard for.

        Returns
        -------
        models.PrivateLeaderboard
        """
        raw_data = await self.api.get_private_leaderboard(league_id)
        entrants: list[leagues.PrivateLeaderboardEntrant] = []
        for member in raw_data.memRank:
            entrants.append(
                leagues.PrivateLeaderboardEntrant(
                    team_id=member.teamId,
                    team_number=member.teamNo,
                    team_name=member.teamName,
                    user_name=member.userName,
                    is_league_admin=commons.value_to_bool(member.isAdmin),
                    overall_points=member.total_current_points,
                    rank_in_league=member.rank,
                    guid=member.guid,
                )
            )

        return leagues.PrivateLeaderboard(
            members=entrants,
            league_id=league_id,
            league_member_count=(
                int(raw_data.leagueInfo.memCount)
                if raw_data.leagueInfo.memCount
                else None
            ),
            league_invite_code=raw_data.leagueInfo.leagueCode,
            league_name=raw_data.leagueInfo.leagueName,
        )

    async def get_user_leagues(self) -> leagues.UserLeagues:
        """Fetch the various user leagues you are a part of.

        Notes
        -----
        Does not appear to include public leagues.

        Returns
        -------
        leagues.UserLeagues
        """
        raw_data = await self.api.get_user_leagues()
        data: list[leagues.UserLeaguesEntrant] = []
        for league in raw_data.leaguesdata:
            teams_in_league: list[leagues.UserLeagueTeam] = []
            for team in league.teamInfo:
                teams_in_league.append(
                    leagues.UserLeagueTeam(
                        team_number=team.teamNo,
                        rank_in_league=team.userRank,
                    )
                )

            data.append(
                leagues.UserLeaguesEntrant(
                    league_id=league.leagueId,
                    league_invite_code=league.leagueCode,
                    league_name=league.leagueName,
                    league_type=league.leagueType,
                    is_league_admin=commons.value_to_bool(league.leagueAdmin),
                    member_count=(
                        int(league.memeberCount) if league.memeberCount else None
                    ),
                    league_vip_flag=league.legaueVipFlag,
                    teams_in_league=teams_in_league,
                )
            )

        return leagues.UserLeagues(
            leagues=data,
            total_count=raw_data.leaguestotcnt,
            vip_count=raw_data.leaguesvipcnt,
            classic_leagues_count=raw_data.leaguesclassiccnt,
        )
