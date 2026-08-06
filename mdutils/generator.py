"""Markdown 文档生成模块

提供 Markdown 各元素的生成函数，支持：
- 标题、段落、代码块
- 表格、列表、引用
- 文字样式（加粗、斜体、行内代码）
- 链接、图片、分割线
"""


def heading(text, level=1):
    """生成 Markdown 标题。

    Args:
        text: 标题文本。
        level: 标题级别（1-6）。

    Returns:
        str: Markdown 标题字符串。
    """
    if level < 1 or level > 6:
        raise ValueError("标题级别必须在 1-6 之间")
    return f"{'#' * level} {text}"


def table(headers, rows, alignment=None):
    """生成 Markdown 表格。

    Args:
        headers: 表头列表，如 ["姓名", "分数"]。
        rows: 数据行列表，每行为列表，如 [["张三", 95], ["李四", 88]]。
        alignment: 对齐方式列表，可选 "left"/"center"/"right"，
            默认为全部左对齐。

    Returns:
        str: Markdown 表格字符串。

    Example:
        >>> table(["姓名", "分数"], [["张三", 95], ["李四", 88]])
        '| 姓名 | 分数 |\\n| :--- | :--- |\\n| 张三 | 95 |\\n| 李四 | 88 |'
    """
    if not headers or not rows:
        return ""

    def fmt_row(cells):
        return "| " + " | ".join(str(c) for c in cells) + " |"

    # 对齐标记映射
    align_map = {
        "left": ":---",
        "center": ":---:",
        "right": "---:",
    }
    if alignment is None:
        alignment = ["left"] * len(headers)
    # 补齐缺失的对齐设置
    align_cols = alignment + ["left"] * (len(headers) - len(alignment))
    sep_row = "| " + " | ".join(
        align_map.get(a, ":---") for a in align_cols
    ) + " |"

    result = [fmt_row(headers), sep_row]
    for row in rows:
        # 补齐短行
        padded = list(row) + [""] * (len(headers) - len(row))
        result.append(fmt_row(padded[:len(headers)]))

    return "\n".join(result)


def code_block(code, language=""):
    """生成 Markdown 代码块。

    Args:
        code: 代码内容。
        language: 编程语言名称（可选）。

    Returns:
        str: Markdown 代码块字符串。

    Example:
        >>> code_block("print('Hello, World!')", "python")

    """
    return f"```{language}\n{code}\n```"


def link(text, url, title=None):
    """生成 Markdown 链接。

    Args:
        text: 显示文本。
        url: 链接地址。
        title: 鼠标悬停提示文本（可选）。

    Returns:
        str: Markdown 链接字符串。

    Example:
        >>> link("OpenAI", "https://www.openai.com", "OpenAI 官网")
        '[OpenAI](https://www.openai.com "OpenAI 官网")'
    """
    if title:
        return f"[{text}]({url} \"{title}\")"
    return f"[{text}]({url})"


def image(alt_text, url, title=None):
    """生成 Markdown 图片。

    Args:
        alt_text: 替代文本。
        url: 图片地址。
        title: 鼠标悬停提示文本（可选）。

    Returns:
        str: Markdown 图片字符串。

    Example:
        >>> image("示例图片", "https://example.com/image.png", "图片标题")
        '![示例图片](https://example.com/image.png "图片标题")'
    """
    if title:
        return f"![{alt_text}]({url} \"{title}\")"
    return f"![{alt_text}]({url})"


def bold(text):
    """生成加粗文本。"""
    return f"**{text}**"


def italic(text):
    """生成斜体文本。"""
    return f"*{text}*"


def inline_code(text):
    """生成行内代码。"""
    return f"`{text}`"


def unordered_list(items, indent=0):
    """生成无序列表。

    Args:
        items: 列表项列表（可以是字符串或嵌套列表）。
        indent: 缩进级别（用于嵌套列表）。

    Returns:
        str: Markdown 无序列表字符串。

    Example:
        >>> unordered_list(["苹果", "香蕉", ["橙子", "葡萄"]])
    """
    prefix = "  " * indent
    result = []
    for item in items:
        if isinstance(item, list):
            result.append(unordered_list(item, indent + 1))
        else:
            result.append(f"{prefix}- {item}")
    return "\n".join(result)


def ordered_list(items, start=1):
    """生成有序列表。

    Args:
        items: 列表项列表。
        start: 起始序号（默认 1）。

    Returns:
        str: Markdown 有序列表字符串。
    
    Example:
        >>> ordered_list(["第一项", "第二项", "第三项"], start=1)
        '1. 第一项\n2. 第二项\n3. 第三项'
    """
    result = []
    for i, item in enumerate(items, start=start):
        result.append(f"{i}. {item}")
    return "\n".join(result)


def horizontal_rule():
    """生成分割线。"""
    return "---"


def blockquote(text):
    """生成引用块。

    Args:
        text: 引用文本（可含换行）。

    Returns:
        str: Markdown 引用块字符串。

    Example:
        >>> blockquote("这是引用文本。\n可以换行。")
        
    """
    lines = text.splitlines()
    quoted = [f"> {line}" if line else ">" for line in lines]
    return "\n".join(quoted)
