"""Markdown 文档编辑模块

提供 Markdown 文档内容的修改功能，包括：
- 替换指定标题下的区块
- 删除指定区块
- 在标题后插入内容
- 在指定区块之后插入新区块
- 更新 YAML 前置元信息
"""

import re


def insert_section_after(text, anchor_heading, new_heading, content):
    """在指定标题的区块之后插入一个新区块（新标题+内容）。

    新区块的标题级别与锚点标题一致；插入位置在锚点区块内容之后、
    下一个任意标题之前（若锚点是最后一个标题，则插到文档末尾）。

    Args:
        text: 原始 Markdown 文本。
        anchor_heading: 锚点标题文本（新块插在它的区块之后）。
        new_heading: 新标题文本（不含 # 号）。
        content: 新区块的内容。

    Returns:
        str: 插入后的 Markdown 文本。

    Raises:
        ValueError: 如果未找到锚点标题。

    Example:
        >>> text = "# A\n\n内容A\n\n## B\n\n内容B"
        >>> new = insert_section_after(text, "A", "新块", "内容新")
        >>> print(new)
        # A
        # 内容A
        # 新块
        # 内容新
        # ## B
        # 内容B
    """
    lines = text.splitlines()

    anchor_idx = None
    for i, line in enumerate(lines):
        match = re.match(r"^(#{1,6})\s+(.+?)(?:\s+#*)?$", line.strip())
        if match and match.group(2).strip() == anchor_heading:
            anchor_idx = i
            break

    if anchor_idx is None:
        raise ValueError("锚点标题未找到")

    # 找到下一个任意级别标题，作为插入位置
    end_idx = len(lines)
    for i in range(anchor_idx + 1, len(lines)):
        if re.match(r"^(#{1,6})\s+", lines[i].strip()):
            end_idx = i
            break

    level_match = re.match(r"^(#{1,6})\s+", lines[anchor_idx])
    level = len(level_match.group(1))
    new_block = f"\n{'#' * level} {new_heading}\n\n{content}".strip()

    result_lines = lines[:end_idx] + [new_block] + lines[end_idx:]
    return "\n".join(result_lines).strip() + "\n"


def replace_section(text, heading_text, new_content):
    """替换指定标题下的区块内容。

    Args:
        text: 原始 Markdown 文本。
        heading_text: 目标标题文本。
        new_content: 新的区块内容（不包含标题行）。

    Returns:
        str: 替换后的 Markdown 文本。

    Example:
        >>> text = "# Title\n\nOld content\n\n## Subtitle\n\nMore content"
        >>> new_text = replace_section(text, "Title", "New content")
        >>> print(new_text)
        # Output:
        # Title
        # New content
        # Subtitle
        # More content

    """
    lines = text.splitlines()
    start_idx = None
    end_idx = None

    for i, line in enumerate(lines):
        match = re.match(r"^(#{1,6})\s+(.+?)(?:\s+#*)?$", line.strip())
        if match:
            title = match.group(2).strip()
            if title == heading_text and start_idx is None:
                start_idx = i
                continue
            if start_idx is not None:
                end_idx = i
                break

    if start_idx is None:
        return text  # 未找到目标标题，返回原文

    if end_idx is None:
        end_idx = len(lines)

    # 组装新文本：标题行 + 新内容 + 剩余部分
    heading_line = lines[start_idx]
    before = lines[:start_idx + 1]
    after = lines[end_idx:]

    result_lines = before + [new_content] + after
    return "\n".join(result_lines).strip() + "\n"


def delete_section(text, heading_text):
    """删除指定标题下的区块内容（保留标题行）。

    Args:
        text: 原始 Markdown 文本。
        heading_text: 目标标题文本。

    Returns:
        str: 删除区块后的 Markdown 文本。

    Example:
        >>> text = "# Title\n\nOld content\n\n## Subtitle\n\nMore content"
        >>> new_text = delete_section(text, "Title")
        >>> print(new_text)
        # Output:
        # Title
        # Subtitle
        # More content

    """
    return replace_section(text, heading_text, "")


def insert_after_heading(text, heading_text, content):
    """在指定标题行之后插入内容。

    Args:
        text: 原始 Markdown 文本。
        heading_text: 目标标题文本。
        content: 要插入的内容。

    Returns:
        str: 插入后的 Markdown 文本。

    Raises:
        ValueError: 如果未找到指定标题。

    Example:
        >>> text = "# Title\n\nOld content\n\n## Subtitle\n\nMore content"
        >>> new_text = insert_after_heading(text, "Title", "New content")
        >>> print(new_text)
        # Output:
        # Title
        # New content
        # Subtitle
        # More content

    """
    lines = text.splitlines()
    for i, line in enumerate(lines):
        match = re.match(r"^(#{1,6})\s+(.+?)(?:\s+#*)?$", line.strip())
        if match:
            title = match.group(2).strip()
            if title == heading_text:
                before = lines[:i + 1]
                after = lines[i + 1:]
                result_lines = before + [content] + after
                return "\n".join(result_lines).strip() + "\n"

    raise ValueError("指定标题未找到")


def update_frontmatter(text, key, value):
    """更新 YAML 前置元信息中的键值对。

    如果 key 已存在则更新，不存在则追加到末尾。
    如果文档没有前置元信息（--- 包裹的 YAML 区块），则创建。

    Args:
        text: 原始 Markdown 文本。
        key: 键名。
        value: 值（字符串、数字或布尔值）。

    Returns:
        str: 更新后的 Markdown 文本。

    Example:
        >>> text = "---\ntitle: Old Title\n---\n# Content"
        >>> new_text = update_frontmatter(text, "title", "New Title")
        >>> print(new_text)
        # Output:
        # ---
        # title: New Title
        # ---
        # # Content
    """
    lines = text.splitlines()

    # 检查是否有前置元信息
    if lines and lines[0].strip() == "---":
        end_idx = None
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                end_idx = i
                break

        if end_idx is not None:
            # 在已有的 frontmatter 中更新
            frontmatter_lines = lines[1:end_idx]
            updated = False

            for i, line in enumerate(frontmatter_lines):
                match = re.match(rf"^{re.escape(key)}\s*:\s*", line)
                if match:
                    frontmatter_lines[i] = f"{key}: {value}"
                    updated = True
                    break

            if not updated:
                frontmatter_lines.append(f"{key}: {value}")

            result_lines = ["---"] + frontmatter_lines + ["---"] + lines[end_idx + 1:]
            return "\n".join(result_lines).strip() + "\n"

    # 没有前置元信息，直接创建
    frontmatter = f"---\n{key}: {value}\n---\n"
    return frontmatter + text
