# PDF合并工具 merge.py

## 简介

`merge.py` 可以将多个 PDF 文件合并为一个文件。支持自定义输出路径、创建书签。

## 功能特点

- 按顺序合并PDF
- 支持创建书签以便导航

## 使用方法

### 基本语法

```PowerShell
python .\scripts\merge.py <输入文件1> <输入文件2> ... [-o 输出文件] [-b]
```

### 参数说明

| 参数 | 说明 |
|------|------|
| `input_files` | 要合并的 PDF 文件路径列表（至少2个） |
| `-o, --output-file` | 可选，输出合并后的 PDF 文件路径，默认为保存到第一个PDF的文件夹 |
| `-b, --create-bookmarks` | 可选，为每个源文件创建书签 |

### 使用示例

#### 1. 基本合并
```PowerShell
python .\scripts\merge.py file1.pdf file2.pdf file3.pdf -o merged.pdf
```

#### 2. 合并并创建书签
```PowerShell
python .\scripts\merge.py chapter1.pdf chapter2.pdf chapter3.pdf -o book.pdf -b
```

#### 43. 使用默认输出路径
```PowerShell
python .\scripts\merge.py part1.pdf part2.pdf part3.pdf
# 将在第一个 PDF 所在目录生成 merged.pdf
```

## 输出行为

### 指定输出文件
当使用 `-o` 参数指定输出路径时，合并后的 PDF 将保存到指定位置：
```PowerShell
python .\scripts\merge.py a.pdf b.pdf -o C:\output\combined.pdf
```

### 默认输出
当不指定输出文件时，程序会在**第一个输入 PDF 所在的目录**创建 `merged.pdf` 文件：
```PowerShell
python .\scripts\merge.py C:\docs\a.pdf D:\docs\b.pdf
# 输出：C:\docs\merged.pdf
```

## 注意事项

1. **文件顺序**：合并顺序严格按照命令行输入顺序
2. **文件验证**：程序会检查每个输入文件是否存在
3. **错误处理**：单个文件插入失败不影响其他文件的合并
4. **书签功能**：使用 `-b` 参数可为每个源文件创建书签，方便导航
5. **权限要求**：输出目录需要有写入权限

## 常见问题

### Q: 合并后的文件顺序不对？
A: 请检查命令行中输入文件的顺序，程序严格按照输入顺序合并。

### Q: 某些文件合并失败？
A: 可能的原因：
   - 文件损坏或密码保护
   - Adobe Acrobat 无法读取该 PDF
   - 文件路径包含特殊字符

程序会继续处理剩余文件并报告失败数量。

## 性能提示

- 对于超大文件（100MB以上），确保系统有足够内存