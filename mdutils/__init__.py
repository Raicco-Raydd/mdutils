"""mdutils - Markdown 文档工具箱

一个为 OpenClaw Agent 设计的 Markdown 文档处理工具包。
提供解析、编辑、生成 Markdown 文档的完整功能。
"""

from .editor import (
    replace_section,
    delete_section,
    insert_after_heading,
    update_frontmatter,
)

from . import parser as _parser
from . import generator as _generator
from . import utils as _utils

__all__ = [
    "replace_section",
    "delete_section",
    "insert_after_heading",
    "update_frontmatter",
]
__version__ = "2.3.0"
