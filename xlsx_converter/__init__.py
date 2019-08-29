#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------------------
#       @file  __init__.py
#      @brief  init file.
#
#     @author  VyronLee, lwz_jz@hotmail.com
#
#   @internal
#    Modified  2019-08-28 23:54
#   Copyright  Copyright (c) 2019, VyronLee
# ============================================================
from .converter import XlsxConverter


def convert(conf=None,
            ip=None,
            op=None,
            sheet_name="Sheet1",
            filter_re=".*",
            indexers=None,
            out_format="json",
            verbose=1):
    if indexers is None:
        indexers = []

    if verbose >= 0:
        print("Converting file: %s, using sheet: %s, output: %s" % (ip, sheet_name, op))

    ret = XlsxConverter(conf).convert(ip, op, sheet_name, filter_re, indexers, out_format)

    if verbose >= 0:
        if ret:
            print("\033[F", end='')
            print("Converting file: %s, using sheet: %s, output: %s, %s" % (ip, sheet_name, op, "succeed!"))

    return ret
