#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: Fushan Wen <qydwhotmail@gmail.com>
# SPDX-License-Identifier: MIT

import argparse
import logging
import sys

from AcrobatPDFProcessor import PDDoc


def main():
    parser = argparse.ArgumentParser(
        description="从PDF文件中替换指定页面",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
页面范围格式示例:
  %(prog)s input.pdf replace.pdf --start 2 -o output.pdf   # 从原文件第2页开始替换（页码从1开始）
        """
    )

    parser.add_argument("input_pdf", help="输入PDF文件路径")
    parser.add_argument("replace_pdf", help="替换PDF文件路径")
    parser.add_argument("--start", type=int, required=True,
                       help="开始替换的页面页码（从1开始）")
    parser.add_argument("--num-pages", type=int,
                       help="要替换的页面数量，默认为替换PDF文件的页数")
    parser.add_argument("-o", "--output", help="输出PDF文件路径（默认保存到原文件）")

    args = parser.parse_args()

    if args.start < 1:
        parser.error("开始页码必须大于等于1")

    # 配置日志
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    console_handler = logging.StreamHandler(sys.stdout)
    logger.addHandler(console_handler)

    # 先打开PDF获取总页数
    with PDDoc(args.input_pdf) as source_doc:
        total_pages = source_doc.GetNumPages()

        with PDDoc(args.replace_pdf) as replace_doc:
            replace_pages = replace_doc.GetNumPages()
            if args.num_pages is None or args.num_pages > replace_pages or args.num_pages < 1:
                num_pages = replace_pages
            else:
                num_pages = args.num_pages
            if args.start + replace_pages - 1 > total_pages:
                parser.error("替换页面范围超出文件总页数")

            if not source_doc.ReplacePages(args.start - 1, replace_doc, 0, num_pages, False):
                logger.error("页面替换失败")
                sys.exit(1)

        n_type = (PDDoc.PDSaveFull | PDDoc.PDSaveLinearized)
        if not source_doc.Save(n_type, args.output):
            logger.error("保存输出PDF文件失败，检查目标PDF文件是否被程序占用")
            sys.exit(1)

        logger.info(f"已成功从第 {args.start} 页开始替换 {num_pages} 页并保存到 {args.output or args.input_pdf}")



if __name__ == "__main__":
    main()
