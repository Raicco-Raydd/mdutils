"""Markdown 文档解析模块

提供 Markdown 文本的结构化解析功能，包括：
- 标题层级提取
- 区块定位与提取
- 代码块提取
- 表格提取
- 完整文档树生成
"""

import re


def parse_headings(text):
    """提取 Markdown 文本中所有标题，返回列表 [(level, title), ...]。

    Args:
        text: Markdown 文本字符串。

    Returns:
        list[tuple[int, str]]: 标题列表，每个元素为 (标题级别, 标题文本)。

    Example:
        >>> text = "# Title\n\n## Subtitle\n\n### Sub-subtitle"
        >>> parse_headings(text)
        [(1, 'Title'), (2, 'Subtitle'), (3, 'Sub-subtitle')]

    """
    pattern = r"^(#{1,6})\s+(.+?)(?:\s+#*)?$"
    headings = []
    for line in text.splitlines():
        match = re.match(pattern, line.strip())
        if match:
            level = len(match.group(1))
            title = match.group(2).strip()
            headings.append((level, title))
    return headings


def extract_section(text, heading_text):
    """提取指定标题下的文档区块内容。

    从第一个匹配的标题开始，到下一个任意标题结束。

    Args:
        text: Markdown 文本字符串。
        heading_text: 目标标题文本（不含 # 号）。

    Returns:
        str: 区块内容（不含标题行），未找到返回空字符串。

    Example:
        >>> text = "# Title\n\nContent\n\n## Subtitle\n\nMore"
        >>> extract_section(text, "Title")
        'Content'
    """
    lines = text.splitlines()
    start_idx = None

    for i, line in enumerate(lines):
        match = re.match(r"^(#{1,6})\s+(.+?)(?:\s+#*)?$", line.strip())
        if match:
            title = match.group(2).strip()
            if title == heading_text and start_idx is None:
                start_idx = i
                break

    if start_idx is None:
        return ""

    content_lines = []
    for line in lines[start_idx + 1:]:
        if re.match(r"^(#{1,6})\s+", line.strip()):
            break
        content_lines.append(line)

    return "\n".join(content_lines).strip()


def extract_code_blocks(text):
    """提取 Markdown 文本中所有代码块。

    Args:
        text: Markdown 文本字符串。

    Returns:
        list[dict]: 代码块列表，每个元素为
            {"language": str, "code": str}。
    
    
    """
    pattern = r"```(\w*)\n(.*?)```"
    matches = re.findall(pattern, text, re.DOTALL)
    blocks = []
    for lang, code in matches:
        blocks.append({"language": lang.strip(), "code": code.strip()})
    return blocks


def extract_tables(text):
    """提取 Markdown 文本中的所有表格。

    支持标准 Markdown 表格格式（含对齐分隔行）。

    Args:
        text: Markdown 文本字符串。

    Returns:
        list[list[list[str]]]: 表格列表，每个表格为 [headers, rows]，
            headers 为表头列表，rows 为行列表（每行为字符串列表）。
    """
    lines = text.splitlines()
    tables = []
    i = 0

    while i < len(lines):
        # 找表头行
        if "|" in lines[i]:
            header_line = lines[i].strip()
            headers = [h.strip() for h in header_line.split("|")]
            headers = [h for h in headers if h]  # 去掉首尾空

            # 检查下一行是否是分隔行
            if i + 1 < len(lines):
                sep_line = lines[i + 1].strip()
                if re.match(r"^[\s:|:-]+$", sep_line):
                    # 确认是表格分隔行
                    sep_parts = sep_line.split("|")
                    sep_parts = [s.strip() for s in sep_parts if s.strip()]
                    if all(re.match(r"^:?-+:?$", s) for s in sep_parts):
                        # 读取数据行
                        rows = []
                        j = i + 2
                        while j < len(lines) and "|" in lines[j]:
                            row = lines[j].strip()
                            cells = [c.strip() for c in row.split("|")]
                            cells = [c for c in cells if c]
                            rows.append(cells)
                            j += 1
                        tables.append([headers, rows])
                        i = j
                        continue
        i += 1

    return tables


def get_structure(text):
    """获取完整的文档结构树。

    Args:
        text: Markdown 文本字符串。

    Returns:
        list[dict]: 文档结构树，每个节点包含
            {"level": int, "title": str, "children": list}
    """
    headings = parse_headings(text)
    if not headings:
        return []

    root = []
    stack = []

    for level, title in headings:
        node = {"level": level, "title": title, "children": []}
        # 向上回溯，找到合适的父节点
        while stack and stack[-1]["level"] >= level:
            stack.pop()
        if stack:
            stack[-1]["children"].append(node)
        else:
            root.append(node)
        stack.append(node)

    return root
