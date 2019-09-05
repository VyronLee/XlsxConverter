#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------------------
#       @file  lua_dumper.py
#      @brief  Dumper data as lua format.
#
#     @author  VyronLee, lwz_jz@hotmail.com
#   @Modified  2019-09-29 19:48
#  @Copyright  Copyright (c) 2019, VyronLee
# ============================================================

import os
from .template import lua_file_template
from ..dumper import Dumper


class LuaDumper(Dumper):

    def compose(self, file_path, sheet_name, keys, contents, indexes):
        file_name = os.path.splitext(os.path.basename(file_path))[0]

        key_content = ""
        for i in range(0, len(keys)):
            key_content = key_content + "\t[\'%s\'] = {index=%d,type=\"%s\",brief=\"%s\"},\n" % (
                keys[i][0], i + 1, keys[i][1], keys[i][2])

        record_content = ""
        for i in range(0, len(contents)):
            record_content = record_content + "\t[%d] = __mt(%s, mt),\n" % (
                i + 1, self.content_to_table_string(contents[i]))

        indexes_content = ""
        for item in indexes:
            indexes_content = indexes_content + "\t[\'%s\'] = {\n" % item
            sorted_indexes = sorted(indexes[item], key=lambda x: x[0])
            for idx in sorted_indexes:
                value_indexes = ['%r' % (val + 1) for val in indexes[item][idx]]
                indexes_content = indexes_content + "\t\t[\'%s\'] = {%s},\n" % (idx, ','.join(value_indexes))
            indexes_content = indexes_content + "\t},\n"

        template = lua_file_template
        template = template.replace("__FILENAME__", file_name)
        template = template.replace("__SHEETNAME__", sheet_name)
        template = template.replace("__SHEET_KEY_SEGMENT__", key_content)
        template = template.replace("__SHEET_DATA_SEGMENT__", record_content)
        template = template.replace("__SHEET_INDEX_SEGMENT__", indexes_content)
        return template

    @staticmethod
    def content_to_table_string(content):
        """convert content to lua table string format

        :content: content to convert
        :returns: lua table string

        """
        table = "{"
        for ele in content:
            if type(ele) is float:
                table = table + ('%r' % ele).rstrip('0').rstrip('.') + ','
            elif type(ele) is str:
                table = table + ('\'%s\'' % ele.replace('"', '\\"').replace('\'', '\\\'')) + ','
            elif type(ele) is int:
                table = table + ('%r' % ele) + ','
            else:
                print("Error: Unhandled value type: " + type(ele))
        table = table + "}"
        return table

    def dump(self, file_path, sheet_name, output_dir, keys, contents, indexes, options):
        data = self.compose(file_path, sheet_name, keys, contents, indexes)
        if data is None:
            return False

        filename = os.path.splitext(os.path.basename(file_path))[0]
        os.makedirs(output_dir, exist_ok=True)
        with open("%s/%s_%s.lua" % (output_dir, filename, sheet_name), 'w') as ofp:
            ofp.write(data)

        return True
