from typing import Optional

from fastapi import Depends, HTTPException, Path
from starlette import status

from app1.api.dependencies import items, authentication, database
from app1.db.errors import EntityDoesNotExist
from app1.db.repositories.comments import CommentsRepository
from app1.models.domain.items import Item
from app1.models.domain.comments import Comment
from app1.models.domain.users import User
from app1.resources import strings


async def get_comment_by_id_from_path(
    comment_id: int = Path(..., ge=1),
    item: Item = Depends(items.get_item_by_slug_from_path),
    user: Optional[User] = Depends(
        authentication.get_current_user_authorizer(required=False),
    ),
    comments_repo: CommentsRepository = Depends(
        database.get_repository(CommentsRepository),
    ),
) -> Comment:
    try:
        return await comments_repo.get_comment_by_id(
            comment_id=comment_id,
            item=item,
            user=user,
        )
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=strings.COMMENT_DOES_NOT_EXIST,
        )


