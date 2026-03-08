# PDF水印批量添加工具 (add_watermark.py)

## 简介
`add_watermark.py` 支持对多个 PDF 文件批量添加自定义水印，并提供灵活的页码控制、透明度调节等高级功能。

## 使用方法

### 基本语法
```PowerShell
python .\scripts\add_watermark.py <水印文件> <目标PDF文件1> [<目标PDF文件2> ...] [选项]
```

### 参数说明

| 参数 | 类型 | 说明 |
|------|------|------|
| `watermark` | 位置参数 | 水印 PDF 文件路径 |
| `pdf_files` | 位置参数 | 一个或多个待添加水印的目标 PDF 文件路径 |
| `-o, --output-folder` | 可选 | 输出文件夹路径（默认与输入文件相同目录） |
| `--start` | 可选 | 起始页码（从 0 开始，默认 0） |
| `--end` | 可选 | 结束页码（默认 -1，表示最后一页） |
| `--source-page` | 可选 | 水印来源页码（从 0 开始，默认 0） |
| `--opacity` | 可选 | 水印透明度（0.0 ~ 1.0，默认 1.0） |

### 使用示例

#### 1. 基本用法：为单个 PDF 添加水印
```PowerShell
python .\scripts\add_watermark.py watermark.pdf document.pdf
```

#### 2. 批量处理多个 PDF
```PowerShell
python .\scripts\add_watermark.py watermark.pdf doc1.pdf doc2.pdf doc3.pdf
```

#### 3. 指定输出文件夹和透明度
```PowerShell
python .\scripts\add_watermark.py logo.pdf report.pdf -o ./output --opacity 0.5
```

#### 4. 控制水印添加的页码范围
```PowerShell
# 从第2页到第5页添加水印（页码从0开始）
python .\scripts\add_watermark.py watermark.pdf document.pdf --start 1 --end 4
```

#### 5. 使用水印文件的指定页面
```PowerShell
# 使用水印文件的第3页作为水印
python .\scripts\add_watermark.py watermark.pdf document.pdf --source-page 2
```

#### 6. 组合使用多个参数
```PowerShell
python .\scripts\add_watermark.py company_logo.pdf annual_report.pdf \
    -o ./processed \
    --start 2 \
    --end 8 \
    --source-page 0 \
    --opacity 0.7
```

## 注意事项

1. **Adobe Acrobat 要求**：必须安装 Adobe Acrobat Pro，且确保 Acrobat 未处于保护模式（可在首选项中关闭）。
2. **文件路径**：建议使用绝对路径，避免因相对路径导致文件找不到的问题。
3. **水印文件**：水印文件必须是 PDF 格式，可以包含多页，通过 `--source-page` 指定使用的页面。
4. **错误处理**：脚本会逐个处理 PDF 文件，单个文件处理失败不影响其他文件的处理。
5. **输出覆盖**：如果未指定输出文件夹，脚本会直接覆盖原文件。建议使用 `-o` 参数指定输出文件夹，避免意外覆盖。

## 常见问题

**Q: 支持哪些水印格式？**
A: 目前仅支持 PDF 文件作为水印源。如需图片水印，可先将图片转换为 PDF。