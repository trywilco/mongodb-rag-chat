from fastapi import APIRouter, Depends

from app1.api.dependencies.database import get_repository
from app1.db.repositories.tags import TagsRepository
from app1.models.schemas.tags import TagsInList

router = APIRouter()


@router.get("", response_model=TagsInList, name="tags:get-all")
async def get_all_tags(
    tags_repo: TagsRepository = Depends(get_repository(TagsRepository)),
) -> TagsInList:
    tags = await tags_repo.get_all_tags()
    return TagsInList(tags=tags)
