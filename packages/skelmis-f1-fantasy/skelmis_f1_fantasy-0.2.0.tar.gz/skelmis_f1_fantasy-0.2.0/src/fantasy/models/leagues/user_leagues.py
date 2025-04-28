from pydantic import BaseModel, Field


class UserLeagueTeam(BaseModel):
    team_number: int = Field(description="Is this team 1/2/3")
    rank_in_league: int | None


class UserLeaguesEntrant(BaseModel):
    # Bunch of fields missing but unsure of use case
    league_id: int
    teams_in_league: list[UserLeagueTeam]
    league_invite_code: str
    league_name: str
    league_type: str = Field(description="API internal type")
    is_league_admin: bool
    member_count: int | None
    league_vip_flag: int = Field(description="API field")


class UserLeagues(BaseModel):
    leagues: list[UserLeaguesEntrant]
    vip_count: int
    total_count: int
    classic_leagues_count: int
