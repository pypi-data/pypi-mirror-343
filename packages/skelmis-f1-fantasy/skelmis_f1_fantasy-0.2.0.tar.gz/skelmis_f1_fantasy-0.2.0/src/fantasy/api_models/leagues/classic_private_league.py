from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel

from fantasy.api_models.encoder import URLEncodedStr


class TeamInfoItem(BaseModel):
    teamNo: int
    userRank: int


class Tag(BaseModel):
    id: int
    name: str


class Detail(BaseModel):
    isWebPurifyCalled: int
    isProfaneNameFlag: int
    publicDefault: Optional[str]
    leagueVIPFlag: int
    showLeaderBoard: int
    createdDate: Optional[str]
    bannerUrl: str
    bannerInternalUrl: str
    pinDate: Optional[str]
    leagueId: str
    leagueName: URLEncodedStr
    leagueCode: str
    isAdmin: int
    isProfanity: str
    isSystemNameUpd: int
    memberCount: str
    teamInfo: Optional[List[TeamInfoItem]]
    leagueType: str
    rno: int
    isReportFlag: int
    isReportLeagueCount: int
    isLeagueCountDay: int
    memberPer: int
    maxMembers: int
    noOfTeams: int
    isSponsor: int
    isPinned: int
    isLastChance: int
    isPopular: int
    isNew: int
    isJoined: int
    tag: Optional[Tag]


class Count(BaseModel):
    classicLeagueCount: int
    vipLeagueCount: int
    leagueCount: int
    sponsorleagueCount: int


class PrivateClassicLeaguesResponse(BaseModel):
    Details: List[Detail]
    VipLeague: List
    Count: Count
