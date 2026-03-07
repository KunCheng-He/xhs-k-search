from typing import Optional, List
from pydantic import BaseModel


class User(BaseModel):
    user_id: str
    nickname: str
    avatar: Optional[str] = None
    desc: Optional[str] = None


class Note(BaseModel):
    note_id: str
    title: str
    desc: Optional[str] = None
    cover: Optional[str] = None
    author: User
    liked_count: int = 0
    comment_count: int = 0
    collect_count: int = 0
    share_count: int = 0
    tag_list: List[str] = []


class Comment(BaseModel):
    comment_id: str
    user: User
    content: str
    liked_count: int = 0
    create_time: int = 0


class NoteDetail(BaseModel):
    note: Note
    comment_list: List[Comment] = []


class SearchResult(BaseModel):
    items: List[Note]
    total: int = 0
    has_more: bool = False
