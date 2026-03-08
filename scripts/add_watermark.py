#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: Fushan Wen <qydwhotmail@gmail.com>
# SPDX-License-Identifier: MIT

import argparse
import logging
import os
import sys

from AcrobatPDFProcessor import PDDoc

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="添加水印到PDF文件")
    parser.add_argument("watermark", help="水印文件路径")
    parser.add_argument("pdf_files", nargs="+", help="待添加水印的PDF文件路径")
    parser.add_argument("-o", "--output-folder", type=str, help="输出文件夹路径（默认与输入文件相同）")
    parser.add_argument("--start", type=int, default=0, help="开始页码（默认从0开始）")
    parser.add_argument("--end", type=int, default=-1, help="结束页码（默认到最后一页）")
    parser.add_argument("--source-page", type=int, default=0, help="水印来源页码（默认为0）")
    parser.add_argument("--opacity", type=float, default=1.0, help="水印透明度（默认1.0）")

    args = parser.parse_args()
    assert len(args.pdf_files) > 0, "请提供至少一个PDF文件"

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    console_handler = logging.StreamHandler(sys.stdout)
    logger.addHandler(console_handler)

    for pdf_file in args.pdf_files:
        with PDDoc(pdf_file) as doc:
            try:
                doc.add_watermark(args.watermark, args.source_page, args.start, args.end, nOpacity=args.opacity)
            except Exception as e:
                logger.error(f"为{pdf_file}添加水印失败：{e}")
                continue

            if args.output_folder:
                if not os.path.exists(args.output_folder):
                    os.makedirs(args.output_folder)
                output_path = os.path.join(args.output_folder, os.path.basename(pdf_file))
            else:
                output_path = pdf_file

            try:
                doc.Save(PDDoc.PDSaveFull, output_path)
            except Exception as e:
                logger.error(f"保存到{output_path}失败：{e}")
