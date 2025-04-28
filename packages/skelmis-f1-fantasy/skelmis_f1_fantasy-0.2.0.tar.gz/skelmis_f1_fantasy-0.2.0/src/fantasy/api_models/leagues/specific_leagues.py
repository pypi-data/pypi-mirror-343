from __future__ import annotations

from pydantic import BaseModel

from fantasy.api_models.encoder import URLEncodedStr


class TeamInfoItem(BaseModel):
    teamNo: int
    userRank: int


class League(BaseModel):
    isProfaneNameFlag: int
    leagueVIPFlag: int
    createdDate: str
    isenableforusers: int
    raceWeek: None
    locktime: None
    disableonlist: int
    showonlist: int
    isWebPurifyCalled: int
    publicDefault: None
    showLeaderBoard: int
    bannerUrlFlag: int
    bannerUrl: str
    bannerInternalUrl: str
    leagueId: str
    leagueName: URLEncodedStr
    leagueCode: str
    isAdmin: int
    isProfanity: str
    isSystemNameUpd: int
    memberCount: str
    teamInfo: list[TeamInfoItem]
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
    tag: None


class TotalLeaguesCount(BaseModel):
    """How many leagues your user is in."""

    privateCount: int
    classicCount: int
    miniCount: int
    H2HCount: int


class SpecificLeagueResponse(BaseModel):
    Details: list[League]
    Count: TotalLeaguesCount
