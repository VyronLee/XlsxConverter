#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------------------
#       @file  lua_multiple_conversion_test.py
#      @brief  Single file conversion test.
#
#     @author  VyronLee, lwz_jz@hotmail.com
#   @Modified  2019-08-29, 17:40
#  @Copyright  Copyright (c) 2019, VyronLee
# ============================================================

import sys
import xlsx_converter

FILE_2_CONVERT = [
    {"basename": "ActorConf", "indexers": [["id"]]},
    {"basename": "EquipmentConf", "indexers": [["id"], ["quality"], ["id", "quality"]]},
]


def run_test():
    conf = {
        "header_row_count": 4,
        "key_row_index": 0,
        "type_row_index": 1,
        "filter_row_index": 2,
        "brief_row_index": 3,
    }
    re = ".*s+"  # just filter out cols contains 's'

    for item in FILE_2_CONVERT:
        ip = "./input/%s.xlsx" % item["basename"]
        op = "./output/%s.lua" % item["basename"]

        result = xlsx_converter.convert(conf=conf, ip=ip, op=op, filter_re=re, indexers=item["indexers"], out_format="lua")
        if not result:
            print("Error: Convert failed!")
            return result

    return True


if __name__ == '__main__':
    ret = run_test()
    print("Run test finished, exit code: %s" % ret)
    sys.exit(ret)
