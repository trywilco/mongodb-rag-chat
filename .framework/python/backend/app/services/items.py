from slugify import slugify

from app1.db.errors import EntityDoesNotExist
from app1.db.repositories.items import ItemsRepository
from app1.models.domain.items import Item
from app1.models.domain.users import User


async def check_item_exists(items_repo: ItemsRepository, slug: str) -> bool:
    try:
        await items_repo.get_item_by_slug(slug=slug)
    except EntityDoesNotExist:
        return False

    return True


def get_slug_for_item(title: str) -> str:
    return slugify(title)


def check_user_can_modify_item(item: Item, user: User) -> bool:
    return item.seller.username == user.username
