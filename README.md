# mdutils

![mdutils logo](properties/Mdutils.png)

Markdown 文档工具箱 — 专为 AI Agent 工作流设计。

> **v2.1.0** 🎉 重大更新：新增 **Web UI**（预览 + 结构化编辑），详见下方「🌐 Web UI」章节。

## 🚀 30 秒快速上手

```bash
# CLI 版 — 查看文档结构
mdutils read MEMORY.md headings
mdutils read README.md extract-section "功能模块"
mdutils generate table "姓名,分数" "张三,95" "李四,88"

# Python 版
from mdutils.parser import extract_section
from mdutils.generator import table
```

## 功能模块

| 模块 | 功能 |
|:---|:---|
| `parser` | 解析 Markdown 结构（标题、区块、代码块、表格） |
| `editor` | 编辑 Markdown 文档（替换、删除、插入区块、**区块后插入新块**） |
| `generator` | 生成 Markdown 元素（表格、列表、代码块、链接等） |
| `utils` | 文件读写、批量搜索等辅助工具 |

## 🌐 Web UI（v2.0+）

本地浏览器界面：**左目录树 + 右预览**，支持按区块结构化编辑。

```bash
cd webui
pip install fastapi uvicorn
py -m uvicorn app:app --host 127.0.0.1 --port 8765
# 浏览器打开 http://127.0.0.1:8765
```

功能：实时渲染预览、目录树（引导线+级别徽标+滚动跟随）、区块编辑（替换/插入/**添加新区块**）、删除、YAML 元信息、20 步撤销、文件目录浏览、最近历史、蒙版式新手指引。

## CLI 命令行工具

安装后可直接通过终端调用 `mdutils` 命令：

```bash
# 从 stdin 管道输入 Markdown 文本
type MEMORY.md | mdutils headings
type MEMORY.md | mdutils extract-section "核心身份"
type MEMORY.md | mdutils replace-section "旧标题" "新内容"

# 使用 read 子命令直接读取文件
mdutils read MEMORY.md headings
mdutils read MEMORY.md structure
mdutils read README.md extract-section "功能模块"

# 文件搜索与写入
mdutils find .
mdutils find ./docs --no-recursive
mdutils write output.md "# 新文档\n\n正文内容"

# 生成 Markdown 元素
mdutils generate heading "文档标题" 1
mdutils generate table "姓名,分数" "张三,95" "李四,88"
mdutils generate link "OpenAI" "https://openai.com"
mdutils generate ulist "苹果,香蕉,橙子"
mdutils generate code < script.py python
```

### 命令一览

| 命令 | 功能 |
|:---|:---|
| `headings` | 提取所有标题层级 |
| `extract-section <标题>` | 提取指定标题下的区块 |
| `replace-section <标题> <内容>` | 替换指定区块内容 |
| `delete-section <标题>` | 删除指定区块（保留标题行） |
| `insert-after <标题> <内容>` | 在标题后插入内容 |
| `insert-section-after <锚点> <新标题> <内容>` | 在区块之后插入新区块（级别继承锚点） |
| `code-blocks` | 提取所有代码块 |
| `tables` | 提取所有表格 |
| `structure` | 获取文档结构树 |
| `update-frontmatter <键> <值>` | 更新 YAML 前置元信息 |
| `read <文件> [子命令]` | 读取文件后执行子命令 |
| `write <文件> [内容]` | 写入文件（省略内容则从 stdin 读） |
| `find <目录>` | 搜索 Markdown 文件 |
| `generate <元素> [参数]` | 生成 Markdown 元素 |

`generate` 支持的元素：`heading` / `table` / `code` / `link` / `image` / `ulist` / `olist` / `hr` / `quote`

## 安装

```bash
# 标准安装
pip install .

# 开发模式（修改源码后无需重装）
pip install -e .
```

## Python API 快速上手

```python
from mdutils.parser import parse_headings, extract_section
from mdutils.generator import table, code_block, heading

# 解析标题
text = "# 项目简介\n这是项目描述。\n## 安装说明\n详细安装步骤。"
headings = parse_headings(text)
# → [(1, "项目简介"), (2, "安装说明")]

# 提取特定区块
content = extract_section(text, "项目简介")

# 生成 Markdown 元素
t = table(["姓名", "分数"], [["张三", 95], ["李四", 88]])

# 生成代码块
cb = code_block("print('hello')", "python")

# 生成标题
h = heading("文档标题", 1)
```

```python
from mdutils.editor import replace_section, insert_after_heading, insert_section_after, update_frontmatter

# 替换区块
new_doc = replace_section(text, "项目简介", "新的项目描述。")

# 插入内容
new_doc = insert_after_heading(text, "安装说明", "1. 首先 pip install")

# 在指定区块之后插入新区块（新标题级别继承锚点）
new_doc = insert_section_after(text, "项目简介", "开发计划", "- 阶段一\n- 阶段二")

# 更新或创建 YAML 前置元
new_doc = update_frontmatter(text, "author", "张三")
```

```python
from mdutils.utils import read_md, write_md, find_md_files

# 搜索 .md 文件
files = find_md_files("./docs")

# 读取文件
content = read_md("README.md")
```

## 运行测试

```bash
cd lesson5
python -m pytest tests/ -v
```

或直接运行：

```bash
python tests/test_all.py
```

## 项目结构

```
lesson5/
├── mdutils/
│   ├── __init__.py     # 包总入口
│   ├── cli.py          # 命令行接口
│   ├── parser.py       # Markdown 解析
│   ├── editor.py       # Markdown 编辑
│   ├── generator.py    # Markdown 生成
│   └── utils.py        # 工具函数
├── tests/
│   ├── __init__.py
│   └── test_all.py     # 单元测试
├── setup.py            # 安装配置
├── CHANGELOG.md        # 更新日志
└── README.md           # 项目说明
```

## ⚠️ 常见问题

**Q: Windows 下管道输中文乱码怎么办？**

PowerShell 的默认 `$OutputEncoding` 可能不支持中文。建议：
- **改用 `mdutils read` 子命令**读取文件（自动处理编码）
- 或在 PowerShell 中临时设置 `$OutputEncoding = [Console]::OutputEncoding` 后再管道

**Q: `extract-section` 返回空？**

标题文本需要精确匹配（大小写敏感）。如果文档中有 `# 项目简介`，应写 `extract-section "项目简介"`，无需包含 `#`。

**Q: `replace-section` 没生效？**

命令会检查标题是否存在。如果标题没找到，会显示 `❌ 操作无效：未找到标题`。请核对标题文本是否完全一致。

**Q: 表格行列数对不上？**

`generate table` 会检查每行的列数与表头是否一致，不一致时会输出 `⚠️ 第N行列数不一致` 警告。

**Q: 文件找不到？**

`read` 和 `write` 子命令会显示具体的路径错误信息。建议使用绝对路径或确认当前工作目录。

**Q: 复杂 Markdown 格式支持？**

本工具专注于**结构化** Markdown 操作（标题/区块/表格/代码块）。嵌套列表、多维表格等复杂格式的解析可能有限，请在使用前先测试。

**Q: 如何获取帮助？**

- CLI: `py -m mdutils.cli -h`
- 单个命令用法：不带参数运行即可看到用法提示
- 查看 `CHANGELOG.md` 了解版本更新
