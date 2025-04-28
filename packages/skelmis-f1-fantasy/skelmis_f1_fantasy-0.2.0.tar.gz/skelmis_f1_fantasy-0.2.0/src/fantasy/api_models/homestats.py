from typing import Annotated

from pydantic import BaseModel, EncodedStr

from fantasy.api_models.encoder import URLEncodedStr


class BestDriver(BaseModel):
    playerId: str
    points: int
    type: str
    skillId: int


class TeamDetail(BaseModel):
    teamId: int
    teamNo: int
    teamName: URLEncodedStr
    racePoints: int
    racePointsDifference: int
    chipsUsed: list
    bestDrivers: list[BestDriver]


class PreviousRaceResults(BaseModel):
    previousMatchdayId: int
    currentMatchdayId: int
    teamDetails: list[TeamDetail]


class RaceweekStats(BaseModel):
    gamedayId: int
    points: int


class Transfers(BaseModel):
    total: int
    free: int
    negative: int


class ChipsUsedItem(BaseModel):
    chipId: int
    chipGamedayId: int


class SeasonStat(BaseModel):
    teamId: int
    teamNo: int
    teamName: URLEncodedStr
    points: int
    raceweekStats: RaceweekStats
    bestDrivers: list[BestDriver]
    transfers: Transfers
    chipsUsed: list[ChipsUsedItem]


class PrivateItem(BaseModel):
    leaguename: str
    rank: int


class PublicItem(BaseModel):
    leaguename: str
    rank: int


class LeagueSummaryItem(BaseModel):
    teamNo: int
    teamName: None
    private: list[PrivateItem]
    public: list[PublicItem]


class HomeStatsResponse(BaseModel):
    previousRaceResults: PreviousRaceResults
    seasonStats: list[SeasonStat]
    featuredLeague: None
    sponsorLeague: None
    leagueSummary: list[LeagueSummaryItem]
