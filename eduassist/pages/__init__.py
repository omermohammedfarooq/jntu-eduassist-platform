"""Pages module containing individual page renderers."""

from .assistant import render_assistant_tab
from .results import render_results_tab
from .practice import render_practice_tab
from .auth import render_auth_page
from .forum import render_forum_page

__all__ = [
    "render_assistant_tab", 
    "render_results_tab", 
    "render_practice_tab",
    "render_auth_page",
    "render_forum_page"
]
