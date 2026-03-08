# PDF导出工具 export.py

## 简介

`export.py` 可以将 PDF 文件批量导出为多种常见格式，包括 Word、PowerPoint、Excel、文本文件和图片格式。

## 功能特点

- 支持批量转换多个 PDF 文件
- 支持多种输出格式
- 自动根据文件扩展名识别导出格式
- 可选的覆盖输出文件功能
- 详细的日志输出

## 支持的输出格式

| 格式 | 文件扩展名 | 说明 |
|------|-----------|------|
| Word | .docx | 导出为 Word 文档 |
| PowerPoint | .pptx | 导出为 PowerPoint 演示文稿 |
| Excel | .xlsx | 导出为 Excel 表格 |
| 文本 | .txt | 导出为纯文本文件 |
| PNG | .png | 导出为 PNG 图片（多页面自动添加后缀） |
| JPEG | .jpeg, .jpg | 导出为 JPEG 图片（多页面自动添加后缀） |

## 使用方法

### 基本语法

```PowerShell
python .\scripts\export.py <输入PDF文件1> <输出文件1> [<输入PDF文件2> <输出文件2> ...] [--overwrite]
```

### 参数说明

| 参数 | 说明 |
|------|------|
| `files` | 输入PDF文件路径和输出文件路径交替指定，数量必须为偶数 |
| `--overwrite` | 可选参数，当输出文件已存在时覆盖，默认跳过 |

### 使用示例

#### 1. 导出单个 PDF 为 Word 文档
```PowerShell
python .\scripts\export.py document.pdf document.docx
```

#### 2. 导出多个 PDF 为不同格式
```PowerShell
python .\scripts\export.py report.pdf report.docx manual.pdf manual.pptx
```

#### 3. 导出为图片格式
当PDF有多个页面，导出时会自动为每页创建单独的文件（如scan_1.png, scan_2.png等），不要指定多个输出文件
```PowerShell
python .\scripts\export.py scan.pdf scan.png
```

#### 4. 批量导出并允许覆盖
```PowerShell
python .\scripts\export.py file1.pdf file1.docx file2.pdf file2.docx --overwrite
```

## 注意事项

1. **文件配对**：输入文件和输出文件必须成对出现，数量必须为偶数
2. **格式识别**：输出格式完全由文件扩展名决定，请确保使用支持的扩展名
3. **文件存在**：默认情况下，如果输出文件已存在，程序会跳过并给出警告
4. **错误处理**：单个文件转换失败不会影响其他文件的处理

## 常见问题

### Q: 为什么导出失败？
A: 可能的原因：
   - Adobe Acrobat Pro 未正确安装
   - 输入 PDF 文件损坏或受密码保护
   - 输出路径无写入权限
   - Adobe Acrobat 保护模式未关闭

### Q: 支持批量转换更多文件吗？
A: 支持，只需按顺序列出所有输入输出文件对即可。