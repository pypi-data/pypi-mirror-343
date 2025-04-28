from __future__ import annotations

from typing import List

from pydantic import BaseModel

from fantasy.api_models.encoder import URLEncodedStr


class TeamInfoItem(BaseModel):
    teamNo: int
    userRank: int


class Detail(BaseModel):
    isProfaneNameFlag: int
    leagueVIPFlag: int
    createdDate: str
    isenableforusers: int
    raceWeek: None
    locktime: None
    disableonList: int
    showonList: int
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
    teamInfo: List[TeamInfoItem]
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


class Count(BaseModel):
    privateCount: int
    classicCount: int
    miniCount: int
    H2HCount: int


class PinnedLeaguesResponse(BaseModel):
    Details: List[Detail]
    Count: Count
