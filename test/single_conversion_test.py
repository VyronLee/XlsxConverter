#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------------------
#       @file  single_conversion_test.py
#      @brief  Single file conversion test.
#
#     @author  VyronLee, lwz_jz@hotmail.com
#   @Modified  2019-08-29, 11:56
#  @Copyright  Copyright (c) 2019, VyronLee
# ============================================================

import sys
import xlsx_converter


def run_test(out_format):
    conf = {
        "header_row_count": 4,
        "key_row_index": 0,
        "type_row_index": 1,
        "filter_row_index": 2,
        "brief_row_index": 3,
    }
    ip = "./input/ActorConf.xlsx"
    op = "./output"
    re = ".*c+"  # just filter out cols contains 'c'
    idx = [["id"]]
    sheet_name = "Properties"
    options = {
        "generate_codes": True,
        "codes_type": "python",
    }
    return xlsx_converter.convert(
        conf=conf,
        ip=ip,
        op=op,
        filter_re=re,
        indexers=idx,
        sheet_name=sheet_name,
        out_format=out_format,
        options=options
    )


if __name__ == '__main__':
    ret = True
    ret = ret and run_test("json")
    ret = ret and run_test("lua")
    ret = ret and run_test("pb")
    print("Run test finished, exit code: %s" % ret)
    sys.exit(ret)
