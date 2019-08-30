#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------------------
#       @file  json_dumper.py
#      @brief  Dumper data as protobuf format.
#
#     @author  VyronLee, lwz_jz@hotmail.com
#   @Modified  2019-09-30 17:36
#  @Copyright  Copyright (c) 2019, VyronLee
# ============================================================
import shutil
import os
import sys
import importlib.util

from google.protobuf import json_format

from ..dumper import Dumper

TEMP_PROTO_DIR = "./temp_proto"
TEMP_PYTHON_PROTO_DIR = "./temp_py_proto"

TEMP_DATA_PROTO_NAME = "data.proto"
TEMP_INDEX_PROTO_NAME = "index.proto"

PY_FILE_DIR = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_DATA_PROTO_PATH = PY_FILE_DIR + "/template_data.proto"
TEMPLATE_INDEX_PROTO_PATH = PY_FILE_DIR + "/template_index.proto"

PROTOC_EXE = "%s/../../bin/%s/protoc" % (PY_FILE_DIR, sys.platform)

PB_VALUE_TYPE_MAP = {
    "int": "int32",
    "float": "float",
    "string": "string",
}


class ProtoBufDumper(Dumper):

    def dump(self, file_path, sheet_name, output_dir, keys, contents, indexes, options):
        # prepare for generating binary data
        temp_data_proto_path, temp_index_proto_path = self.generate_proto(
            "",
            "",
            TEMP_PROTO_DIR,
            TEMP_DATA_PROTO_NAME,
            TEMP_INDEX_PROTO_NAME,
            keys
        )

        # generate data binary
        ret = self.generate_codes(temp_data_proto_path, TEMP_PYTHON_PROTO_DIR)
        if not ret:
            return False

        ret = self.save_data_binary(output_dir, file_path, sheet_name, keys, contents)
        if not ret:
            return False

        # generate index binary
        ret = self.generate_codes(temp_index_proto_path, TEMP_PYTHON_PROTO_DIR)
        if not ret:
            return False

        ret = self.save_index_binary(output_dir, file_path, sheet_name, indexes)
        if not ret:
            return False

        return True

    @staticmethod
    def generate_proto(file_name, sheet_name, output_dir, data_proto_name, index_proto_name, keys):
        message_body = ""
        for i in range(0, len(keys)):
            message_body += "\n\t%s %s = %s;" % (PB_VALUE_TYPE_MAP[keys[i][1]], keys[i][0], i + 1)

        os.makedirs(os.path.abspath(output_dir), exist_ok=True)

        dst_data_proto_path = output_dir + "/" + data_proto_name
        dst_index_proto_path = output_dir + "/" + index_proto_name

        shutil.copyfile(TEMPLATE_DATA_PROTO_PATH, dst_data_proto_path)
        shutil.copyfile(TEMPLATE_INDEX_PROTO_PATH, dst_index_proto_path)

        with open(dst_data_proto_path, "rt") as fp:
            content = fp.read()
            content = content.replace("__XLSX_FILENAME__", file_name)
            content = content.replace("__XLSX_SHEETNAME__", sheet_name)
            content = content.replace("__MESSAGE_BODY__", message_body)
            fp.close()

        with open(dst_data_proto_path, "wt") as fp:
            fp.write(content)
            fp.close()

        return dst_data_proto_path, dst_index_proto_path

    @staticmethod
    def generate_codes(proto_path, out_dir):
        os.makedirs(os.path.abspath(out_dir), exist_ok=True)

        cmd = "%s -I%s --python_out=%s %s" % (PROTOC_EXE, TEMP_PROTO_DIR, out_dir, proto_path)

        try:
            os.system(cmd)
        except Exception as e:
            print("Error: execute cmd failed: %s", e)
            return False

        return True

    def save_data_binary(self, output_dir, file_path, sheet_name, keys, contents):
        pb_module = self.load_module("%s/data_pb2.py" % TEMP_PYTHON_PROTO_DIR)

        data = [{keys[i][0]: content[i] for i in range(0, len(content))} for content in contents]
        sheet = pb_module.Sheet()
        for val in data:
            record = pb_module.Record()
            json_format.ParseDict(val, record)
            sheet.data.append(record)
        serialized_data = sheet.SerializeToString()

        os.makedirs(output_dir, exist_ok=True)
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        output_file_path = "%s/%s_%s.dat.pb" % (output_dir, file_name, sheet_name)
        with open(output_file_path, "wb") as of:
            of.write(serialized_data)

        return True

    def save_index_binary(self, output_dir, file_path, sheet_name, indexes):
        pb_module = self.load_module("%s/index_pb2.py" % TEMP_PYTHON_PROTO_DIR)

        indexes_dict = pb_module.XlsxRecordIndexesDict()
        for k1 in indexes:
            group_index_dict = indexes_dict.values[k1]
            for k2 in indexes[k1]:
                record_ids = group_index_dict.values[k2]
                for record_id in indexes[k1][k2]:
                    record_ids.values.append(record_id)
        serialized_data = indexes_dict.SerializeToString()

        os.makedirs(output_dir, exist_ok=True)
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        output_file_path = "%s/%s_%s.idx.pb" % (output_dir, file_name, sheet_name)
        with open(output_file_path, "wb") as of:
            of.write(serialized_data)

        return True

    @staticmethod
    def load_module(py_path, module_name="None"):
        spec = importlib.util.spec_from_file_location(module_name, py_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
