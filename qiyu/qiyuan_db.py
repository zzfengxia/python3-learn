import db_connect

# 查询普通租户
qiyuan_db_name_sql = """
    SELECT
        t.`SCHEMA_NAME`
    FROM
        information_schema.`SCHEMATA` t 
    WHERE
        SUBSTR( t.`SCHEMA_NAME`, 1, 6 ) = 'qiyuan' 
        AND SUBSTR( t.`SCHEMA_NAME`, 1, 7 ) != 'qiyuan_'
"""

# 查询服务商租户
qiyuan_sp_db_name_sql = """
    SELECT
        t.`SCHEMA_NAME` 
    FROM
        information_schema.`SCHEMATA` t 
    WHERE
        SUBSTR( t.`SCHEMA_NAME`, 1, 9 ) = 'qiyuan_sp'
"""

# 查询平台库
qiyuan_pf_db_name_sql = """
    SELECT
        t.`SCHEMA_NAME` 
    FROM
        information_schema.`SCHEMATA` t 
    WHERE
        SUBSTR( t.`SCHEMA_NAME`, 1, 9 ) = 'qiyuan_pf'
"""


def select_from_tenant(sql, db_name):
    """
    在指定库执行查询
    :return:
    """
    try:
        # 打开数据库连接  url,username,password,database
        db = db_connect.DataBaseService(db_config, prefix).get_connect(db_name)
        if db is None:
            return

        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        cursor.execute(sql)
        # 使用 fetchone() 方法获取一条数据
        data = cursor.fetchall()

        # 关闭数据库连接
        cursor.close()
        db.close()
    except Exception as e:
        print("SQL 查询异常  ", e)

    return data


def executor_from_tenant(sql, db_name):
    """
    在指定库执行增删改,DDL
    :return:
    """
    try:
        # 打开数据库连接  url,username,password,database
        db = db_connect.DataBaseService(db_config, prefix).get_connect(db_name)
        if db is None:
            return

        # 使用cursor()方法获取操作游标
        cursor = db.cursor()

        cursor.execute(sql)
        # 更新操作需要提交事务
        db.commit()
        # 关闭数据库连接
        cursor.close()
        db.close()
    except Exception as e:
        print("SQL执行异常   ", e)


def get_db_list(db_sql):
    """
    查询租户的数据库
    :return:
    """

    db_name = "information_schema"
    db_list = []
    data = select_from_tenant(db_sql, db_name)
    for inx, item in enumerate(data):
        db_list.append(str(item[0]))
    # print("------------------------------------------")
    return db_list


def print_result(result_set):
    """
    打印查询结果
    :return:
    """
    for row in result_set:
        print(row)


def select(sql, db_list):
    """
    查询
    :return:
    """
    for db_name in db_list:
        print("-" * 45, db_name, "-" * 45)
        data = select_from_tenant(sql, db_name)
        print_result(data)
        print("-" * 100)
        print("\n\n")


def update(sql, db_list):
    """
    更新
    :return:
    """

    for db_name in db_list:
        print("-" * 45, db_name, "-" * 45)
        executor_from_tenant(sql, db_name)
        print("-" * 100)
        print("\n\n")

db_config = 'D:\\qiyu-work\\mysql_connect_conf.yaml'
prefix = 'newlink_uat'

if __name__ == '__main__':
    sql = "select * from dy_account  where id = 1"
    # qiyuan_db_name_sql
    # qiyuan_sp_db_name_sql
    # qiyuan_pf_db_name_sql

    db_list = get_db_list(qiyuan_db_name_sql)
    #select(sql, db_list)
    select(sql, db_list)
