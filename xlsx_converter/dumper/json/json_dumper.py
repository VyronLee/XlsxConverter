#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------------------
#       @file  json_dumper.py
#      @brief  Dumper data as json format.
#
#     @author  VyronLee, lwz_jz@hotmail.com
#   @Modified  2019-09-29 19:48
#  @Copyright  Copyright (c) 2019, VyronLee
# ============================================================

import json
import os
from ..dumper import Dumper


class JsonDumper(Dumper):

    def dump(self, file_path, sheet_name, output_dir, keys, contents, indexes, options):

        data = self.compose(keys, contents, indexes)
        if data is None:
            return False

        abs_path = os.path.abspath(output_dir)
        dir_name = os.path.dirname(abs_path)
        base_name = os.path.basename(output_dir)
        os.makedirs(dir_name, exist_ok=True)
        with open("%s/%s_%s.json" % (dir_name, base_name, sheet_name), 'w') as ofp:
            json.dump(data, ofp, ensure_ascii=False, indent=4)

        return True

    @staticmethod
    def compose(keys, contents, indexes):
        """ compose keys and contents context

        :keys: keys context
        :contents: contents context
        :returns: object if succeed

        """
        kv_objs = [{keys[i][0]: content[i] for i in range(0, len(content))} for content in contents]

        return {
            "data": kv_objs,
            "index": indexes,
        }
