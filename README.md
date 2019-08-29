xls2json
=======

一个用于把 xls/xlsx 文件转换成 Json 文件的工具。

QuickLook
=========

生成的 Json 文件样式:

```json
{
    "data": [
        {
            "id": 1,
            "hp": 100,
            "mp": 50,
            "attack": 10,
            "defend": 10
        },
        {
            "id": 2,
            "hp": 80,
            "mp": 200,
            "attack": 12,
            "defend": 8
        },
        {
            "id": 3,
            "hp": 80,
            "mp": 100,
            "attack": 15,
            "defend": 5
        }
    ],
    "index": {
        "id": {
            "1": [
                1
            ],
            "2": [
                2
            ],
            "3": [
                3
            ]
        }
    }
}
```

data 部分为表格数据存储；index 部分为快速索引存储，可用于快速查询数据。



Installation
============

``` shell
git clone https://github.com/VyronLee/xls2json.git
cd xls2json
pip install -e .
```



Usage
=====

一个简单的使用方式:

``` python
conf = {                        # header config.
    "header_row_count": 4,
    "key_row_index":    0,
    "type_row_index":   1,
    "filter_row_index": 2,
    "brief_row_index":  3,
}
ip = "./input/ActorConf.xlsx"    # input file path.
op = "./output/ActorConf.json"   # output file path.
re = ".*c+"                      # just filter out cols contains 'c'
idx = [["id"]]                   # indexer list.

xls2json.convert(conf=conf, ip=ip, op=op, filter_re=re, indexers=idx)
```

可查看 test 用例获得更详细的用法。

Feature
=============

使用该工具生成的 Json 配置表具有以下特点：

* 数据索引快速

  该工具生成 Json 文件时要求用户提供一个“索引字段列表”，工具会根据设定的索引字段预先生成 key-values 映射关系，大大减小数据索引的时间复杂度。而且索引字段支持单个键值索引或者多个键值索引，键值不设个数限制，可根据实际需求进行配置。

* 可根据输入进行配置列过滤

  该工具可供用户输入一个“配置列过滤正则表达式”，只有符合表达式的列数据才会实际生成到 Json 文件中。该功能在客户端与服务端使用同一套配置表时会十分方便，仅仅输出实际需要的字段，避免数据冗余。

Test
====

测试用例执行流程：

``` bash
cd test
pip install -e ..
python test1.py
python test2.py
```

可自行调整 input 里的 xlsx 文件，进行需要的数据测试。


License
=======

Apache License 2.0.

