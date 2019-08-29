#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------------------
#       @file  converter.py
#      @brief  Parse and convert xls/xlsx file to json.
#
#     @author  VyronLee, lwz_jz@hotmail.com
#   @Modified  2019-08-28 23:55
#  @Copyright  Copyright (c) 2019, VyronLee
# ============================================================

import re

VALID_KEY_TYPES = ["int", "float", "string", ]


class XlsxParser(object):
    """Parse and rearrange xls/xlsx data."""

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

    def parse_key(self, sheet):
        """parse keys from file data

        :sheet: the sheet
        :returns: key name <-> type array if succeed, otherwise None

        """

        keys = sheet.row_values(self.conf["key_row_index"])
        types = sheet.row_values(self.conf["type_row_index"])
        briefs = sheet.row_values(self.conf["brief_row_index"])

        if len(keys) != len(types):
            print("Error: Key count doesn't equal to type count!")
            return None

        # Validate key types
        for i in range(0, len(keys)):
            if types[i] not in VALID_KEY_TYPES:
                print("Error: Unknown key type: %s, must be one of: %s" % (types[i], VALID_KEY_TYPES))
                return None

        return list(zip(keys, types, briefs))

    def parse_content(self, keys, sheet):
        """ parse content from file data

        :keys: data keys
        :sheet: the sheet
        :returns: content array if succeed, otherwise None

        """
        results = []
        for row_idx in range(self.conf["header_row_count"], sheet.nrows):
            array = []
            contents = sheet.row_values(row_idx)
            content_len = len(contents)
            for i in range(0, len(keys)):
                if i < content_len:
                    value = contents[i]
                    try:
                        if keys[i][1] == "int":
                            new_value = int(value == "" and "0" or value)
                        elif keys[i][1] == "float":
                            new_value = float(value == "" and "0" or value)
                        elif keys[i][1] == "string":
                            new_value = ('%s' % value)
                        else:
                            print("Error: Unhandled value type: " + keys[i][1])
                            return None
                    except ValueError as e:
                        print(
                            "Error: Content parse failed, value_type: %s, value: %s, row: %s, col: %s, message: %s" % (
                                keys[i][1], value, row_idx + 1, i + 1, e))
                        return None
                else:  # insert default value
                    if keys[i][1] == "int":
                        new_value = 0
                    elif keys[i][1] == "float":
                        new_value = 0
                    elif keys[i][1] == "string":
                        new_value = ""
                    else:
                        print("Error: Unhandled value type: " + keys[i][1])
                        return None
                array.append(new_value)
            results.append(array)
        return results

    def parse_indexes(self, keys, values, indexers):
        """generate indexer from keys and values.

        :keys: keys
        :values: values
        :indexers: indexers
        :returns: index content if succeed, otherwise None.

        """
        ret = {}
        for item in indexers:
            ret_1 = self.parse_index(keys, values, item)
            if not ret_1:
                return None
            ret['-'.join(item)] = ret_1

        return ret

    @staticmethod
    def parse_index(keys, values, indexer):
        key_idxs = []
        for key in indexer:
            # check key index
            found = None
            key_idx = 0
            for idx in range(len(keys)):
                if keys[idx][0] == key:
                    key_idx = idx
                    found = True
                    break
            if not found:
                print("Error: Generate indexer failed, cannot find key: " + key)
                return None
            if keys[key_idx][1] != "int" and keys[key_idx][1] != "string":
                print("Error: Only one of types ('int' or 'string') can be use as key: " + keys[key_idx][1])
                return None
            key_idxs.append(key_idx)

        # filter value from 'values' by keys
        ret = {}
        for item_idx in range(len(values)):
            key_values = ['%s' % values[item_idx][idx] for idx in key_idxs]
            key_values_hash = '-'.join(key_values)

            if not ret.__contains__(key_values_hash):
                ret[key_values_hash] = []
            ret[key_values_hash].append(item_idx)

        return ret

    def filter_data(self, sheet, keys, contents, filter_re):
        """ filter data by regex 'filter_re'

        :sheet: sheet to read from
        :keys: keys
        :contents: contents
        :filter_re: filter regex
        :returns: new keys and contents / None
        """
        try:
            pattern = re.compile(filter_re)
        except Exception:
            print("regex compile error: %s" % filter_re)
            return None

        filters = sheet.row_values(self.conf["filter_row_index"])

        # calculate valid columns.
        valid_cols = list(filter(lambda col: pattern.match(filters[col]), [t[0] for t in enumerate(keys)]))

        # filter keys
        new_keys = [keys[i] for i in valid_cols]

        # filter contents
        new_contents = [[content[i] for i in valid_cols] for content in contents]

        return new_keys, new_contents
