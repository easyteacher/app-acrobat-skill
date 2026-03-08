#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: Fushan Wen <qydwhotmail@gmail.com>
# SPDX-License-Identifier: MIT

import argparse
import logging
import sys

from AcrobatPDFProcessor import AVDoc

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="打印PDF文件")
    parser.add_argument("input_pdfs", nargs="+", help="输入PDF文件路径")
    parser.add_argument("--start", type=int, default=0, help="开始页码（默认从0开始）")
    parser.add_argument("--end", type=int, default=-1, help="结束页码（默认到最后一页）")
    parser.add_argument("--ps-level", type=int, choices=[2, 3], default=3, help="PostScript Level (2 or 3)")
    parser.add_argument("--disable-shrink-to-fit", action="store_true", help="是否禁用缩放页面到适合纸张（保持原大小）")
    parser.add_argument("--reversed", action="store_true", help="是否反向打印（从最后一页开始）")
    parser.add_argument("--page-option", type=int, choices=[0, 1, 2], default=0, help="页面选项 (0: 全部打印, 1: 打印偶数页, 2: 打印奇数页)")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    console_handler = logging.StreamHandler(sys.stdout)
    logger.addHandler(console_handler)

    for input_pdf in args.input_pdfs:
        with AVDoc() as a:
            if not a.Open(input_pdf):
                logger.error(f"无法打开PDF文件: {input_pdf}，跳过打印。")
                continue
            try:
                ret = a.PrintPagesEx(args.start, args.end, nPSLevel=args.ps_level, bShrinkToFit=not args.disable_shrink_to_fit, bReverse=args.reversed, iPageOption=args.page_option)
                if ret:
                    logger.info(f"成功打印 {input_pdf} 从第{args.start}页到第{args.end}页")
                else:
                    logger.error(f"打印 {input_pdf} 从第{args.start}页到第{args.end}页失败")
            except Exception as e:
                logger.error(f"打印 {input_pdf} 从第{args.start}页到第{args.end}页失败: {e}")

