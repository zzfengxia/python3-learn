#!/usr/bin/env python3
# coding  : utf-8
# @author : Francis.zz
# @date   : 2020-09-11 14:48
# @desc   : 批量删除Kibana索引模式

import json
import urllib.request as req_lib

get_id_url = 'http://172.16.80.127:5601/api/saved_objects/?type=index-pattern&per_page=10000'
delete_index_url = 'http://172.16.80.127:5601/api/saved_objects/index-pattern/'
kibana_version = '6.2.4'

req = req_lib.Request(get_id_url)
req.add_header('kbn-version', kibana_version)
req.add_header('User-Agent', 'python_script')
res = req_lib.urlopen(req)

# parse json data
saved_objects = json.loads(res.read())['saved_objects']
delete_size = 0
for objs in saved_objects:
    index_id = (objs['id'])
    print("开始删除index pattern id:", index_id)
    delete_req = req_lib.Request(delete_index_url + index_id)
    delete_req.add_header('kbn-version', kibana_version)
    delete_req.add_header('User-Agent', 'python_script')
    delete_req.get_method = lambda: 'DELETE'
    try:
        req_lib.urlopen(delete_req).read()
        delete_size += 1
    except BaseException as e:
        print("删除失败，索引:%s" % index_id, e)
        continue

print(f'成功删除 {delete_size} 条索引模式数据')
if __name__ == '__main__':
    pass
