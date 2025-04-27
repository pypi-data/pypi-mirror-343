from __future__ import annotations

from typing import List

from pydantic import BaseModel

from fantasy.api_models.encoder import URLEncodedStr


class TeamRacePoints(BaseModel):
    mds: int
    phId: int
    pts: float | None

    @property
    def points(self) -> float:
        return self.pts


class RacePoints(BaseModel):
    racePt: float
    gdId: int
    poinstDif: float


class OverallBestweek(BaseModel):
    gdid: int
    points: float


class BestDriverWeekItem(BaseModel):
    playerid: str
    points: float
    playertype: str
    skillid: int
    gdid: int


class BestDriverOverallItem(BaseModel):
    playerid: str
    points: float
    playertype: str
    skillid: int


class Userhome(BaseModel):
    teanNo: int
    ovPoints: float
    racePoints: RacePoints
    overallBestweek: OverallBestweek
    bestDriverWeek: List[BestDriverWeekItem]
    bestDriverOverall: List[BestDriverOverallItem]
    totalTransfer: int
    freeTransfer: int
    nigativeTransfer: int


class ValueItem(BaseModel):
    ftmdid: int
    ftgdid: int
    cugdid: int
    cumdid: int
    prvmdid: int
    islastday: int
    lastdaygdid: int
    teamid: int
    teamno: int
    teamname: URLEncodedStr
    iswildcardtaken: int
    wildcardtakengd: int
    islimitlesstaken: int
    limitlesstakengd: int
    isfinalfixtaken: int
    finalfixtakengd: int
    isextradrstaken: int
    extradrstakengd: int
    isnonigativetaken: int
    nonigativetakengd: int
    isautopilottaken: int
    isautopilottakengd: int
    islateonboard: int
    mddetails: dict[str, TeamRacePoints]
    userhome: Userhome
    teamcount: int
    iswebpurifycalled: int
    webpurifyresponse: str
    issystemnameupd: int

    @property
    def points_per_race(self) -> dict[str, TeamRacePoints]:
        return self.mddetails


class UserGameDaysResponse(BaseModel):
    data: list[ValueItem]
