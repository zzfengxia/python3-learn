import db_connect

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
newlink_pf_db_name_sql = """
    SELECT
        t.`SCHEMA_NAME` 
    FROM
        information_schema.`SCHEMATA` t 
    WHERE
        SUBSTR( t.`SCHEMA_NAME`, 1, 10 ) = 'ai_center'
"""


def select_from_tenant(sql, db_name, res_column=False):
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
        # 获取字段名列表
        column_names = [column[0] for column in cursor.description]
        res = {'column_name': column_names}
        # 使用 fetchone() 方法获取一条数据
        data = cursor.fetchall()
        res['data'] = data
        # 关闭数据库连接
        cursor.close()
        db.close()
        if not res_column:
            return data
        return res
    except Exception as e:
        print("SQL 查询异常  ", e)
        return


def executor_from_tenant(sql, db_name):
    """
    在指定库执行增删改,DDL
    :return:
    """
    # 打开数据库连接  url,username,password,database
    db = db_connect.DataBaseService(db_config, prefix).get_connect(db_name)
    if db is None:
        return
    try:
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        # 支持多条insert语句，使用“;”分割
        row_num = cursor.execute(sql)
        # 更新操作需要提交事务
        db.commit()

        # 关闭数据库连接
        cursor.close()
        db.close()
        return row_num
    except Exception as e:
        # 发生错误时回滚
        db.rollback()
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
    if result_set is None:
        return
    data = result_set['data']
    if data is None or len(data) == 0:
        return
    # 打印字段名
    column_names = result_set['column_name']
    for column_name in column_names:
        print(f"{column_name:<40}", end="")
    print()
    # 打印结果集
    for row in data:
        for value in row:
            if value is None:
                print(f"{'':<40}", end="")
            else:
                print(f"{value:<40}", end="")
    print()


def select(sql, db_list):
    """
    查询
    :return:
    """
    for db_name in db_list:
        print("-" * 45, db_name, "-" * 45)
        data = select_from_tenant(sql, db_name, True)
        if data is not None:
            print_result(data)
        print("-" * (92 + len(db_name)))
        print("\n\n")


def update(sql, db_list):
    """
    更新
    :return:
    """

    for db_name in db_list:
        print("-" * 45, db_name, "-" * 45)
        upt_lines = sql.splitlines()
        for line in upt_lines:
            line = line.strip()
            if line and line != '':
                row_num = executor_from_tenant(line, db_name)
                if row_num is not None:
                    print(f"更新行数：${row_num}")
        print("-" * 100)
        print("\n\n")

def create(sql, db_list):
    """
    更新
    :return:
    """

    for db_name in db_list:
        print("-" * 45, db_name, "-" * 45)
        line = sql.strip()
        if line and line != '':
            row_num = executor_from_tenant(line, db_name)
            if row_num is not None:
                print(f"更新行数：${row_num}")
        print("-" * 100)
        print("\n\n")

db_config = 'D:\\qiyu-work\\mysql_connect_conf.yaml'
prefix = 'newlink_uat'
database_prefix = 'newlink'
# prefix = 'local'

# 查询普通租户
newlink_db_name_sql = f"""
    SELECT
        t.`SCHEMA_NAME`
    FROM
        information_schema.`SCHEMATA` t 
    WHERE
        SUBSTR( t.`SCHEMA_NAME`, 1, {len(database_prefix)} ) = '{database_prefix}' 
        AND SUBSTR( t.`SCHEMA_NAME`, 1, {len(database_prefix) + 1} ) != '{database_prefix}_' 
"""

if __name__ == '__main__':
    query_sql = """
    #
    #         """
    # # upt_sql = "update le_live_report_custom_field set field_desc = '在统计时间内，新增关注数-取消关注数' where field_code = 'sph_fans_add_num'"
    upt_sql = """
        ALTER TABLE `sph_video` DROP INDEX `idx_video_id`, ADD UNIQUE INDEX `idx_video_id`(`tenant_id`, `video_id`, `is_deleted`) USING BTREE
        ALTER TABLE `sph_account` DROP INDEX `idx_nick_name`, ADD INDEX `idx_nick_name`(`nick_name`) USING BTREE
        """
    # # # newlink_db_name_sql
    db_list = get_db_list(newlink_db_name_sql)
    update(upt_sql, db_list)
    #create(upt_sql, db_list)
    # select(query_sql, db_list)
