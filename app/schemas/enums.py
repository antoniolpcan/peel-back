from enum import Enum

class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"

class PostSortField(str, Enum):
    title = "title"
    likes = "likes"
    created_at = "created_at"