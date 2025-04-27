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
    isProfaneNameFlag: int
    leagueVIPFlag: int
    createdDate: None
    isenableforusers: int
    raceWeek: None
    locktime: None
    disableonList: int
    showonList: int
    isWebPurifyCalled: int
    publicDefault: Optional[str]
    showLeaderBoard: int
    bannerUrlFlag: int
    bannerUrl: str
    bannerInternalUrl: str
    orderNo: int
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
    privateCount: int
    classicCount: int
    miniCount: int
    H2HCount: int


class FeaturedLeaguesResponse(BaseModel):
    Details: List[Detail]
    Count: Count
