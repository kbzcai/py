#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymysql

from flask import Flask

app = Flask(__name__)


@app.route('/data')
def index():
    data_list = {}
    # 连接数据库
    db = pymysql.connect(host="localhost", user="root", password="123456", database="mes")
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # SQL 查询语句
    sql = "SELECT * FROM mes_primary_produce_plan"
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        for row in results:
            productNo = row[1]
            planNo = row[3]
            planNum = row[6]
            # 打印结果
            print("productNo=%s,planNo=%s,planNum=%d" % \
                  (productNo, planNo, planNum))
        return "获取"
    except:
        print("Error: unable to fetch data")
        return "未获取"
    # 关闭数据库连接
    db.close()


if __name__ == '__main__':
    app.run(host="192.168.1.62", port=5000)
