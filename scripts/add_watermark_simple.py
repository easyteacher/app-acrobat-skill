#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: Fushan Wen <qydwhotmail@gmail.com>
# SPDX-License-Identifier: MIT

import PyPDF2
import os
import sys

def add_watermark(watermark_pdf, input_pdf, output_pdf=None):
    """
    为PDF文件添加水印
    """
    if output_pdf is None:
        # 在原文件名后添加_watermarked
        base, ext = os.path.splitext(input_pdf)
        output_pdf = f"{base}_watermarked{ext}"

    # 读取水印PDF
    watermark_reader = PyPDF2.PdfReader(watermark_pdf)
    watermark_page = watermark_reader.pages[0]

    # 读取输入PDF
    input_reader = PyPDF2.PdfReader(input_pdf)
    writer = PyPDF2.PdfWriter()

    # 为每一页添加水印
    for i in range(len(input_reader.pages)):
        page = input_reader.pages[i]

        # 合并水印到当前页
        page.merge_page(watermark_page)

        # 添加到输出
        writer.add_page(page)

    # 保存输出PDF
    with open(output_pdf, 'wb') as output_file:
        writer.write(output_file)

    print(f"水印添加完成！输出文件: {output_pdf}")
    return output_pdf

if __name__ == "__main__":
    assert len(sys.argv) > 3, "用法: python add_watermark_simple.py <水印PDF文件> <要添加水印的PDF文件> [输出PDF文件]"

    watermark_pdf = sys.argv[1]
    input_pdf = sys.argv[2]
    output_pdf = sys.argv[3] if len(sys.argv) > 3 else None

    if not os.path.exists(watermark_pdf):
        print(f"错误: 水印文件不存在: {watermark_pdf}")
        sys.exit(1)

    if not os.path.exists(input_pdf):
        print(f"错误: 输入文件不存在: {input_pdf}")
        sys.exit(1)

    add_watermark(watermark_pdf, input_pdf, output_pdf)