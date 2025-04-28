from __future__ import annotations

import json
from typing import Literal

import httpx

from fantasy import api_models


class APIClient:
    def __init__(self, *, token: str, user_guid: str):
        """Not intended to be instantiated directly."""
        self.token = token
        self.user_guid = user_guid
        self._client = httpx.AsyncClient(
            base_url="https://fantasy.formula1.com",
            cookies={"F1_FANTASY_007": self.token},
        )

    async def request(
        self,
        method: Literal["GET", "POST", "PUT", "PATCH", "DELETE"],
        url: str,
        json_data: dict = None,
    ) -> dict:
        resp = await self._client.request(method, url, json=json_data)
        resp.raise_for_status()
        return resp.json()

    async def _handle_api_call(self, url: str, model):
        data = await self.request("GET", url)

        if data["Data"] is None:
            raise ValueError(data["Meta"])

        if isinstance(data["Data"]["Value"], list):
            return model(data=data["Data"]["Value"])

        return model(**data["Data"]["Value"])

    async def get_public_starter_leagues(
        self,
    ) -> api_models.PublicStarterLeagueResponse:
        """Return the starter leagues.

        Returns
        -------
        api_models.PublicStarterLeagueResponse
        """
        return await self._handle_api_call(
            f"/services/user/league/{self.user_guid}/getuserpublicleague/1",
            api_models.PublicStarterLeagueResponse,
        )

    async def get_public_classic_leagues(
        self,
    ) -> api_models.PublicClassicLeagueResponse:
        """Return the classic public leagues.

        Returns
        -------
        api_models.PublicClassicLeagueResponse
        """
        return await self._handle_api_call(
            f"/services/user/league/{self.user_guid}/1/1/100/0/0/publicleague",
            api_models.PublicClassicLeagueResponse,
        )

    async def get_private_classic_leagues(
        self,
    ) -> api_models.PrivateClassicLeaguesResponse:
        """Return the classic private leagues.

        Returns
        -------
        api_models.PrivateClassicLeaguesResponse
        """
        return await self._handle_api_call(
            f"/services/user/league/{self.user_guid}/1/0/0/privateleague",
            api_models.PrivateClassicLeaguesResponse,
        )

    async def get_h2h_leagues(
        self,
    ) -> api_models.Head2HeadLeaguesResponse:
        """Return the head 2 head leagues.

        Returns
        -------
        api_models.Head2HeadLeaguesResponse
        """
        return await self._handle_api_call(
            f"/services/user/league/{self.user_guid}/1/0/0/hthbattle",
            api_models.Head2HeadLeaguesResponse,
        )

    async def get_pinned_leagues(
        self,
    ) -> api_models.PinnedLeaguesResponse:
        """Return the pinned leagues.

        Returns
        -------
        api_models.PinnedLeaguesResponse
        """
        return await self._handle_api_call(
            f"/services/user/league/{self.user_guid}/1/0/0/pinnedleague",
            api_models.PinnedLeaguesResponse,
        )

    async def get_user_leagues(
        self,
    ) -> api_models.UserLeaguesResponse:
        """Return the user leagues.

        Returns
        -------
        api_models.UserLeaguesResponse
        """
        return await self._handle_api_call(
            f"/services/user/league/{self.user_guid}/getuserleague/1",
            api_models.UserLeaguesResponse,
        )

    async def get_featured_leagues(
        self,
    ) -> api_models.FeaturedLeaguesResponse:
        """Return the featured leagues.

        Returns
        -------
        api_models.FeaturedLeaguesResponse
        """
        return await self._handle_api_call(
            f"/services/user/league/{self.user_guid}/1/0/0/featuredleague",
            api_models.FeaturedLeaguesResponse,
        )

    async def get_mini_leagues(self):
        raise NotImplementedError("I cant implement this until I get my hands on one.")

    async def get_h2h_leaderboard(self):
        raise NotImplementedError("I cant implement this until I get my hands on one.")

    async def get_public_leaderboard(self):  # leaderboard_id: int
        raise NotImplementedError(
            "I don't currently use this, therefore its not implemented."
        )

    async def get_private_leaderboard(
        self, league_id: int
    ) -> api_models.PrivateLeagueLeaderboardResponse:
        """Fetch a private leagues leaderboard.

        Parameters
        ----------
        league_id: int
            The league to get a leaderboard for.

        Returns
        -------
        api_models.PrivateLeagueLeaderboardResponse
        """
        return await self._handle_api_call(
            f"/services/user/leaderboard/{self.user_guid}/pvtleagueuserrankget/1/{league_id}/0/1/1/1000/",
            api_models.PrivateLeagueLeaderboardResponse,
        )

    async def get_user_game_days(self) -> api_models.UserGameDaysResponse:
        """Get how an insight into how many points you gained each race.

        Returns
        -------
        api_models.UserGameDaysResponse
        """
        return await self._handle_api_call(
            f"/services/user/gameplay/{self.user_guid}/getusergamedaysv1/1",
            api_models.UserGameDaysResponse,
        )

    async def get_current_race_id(self) -> int:
        """Fetches the current race id.

        Raises
        ------
        ValueError
            Due to how this works internally, this method
            relies on you having at least one team.

        Returns
        -------
        int
            The race id to use
        """
        data: api_models.UserGameDaysResponse = await self.get_user_game_days()
        races_occurred = data.data[0].mddetails.keys()
        return int(max(races_occurred))

    async def get_drivers_and_constructors(
        self, race_id: int
    ) -> api_models.DriversAndConstructorsResponse:
        """

        Parameters
        ----------
        race_id: int
            The race ID to get the drivers and constructors for.

            1 indexed from the start of the year.

            Historical data appears to be fetchable via older race ids.

            To get the current race id, call get_current_race_id()

        Returns
        -------
        api_models.DriversAndConstructorsResponse
        """
        return await self._handle_api_call(
            f"/feeds/drivers/{race_id}_en.json",
            api_models.DriversAndConstructorsResponse,
        )

    async def get_my_teams(self, race_id: int) -> api_models.CurrentUsersTeamsResponse:
        """List all the auth'd users current teams.

        Parameters
        ----------
        race_id: int
            The race id to fetch the teams as at.

            To get the current race id, call get_current_race_id()

        Returns
        -------
        api_models.CurrentUsersTeamsResponse
        """
        return await self._handle_api_call(
            # str and int's in path seem arbitrary.
            # Copied this from my observed requests
            f"/services/user/gameplay/{self.user_guid}/getteam/1/1/{race_id}/1",
            api_models.CurrentUsersTeamsResponse,
        )

    async def get_home_stats(self) -> api_models.HomeStatsResponse:
        """Get the home page stats.

        These are previous race result + season stats
        for the currently authed user.

        Returns
        -------
        api_models.HomeStatsResponse
        """
        return await self._handle_api_call(
            f"/services/user/cards/{self.user_guid}/homestats",
            api_models.HomeStatsResponse,
        )

    @staticmethod
    async def _renew_reese_token(old_token: str) -> api_models.Reese64Response:
        # Looks like can renew?
        async with httpx.AsyncClient() as client:
            resp: httpx.Response = await client.post(
                url="https://api.formula1.com/6657193977244c13?d=account.formula1.com",
                headers={
                    "Host": "api.formula1.com",
                    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Gecko/137.0",
                    "Accept": "application/json; charset=utf-8",
                    "Accept-Language": "en-US,en;q=0.5",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Referer": "https://account.formula1.com/",
                    "Content-Type": "text/plain; charset=utf-8",
                    "Origin": "https://account.formula1.com",
                    "Sec-Fetch-Dest": "empty",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Site": "same-site",
                    "Dnt": "1",
                    "Sec-Gpc": "1",
                    "Priority": "u=4",
                    "Te": "trailers",
                },
                cookies=[],
                content=f'"{old_token}"',
            )
            resp.raise_for_status()
            return api_models.Reese64Response(**resp.json())

    @staticmethod
    async def _get_reese_token() -> api_models.Reese64Response:
        # TODO This doesn't work
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                "https://api.formula1.com/6657193977244c13?d=account.formula1.com",
                json={
                    "solution": {
                        "interrogation": {
                            "st": 162229509,
                            "sr": 1959639815,
                            "cr": 78830557,
                            "og": 2,
                        },
                        "version": "stable",
                    },
                    "old_token": None,
                    "error": None,
                    "performance": {"interrogation": 401},
                },
            )
            resp.raise_for_status()
            return api_models.Reese64Response(**resp.json())

    @classmethod
    async def _auth_account(
        cls, username: str, password: str, reese84: str
    ) -> api_models.AuthResponse:
        """Token is valid for about five days"""
        async with httpx.AsyncClient() as client:
            resp: httpx.Response = await client.post(
                url="https://api.formula1.com/v2/account/subscriber/authenticate/by-password",
                headers={
                    "Host": "api.formula1.com",
                    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Gecko/137.0",
                    "Accept": "application/json, text/javascript, */*; q=0.01",
                    "Accept-Language": "en-US,en;q=0.5",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Content-Type": "application/json",
                    "Apikey": "fCUCjWrKPu9ylJwRAv8BpGLEgiAuThx7",
                    "Origin": "https://account.formula1.com",
                    "Referer": "https://account.formula1.com/",
                    "Sec-Fetch-Dest": "empty",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Site": "same-site",
                    "Dnt": "1",
                    "Sec-Gpc": "1",
                    "Priority": "u=0",
                    "Te": "trailers",
                },
                cookies=[
                    ("reese84", reese84),
                ],
                json={
                    "Login": username,
                    "Password": password,
                    "DistributionChannel": "d861e38f-05ea-4063-8776-a7e2b6d885a4",
                },
            )
            resp.raise_for_status()
            return api_models.AuthResponse(**resp.json())

    @classmethod
    async def login(cls, username: str, password: str) -> APIClient:
        """Login to the API and receive a valid client."""
        reese_token = await cls._get_reese_token()
        renewed_token = await cls._renew_reese_token(reese_token.token)
        auth = await cls._auth_account(username, password, renewed_token.token)
