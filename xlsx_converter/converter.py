#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------------------
#       @file  converter.py
#      @brief  Xls/Xlsx file converter.
#
#     @author  VyronLee, lwz_jz@hotmail.com
#   @Modified  2019-08-28 23:55
#  @Copyright  Copyright (c) 2019, VyronLee
# ============================================================

import xlrd

from .dumper.dumper import Dumper
from .parser import XlsxParser


class XlsxConverter(object):

    def __init__(self, conf):
        """Constructor.

        :conf: dict, config info, contains:
                - header_row_count  : int,
                - type_row_index    : int,
                - key_row_index     : int,
                - filter_row_index  : int,
                - brief_row_index   : int,
        """
        self.conf = conf

    def convert(self, ip, op, sheet_name, filter_re, indexers, out_format):
        """convert xls file "ip" to specified format, store in path "op"

        :ip: input file path
        :op: output file path
        :sheet_name: name of sheet to read
        :filter_re: filter regex
        :indexer: indexer array
        :returns: True if succeed, otherwise False

        """
        try:
            book = xlrd.open_workbook(filename=ip)
        except Exception:
            print("Error: Open workbook failed, filename: %s" % ip)
            return False

        sheet = book.sheet_by_name(sheet_name)
        if not sheet:
            print("Error: Sheet doesn't exist: ", sheet_name)
            return False

        if sheet.nrows < self.conf["header_row_count"]:
            print("Error: Invalid input file, line count less than %s: %s, sheet name: %s" % (
                self.conf["header_row_count"], ip, sheet_name))
            return False

        parser = XlsxParser(self.conf)

        keys = parser.parse_key(sheet)
        if keys is None:
            return False

        contents = parser.parse_content(keys, sheet)
        if contents is None:
            return False

        indexes = parser.parse_indexes(keys, contents, indexers)
        if indexes is None:
            return False

        keys, contents = parser.filter_data(sheet, keys, contents, filter_re)
        if keys is None:
            return False

        dumper = Dumper()
        if out_format == "lua":
            from .dumper.lua.lua_dumper import LuaDumper
            dumper = LuaDumper()
        elif out_format == "json":
            from .dumper.json.json_dumper import JsonDumper
            dumper = JsonDumper()
        return dumper.dump(op, keys, contents, indexes)
