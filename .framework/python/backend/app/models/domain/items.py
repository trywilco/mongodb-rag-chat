from typing import List, Optional

from app1.models.common import DateTimeModelMixin, IDModelMixin
from app1.models.domain.profiles import Profile
from app1.models.domain.rwmodel import RWModel


class Item(IDModelMixin, DateTimeModelMixin, RWModel):
    slug: str
    title: str
    description: str
    tags: List[str]
    seller: Profile
    favorited: bool
    favorites_count: int
    image: Optional[str]
    body: Optional[str]
