from pydantic import BaseModel

from app1.models.domain.profiles import Profile


class ProfileInResponse(BaseModel):
    profile: Profile
