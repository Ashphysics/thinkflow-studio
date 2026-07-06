"""
UI Pages Package for ThinkFlow Studio.

Contains individual Streamlit sub-pages loaded dynamically via the multipage router.

TODOs:
    - [ ] Setup permissions routes preventing unauthenticated access to history pages.
    - [ ] Create specialized analytics panels displaying model token utilization costs.
"""

from typing import List


class PagesRegistry:
    """
    Placeholder registry mapping python scripts to UI route paths.
    """
    AVAILABLE_PAGES: list[str] = [
        "dashboard.py",
        "new_session.py",
        "history.py",
        "mcp_settings.py"
    ]
