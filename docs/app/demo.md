# mdutils 预览演示

这是一个用来展示 **mdutils Web UI** 渲染效果的演示文档，覆盖了常用的 Markdown 元素。

## 文本样式

支持 *斜体*、**加粗**、***加粗斜体***、~~删除线~~、`行内代码` 和 [超链接](https://github.com)。

> 引用块：品质是唯一的付费 trigger。

---

## 列表

### 无序列表

- 解析 Markdown 结构
- 编辑文档区块
- 生成表格 / 代码块

### 有序列表

1. 读取文件
2. 提取标题结构
3. 渲染预览

## 表格

| 模块 | 功能 | 状态 |
|:---|:---|:---:|
| parser | 解析结构 | ✅ |
| editor | 编辑区块 | ✅ |
| generator | 生成元素 | ✅ |
| renderer | 渲染预览 | 🚧 开发中 |

## 代码块

```python
def greet(name: str) -> str:
    """示例函数"""
    return f"你好, {name}!"

print(greet("Rai"))
```

## 图片

![演示图片](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI2NDAiIGhlaWdodD0iMTAwIj48cmVjdCB3aWR0aD0iNjQwIiBoZWlnaHQ9IjEwMCIgZmlsbD0iIzEwMTYxZiIvPjx0ZXh0IHg9IjIwIiB5PSI2MiIgZm9udC1zaXplPSIyNiIgZmlsbD0iIzRmZDZiZSIgZm9udC1mYW1pbHk9InNhbnMtc2VyaWYiPm1kdXRpbHMgcHJldmlldyBPSzwvdGV4dD48L3N2Zz4=)

## 深层嵌套

### 第三层

试试目录树的多级跳转。

#### 第四层

能缩进多深，目录树就长多深。
