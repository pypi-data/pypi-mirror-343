from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel

from fantasy.api_models.encoder import URLEncodedStr


class SessionWisePoint(BaseModel):
    sessionnumber: int
    sessiontype: str
    points: Optional[int]
    nonegative_points: Optional[int]


class AdditionalStats(BaseModel):
    fastest_lap_pts: float
    dotd_pts: float
    overtaking_pts: float
    q3_finishes_pts: float
    top10_race_position_pts: float
    top8_sprint_position_pts: float
    total_position_pts: float
    total_position_gained_lost: float
    total_dnf_dq_pts: float
    value_for_money: float


class ConstructorOrDriverItem(BaseModel):
    PlayerId: str
    Skill: int
    PositionName: str
    Value: float
    TeamId: str
    FUllName: str
    DisplayName: str
    TeamName: URLEncodedStr
    Status: str
    IsActive: str
    DriverTLA: str
    DriverReference: str
    CountryName: str
    OverallPpints: str
    GamedayPoints: str
    SelectedPercentage: str
    CaptainSelectedPercentage: str
    OldPlayerValue: float
    BestRaceFinished: str
    HigestGridStart: str
    HigestChampFinish: str
    FastestPitstopAward: str
    BestRaceFinishCount: int
    HighestGridStartCount: int
    HighestChampFinishCount: int
    FastestPitstopAwardCount: int
    QualifyingPoints: str
    RacePoints: str
    SprintPoints: str
    NoNegativePoints: str
    F1PlayerId: str
    FirstName: str
    LastName: str
    SessionWisePoints: List[SessionWisePoint]
    AdditionalStats: AdditionalStats
    old_Value: float
    new_value: float
    ProjectedGamedayPoints: str
    ProjectedNoNegativePoints: str
    ProjectedOverallPpints: str


class DriversAndConstructorsResponse:
    data: list[ConstructorOrDriverItem]
