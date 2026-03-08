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
    parser = argparse.ArgumentParser(description="合并多个PDF文件")
    parser.add_argument("input_files", nargs="+", help="输入PDF文件路径")
    parser.add_argument("-o", "--output-file", help="输出合并后的PDF文件路径")
    parser.add_argument("-b", "--create-bookmarks", action="store_true", help="是否创建书签")
    args = parser.parse_args()

    if len(args.input_files) < 2:
        parser.error("至少需要2个输入文件")

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    console_handler = logging.StreamHandler(sys.stdout)
    logger.addHandler(console_handler)

    with PDDoc() as pd_doc:
        pd_doc.Create()

        success_count = 0
        for input_file in args.input_files:
            if not os.path.exists(input_file):
                logger.error(f"错误：文件 {input_file} 不存在")
                continue

            try:
                with PDDoc(input_file) as temp_pd_doc:
                    pd_doc.InsertPages(-1, temp_pd_doc, 0, temp_pd_doc.GetNumPages(), args.create_bookmarks)
            except Exception as e:
                logger.error(f"插入 {input_file} 失败: {e}")
                continue

            success_count += 1

        n_type = (PDDoc.PDSaveFull | PDDoc.PDSaveLinearized)
        if args.output_file:
            ret = pd_doc.Save(PDDoc.PDSaveFull | PDDoc.PDSaveLinearized, args.output_file)
        else:
            # 保存到第一个pdf的文件夹
            ret = pd_doc.Save(n_type, os.path.join(os.path.dirname(args.input_files[0]), "merged.pdf"))

        if ret:
            logger.info(f"已合并 {success_count} 个文件到 {args.output_file}，{len(args.input_files) - success_count} 个文件合并失败")
        else:
            logger.error(f"保存到{args.output_file or os.path.join(os.path.dirname(args.input_files[0]), 'merged.pdf')}失败")
