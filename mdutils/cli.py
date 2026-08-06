"""mdutils CLI 命令行入口

提供可通过命令行调用的接口，供 OpenClaw Agent 通过 exec 工具使用。
所有命令均从 stdin 读取 Markdown 文本，从参数读取选项。

用法:
    type "获取标题" | py -m mdutils.cli headings
    type < MEMORY.md | py -m mdutils.cli extract-section "标题名"
    type < MEMORY.md | py -m mdutils.cli replace-section "标题名" "新内容"

    # 若不支持管道，也可使用 read 命令：
    py -m mdutils.cli read MEMORY.md headings
"""

import sys
import json
import os


# ── Windows 编码兼容 ──────────────────────────

def _ensure_utf8_stdio():
    """将 stdout/stderr 设为 UTF-8，确保 CJK/emoji 等字符可正常输出。

    注意：不处理 stdin 编码——Windows 管道默认使用系统代码页（如 GBK），
    强制设 UTF-8 反而会使管道中文乱码。如需读取非 UTF-8 文件，
    请使用 read 子命令（自动处理文件编码回退）。
    """
    for stream in (sys.stdout, sys.stderr):
        try:
            if stream.encoding and stream.encoding.upper() != "UTF-8":
                stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass


_ensure_utf8_stdio()

from .parser import (
    parse_headings,
    extract_section,
    extract_code_blocks,
    extract_tables,
    get_structure,
)
from .editor import (
    replace_section,
    delete_section,
    insert_after_heading,
    insert_section_after,
    update_frontmatter,
)
from .generator import (
    heading, table, code_block, link, image, bold, italic, inline_code,
    unordered_list, ordered_list, horizontal_rule, blockquote,
)
from .utils import read_md, write_md, find_md_files


# ── 子命令实现 ──────────────────────────────

def cmd_headings(args):
    """提取并打印所有标题"""
    text = _read_input(args)
    results = parse_headings(text)
    _print_json(results)


def cmd_extract_section(args):
    """提取指定标题下的区块内容"""
    text = _read_input(args)
    if not args:
        _die("用法：extract-section <标题>")
    result = extract_section(text, args[0])
    if not result:
        _warn(f"未找到标题：「{args[0]}」，返回空")
    print(result)


def cmd_replace_section(args):
    """替换指定标题下的区块"""
    text = _read_input(args)
    if len(args) < 2:
        _die("用法：replace-section <标题> <新内容>")
    result = replace_section(text, args[0], args[1])
    if result == text:
        _die(f"操作无效：未找到标题「{args[0]}」")
    print(result)


def cmd_delete_section(args):
    """删除指定标题下的区块内容（保留标题行）"""
    text = _read_input(args)
    if not args:
        _die("用法：delete-section <标题>")
    result = delete_section(text, args[0])
    if result == text:
        _die(f"操作无效：未找到标题「{args[0]}」")
    print(result)


def cmd_insert_after(args):
    """在指定标题后插入内容"""
    text = _read_input(args)
    if len(args) < 2:
        _die("用法：insert-after <标题> <内容>")
    try:
        result = insert_after_heading(text, args[0], args[1])
        print(result)
    except ValueError:
        _die(f"未找到标题：「{args[0]}」")


def cmd_insert_section_after(args):
    """在指定区块之后插入新区块（级别继承锚点）"""
    text = _read_input(args)
    if len(args) < 3:
        _die("用法：insert-section-after <锚点标题> <新标题> <新内容>")
    try:
        result = insert_section_after(text, args[0], args[1], args[2])
        print(result)
    except ValueError:
        _die(f"未找到锚点标题：「{args[0]}」")


def cmd_code_blocks(args):
    """提取所有代码块"""
    text = _read_input(args)
    results = extract_code_blocks(text)
    _print_json(results)


def cmd_tables(args):
    """提取所有表格"""
    text = _read_input(args)
    results = extract_tables(text)
    _print_json(results)


def cmd_structure(args):
    """获取文档结构树"""
    text = _read_input(args)
    results = get_structure(text)
    _print_json(results)


def cmd_update_frontmatter(args):
    """更新 YAML 前置元信息"""
    text = _read_input(args)
    if len(args) < 2:
        _die("用法：update-frontmatter <键> <值>")
    try:
        result = update_frontmatter(text, args[0], args[1])
        print(result)
    except Exception as e:
        _die(f"前置元信息更新失败：{e}")


def cmd_read(args):
    """读取文件然后执行另一个命令"""
    if len(args) < 1:
        _die("用法：read <文件路径> [子命令] [参数...]")
    filepath = args[0]
    sub_cmd = args[1] if len(args) > 1 else "headings"
    sub_args = args[2:] if len(args) > 2 else []

    if not os.path.exists(filepath):
        _die(f"文件不存在：{filepath}")
    if not os.path.isfile(filepath):
        _die(f"路径不是文件：{filepath}")

    try:
        text = read_md(filepath)
    except PermissionError:
        _die(f"无权限读取：{filepath}")
    except Exception as e:
        _die(f"读取失败：{filepath} — {e}")

    # 将文本注入到 args 列表，让子命令从 _read_input 读取
    _set_piped_text(text)
    _run_subcommand(sub_cmd, sub_args)


def cmd_write(args):
    """将 stdin 或参数内容写入文件"""
    if len(args) < 1:
        _die("用法：write <文件路径> [内容]")
    filepath = args[0]
    if len(args) > 1:
        content = " ".join(args[1:])
    else:
        content = sys.stdin.read()
    try:
        write_md(filepath, content)
        print(f"✅ 已写入 {filepath}")
    except PermissionError:
        _die(f"无权限写入：{filepath}")
    except Exception as e:
        _die(f"写入失败：{e}")


def cmd_find(args):
    """搜索目录下的 .md 文件"""
    directory = args[0] if args else "."
    recursive = True
    if "--no-recursive" in args:
        recursive = False
    if not os.path.isdir(directory):
        _die(f"目录不存在：{directory}")
    files = find_md_files(directory, recursive=recursive)
    if not files:
        _warn(f"未在 {directory} 中找到 .md 文件")
    for f in files:
        print(f)


def cmd_generate(args):
    """生成 Markdown 元素（子命令：heading, table, list 等）"""
    if not args:
        print("可用子命令：heading, table, code, link, image, ulist, olist, hr, quote")
        return

    sub = args[0]
    rest = args[1:]

    if sub == "heading":
        if not rest:
            _die("用法：generate heading <文本> [级别]")
        if rest[-1].isdigit() and 1 <= int(rest[-1]) <= 6:
            level = int(rest[-1])
            text = " ".join(rest[:-1])
        else:
            level = 1
            text = " ".join(rest)
        print(heading(text, level=level))
    elif sub == "table":
        if len(rest) < 2:
            _die("用法：generate table <表头> <行1> [行2...]，如：generate table \"姓名,分数\" \"张三,95\"")
        headers = rest[0].split(",")
        rows = [r.split(",") for r in rest[1:]]
        # 检查行列数
        for i, row in enumerate(rows):
            if len(row) != len(headers):
                _warn(f"第{i+1}行列数({len(row)})与表头({len(headers)})不一致")
        print(table(headers, rows))
    elif sub == "code":
        lang = rest[-1] if rest else ""
        code = sys.stdin.read()
        print(code_block(code, lang))
    elif sub == "link":
        if len(rest) < 2:
            _die("用法：generate link <文本> <URL> [标题]")
        title = rest[2] if len(rest) > 2 else None
        print(link(rest[0], rest[1], title))
    elif sub == "image":
        if len(rest) < 2:
            _die("用法：generate image <替代文本> <URL> [标题]")
        title = rest[2] if len(rest) > 2 else None
        print(image(rest[0], rest[1], title))
    elif sub == "ulist":
        if not rest:
            _warn("未提供列表项")
        items = rest[0].split(",") if rest else []
        print(unordered_list(items))
    elif sub == "olist":
        if not rest:
            _warn("未提供列表项")
        items = rest[0].split(",") if rest else []
        print(ordered_list(items))
    elif sub == "hr":
        print(horizontal_rule())
    elif sub == "quote":
        if not rest:
            _warn("未提供引用文本")
        print(blockquote(" ".join(rest)))
    else:
        _die(f"未知生成子命令「{sub}」，可用：heading, table, code, link, image, ulist, olist, hr, quote")


# ── 内部工具 ──────────────────────────────

_piped_text = None

def _set_piped_text(text):
    global _piped_text
    _piped_text = text


def _read_input(args):
    global _piped_text
    if _piped_text is not None:
        text = _piped_text
        _piped_text = None
        return text
    if not sys.stdin.isatty():
        return sys.stdin.read()
    if args:
        return " ".join(args)
    _die("缺少输入：请通过管道传入 Markdown 文本，或使用 read 子命令读取文件")


def _print_json(data):
    print(json.dumps(data, ensure_ascii=False, indent=2))


def _warn(msg):
    """输出警告信息到 stderr（不中断流程）。"""
    print(f"⚠️ {msg}", file=sys.stderr)


def _die(msg):
    """输出错误信息到 stderr 并退出。"""
    print(f"❌ {msg}", file=sys.stderr)
    sys.exit(1)


def _run_subcommand(cmd, args):
    subcommands = {
        "headings": cmd_headings,
        "extract-section": cmd_extract_section,
        "replace-section": cmd_replace_section,
        "delete-section": cmd_delete_section,
        "insert-after": cmd_insert_after,
        "insert-section-after": cmd_insert_section_after,
        "code-blocks": cmd_code_blocks,
        "tables": cmd_tables,
        "structure": cmd_structure,
        "update-frontmatter": cmd_update_frontmatter,
        "read": cmd_read,
        "write": cmd_write,
        "find": cmd_find,
        "generate": cmd_generate,
    }
    sub = subcommands.get(cmd)
    if sub:
        sub(args)
    else:
        _die(f"未知命令：{cmd}")


# ── 入口 ──────────────────────────────

SUBCOMMANDS = {
    "headings": cmd_headings,
    "extract-section": cmd_extract_section,
    "replace-section": cmd_replace_section,
    "delete-section": cmd_delete_section,
    "insert-after": cmd_insert_after,
    "insert-section-after": cmd_insert_section_after,
    "code-blocks": cmd_code_blocks,
    "tables": cmd_tables,
    "structure": cmd_structure,
    "update-frontmatter": cmd_update_frontmatter,
    "read": cmd_read,
    "write": cmd_write,
    "find": cmd_find,
    "generate": cmd_generate,
}


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print("mdutils CLI — Markdown 文档工具箱命令行接口")
        print()
        print("用法:")
        print(f"  py -m mdutils.cli <命令> [参数...]")
        print(f"  type < 文件.md | py -m mdutils.cli <命令> [参数...]")
        print()
        print("命令列表:")
        for name, func in SUBCOMMANDS.items():
            doc = (func.__doc__ or "").split("\n")[0]
            print(f"  {name:25s} {doc}")
        print()
        print("提示：出错时命令行会显示 ❌ 或 ⚠️ 提示，请留意 stderr 输出。")
        print()
        print("示例:")
        print('  type MEMORY.md | py -m mdutils.cli headings')
        print('  type MEMORY.md | py -m mdutils.cli extract-section "核心身份"')
        print('  py -m mdutils.cli find .')
        print('  py -m mdutils.cli generate heading "文档标题" 1')
        return

    command = sys.argv[1]
    args = sys.argv[2:]
    _run_subcommand(command, args)


if __name__ == "__main__":
    main()
