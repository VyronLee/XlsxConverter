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

    def dump(self, filepath, keys, contents, indexes):

        data = self.compose(keys, contents, indexes)
        if data is None:
            return False

        os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
        with open(filepath, 'w') as ofp:
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
