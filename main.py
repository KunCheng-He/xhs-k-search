import argparse
import asyncio
import json
import sys
from pathlib import Path

from login_helper import LoginHelper
from xhs_utils.browser import XHSBrowser
from xhs_utils.api_handler import XHSApiHandler


async def async_main():
    parser = argparse.ArgumentParser(description="小红书搜索脚本")
    parser.add_argument("--keyword", type=str, help="搜索关键词")
    parser.add_argument("--login", action="store_true", help="强制重新登录")
    parser.add_argument("--headless", action="store_true", help="无头模式运行")
    args = parser.parse_args()

    auth_file = Path(__file__).parent / "auth.json"

    if args.login or not auth_file.exists():
        print("请先登录...")
        helper = LoginHelper()
        await helper.login_and_save(auth_file)

    if args.keyword:
        async with XHSBrowser(headless=args.headless) as browser:
            api_handler = XHSApiHandler(browser.context)
            results = await api_handler.search(args.keyword)
            print(json.dumps(results.model_dump(), ensure_ascii=False, indent=2))
    else:
        parser.print_help()


def main():
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
