#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------------------
#       @file  dumper.py
#      @brief  Dumper base class.
#
#     @author  VyronLee, lwz_jz@hotmail.com
#   @Modified  2019-08-28 23:55
#  @Copyright  Copyright (c) 2019, VyronLee
# ============================================================


class Dumper(object):

    def dump(self, file_path, sheet_name, output_dir, keys, contents, indexes, options):
        """

        :param file_path: xlsx file name.
        :param sheet_name: xlsx sheet name.
        :param options: options
        :param output_dir: output directory.
        :param keys: Key values
        :param contents: Content values
        :param indexes: Index values
        """
        print("Error: No dump action implementation!")
        return False
