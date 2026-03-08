---
name: app-acrobat
description: 使用Adobe Acrobat实现PDF处理，包括导出其他格式、打印、合并、添加水印、替换页面功能。
metadata: {"openclaw":{"emoji":"📄","os":["win32"]}}
---

# Adobe Acrobat Skill

## 1. 导出其他格式
支持导出PDF为Word、PowerPoint、Excel、纯文本格式、图片（PNG、JPEG）。
使用说明见`references/export.md`

## 2. 打印PDF文档
如果用户指定了打印机，先设置默认打印机。否则直接使用默认打印机。
使用方法见`references/print.md`

## 3. 合并PDF文档
使用方法见`references/merge.md`

## 4. 添加水印
- 方法1（推荐）：使用Acrobat添加水印。使用方法见`references/add_watermark.md`
- 方法2：使用PyPDF2库添加水印，当方法1失败时使用。
```PowerShell
# 处理单个PDF
python .\scripts\add_watermark_simple.py watermark.pdf input.pdf output.pdf
```

## 5. 替换页面
使用方法见`references/replace.md`