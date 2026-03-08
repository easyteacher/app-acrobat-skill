# PDF页面替换工具使用说明

## 概述

将一个 PDF 文件的页面替换到另一个 PDF 文件中。

## 使用方法

### 基本语法
```PowerShell
python .\scripts\replace.py <原始PDF> <替换PDF> --start <页码> [选项]
```

### 参数说明

| 参数 | 类型 | 必选 | 说明 |
|------|------|------|------|
| `input_pdf` | 位置参数 | 是 | 要修改的原始 PDF 文件路径 |
| `replace_pdf` | 位置参数 | 是 | 提供替换页面的 PDF 文件路径 |
| `--start` | 整数 | 是 | 开始替换的页码（从 1 开始） |
| `--num-pages` | 整数 | 否 | 要替换的页面数量，默认为替换 PDF 的总页数 |
| `-o, --output` | 字符串 | 否 | 输出文件路径，不指定则保存到原文件 |

### 使用示例

#### 示例 1：从第 3 页开始替换
```PowerShell
python .\scripts\replace.py document.pdf newpages.pdf --start 3 -o output.pdf
```

#### 示例 2：只替换 2 页
```PowerShell
python .\scripts\replace.py document.pdf newpages.pdf --start 3 --num-pages 2
```

#### 示例 3：直接修改原文件（不指定输出路径）
```PowerShell
python .\scripts\replace.py document.pdf newpages.pdf --start 3
```

### 页面范围说明

假设原文件有 10 页，替换文件有 5 页：
- `--start 3`：从原文件第 3 页开始替换
- 不指定 `--num-pages`：替换全部 5 页（原文件第 3-7 页被替换）
- `--num-pages 2`：只替换 2 页（原文件第 3-4 页被替换）

## 注意事项

1. **页码索引**：命令中使用的是从 1 开始的页码（符合用户习惯），内部会自动转换为从 0 开始