from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel, to_snake, to_pascal


class Reese64Response(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)
    token: str
    renew_in_sec: int
    cookie_domain: str


class AuthSubscriberResponse(BaseModel):
    FirstName: str
    LastName: str
    HomeCountry: str
    Id: int
    Email: str
    Login: str


class AuthDataResponse(BaseModel):
    subscriptionStatus: str
    subscriptionToken: str


class AuthResponse(BaseModel):
    SessionId: str
    PasswordIsTemporary: bool
    Subscriber: AuthSubscriberResponse
    Country: str
    data: AuthDataResponse
