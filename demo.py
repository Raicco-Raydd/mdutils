"""mdutils 功能演示脚本

演示四个核心模块：parser / editor / generator / utils 的典型用法。
"""

import mdutils
import mdutils.parser as parser
import mdutils.generator as gen
import mdutils.utils as utils
from mdutils import replace_section, delete_section, insert_after_heading, update_frontmatter


def demo_01_generator():
    """生成一份 Markdown 文档"""
    print("=" * 50)
    print("【1】Generator — 生成 Markdown 内容")
    print("=" * 50)

    doc = []
    doc.append(gen.heading("mdutils 功能展示", 1))
    doc.append("一个 Markdown 文档工具箱，支持解析、编辑、生成。")
    doc.append("")

    doc.append(gen.heading("功能列表", 2))
    doc.append(gen.unordered_list(["解析 Markdown 结构", "编辑文档区块", "生成 Markdown 元素", "文件读写工具"]))
    doc.append("")

    doc.append(gen.heading("使用统计", 2))
    doc.append(gen.table(
        ["模块", "函数数量", "状态"],
        [
            ["parser", "5", "OK"],
            ["editor", "4", "OK"],
            ["generator", "12", "OK"],
            ["utils", "3", "OK"],
        ],
        alignment=["left", "center", "center"]
    ))
    doc.append("")

    doc.append(gen.heading("代码示例", 2))
    doc.append(gen.code_block(
        "from mdutils.parser import parse_headings\n"
        'headings = parse_headings("# Hello\\n## World")\n'
        "print(headings)",
        language="python"
    ))
    doc.append("")

    doc.append(gen.blockquote("mdutils — 专为 OpenClaw Agent 设计的 Markdown 工具箱"))
    doc.append("")

    content = "\n".join(doc)
    print(content)
    print()
    return content


def demo_02_parser(markdown_text):
    """解析刚才生成的 Markdown 文档"""
    print("=" * 50)
    print("【2】Parser — 解析 Markdown 结构")
    print("=" * 50)

    # 提取标题
    headings = parser.parse_headings(markdown_text)
    print(f"[标题] 列表（共 {len(headings)} 个）:")
    for level, title in headings:
        indent = "  " * (level - 1)
        print(f"  {indent}{'#' * level} {title}")

    # 提取代码块
    code_blocks = parser.extract_code_blocks(markdown_text)
    print(f"\n[代码块]（共 {len(code_blocks)} 个）:")
    for i, block in enumerate(code_blocks):
        lang = block["language"] or "无标注"
        code = block["code"][:50] + ("..." if len(block["code"]) > 50 else "")
        print(f"  代码块 #{i + 1}: [{lang}] {code}")

    # 提取表格
    tables = parser.extract_tables(markdown_text)
    print(f"\n[表格]（共 {len(tables)} 个）:")
    for headers, rows in tables:
        print(f"  表头: {headers}")
        print(f"  数据行: {len(rows)} 条")

    # 文档结构树
    structure = parser.get_structure(markdown_text)
    print(f"\n[结构树] 文档结构:")
    def print_tree(nodes, indent=0):
        for node in nodes:
            prefix = "  " * indent
            print(f"  {prefix}├─ {'#' * node['level']} {node['title']}")
            if node["children"]:
                print_tree(node["children"], indent + 1)
    print_tree(structure)

    print()


def demo_03_editor():
    """编辑 Markdown 文档"""
    print("=" * 50)
    print("【3】Editor — 编辑 Markdown 文档")
    print("=" * 50)

    sample = (
        "---\ntitle: 测试文档\nauthor: Raicco\n---\n"
        "# 简介\n这是简介内容。\n## 详情\n这是详细内容。\n"
    )
    print(f"[原始文档]:\n{sample}\n")

    # 插入内容
    edited = insert_after_heading(sample, "简介", "在简介后插入了一段文字。")
    print(f"[编辑] 在「简介」后插入内容:\n{edited}\n")

    # 替换区块
    edited = replace_section(sample, "详情", "详情内容已被替换！")
    print(f"[编辑] 替换「详情」区块:\n{edited}\n")

    # 更新元信息
    edited = update_frontmatter(sample, "version", "1.0.0")
    print(f"[编辑] Frontmatter 添加 version:\n{edited}\n")

    print()


def demo_04_utils():
    """文件读写和搜索"""
    print("=" * 50)
    print("【4】Utils — 文件读写与搜索")
    print("=" * 50)

    import tempfile
    import os

    with tempfile.TemporaryDirectory() as tmpdir:
        # 写入文件
        path = os.path.join(tmpdir, "demo_output.md")
        content = "# 测试文件\n\n由 demo.py 生成。"
        utils.write_md(path, content)
        print(f"[写入] {path}")

        # 读取文件
        read_back = utils.read_md(path)
        print(f"[读取] {read_back!r}")

        # 创建额外文件
        utils.write_md(os.path.join(tmpdir, "sub", "notes.md"), "## 笔记")
        utils.write_md(os.path.join(tmpdir, "sub", "readme.md"), "# README")

        # 搜索 .md 文件
        found = utils.find_md_files(tmpdir, recursive=True)
        print(f"[搜索] .md 文件（递归）:")
        for f in found:
            print(f"  - {os.path.relpath(f, tmpdir)}")

    print()


if __name__ == "__main__":
    print(f"\n[mdutils v{mdutils.__version__}] 功能演示\n")

    doc = demo_01_generator()
    demo_02_parser(doc)
    demo_03_editor()
    demo_04_utils()

    print("=" * 50)
    print("全部演示结束 [OK]")
    print("=" * 50)
