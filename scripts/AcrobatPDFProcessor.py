#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: Fushan Wen <qydwhotmail@gmail.com>
# SPDX-License-Identifier: MIT

# https://opensource.adobe.com/dc-acrobat-sdk-docs/library/interapp/IAC_API_OLE_Objects.html

from enum import Enum
import os
import subprocess
import logging
from typing import Optional

import win32com.client
from win32com.client.dynamic import ERRORS_BAD_CONTEXT
import winerror

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 当遇到 E_NOTIMPL 错误时，不要直接抛出异常，而是继续尝试执行
ERRORS_BAD_CONTEXT.append(winerror.E_NOTIMPL)

class ConvID(Enum):
    docx = "com.adobe.acrobat.docx"
    pptx = "com.adobe.acrobat.pptx"
    xlsx = "com.adobe.acrobat.xlsx"
    txt = "com.adobe.acrobat.plain-text"
    jpeg = "com.adobe.acrobat.jpeg"
    png = "com.adobe.acrobat.png"


class AVDoc:
    """Wrapper for AcroExch.AVDoc"""
    PDAllPages = 0
    PDEvenPagesOnly = 1
    PDOddPagesOnly = 2

    def __init__(self, pdf_path: Optional[str] = None):
        self.av_doc = win32com.client.DispatchEx("AcroExch.AVDoc")

        if pdf_path:
            self.Open(pdf_path)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.Close()
        return False

    def Open(self, pdf_path: str) -> int:
        """
        打开PDF文件

        Args:
            pdf_path: PDF文件绝对路径

        Returns:
            int: 打开状态码（-1：成功，0：失败）
        """
        return self.av_doc.Open(os.path.abspath(pdf_path), "")

    def Close(self, bNoSave: bool = True) -> int:
        """
        关闭PDF文件

        Args:
            bSaveChanges: 是否保存更改（默认：False）

        Returns:
            int: 总是返回-1
        """
        return self.av_doc.Close(bNoSave)

    def GetPDDoc(self) -> PDDoc:
        """
        获取PDDoc对象

        Returns:
            win32com.client.CDispatch: PDDoc对象
        """
        return PDDoc(self.av_doc.GetPDDoc())

    def PrintPagesEx(self, nFirstPage: int = 0, nLastPage: int = -1,
                 nPSLevel: int = 3, bBinaryOk: bool = True,
                 bShrinkToFit: bool = True, bReverse: bool = False,
                 bFarEastFontOpt: bool = True, bEmitHalftones: bool = True,
                 iPageOption: int = 0) -> bool:
        """
        打印PDF文件的指定页面

        Returns:
            bool: 是否成功打印
        """
        page_count = self.GetPDDoc().GetNumPages()

        # 执行打印
        if not nFirstPage:
            nFirstPage = 0
        else:
            nFirstPage = max(0, min(nFirstPage, page_count - 1))

        if not nLastPage or nLastPage < 0:
            nLastPage = page_count - 1
        else:
            nLastPage = max(nFirstPage, min(nLastPage, page_count - 1))

        return self.av_doc.PrintPagesEx(nFirstPage, nLastPage, nPSLevel, bBinaryOk, bShrinkToFit, bReverse, bFarEastFontOpt, bEmitHalftones, iPageOption)

class PDDoc:
    """Wrapper for AcroExch.PDDoc"""

    PDSaveFull = 1
    PDSaveBinaryOK = 16
    PDSaveCollectGarbage = 32
    PDSaveCopy = 2
    PDSaveIncremental = 0
    PDSaveLinearized = 4
    PDSaveWithPSHeader = 8

    def __init__(self, *args):
        self.pdf_path = ""

        if len(args) > 0:
            if isinstance(args[0], str):
                self.pd_doc = win32com.client.DispatchEx("AcroExch.PDDoc")
                self.Open(args[0])
            elif isinstance(args[0], PDDoc):
                self.pd_doc = args[0].pd_doc
            elif isinstance(args[0], win32com.client.CDispatch):
                self.pd_doc = args[0]
            else:
                logger.error(f"PDDoc.__init__: 不支持的参数类型: {type(args[0])}")
        else:
            self.pd_doc = win32com.client.DispatchEx("AcroExch.PDDoc")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.Close()
        return False

    def Create(self) -> int:
        return self.pd_doc.Create()

    def Open(self, pdf_path: str) -> int:
        """
        打开PDF文件

        Args:
            pdf_path: PDF文件绝对路径

        Returns:
            int: 打开状态码（-1：成功，0：失败）
        """
        self.pdf_path = os.path.abspath(pdf_path)
        return self.pd_doc.Open(os.path.abspath(pdf_path))

    def Save(self, nType: int = 0, output_path: Optional[str] = None) -> int:
        """
        保存PDF文件

        Args:
            nType: 保存类型
            output_path: 保存路径（默认：原路径）

        Returns:
            int: 保存状态码（-1：成功，0：失败）
        """
        output_path = output_path or self.pdf_path
        return self.pd_doc.Save(nType, os.path.abspath(output_path))

    def Close(self) -> int:
        """
        关闭PDF文件

        Returns:
            int: 关闭状态码（-1：成功，0：失败）
        """
        return self.pd_doc.Close()

    def GetJSObject(self) -> object:
        """
        获取PDF的JS对象

        Returns:
            object: PDF的JS对象（AcroExch.JSObject）
        """
        return self.pd_doc.GetJSObject()

    def GetNumPages(self) -> int:
        """
        获取PDF总页数

        Returns:
            int: PDF总页数
        """
        return self.pd_doc.GetNumPages()

    def InsertPages(self, nInsertPageAfter: int,
                 iPDDocSource: PDDoc, nStartPage: int,
                 nNumPages: int, bBookmarks: bool) -> int:
        """
        在指定位置插入页面

        Args:
            nInsertPageAfter: 插入位置索引（从0开始）
            iPDDocSource: 要插入的PDDoc对象（AcroExch.PDDoc）
            nStartPage: 要插入的起始页索引（从0开始）
            nNumPages: 要插入的页面数量
            bBookmarks: 是否创建书签

        Returns:
            int: 插入状态码（-1：成功，0：失败）
        """
        if nInsertPageAfter < 0:
            nInsertPageAfter = self.GetNumPages() - 1
        else:
            nInsertPageAfter = min(max(0, nInsertPageAfter), self.GetNumPages() - 1)

        return self.pd_doc.InsertPages(nInsertPageAfter, iPDDocSource.pd_doc, nStartPage, nNumPages, bBookmarks)

    def ReplacePages(self, nStartPage: int,
                 iPDDocSource: PDDoc, nStartSourcePage: int = 0,
                 nNumPages: Optional[int] = None, bMergeTextAnnotations: bool = False) -> int:
        """
        替换指定页面

        Args:
            nStartPage: 要替换的起始页索引（从0开始）
            iPDDocSource: 要替换的PDDoc对象（AcroExch.PDDoc）
            nStartSourcePage: 要替换的起始源页索引（从0开始）
            nNumPages: 要替换的页面数量
            bMergeTextAnnotations: 是否合并文本注释

        Returns:
            int: 替换状态码（-1：成功，0：失败）
        """
        if not nNumPages or nNumPages < 0:
            nNumPages = iPDDocSource.GetNumPages() - nStartSourcePage
        return self.pd_doc.ReplacePages(nStartPage, iPDDocSource.pd_doc, nStartSourcePage, nNumPages, bMergeTextAnnotations)

    def export(self, output_path: str, export_format: ConvID):
        """
        导出PDF

        Args:
            output_path: 输出路径
            export_format: 导出格式常量
        """
        js_obj = self.GetJSObject()
        # 执行导出
        # https://opensource.adobe.com/dc-acrobat-sdk-docs/library/jsapiref/doc.html#saveas
        js_obj.saveAs(output_path, export_format.value)

    def add_watermark(self, watermark_path: str, nSourcePage: Optional[int] = None, nStartPage: Optional[int] = None, nEndPage: Optional[int] = None, bOnTop: bool = True, nHorizAlign: int = 1, nVertAlign: int = 1, nScale: float = 1.0, bFixedPrint: bool = False, nOpacity: float = 1.0):
        """
        添加水印到PDF文件。

        Args:
            watermark_path: 水印PDF路径
            nHorizAlign: 0=left, 1=center, 2=right, 3=top, 4=bottom
            nVertAlign: 0=left, 1=center, 2=right, 3=top, 4=bottom
        """
        js_obj = self.GetJSObject()
        # https://opensource.adobe.com/dc-acrobat-sdk-docs/library/jsapiref/doc.html#addwatermarkfromfile

        if not nSourcePage:
            nSourcePage = 0
        if not nStartPage:
            nStartPage = 0
        else:
            nStartPage = min(max(0, nStartPage), self.GetNumPages() - 1)

        if not nEndPage or nEndPage < 0:
            nEndPage = self.GetNumPages() - 1
        else:
            nEndPage = min(max(nStartPage, nEndPage), self.GetNumPages() - 1)

        js_obj.addWatermarkFromFile(watermark_path, nSourcePage, nStartPage, nEndPage, bOnTop, True, True, nHorizAlign, nVertAlign, 0, 0, False, nScale, bFixedPrint, 0, nOpacity)

class AcrobatPDFProcessor:
    """
    Adobe Acrobat PDF处理类
    API文档：https://opensource.adobe.com/dc-acrobat-sdk-docs/library/interapp/IAC_API_OLE_Objects.html
    """

    def __init__(self):
        """
        初始化Acrobat COM对象
        """
        self.app = None
        self._initialize_acrobat()

    def _initialize_acrobat(self):
        """初始化Acrobat应用程序"""
        try:
            logger.info("Acrobat COM接口初始化中...")
            # 创建Acrobat App COM对象 [citation:1]
            try:
                self.app = win32com.client.DispatchEx("AcroExch.App") # DispatchEx创建新实例，避免线程冲突
            except Exception as e:
                logger.error(f"Acrobat COM对象创建失败，可能需要手动终止现有的Acrobat实例: {e}")

            logger.info("Acrobat COM接口初始化成功")

        except Exception as e:
            logger.error(f"Acrobat初始化失败: {e}")
            logger.error("请确认：1. 已安装Acrobat Pro 2. 已安装pywin32 3. 关闭了保护模式 [citation:5]")
            raise

    def open(self, pdf_path: str) -> Optional[PDDoc]:
        """
        打开PDF文件

        Args:
            pdf_path: PDF文件绝对路径

        Returns:
            bool: 是否成功打开
        """
        abs_path = os.path.abspath(pdf_path)

        if not os.path.exists(pdf_path):
            logger.error(f"PDF文件不存在: {pdf_path}")
            return None

        # 打开PDF
        pd_doc = PDDoc()
        if pd_doc.Open(abs_path):
            logger.info(f"成功打开: {abs_path}")
            return pd_doc

        logger.error(f"打开失败: {abs_path}")
        return None

    def ocr_pdf(self, pd_doc: PDDoc, pdf_path: str, output_path: Optional[str] = None):
        """
        对PDF进行OCR识别（处理扫描件）

        Args:
            pdf_path: 扫描件PDF路径
            output_path: 输出PDF路径（带可搜索文本）

        Returns:
            输出文件路径
        """
        # TODO: Acrobat PDF尚未提供OCR接口
        return

    def quit(self):
        """退出Acrobat"""
        if self.app:
            if not self.app.Exit():
                subprocess.check_call(["taskkill", "/f", "/im", "Acrobat.exe"])
            logger.info("Acrobat已退出")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.quit()
        return False
