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
import importlib

from google.protobuf import json_format

from ..dumper import Dumper

TEMP_PROTO_DIR = "./temp_proto"
TEMP_PYTHON_PROTO_DIR = "./temp_py_proto"

sys.path.append(TEMP_PYTHON_PROTO_DIR)

INDEX_PROTO_NAME = "XlsxRecordIndex.proto"

PY_FILE_DIR = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_DATA_PROTO_PATH = PY_FILE_DIR + "/template_data.proto"
TEMPLATE_INDEX_PROTO_PATH = PY_FILE_DIR + "/template_index.proto"

PROTOC_EXE = "%s/../../bin/%s/protoc" % (PY_FILE_DIR, sys.platform)

PB_VALUE_TYPE_MAP = {
    "int": "int32",
    "float": "float",
    "string": "string",
}

OPTIONS_CODE_TYPE_TO_ARGS = {
    "cpp": "cpp_out",
    "csharp": "csharp_out",
    "java": "java_out",
    "js": "js_out",
    "objc": "objc_out",
    "php": "php_out",
    "python": "python_out",
    "ruby": "ruby_out",
}


def import_or_reload(module_name, *names):
    import sys

    if module_name in sys.modules:
        return importlib.reload(sys.modules[module_name])
    else:
        return __import__(module_name, fromlist=names)


def get_class_by_name(name, module):
    if module:
        return getattr(module, name)
    else:
        return getattr(sys.modules[__name__], name)


class ProtoBufDumper(Dumper):

    def dump(self, file_path, sheet_name, output_dir, keys, contents, indexes, options):
        # shutil.rmtree(TEMP_PROTO_DIR, ignore_errors=True)
        # shutil.rmtree(TEMP_PYTHON_PROTO_DIR, ignore_errors=True)

        ret = self.generate_binary_data(file_path, sheet_name, output_dir, keys, contents, indexes, options)
        if not ret:
            return False

        if options is None:
            return True

        if "generate_codes" in options and options["generate_codes"]:
            ret = self.generate_source_codes(file_path, sheet_name, output_dir, keys, contents, indexes, options)
            if not ret:
                return False

        return True

    def generate_binary_data(self, file_path, sheet_name, output_dir, keys, contents, indexes, options):
        filename = os.path.splitext(os.path.basename(file_path))[0]

        # prepare for generating binary data
        temp_data_proto_path, temp_index_proto_path = self.generate_proto(
            filename,
            sheet_name,
            TEMP_PROTO_DIR,
            "%s_%s.proto" % (filename, sheet_name),
            INDEX_PROTO_NAME,
            keys
        )

        # generate data binary
        ret = self.generate_codes(temp_data_proto_path, TEMP_PYTHON_PROTO_DIR, "python_out")
        if not ret:
            return False

        ret = self.save_data_binary(output_dir, filename, sheet_name, keys, contents)
        if not ret:
            return False

        # generate index binary
        ret = self.generate_codes(temp_index_proto_path, TEMP_PYTHON_PROTO_DIR, "python_out")
        if not ret:
            return False

        ret = self.save_index_binary(output_dir, filename, sheet_name, indexes)
        if not ret:
            return False

        return True

    def generate_source_codes(self, file_path, sheet_name, output_dir, keys, contents, indexes, options):
        filename = os.path.splitext(os.path.basename(file_path))[0]

        # prepare for generating binary data
        temp_data_proto_path, temp_index_proto_path = self.generate_proto(
            filename,
            sheet_name,
            TEMP_PROTO_DIR,
            "%s_%s.proto" % (filename, sheet_name),
            INDEX_PROTO_NAME,
            keys
        )

        # generate data binary
        if "codes_type" not in options:
            raise Exception("Codes type must be specified in options")

        if options["codes_type"] not in OPTIONS_CODE_TYPE_TO_ARGS:
            raise Exception("Unsupported code type: " + options["codes_type"])

        ret = self.generate_codes(temp_data_proto_path, output_dir, OPTIONS_CODE_TYPE_TO_ARGS[options["codes_type"]])
        if not ret:
            return False

        ret = self.generate_codes(temp_index_proto_path, output_dir, OPTIONS_CODE_TYPE_TO_ARGS[options["codes_type"]])
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
    def generate_codes(proto_path, out_dir, pb_out_args):
        os.makedirs(os.path.abspath(out_dir), exist_ok=True)

        cmd = "%s -I%s --%s=%s %s" % (PROTOC_EXE, TEMP_PROTO_DIR, pb_out_args, out_dir, proto_path)

        try:
            os.system(cmd)
        except Exception as e:
            print("Error: execute cmd failed: %s", e)
            return False

        return True

    @staticmethod
    def save_data_binary(output_dir, file_name, sheet_name, keys, contents):
        pb_module = import_or_reload("%s_%s_pb2" % (file_name, sheet_name))

        data = [{keys[i][0]: content[i] for i in range(0, len(content))} for content in contents]
        sheet = get_class_by_name("%s_%s_Sheet" % (file_name, sheet_name), pb_module)()
        for val in data:
            record = get_class_by_name("%s_%s_Record" % (file_name, sheet_name), pb_module)()
            json_format.ParseDict(val, record)
            sheet.data.append(record)
        serialized_data = sheet.SerializeToString()

        os.makedirs(output_dir, exist_ok=True)
        output_file_path = "%s/%s_%s.dat.pb" % (output_dir, file_name, sheet_name)
        with open(output_file_path, "wb") as of:
            of.write(serialized_data)

        return True

    @staticmethod
    def save_index_binary(output_dir, file_name, sheet_name, indexes):
        pb_module = import_or_reload("%s_pb2" % os.path.splitext(INDEX_PROTO_NAME)[0])

        indexes_dict = pb_module.XlsxRecordIndexesDict()
        for k1 in indexes:
            group_index_dict = indexes_dict.values[k1]
            for k2 in indexes[k1]:
                record_ids = group_index_dict.values[k2]
                for record_id in indexes[k1][k2]:
                    record_ids.values.append(record_id)
        serialized_data = indexes_dict.SerializeToString()

        os.makedirs(output_dir, exist_ok=True)
        output_file_path = "%s/%s_%s.idx.pb" % (output_dir, file_name, sheet_name)
        with open(output_file_path, "wb") as of:
            of.write(serialized_data)

        return True
