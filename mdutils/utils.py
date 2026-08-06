"""工具函数模块

提供文件读写、批量搜索等辅助功能。
"""

import os


def read_md(path, encoding="utf-8"):
    """读取 Markdown 文件,返回字符串内容。

    Args:
        path: 文件路径。
        encoding: 文件编码，默认 utf-8。

    Returns:
        str: 文件内容。

    Raises:
        FileNotFoundError: 文件不存在时抛出。
        PermissionError: 文件权限不足时抛出。

    Note:
        若指定编码读取失败，会自动尝试 gbk/cp936 回退（Windows 兼容）。

    Example:
        >>> from mdutils.utils import read_md 
        >>> content = read_md("example.md")
        >>> print(content)
    
    """
    try:
        with open(path, "r", encoding=encoding) as f:
            return f.read()
    except UnicodeDecodeError:
        # Windows 下文件可能是 GBK 编码，尝试 fallback
        with open(path, "r", encoding="gbk") as f:
            return f.read()


def write_md(path, content, encoding="utf-8"):
    """写入 Markdown 文件。

    自动创建不存在的目录路径。

    Args:
        path: 文件路径。
        content: 要写入的内容。
        encoding: 文件编码，默认 utf-8。
    
    Raises:
        PermissionError: 文件权限不足时抛出。
        FileNotFoundError: 父目录非法时抛出。
    
    Example:
        >>> from mdutils.utils import write_md
        >>> write_md("example.md", "# Hello, World!")

    """
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding=encoding) as f:
        f.write(content)


def find_md_files(directory, recursive=True):
    """搜索目录下所有 Markdown 文件。

    Args:
        directory: 搜索的根目录。
        recursive: 是否递归搜索子目录，默认 True。

    Returns:
        list[str]: 匹配的 .md 文件路径列表。

    Raises:
        PermissionError: 目录权限不足时抛出。
    
    Example:
        >>> from mdutils.utils import find_md_files
        >>> md_files = find_md_files("docs", recursive=True)
        >>> print(md_files)

    """
    md_files = []
    if recursive:
        for root, _, files in os.walk(directory):
            for f in files:
                if f.endswith(".md"):
                    md_files.append(os.path.join(root, f))
    else:
        for f in os.listdir(directory):
            if f.endswith(".md"):
                md_files.append(os.path.join(directory, f))
    return sorted(md_files)
