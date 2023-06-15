import csv
import re

"""
markdown表格格式的API请求响应说明文档转为java实体类
"""


class ApiTableToEntity(object):
    def __init__(self, file_path):
        self.file_name = file_path

    # 转为包装类型，首字母大写
    def __to_type(self, ori):
        if ori:
            ori = ori[:ori.index('(')]
            return ori[0].upper() + ori[1:]

    def __deal_var_name(self, ori_str):
        return ori_str

    def parse_data(self, params):
        skit_line = params[0]
        var_index = params[1]
        type_index = params[2]
        remarks = params[3]
        max_size = params[4]

        data = []
        ori_line_size = 0
        with open(self.file_name, 'r') as file:
            reader = csv.reader(file, delimiter='|')
            for line in reader:
                if not line or not line[0].strip():
                    continue
                ori_line_size += 1
                line = [cell.strip() for cell in line[1:-1]]
                if len(line) != max_size:
                    print(f"解析失败的行：{line}")
                    continue
                data.append(line)

        parse_size = 0
        for i in range(len(data)):
            if i < skit_line:
                continue
            line_data = data[i]
            var_name = self.__deal_var_name(line_data[var_index])
            print("/**")
            for remark in remarks:
                remark_str = remark.assembly_msg(line_data)
                if remark_str:
                    print(f"* {remark_str}")
            print("*/")
            print(f"private {self.__to_type(line_data[type_index])} {var_name};")
            print()
            parse_size += 1

        print(f"数据总行数：{ori_line_size}, 解析属性数量：{parse_size}")


class Remark:
    def __init__(self, index, prefix):
        self.index = index
        self.prefix = prefix

    def assembly_msg(self, line):
        if len(line) >= self.index:
            value = line[self.index]
            if value:
                return f"{self.prefix}{value}" if self.prefix else value
        return None


if __name__ == '__main__':
    # 参数
    """
    1：跳过行数
    2：变量名索引
    3：类型索引
    4：备注索引，可以是个数组
    5: 数据行使用“|”切分的数量
    """
    params = [2, 1, 3, [Remark(0, None), Remark(2, "是否必填："), Remark(5, "描述："), Remark(3, "长度：")], 6]
    tool = ApiTableToEntity("D:\\qiyu-work\\文档\\UNIT网站功能API文档-20210621.pdf")
    tool.parse_data(params)
