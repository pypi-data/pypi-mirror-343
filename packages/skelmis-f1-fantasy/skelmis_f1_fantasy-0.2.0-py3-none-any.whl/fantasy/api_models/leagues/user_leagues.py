from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel

from fantasy.api_models.encoder import URLEncodedStr


class TeamInfoItem(BaseModel):
    teamNo: int
    userRank: Optional[int]


class Leaguesdatum(BaseModel):
    rno: int
    leagueId: int
    teamInfo: List[TeamInfoItem]
    leagueCode: str
    leagueName: URLEncodedStr
    leagueType: str
    leagueAdmin: int
    memeberCount: str
    legaueVipFlag: int
    isSystemnameupd: int
    leagueReportCnt: int
    leagueReportFlg: int
    leagueReportDays: int
    isWebpurifycalled: int
    webPurifyresponse: str


class UserLeaguesResponse(BaseModel):
    leaguesdata: List[Leaguesdatum]
    fetchhthdata: int
    fetchvipdata: int
    leaguestotcnt: int
    leaguesvipcnt: int
    leagueshthscnt: int
    fetchclassicdata: int
    leaguesclassiccnt: int
