from __future__ import annotations

from typing import List

from pydantic import BaseModel

from fantasy.api_models.encoder import URLEncodedStr


class User(BaseModel):
    teamNo: int
    socialId: str
    isLeft: int
    isLeftAdmin: int
    userName: str
    teamName: URLEncodedStr
    userGuid: str
    points: str
    # Unsure of this type at time of writing as dont have one
    lastFiveResult: None | dict | list


class Detail(BaseModel):
    leagueId: str
    leagueName: URLEncodedStr
    leagueCode: str
    isActive: int
    battleStartGameday: int
    battleStartMatchday: int
    memberCount: str
    users: List[User]
    maximumMembers: str
    isReportFlag: int
    isReportLeagueCount: int
    isLeagueCountDay: int
    rno: int
    seasonTabFlag: int
    isPopular: int
    isWebPurifyCalled: int
    isSystemNameUpd: int
    gamedayId: int
    leagueType: str
    isAdmin: int
    isPinned: int
    pinDate: None


class Count(BaseModel):
    headtoheadCount: int


class Head2HeadLeaguesResponse(BaseModel):
    Details: List[Detail]
    Count: Count
