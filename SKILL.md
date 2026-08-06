# mdutils — Markdown 文档工具箱 (Skill)

> **v2.1.0** — 重大更新：新增 Web UI（预览+结构化编辑）、`insert_section_after` 区块插入。

Markdown 文档的解析/编辑/生成工具包。封装 Python `mdutils` CLI，供 Agent 通过 exec 调用处理 .md 文件。

## 前置条件

```bash
pip install /path/to/MarkdownSkill
```

## Web UI（人机交互界面，可选）

```bash
cd webui && py -m uvicorn app:app --host 127.0.0.1 --port 8765
# 浏览器打开 http://127.0.0.1:8765
```

功能：实时渲染预览、目录树、区块编辑/添加/删除、YAML 元信息、撤销、历史、新手指引。

## 函数

### mdutils_read_section(filePath, headingText)
提取指定标题下的区块内容。
```
exec: py -m mdutils.cli read "<filePath>" extract-section "<headingText>"
```

### mdutils_get_headings(filePath)
提取文件中的所有标题（JSON 格式）。
```
exec: py -m mdutils.cli read "<filePath>" headings
```

### mdutils_replace_section(filePath, headingText, newContent)
替换指定标题下的区块内容。
```
exec: py -m mdutils.cli read "<filePath>" replace-section "<headingText>" "<newContent>"
```

### mdutils_delete_section(filePath, headingText)
删除指定标题下的区块内容（保留标题行）。
```
exec: py -m mdutils.cli read "<filePath>" delete-section "<headingText>"
```

### mdutils_insert_after(filePath, headingText, content)
在指定标题后插入内容。
```
exec: py -m mdutils.cli read "<filePath>" insert-after "<headingText>" "<content>"
```

### mdutils_insert_section_after(filePath, anchorHeading, newHeading, newContent)
在指定区块之后插入新区块（新标题级别继承锚点标题）。
```
exec: py -m mdutils.cli read "<filePath>" insert-section-after "<anchorHeading>" "<newHeading>" "<newContent>"
```

### mdutils_write_file(filePath, content)
写入 Markdown 文件。
```
exec: py -m mdutils.cli write "<filePath>" "<content>"
```

### mdutils_find_files(directory)
搜索目录下所有 .md 文件。
```
exec: py -m mdutils.cli find "<directory>"
```

### mdutils_get_structure(filePath)
获取文档的层级结构树（JSON 格式）。
```
exec: py -m mdutils.cli read "<filePath>" structure
```

### mdutils_get_code_blocks(filePath)
提取文档中的所有代码块（JSON 格式）。
```
exec: py -m mdutils.cli read "<filePath>" code-blocks
```

### mdutils_get_tables(filePath)
提取文档中的所有表格（JSON 格式）。
```
exec: py -m mdutils.cli read "<filePath>" tables
```

### mdutils_generate_element(type, args...)
生成单个 Markdown 元素。

| 类型 | 示例 |
|------|------|
| heading | `py -m mdutils.cli generate heading "标题" 1` |
| table | `py -m mdutils.cli generate table "姓名,分数" "张三,95" "李四,88"` |
| ulist | `py -m mdutils.cli generate ulist "项1,项2,项3"` |
| olist | `py -m mdutils.cli generate olist "项1,项2,项3"` |
| link | `py -m mdutils.cli generate link "文本" "url"` |
| code | `echo "代码" \| py -m mdutils.cli generate code python` |
| quote | `py -m mdutils.cli generate quote "引用文本"` |
| hr | `py -m mdutils.cli generate hr` |

## 使用示例

```python
# 提取 MEMORY.md 中"核心身份"的区块内容
# exec: py -m mdutils.cli read MEMORY.md extract-section "核心身份"

# 获取所有标题
# exec: py -m mdutils.cli read MEMORY.md headings

# 生成二级标题并写入
# exec: py -m mdutils.cli generate heading "今日记录" 2

# 更新 frontmatter
# exec: py -m mdutils.cli read MEMORY.md update-frontmatter "version" "2.0"
```

## 文件结构

```
MarkdownSkill/
├── mdutils/           # Python 包本体
├── tests/             # 单元测试
├── setup.py           # 安装配置
├── SKILL.md           # 本文件（Skill 定义）
└── README.md          # 项目文档
```

## 注意事项

- **跨平台**：命令中的文件路径使用系统原生格式（Windows 用 `\` 或 `/`，Linux/macOS 用 `/`）
- **编码**：确保终端支持 UTF-8 输出（`$env:PYTHONIOENCODING='utf-8'` on Windows）
- **管道中文**：Windows PowerShell 管道传中文可能乱码，推荐用 `read` 子命令替代管道
- **大文件**：`read_md` 一次性读入内存，超大文件建议分批处理
- **依赖**：Python 3.8+，无第三方依赖（仅使用标准库）
