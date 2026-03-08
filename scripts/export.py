#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: Fushan Wen <qydwhotmail@gmail.com>
# SPDX-License-Identifier: MIT

import argparse
import logging
import os
import sys

from AcrobatPDFProcessor import ConvID, PDDoc

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="导出PDF文档到其他格式")
    parser.add_argument("files", type=str, nargs="+", help="输入PDF文件路径")
    parser.add_argument("--overwrite", action="store_true", help="覆盖已存在的输出文件")

    args = parser.parse_args()

    if len(args.files) % 2 != 0:
        parser.error("输入PDF文件路径和输出文件路径数量必须一致")

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    console_handler = logging.StreamHandler(sys.stdout)
    logger.addHandler(console_handler)

    for i in range(0, len(args.files), 2):
        input_pdf = args.files[i]
        output_file = args.files[i + 1]

        if not input_pdf.lower().endswith(".pdf"):
            logger.warning(f"输入文件不是PDF文件: {input_pdf}，跳过。")
            continue

        if os.path.exists(output_file) and not args.overwrite:
            logger.warning(f"输出文件已存在: {output_file}，跳过。")
            continue

        logger.info(f"正在导出 {input_pdf} 到 {output_file}")

        with PDDoc(input_pdf) as a:
            try:
                if output_file.lower().endswith(".docx"):
                    a.export(output_file, ConvID.docx)
                elif output_file.lower().endswith(".pptx"):
                    a.export(output_file, ConvID.pptx)
                elif output_file.lower().endswith(".xlsx"):
                    a.export(output_file, ConvID.xlsx)
                elif output_file.lower().endswith(".txt"):
                    a.export(output_file, ConvID.txt)
                elif output_file.lower().endswith(".png"):
                    a.export(output_file, ConvID.png)
                elif output_file.lower().endswith(".jpeg") or output_file.lower().endswith(".jpg"):
                    a.export(output_file, ConvID.jpeg)
                else:
                    logger.warning(f"不支持的输出文件格式: {output_file}，跳过。")
                    continue
            except Exception as e:
                logger.error(f"导出{output_file}失败: {e}")

        logger.info(f"已导出 {input_pdf} 到 {output_file}")
