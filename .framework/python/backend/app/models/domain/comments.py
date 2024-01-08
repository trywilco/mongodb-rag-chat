from app1.models.common import DateTimeModelMixin, IDModelMixin
from app1.models.domain.profiles import Profile
from app1.models.domain.rwmodel import RWModel


class Comment(IDModelMixin, DateTimeModelMixin, RWModel):
    body: str
    seller: Profile
