# 更改数据库字段名

import pymysql
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
        "host":"123.56.28.8",
        "port":3306,
        "user":"lanlan",
        "passwd":"lan123",
        "database":"opotclass"
    }


    db = connectDB(profile)
    cursor = db.cursor()
    all_data = 951
    index = 2
    interval = 1
    while index <= all_data:

        sql = "alter table zsdtable{0} change column timuid md5 varchar(100) NOT NULL;".format(index)
        index = index+interval

        cursor.execute(sql)
        cursor.fetchall()

        print("doing:" + str(index))