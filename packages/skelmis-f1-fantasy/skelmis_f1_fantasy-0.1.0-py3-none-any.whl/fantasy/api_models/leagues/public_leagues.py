from __future__ import annotations

from typing import List

from pydantic import BaseModel

from fantasy.api_models.encoder import URLEncodedStr


class TeamInfoItem(BaseModel):
    teamNo: int
    userRank: int


class Leaguesdatum(BaseModel):
    rno: int
    leagueId: str
    teamInfo: List[TeamInfoItem]
    leagueCode: None
    leagueName: URLEncodedStr
    leagueType: str
    countryCode: str
    leagueAdmin: int
    memberCount: str
    legaueVipFlag: int
    publicdefault: int
    leagueReportCnt: None
    leagueReportFlg: None
    leagueReportDays: None
    isShowleaderboard: int


class PublicStarterLeagueResponse(BaseModel):
    leaguesdata: List[Leaguesdatum]
    leaguespubliccnt: int
