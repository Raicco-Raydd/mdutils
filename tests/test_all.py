"""mdutils 单元测试"""

from mdutils.parser import (
    parse_headings,
    extract_section,
    extract_code_blocks,
    extract_tables,
    get_structure,
)
from mdutils.editor import (
    replace_section,
    delete_section,
    insert_after_heading,
    update_frontmatter,
)
from mdutils.generator import (
    heading,
    table,
    code_block,
    link,
    image,
    bold,
    italic,
    inline_code,
    unordered_list,
    ordered_list,
    horizontal_rule,
    blockquote,
)
from mdutils.utils import read_md, write_md, find_md_files
import os
import tempfile


# ============================
# parser 测试
# ============================

def test_parse_headings():
    text = "# 一级标题\n## 二级标题\n普通文本\n### 三级标题"
    result = parse_headings(text)
    assert result == [(1, "一级标题"), (2, "二级标题"), (3, "三级标题")], f"Got {result}"


def test_parse_headings_empty():
    assert parse_headings("普通文本\n没有标题") == []


def test_extract_section():
    text = "# 简介\n这是简介内容。\n## 详情\n详细内容。"
    result = extract_section(text, "简介")
    assert result == "这是简介内容。", f"Got {result!r}"


def test_extract_section_not_found():
    text = "# 标题\n内容"
    result = extract_section(text, "不存在")
    assert result == ""


def test_extract_code_blocks():
    text = "```python\nprint('hello')\n```\n普通文本\n```\n纯代码块\n```"
    result = extract_code_blocks(text)
    assert len(result) == 2
    assert result[0]["language"] == "python"
    assert "hello" in result[0]["code"]


def test_extract_tables():
    text = """| 姓名 | 分数 |
| :--- | :--- |
| 张三 | 95 |
| 李四 | 88 |"""
    result = extract_tables(text)
    assert len(result) == 1
    headers, rows = result[0]
    assert headers == ["姓名", "分数"]
    assert rows == [["张三", "95"], ["李四", "88"]]


def test_get_structure():
    text = "# 一级\n## 二级A\n### 三级\n## 二级B"
    result = get_structure(text)
    assert len(result) == 1
    assert result[0]["title"] == "一级"
    assert len(result[0]["children"]) == 2


def test_get_structure_empty():
    assert get_structure("普通文本") == []


# ============================
# editor 测试
# ============================

def test_replace_section():
    text = "# 标题\n旧内容\n## 其他\n其他内容"
    result = replace_section(text, "标题", "新内容")
    assert "# 标题" in result
    assert "新内容" in result
    assert "旧内容" not in result


def test_replace_section_not_found():
    text = "# 标题\n内容"
    result = replace_section(text, "不存在", "新内容")
    assert result == text


def test_delete_section():
    text = "# 标题\n待删除内容\n## 其他\n其他内容"
    result = delete_section(text, "标题")
    assert "# 标题" in result
    assert "待删除内容" not in result
    assert "其他内容" in result


def test_insert_after_heading():
    text = "# 标题\n## 子标题"
    result = insert_after_heading(text, "标题", "插入内容")
    assert "插入内容" in result
    # 内容应在标题行和子标题之间
    lines = result.splitlines()
    idx_content = lines.index("插入内容")
    idx_sub = lines.index("## 子标题")
    assert idx_content < idx_sub, "插入内容应在子标题之前"


def test_update_frontmatter_create():
    text = "# 标题\n内容"
    result = update_frontmatter(text, "author", "张三")
    assert result.startswith("---")
    assert "author: 张三" in result
    assert "# 标题" in result


def test_update_frontmatter_update():
    text = "---\nauthor: 旧名\n---\n# 标题"
    result = update_frontmatter(text, "author", "新名")
    assert "author: 新名" in result
    assert "旧名" not in result


# ============================
# generator 测试
# ============================

def test_heading():
    assert heading("标题", 1) == "# 标题"
    assert heading("标题", 3) == "### 标题"


def test_heading_invalid_level():
    try:
        heading("标题", 7)
        assert False, "应该抛出 ValueError"
    except ValueError:
        pass


def test_table():
    result = table(["姓名"], [["张三"], ["李四"]])
    assert "| 姓名 |" in result
    assert "| 张三 |" in result


def test_table_empty():
    assert table([], []) == ""


def test_code_block():
    result = code_block("print('hi')", "python")
    assert "```python" in result
    assert "print('hi')" in result
    assert "```" in result


def test_link():
    assert link("文本", "http://example.com") == "[文本](http://example.com)"
    assert link("文本", "http://example.com", "提示") == '[文本](http://example.com "提示")'


def test_image():
    result = image("图", "img.png")
    assert "![图]" in result
    assert "(img.png)" in result


def test_bold_italic_inline():
    assert bold("文字") == "**文字**"
    assert italic("文字") == "*文字*"
    assert inline_code("x = 1") == "`x = 1`"


def test_unordered_list():
    result = unordered_list(["A", "B", "C"])
    lines = result.splitlines()
    assert all(line.startswith("- ") for line in lines)


def test_unordered_list_nested():
    result = unordered_list(["A", ["B1", "B2"], "C"])
    lines = result.splitlines()
    assert "- A" in lines
    assert "- C" in lines
    assert "  - B1" in lines or "- B1" in lines


def test_ordered_list():
    result = ordered_list(["A", "B"], start=1)
    assert "1. A" in result
    assert "2. B" in result


def test_horizontal_rule():
    assert horizontal_rule() == "---"


def test_blockquote():
    text = "第一行\n\n第二行"
    result = blockquote(text)
    lines = result.splitlines()
    assert all(line.startswith(">") for line in lines)


# ============================
# utils 测试
# ============================

def test_read_write_md():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, "test.md")
        content = "# 测试\n内容"
        write_md(path, content)
        result = read_md(path)
        assert result == content


def test_find_md_files():
    with tempfile.TemporaryDirectory() as tmpdir:
        open(os.path.join(tmpdir, "a.md"), "w").close()
        os.makedirs(os.path.join(tmpdir, "sub"))
        open(os.path.join(tmpdir, "sub", "b.md"), "w").close()
        open(os.path.join(tmpdir, "sub", "c.txt"), "w").close()

        recursive = find_md_files(tmpdir, recursive=True)
        assert len(recursive) == 2

        non_recursive = find_md_files(tmpdir, recursive=False)
        assert len(non_recursive) == 1


if __name__ == "__main__":
    # 运行所有以 test_ 开头函数
    test_functions = [
        v for k, v in globals().items()
        if k.startswith("test_") and callable(v)
    ]
    passed = 0
    failed = 0
    for test_fn in test_functions:
        try:
            test_fn()
            print(f"  [PASS] {test_fn.__name__}")
            passed += 1
        except Exception as e:
            print(f"  [FAIL] {test_fn.__name__}: {e}")
            failed += 1
    print(f"\n测试结果：{passed} 通过, {failed} 失败, 共 {passed + failed} 项")
