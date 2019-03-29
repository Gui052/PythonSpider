import pymysql
import re

def insert_to_database(db,lists,sql):
    '''
    插入数据库
    :param db: 链接实例
    :param lists:数据列表，二维
    :param sql: sql语句
    :return:
    '''
    cursor = db.cursor()
    try:
        cursor.executemany(sql,lists)
        # print(cursor.rowcount) # 输出实际插入数量
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()

def select_from_database(db,sql):
    '''
    选择数据
    :param db: 链接实例
    :param sql: sql语句
    :return:
    '''
    cursor=db.cursor()
    cursor.execute(sql)
    return cursor.fetchall()

def connectDB(profile):
    '''
    链接数据库
    :param profile: 配置信息
    :return:连接实例
    '''
    db = pymysql.connect(host=profile['host'], port=profile['port'],
                         user=profile['user'], passwd=profile['passwd'],
                         db=profile['database'], charset='utf8')
    return db


if __name__ == '__main__':
    profile = {
        "host":"127.0.0.1",
        "port":3306,
        "user":"lan",
        "passwd":"lanlan123",
        "database":"opot"
    }

    xuxun = {
        "host": "101.200.41.95",
        "port": 3306,
        "user": "lan",
        "passwd": "lanlan123",
        "database": "opot"
    }

    db = connectDB(profile)

    webdb = connectDB(xuxun)

    all_data = 58860
    index = 0
    interval = 1000
    while index <= all_data:

        addcount = 1000
        if all_data-index<addcount:
            addcount = all_data-index

        select_sql = "select * from shijuan_tm limit {0},{1}".format(index, addcount)

        data_list = select_from_database(webdb,select_sql)

        if len(data_list) == 0:
            break

        output_list = []

        for i in data_list:
            temp_list = []
            for k in i:
                temp_list.append(k)

            output_list.append(temp_list)

        # insert
        insert_sql = "insert into shijuan_tm values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        insert_to_database(db,output_list,insert_sql)

        index = index + interval # 递进

        print("doing:" + str(index))
