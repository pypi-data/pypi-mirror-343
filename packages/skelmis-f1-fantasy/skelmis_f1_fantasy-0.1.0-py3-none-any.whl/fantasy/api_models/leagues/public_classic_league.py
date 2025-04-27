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
    publicDefault: str
    leagueVIPFlag: int
    showLeaderBoard: int
    bannerUrl: Optional[str]
    bannerInternalUrl: Optional[str]
    pinDate: None
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
    tag: Tag


class Count(BaseModel):
    leagueCount: int
    sponsorleagueCount: int


class PublicClassicLeagueResponse(BaseModel):
    Details: List[Detail]
    Count: Count
