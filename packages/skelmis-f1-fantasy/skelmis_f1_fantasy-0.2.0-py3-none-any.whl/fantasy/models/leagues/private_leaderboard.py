from pydantic import BaseModel, Field


class PrivateLeaderboardEntrant(BaseModel):
    team_id: int
    team_number: int = Field(description="Is this the users team 1/2/3?")
    team_name: str
    user_name: str
    is_league_admin: bool
    overall_points: int
    rank_in_league: int
    guid: str


class PrivateLeaderboard(BaseModel):
    members: list[PrivateLeaderboardEntrant]
    league_id: int
    league_member_count: int | None
    league_invite_code: str
    league_name: str
