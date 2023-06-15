import pymysql
import yaml
import os


class DataBaseService(object):
    def __init__(self, cfg_file, prefix='local'):
        self.host = ''
        self.port = ''
        self.user_name = ''
        self.password = ''
        self.init_config(cfg_file, prefix)

    def init_config(self, cfg_file, prefix='local'):
        with open(cfg_file) as f:
            config_data = yaml.safe_load(f)
            db_conf = config_data[prefix]
            if db_conf is not None:
                self.host = db_conf['host']
                self.port = db_conf['port']
                self.user_name = db_conf['user-name']
                self.password = db_conf['password']

    def get_connect(self, db_name):
        if not self.connect_test():
            return None
        # 建立数据库连接
        conn = pymysql.connect(host=str(self.host), port=int(self.port),
                               user=self.user_name, password=str(self.password), db=db_name)
        return conn

    def connect_test(self):
        """
        测试连接，python方法如果以test开头，默认为是一个测试用例
        :return:
        """
        try:
            # 建立数据库连接
            conn = pymysql.connect(host=str(self.host), port=int(self.port),
                                   user=self.user_name, password=str(self.password), db='mysql')
            # 创建游标对象
            cursor = conn.cursor()
            # 执行SQL查询
            cursor.execute("SELECT * FROM user")
            # 获取查询结果
            results = cursor.fetchall()

            # 处理查询结果
            # for row in results:
            # 对每一行数据进行处理
            # print(row)
            # 关闭游标
            cursor.close()
            # 关闭数据库连接
            conn.close()
            # print("连接成功")
            return True
        except pymysql.err.MySQLError as e:
            print('连接失败', e)
            return False


if __name__ == '__main__':
    db_conn = DataBaseService('D:\\qiyu-work\\mysql_connect_conf.yaml')
    conn = db_conn.get_connect()
