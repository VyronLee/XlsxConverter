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

        filename = os.path.splitext(os.path.basename(file_path))[0]
        os.makedirs(output_dir, exist_ok=True)
        with open("%s/%s_%s.json" % (output_dir, filename, sheet_name), 'w') as ofp:
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
