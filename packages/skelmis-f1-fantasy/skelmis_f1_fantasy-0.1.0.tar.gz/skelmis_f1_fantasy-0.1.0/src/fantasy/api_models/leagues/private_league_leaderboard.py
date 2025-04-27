from __future__ import annotations

from typing import List

from pydantic import BaseModel

from fantasy.api_models.encoder import URLEncodedStr


class LeagueInfo(BaseModel):
    leagueid: int
    memCount: str
    leagueCode: str
    leagueName: URLEncodedStr


class MemRankItem(BaseModel):
    teamId: int
    teamNo: int
    teamName: URLEncodedStr
    userName: str
    guid: str
    isAdmin: int
    rno: int
    ovPoints: int
    rank: int
    trend: int
    lpgdid: int

    @property
    def total_current_points(self) -> int:
        return self.ovPoints

    @property
    def current_place(self) -> int:
        return self.rank


class UserRankItem(BaseModel):
    teamId: int
    teamNo: int
    teamName: URLEncodedStr
    userName: str
    guid: str
    isAdmin: int
    rno: int
    ovPoints: int
    rank: int
    trend: int

    @property
    def total_current_points(self) -> int:
        return self.ovPoints


class PrivateLeagueLeaderboardResponse(BaseModel):
    leagueInfo: LeagueInfo
    memRank: List[MemRankItem]
    userRank: List[UserRankItem]

    @property
    def rankings(self) -> list[MemRankItem]:
        # userRank is in memRank anyway it appears
        return self.memRank
