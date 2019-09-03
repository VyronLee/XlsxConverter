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

    def convert(self, out_format, filepath, output_dir, sheet_name, filter_re, indexers, options=None):
        """convert xls file "ip" to specified format, store in path "op"

        :out_format: format to convert
        :filepath: input file path
        :output_dir: output directory
        :sheet_name: name of sheet to read
        :filter_re: filter regex
        :indexer: indexer array
        :options: additional options
        :returns: True if succeed, otherwise False

        """
        if options is None:
            options = {}
        try:
            book = xlrd.open_workbook(filename=filepath)
        except Exception:
            print("Error: Open workbook failed, filename: %s" % filepath)
            return False

        sheet = book.sheet_by_name(sheet_name)
        if not sheet:
            print("Error: Sheet doesn't exist: ", sheet_name)
            return False

        if sheet.nrows < self.conf["header_row_count"]:
            print("Error: Invalid input file, line count less than %s: %s, sheet name: %s" % (
                self.conf["header_row_count"], filepath, sheet_name))
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
        elif out_format == "pb":
            from .dumper.protobuf.protobuf_dumper import ProtoBufDumper
            dumper = ProtoBufDumper()
        return dumper.dump(filepath, sheet_name, output_dir, keys, contents, indexes, options)
