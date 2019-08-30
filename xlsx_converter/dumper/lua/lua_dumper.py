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

    def compose(self, tb_name, keys, contents, indexes):
        """ compose keys and contents context into lua file format

        :tb_name: lua file name
        :keys: keys context
        :contents: contents context
        :returns: lua file data string if succeed

        """
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

        return lua_file_template % (tb_name, key_content, record_content, indexes_content)

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
        data = self.compose(os.path.basename(output_dir), keys, contents, indexes)
        if data is None:
            return False

        abs_path = os.path.abspath(output_dir)
        dir_name = os.path.dirname(abs_path)
        base_name = os.path.basename(output_dir)
        os.makedirs(dir_name, exist_ok=True)
        with open("%s/%s_%s.lua" % (dir_name, base_name, sheet_name), 'w') as ofp:
            ofp.write(data)

        return True
