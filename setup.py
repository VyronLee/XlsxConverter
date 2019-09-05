#!/usr/bin/env python
#-*- coding: utf-8 -*-

#------------------------------------------------------------
#       @file  setup.py
#      @brief  setup script.
#
#     @author  VyronLee, lwz_jz@hotmail.com
#
#   @internal
#    Modified  2019-08-28 23:53
#   Copyright  Copyright (c) 2019, VyronLee
#============================================================

from setuptools import setup, find_packages
setup(
    name = "XlsxConverter",
    version = "1.0.0",
    packages = find_packages(),

    install_requires = ['xlrd>=1.0.0', 'protobuf>=3.9.1'],

    author = "VyronLee",
    author_email = "lwz_jz@hotmail.com",
    description = "A set of tools for converting xls/xlsx file to multiple format, such as json, lua, protobuf, etc.",
    license = "Apache 2.0",
    keywords = ["xls","xlsx","json","lua","protobuf"],
    url = "https://github.com/VyronLee/XlsxConverter"
)
