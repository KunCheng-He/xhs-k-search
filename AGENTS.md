# AGENTS.md - Development Guidelines for xhs-k-search

## Project Overview

This is a Xiaohongshu (小红书) search script that uses browser automation to fetch search results, post content, and comment data.

**Tech Stack:**
- Python 3.14
- Playwright (browser automation)
- playwright-stealth (anti-detection)
- Pydantic (data models)

---

## Build / Run Commands

### Installation

```bash
uv sync
uv run playwright install chromium
```

### Running the Script

```bash
# Login (first time only)
uv run python main.py --login

# Search with keyword
uv run python main.py --keyword "Python"

# Search in headless mode
uv run python main.py --keyword "Python" --headless
```

### Linting

```bash
uv run ruff check .
```

### Formatting

```bash
uv run ruff format .
```

### Running a Single Test

**Note:** This project currently has no test suite. If tests are added:

```bash
# With pytest
uv run pytest tests/test_file.py::test_function_name -v

# Or with unittest
uv run python -m unittest tests.test_file.test_function_name
```

---

## Code Style Guidelines

### Imports

Order imports as follows:
1. Standard library (`asyncio`, `json`, `pathlib`, `typing`)
2. Third-party packages (`playwright`, `pydantic`)
3. Local project modules (`xhs_utils`, `login_helper`)

```python
import asyncio
import json
from pathlib import Path
from typing import Optional, List, Dict, Any

from playwright.async_api import BrowserContext, Page, Route, Request
from pydantic import BaseModel

from xhs_utils.browser import XHSBrowser
from xhs_utils.api_handler import XHSApiHandler
```

### Formatting

- Use **ruff** for formatting (configured for this project)
- Run `ruff format .` before committing
- Line length: follow ruff defaults (usually 88 characters)
- Use 4 spaces for indentation (PEP 8)

### Types

- Use **type hints** for all function parameters and return types
- Use `Optional[T]` instead of `T | None` for compatibility
- Use `List[T]`, `Dict[K, V]` from typing module

```python
async def search(self, keyword: str, limit: int = 20) -> SearchResult:
    if not self.context:
        raise ValueError("Browser context is not available")
```

### Naming Conventions

- **Classes**: PascalCase (e.g., `XHSBrowser`, `XHSApiHandler`, `LoginHelper`)
- **Functions/variables**: snake_case (e.g., `async_main`, `auth_file`, `search_data`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `DEFAULT_TIMEOUT`)
- **Private methods**: prefix with underscore (e.g., `_init_browser`, `_intercept_api`)

### Pydantic Models

- Define data models using `BaseModel` from pydantic
- Use `Optional[T] = None` for optional fields with defaults
- Use primitive types with defaults for numeric fields
- Add `@property` methods for computed fields (see `Note.url`)

```python
class Note(BaseModel):
    note_id: str
    xsec_token: Optional[str] = None
    title: str
    cover: Optional[str] = None
    liked_count: int = 0

    @property
    def url(self) -> str:
        if self.xsec_token:
            return f"https://www.xiaohongshu.com/..."
        return f"https://www.xiaohongshu.com/..."
```

### Async/Await Patterns

- Use `async def` for asynchronous functions
- Always use `await` when calling async functions
- Use `async with` for context managers
- Prefer `asyncio.run()` in entry points

```python
async def __aenter__(self):
    self.playwright, self.browser, self.context = await self._init_browser()
    return self
```

### Error Handling

- Use specific exception types when possible
- For API parsing errors, use try/except with graceful degradation
- Never let exceptions propagate silently in production code
- Log errors or provide meaningful error messages

```python
try:
    user_info = note_card.get("user", {})
    author = User(...)
except Exception as e:
    pass  # Skip malformed entries
```

### Context Managers

- Implement both sync and async context managers when appropriate
- Use `__enter__`/`__exit__` for sync and `__aenter__`/`__aaexit__` for async
- Ensure proper cleanup in exit methods

```python
class XHSBrowser:
    async def __aenter__(self):
        # initialization
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
```

### Browser Automation

- Always use stealth mode for anti-detection
- Handle storage state for authentication
- Use appropriate wait times (`wait_for_timeout`)
- Close pages and contexts properly

---

## Project Structure

```
xhs-k-search/
├── .python-version          # Python 3.14
├── pyproject.toml           # Dependencies
├── main.py                  # Entry point
├── login_helper.py          # Login logic
├── xhs_utils/
│   ├── __init__.py
│   ├── browser.py           # Browser management
│   ├── api_handler.py       # API intercept & parsing
│   └── data_models.py       # Pydantic models
├── auth.json                # Login state (auto-generated, don't commit)
└── .ruff_cache/             # Ruff cache
```

---

## Common Tasks

### Adding a New Data Model

1. Add to `xhs_utils/data_models.py`
2. Use Pydantic `BaseModel`
3. Include proper type hints and defaults

### Adding a New API Endpoint

1. Add method to `XHSApiHandler` in `xhs_utils/api_handler.py`
2. Use route interception or direct Playwright navigation
3. Parse response into appropriate Pydantic model

### Modifying Browser Behavior

1. Edit `XHSBrowser` in `xhs_utils/browser.py`
2. Remember to hook stealth configuration

---

## Important Notes

- **Never commit `auth.json`** - contains login credentials
- Test in headless mode for CI/automation
- Respect rate limits when making requests
- The project uses Chinese language for user-facing output
