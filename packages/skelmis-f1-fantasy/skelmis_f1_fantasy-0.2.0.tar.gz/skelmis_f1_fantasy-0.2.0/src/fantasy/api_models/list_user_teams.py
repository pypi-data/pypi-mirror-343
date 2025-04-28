from typing import Optional

from pydantic import BaseModel

from fantasy.api_models.encoder import URLEncodedStr


class PlayeridItem(BaseModel):
    id: str
    isfinal: int
    iscaptain: int
    ismgcaptain: int
    playerpostion: int


class TeamInfo(BaseModel):
    teamBal: float
    teamVal: float
    maxTeambal: float
    subsallowed: int
    userSubsleft: int


class UserTeamItem(BaseModel):
    gdrank: None
    ovrank: int
    teamno: int
    teambal: float
    teamval: Optional[float] = None
    gdpoints: None
    matchday: int
    ovpoints: float
    playerid: list[PlayeridItem]
    teamname: URLEncodedStr
    usersubs: int
    boosterid: None
    team_info: TeamInfo
    fttourgdid: int
    fttourmdid: int
    iswildcard: Optional[int]
    maxteambal: Optional[float] = None
    capplayerid: str
    subsallowed: int
    isaccounting: int
    usersubsleft: int
    extrasubscost: int
    islateonboard: Optional[int]
    mgcapplayerid: None
    race_category: None
    finalfxracecat: None
    finalfxraceday: None
    isboostertaken: Optional[int]
    extradrstakengd: None
    finalfixtakengd: None
    isextradrstaken: int
    isfinalfixtaken: int
    issystemnameupd: int
    iswildcardtaken: int
    wildcardtakengd: int
    autopilottakengd: None
    isautopilottaken: int
    islimitlesstaken: int
    limitlesstakengd: None
    isnonigativetaken: int
    iswebpurifycalled: int
    nonigativetakengd: Optional[int]
    webpurifyresponse: str
    finalfxnewplayerid: None
    finalfxoldplayerid: None
    player_swap_details: None
    is_wildcard_taken_gd_id: None
    inactive_driver_penality_points: int


class CurrentUsersTeamsResponse(BaseModel):
    mdid: int
    userTeam: list[UserTeamItem]
    retval: int
