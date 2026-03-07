import asyncio
import json
from typing import Optional, List, Dict, Any
from playwright.async_api import BrowserContext, Page, Route, Request
from xhs_utils.data_models import SearchResult, Note, User


class XHSApiHandler:
    def __init__(self, context: Optional[BrowserContext]):
        self.context = context
        self.page: Optional[Page] = None
        self.search_data: List[Dict[str, Any]] = []

    async def _intercept_api(self, route: Route, request: Request):
        response = await route.fetch()
        try:
            data = await response.json()
            if "items" in data or ("data" in data and "items" in data.get("data", {})):
                self.search_data.append(data)
        except Exception:
            pass
        await route.continue_()

    async def search(self, keyword: str, limit: int = 20) -> SearchResult:
        if not self.context:
            raise ValueError("Browser context is not available")

        self.page = await self.context.new_page()
        self.search_data = []

        await self.page.route("**/api/sns/web/v1/search/notes*", self._intercept_api)

        search_url = (
            f"https://www.xiaohongshu.com/search_result?keyword={keyword}&type=51"
        )
        await self.page.goto(search_url)
        await self.page.wait_for_timeout(3000)

        for _ in range(3):
            await self.page.mouse.wheel(0, 500)
            await self.page.wait_for_timeout(1000)

        items = []

        for data in self.search_data:
            result_items = (
                data.get("data", {}).get("items", [])
                if "data" in data
                else data.get("items", [])
            )
            for item in result_items:
                note_card = item.get("note_card", {})
                if note_card:
                    try:
                        user_info = note_card.get("user", {})
                        interact_info = note_card.get("interact_info", {})
                        cover_info = note_card.get("cover", {})

                        author = User(
                            user_id=user_info.get("user_id", ""),
                            nickname=user_info.get("nickname", "")
                            or user_info.get("nick_name", ""),
                            avatar=user_info.get("avatar", ""),
                        )

                        note = Note(
                            note_id=item.get("note_id", "") or item.get("id", ""),
                            title=note_card.get("display_title", ""),
                            cover=cover_info.get("url_default", "")
                            or cover_info.get("url", ""),
                            liked_count=int(interact_info.get("liked_count", 0) or 0),
                            comment_count=int(
                                interact_info.get("comment_count", 0) or 0
                            ),
                            collect_count=int(
                                interact_info.get("collected_count", 0) or 0
                            ),
                            share_count=int(interact_info.get("shared_count", 0) or 0),
                            author=author,
                        )
                        items.append(note)
                    except Exception as e:
                        pass

        await self.page.close()
        return SearchResult(
            items=items[:limit], total=len(items), has_more=len(items) > limit
        )
