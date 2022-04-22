#!/usr/bin/env python3.6
# -*- encoding: utf-8 -*-
# http接口接收产品型号和当班加工数量后下发12个plc，每个工位工序为产品型号➕数字
"""
@Description : 
@File        : PLC_Read_Write(v1.0).py
@Project     : 20200123
@Time        : 2021/3/4 上午9:28
@Author      : 胡贤明
@Software    : PyCharm
"""

import sys
import socket

sys.path.append(r"F:\cyj\pythonproject\py\venv\Lib\site-packages")
import time
from HslCommunication import SiemensS7Net
from HslCommunication import SiemensPLCS
import pymysql
import datetime
from flask import Flask, jsonify, make_response
import threading
from flask_cors import CORS

app = Flask(__name__)
state1 = None


def read_data_plc(plc):
    try:
        data_list = {}
        STYLE = plc.ReadString("DB33.0", 10)
        # 产品型号
        if STYLE.IsSuccess:
            print("读取STYLE成功", STYLE.Content)
            data_list["product_type"] = str(STYLE.Content)
        else:
            print("读取STYLE失败")
            data_list["product_type"] = None
        Device_Status = plc.ReadInt16("DB33.12")
        # 设备状态
        if Device_Status.IsSuccess:
            print("读取Device_Status成功", Device_Status.Content)
            d1 = str(Device_Status.Content)
            d2 = bin(int(d1))
            d3 = d2[2:]
            data_list["r1_equipment_status"] = d3
        else:
            print("读取Device_Status失败")
            data_list["r1_equipment_status"] = None
        Fault_Code = plc.ReadInt16("DB33.14")
        # 错误代码
        if Fault_Code.IsSuccess:
            print("读取Fault_Code成功", Fault_Code.Content)
            data_list["fail_code"] = str(Fault_Code.Content)
        else:
            print("读取Fault_Code失败")
            data_list["fail_code"] = None
        Recerve = plc.ReadInt16("DB33.16")
        # 预留
        if Recerve.IsSuccess:
            print("读取Recvrve成功", Recerve.Content)
            data_list["recerve"] = str(Recerve.Content)
        else:
            print("读取Recvrve失败")
            data_list["recerve"] = None
        countA = plc.ReadInt16("DB33.18")
        # 当前加工数量
        if countA.IsSuccess:
            print("读取countA成功", countA.Content)
            data_list["prod_num"] = countA.Content
        else:
            print("读取countA失败")
            data_list["prod_num"] = None
        R1_JOB = plc.ReadInt16("DB33.20")
        # 机器人1程序号
        if R1_JOB.IsSuccess:
            print("读取R1_JOB成功", R1_JOB.Content)
            data_list["r1_rob_no"] = str(R1_JOB.Content)
        else:
            print("读取R1_JOB失败")
            data_list["r1_rob_no"] = None
        Weld1_Code = plc.ReadInt16("DB33.22")
        # w1焊缝号
        if Weld1_Code.IsSuccess:
            print("读取Weld1_Code成功", Weld1_Code.Content)
            data_list["r1_weld_line_no"] = str(Weld1_Code.Content)
        else:
            print("读取Weld1_Code失败")
            data_list["r1_weld_line_no"] = None
        W1_Current = plc.ReadFloat("DB33.24")
        # w1焊接电流
        if W1_Current.IsSuccess:
            print("读取W1_Current成功", W1_Current.Content)
            data_list["r1_electric"] = str(W1_Current.Content)
        else:
            print("读取W1_Current失败")
            data_list["r1_electric"] = None
        W1_Voltage = plc.ReadFloat("DB33.28")
        # w1焊接电压
        if W1_Voltage.IsSuccess:
            print("读取W1_Voltage成功", W1_Voltage.Content)
            data_list["r1_voltage"] = str(W1_Voltage.Content)
        else:
            print("读取W1_Voltage失败")
            data_list["r1_voltage"] = None
        W1_Speed = plc.ReadFloat("DB33.32")
        # w1焊接速度
        if W1_Speed.IsSuccess:
            print("读取W1_Speed成功", W1_Speed.Content)
            data_list["r1_speed"] = str(W1_Speed.Content)
        else:
            print("读取W1_Speed失败")
            data_list["r1_speed"] = None
        W1_JOB = plc.ReadInt16("DB33.36")
        # w1焊接号
        if W1_JOB.IsSuccess:
            print("读取W1_JOB成功", W1_JOB.Content)
            data_list["r1_job"] = str(W1_JOB.Content)
        else:
            print("读取W1_JOB失败")
            data_list["r1_job"] = None
        R2_JOB = plc.ReadInt16("DB33.38")
        # 机器人2程序号
        if R2_JOB.IsSuccess:
            print("读取R2_JOB成功", R2_JOB.Content)
            data_list["r2_rob_no"] = str(R2_JOB.Content)
        else:
            print("读取R2_JOB失败")
            data_list["r2_rob_no"] = None
        Weld2_Code = plc.ReadInt16("DB33.40")
        # w2焊缝号
        if Weld2_Code.IsSuccess:
            print("读取Weld2_Code成功", Weld2_Code.Content)
            data_list["r2_weld_line_no"] = str(Weld2_Code.Content)
        else:
            print("读取Weld2_Code失败")
            data_list["r2_weld_line_no"] = None
        W2_Current = plc.ReadFloat("DB33.42")
        # w2焊接电流
        if W2_Current.IsSuccess:
            print("读取W2_Current成功", W2_Current.Content)
            data_list["r2_electric"] = str(W2_Current.Content)
        else:
            print("读取W2_Current失败")
            data_list["r2_electric"] = None
        W2_Voltage = plc.ReadFloat("DB33.46")
        # w2焊接电压
        if W2_Voltage.IsSuccess:
            print("读取W2_Voltage成功", W2_Voltage.Content)
            data_list["r2_voltage"] = str(W2_Voltage.Content)
        else:
            print("读取W2_Voltage失败")
            data_list["r2_voltage"] = None
        W2_Speed = plc.ReadFloat("DB33.50")
        # w2焊接速度
        if W2_Speed.IsSuccess:
            print("读取W2_Speed成功", W2_Speed.Content)
            data_list["r2_speed"] = str(W2_Speed.Content)
        else:
            print("读取W2_Speed失败")
            data_list["r2_speed"] = None
        W2_JOB = plc.ReadInt16("DB33.54")
        # w2焊接号
        if W2_JOB.IsSuccess:
            print("读取W2_JOB成功", W2_JOB.Content)
            data_list["r2_job"] = str(W2_JOB.Content)
        else:
            print("读取W2_JOB失败")
            data_list["r2_job"] = None
        Gun_Status = plc.ReadInt16("DB33.56")
        # 焊接状态
        if Gun_Status.IsSuccess:
            print("读取Gun_Status成功", Gun_Status.Content)
            data_list["replace_status"] = str(Gun_Status.Content)
        else:
            print("读取Gun_Status失败")
            data_list["replace_status"] = None
        Part_Status = plc.ReadInt16("DB33.58")
        # 零件状态
        if Part_Status.IsSuccess:
            print("读取Part_Status成功", Part_Status.Content)
            data_list["part_status"] = str(Part_Status.Content)
        else:
            print("读取Part_Status失败")
            data_list["part_status"] = None
        W1_Gas = plc.ReadInt16("DB33.60")
        # 枪1气体用量
        if W1_Gas.IsSuccess:
            print("读取W1_Gas成功", W1_Gas.Content)
            data_list["r1_protective_gas"] = str(W1_Gas.Content)
        else:
            print("读取W1_Gas失败")
            data_list["r1_protective_gas"] = None
        W1_Wire = plc.ReadInt16("DB33.62")
        # 枪1焊丝用量
        if W1_Wire.IsSuccess:
            print("读取W1_Wire成功", W1_Wire.Content)
            data_list["r1_welding_wire"] = str(W1_Wire.Content)
        else:
            print("读取W1_Wire失败")
            data_list["r1_welding_wire"] = None
        W2_Gas = plc.ReadInt16("DB33.64")
        # 枪2气体用量
        if W2_Gas.IsSuccess:
            print("读取W2_Gas成功", W2_Gas.Content)
            data_list["r2_protective_gas"] = str(W2_Gas.Content)
        else:
            print("读取W2_Gas失败")
            data_list["r2_protective_gas"] = None
        W2_Wire = plc.ReadInt16("DB33.66")
        # 枪2焊丝用量
        if W2_Wire.IsSuccess:
            print("读取W2_Wire成功", W2_Wire.Content)
            data_list["r2_welding_wire"] = str(W2_Wire.Content)
        else:
            print("读取W2_Wire失败")
            data_list["r2_welding_wire"] = None
        User_ID = plc.ReadString("DB33.68", 10)
        # 用户ID
        if User_ID.IsSuccess:
            print("读取User_ID成功", User_ID.Content)
            data_list["login_id"] = str(User_ID.Content)
        else:
            print("读取User_ID失败")
            data_list["login_id"] = None
        User_Password = plc.ReadString("DB33.80", 10)
        # 用户密码
        if User_Password.IsSuccess:
            print("读取User_Password成功", User_Password.Content)
            data_list["login_password"] = str(User_Password.Content)
        else:
            print("读取User_Password失败")
            data_list["login_password"] = None

        STYLE2 = plc.ReadString("DB33.92", 10)
        # 产品型号2
        if STYLE2.IsSuccess:
            print("读取STYLE2成功", STYLE2.Content)
            data_list["product_type2"] = str(STYLE2.Content)
        else:
            print("读取STYLE2失败")
            data_list["product_type2"] = None

        countB = plc.ReadInt16("DB33.104")
        # 工作站B工位的生产数量
        if countB.IsSuccess:
            print("读取countB成功", countB.Content)
            data_list["countB"] = str(countB.Content)
        else:
            print("读取countB失败")
            data_list["countB"] = None

        Qualifed = plc.ReadInt16("DB33.106")
        # 合格数量
        if Qualifed.IsSuccess:
            print("读取Qualifed成功", Qualifed.Content)
            data_list["Qualifed"] = str(Qualifed.Content)
        else:
            print("读取Qualifed失败")
            data_list["Qualifed"] = None
        Unaccepted = plc.ReadInt16("DB33.108")
        # 手工焊补数量
        if Unaccepted.IsSuccess:
            print("读取Unaccepted成功", Unaccepted.Content)
            data_list["Unaccepted"] = str(Unaccepted.Content)
        else:
            print("读取Unaccepted失败")
            data_list["Unaccepted"] = None
        Switch = plc.ReadInt16("DB33.110")
        # 切换产线（1是切换产线）
        if Switch.IsSuccess:
            print("读取Switch成功", Switch.Content)
            data_list["Switch"] = str(Switch.Content)
        else:
            print("读取Switch失败")
            data_list["Switch"] = None
        # logging.info("从plc读取的数据：%s", str(data_list))
        return data_list

    except Exception as ex:
        print("读取插入数据库失败错误", ex)
        # logging.error("从plc读取数据库失败错误: %s", ex)


class ReadS71200(object):
    state1 = [0, 0, 0, 0, 0, 0]

    def __init__(self, ip, user, password, db_name):
        db = pymysql.connect(host="localhost", user="root", password="123456", database="mes")
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        # SQL 查询语句
        try:
            self.db = db
            self.cursor = cursor
            # = logging.info("数据库连接成功！")
            print("数据库连接成功！")
        except Exception as ex:
            # logging.error("数据库连接错误：%s",ex )
            print(ex)

    def insertData(self, tablename, *key, **kwargs):  # *key返回的是元组(),**返回的是字典
        try:
            values = []
            for value in kwargs.values():
                values.append(value)
            # print(tuple(values))
            # logging.info(tuple(values))
            sql = 'insert into {} {}'.format(tablename, key).replace("'", "") + ' VALUES {}'.format(tuple(values))
            # print(sql)

            self.cursor.execute(sql)
            self.db.commit()
            # logging.info("成功添加数据")
            print("成功添加数据")
            # print("插入数据的ID：", self.cursor.lastrowid)
        except Exception as e:
            # logging.error("插入数据库错误：%s", e)
            print(e)
            # 发生错误时候回滚
            self.db.rollback()

    def plc_connect(self, plc_ip1, plc_ip2, plc_ip3, plc_ip4, plc_ip5, plc_ip6):
        try:
            global siemens1, siemens2, siemens3, siemens4, siemens5, siemens6
            if self.state1[0] == 0:
                siemens1 = SiemensS7Net(SiemensPLCS.S1200, plc_ip1)
                if not siemens1.ConnectServer().IsSuccess:
                    print("PLC1连接失败")
                    self.state1[0] = 0
                else:
                    print("PLC1连接成功")
                    self.state1[0] = 1
            if self.state1[1] == 0:
                siemens2 = SiemensS7Net(SiemensPLCS.S1200, plc_ip2)
                if not siemens2.ConnectServer().IsSuccess:
                    print("PLC2连接失败")
                    # logging.info("PLC2连接失败")
                    self.state1[1] = 0
                else:
                    # logging.info("PLC2连接成功")
                    self.state1[1] = 1
                    print("PLC2连接成功")
            if self.state1[2] == 0:
                siemens3 = SiemensS7Net(SiemensPLCS.S1200, plc_ip3)
                if not siemens3.ConnectServer().IsSuccess:
                    print("PLC3连接失败")
                    # logging.info("PLC3连接失败")
                    self.state1[2] = 0
                else:
                    print("PLC3连接成功")
                    # logging.info("PLC3连接成功")
                    self.state1[2] = 1
            if self.state1[3] == 0:
                siemens4 = SiemensS7Net(SiemensPLCS.S1200, plc_ip4)
                if not siemens4.ConnectServer().IsSuccess:
                    print("PLC4连接失败")
                    # logging.info("PLC4连接失败")
                    self.state1[3] = 0
                else:
                    print("PLC4连接成功")
                    # logging.info("PLC4连接成功")
                    self.state1[3] = 1
            if self.state1[4] == 0:
                siemens5 = SiemensS7Net(SiemensPLCS.S1200, plc_ip5)
                if not siemens5.ConnectServer().IsSuccess:
                    print("PLC5连接失败")
                    # logging.info("PLC5连接失败")
                    self.state1[4] = 0
                else:
                    print("PLC5连接成功")
                    # logging.info("PLC5连接成功")
                    self.state1[4] = 1
            if self.state1[5] == 0:
                siemens6 = SiemensS7Net(SiemensPLCS.S1200, plc_ip6)
                if not siemens6.ConnectServer().IsSuccess:
                    print("PLC6连接失败")
                    # logging.info("PLC6连接失败")
                    self.state1[5] = 0
                else:
                    print("PLC6连接成功")
                    # logging.info("PLC6连接成功")
                    self.state1[5] = 1
            print("plc连接状态:", self.state1)
            return self.state1
        except Exception as ex:
            print("连接PLC错误", ex)

    def write_data_plc(self, plc, style, count):
        try:
            STYLE = plc.WriteString("DB34.0", style)
            countA = plc.WriteInt16("DB34.18", count)
            if STYLE.IsSuccess:
                print("产品型号写入成功")
                # logging.info("产品型号写入成功")
            else:
                print("产品型号写入错误：" + STYLE.Message)
                # logging.info("产品型号写入错误：%s", STYLE.Message)
            if countA.IsSuccess:
                print("当班加工数量写入成功")
                # logging.info("当班加工数量写入成功")
            else:
                print("当班加工数量写入错误", countA.Message)
                # logging.info("当班加工数量写入错误：%s", countA.Message)
        except Exception as ex:
            print("写入PLC错误:", ex)

    def insertDataDB(self, plc, table_name):
        data_list = read_data_plc(plc)
        # logging.info(table_name)
        print(table_name)
        try:
            self.insertData(table_name, "product_type", "r1_equipment_status",
                            "fail_code", "prod_num", "r1_rob_no", "r1_weld_line_no", "r1_electric",
                            "r1_voltage", "r1_speed", "r1_job", "r2_rob_no", "r2_weld_line_no",
                            "r2_electric", "r2_voltage", "r2_speed", "r2_job", "replace_status",
                            "r1_protective_gas", "r2_protective_gas", "r1_welding_wire", "r2_welding_wire",
                            "login_id", "login_password", "part_status", "recerve", "create_time", "product_type2",
                            "prod_numB",
                            "qualifed", "unaccepted",
                            # "switch",
                            product_type=data_list["product_type"],
                            r1_equipment_status=data_list["r1_equipment_status"],
                            fail_code=data_list["fail_code"],
                            prod_num=data_list["prod_num"],
                            r1_rob_no=data_list["r1_rob_no"],
                            r1_weld_line_no=data_list["r1_weld_line_no"],
                            r1_electric=data_list["r1_electric"],
                            r1_voltage=data_list["r1_voltage"],
                            r1_speed=data_list["r1_speed"],
                            r1_job=data_list["r1_job"],
                            r2_rob_no=data_list["r2_rob_no"],
                            r2_weld_line_no=data_list["r2_weld_line_no"],
                            r2_electric=data_list["r2_electric"],
                            r2_voltage=data_list["r2_voltage"],
                            r2_speed=data_list["r2_speed"],
                            r2_job=data_list["r2_job"],
                            replace_status=data_list["replace_status"],
                            r1_protective_gas=data_list["r1_protective_gas"],
                            r2_protective_gas=data_list["r2_protective_gas"],
                            r1_welding_wire=data_list["r1_welding_wire"],
                            r2_welding_wire=data_list["r2_welding_wire"],
                            login_id=data_list["login_id"],
                            login_password=data_list["login_password"],
                            part_status=data_list["part_status"],
                            recerve=data_list["recerve"],
                            create_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            product_type2=data_list["product_type2"],
                            prod_numB=data_list["countB"],
                            qualifed=data_list["Qualifed"],
                            unaccepted=data_list["Unaccepted"]
                            # switch=data_list["Switch"]
                            )
        except Exception as ex:
            # logging.info("数据插入数据库错误：%s",ex)
            print("数据插入数据库错误：", ex)

    def main(self):
        if self.state1[0] == 1:
            self.insertDataDB(siemens1, "mes_plc")
        if self.state1[1] == 1:
            self.insertDataDB(siemens2, "mes_plc_r2")
        if self.state1[2] == 1:
            self.insertDataDB(siemens3, "mes_plc_r3")
        if self.state1[3] == 1:
            self.insertDataDB(siemens4, "mes_plc_r4")
        if self.state1[4] == 1:
            self.insertDataDB(siemens5, "mes_plc_r5")
        if self.state1[5] == 1:
            self.insertDataDB(siemens6, "mes_plc_r6")


class UdpSend(object):
    udp_socket = None

    def init(self):
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def udp_send(self, data, ip):
        data = "192.168.1." + ip + data + "END"
        print(data)
        send_data = data.encode("utf-8")
        self.udp_socket.sendto(send_data, ("192.168.1." + ip, 50505))
        recv_data = self.udp_socket.recvfrom(1024)
        print(recv_data)
        return recv_data

    def close(self):
        self.udp_socket.close()


def read_craftplayer(plc):
    playerdata = plc.ReadString("DB33.28", 28)
    if playerdata.IsSuccess:
        playerdatarecv = str(playerdata.Content)
        print("读取playerdata成功", playerdatarecv)
        return playerdatarecv
    else:
        print("读取playerdata失败")
        return None


def plc_read():
    global plc_data
    plc_data = ReadS71200("192.168.1.101", "root", "123456", "mes")
    plc_data.plc_connect("192.168.1.10", "192.168.1.20", "192.168.1.30",
                         "192.168.1.40", "192.168.1.50", "192.168.1.60")
    while True:
        plc_data.main()
        time.sleep(60)


# def read_plc_craftplsyer():
#     global plc_data
#     udp = UdpSend()
#     udp.init()
#     while True:
#         if plc_data.state1[0] == 1:
#             data = read_craftplayer(siemens1)
#             udp.udp_send(data,"192.168.1.15")
#         if plc_data.state1[1] == 1:
#             data = read_craftplayer(siemens2)
#             udp.udp_send(data, "192.168.1.25")
#         if plc_data.state1[2] == 1:
#             data = read_craftplayer(siemens3)
#             udp.udp_send(data, "192.168.1.35")
#         if plc_data.state1[3] == 1:
#             data = read_craftplayer(siemens4)
#             udp.udp_send(data, "192.168.1.45")
#         if plc_data.state1[4] == 1:
#             data = read_craftplayer(siemens5)
#             udp.udp_send(data, "192.168.1.56")
#         if plc_data.state1[5] == 1:
#             data = read_craftplayer(siemens6)
#             udp.udp_send(data, "192.168.1.66")
#         time.sleep(3)


# def web_send_craftplayer(data):
#     try:
#         udp_s = UdpSend()
#         udp_s.init()
#         data = "192.168.1.15" + data + "END"
#         udp_s.udp_send(data, "192.168.1.15")
#         udp_s.udp_send(data, "192.168.1.25")
#         udp_s.udp_send(data, "192.168.1.35")
#         udp_s.udp_send(data, "192.168.1.45")
#         udp_s.udp_send(data, "192.168.1.56")
#         udp_s.udp_send(data, "192.168.1.66")
#         # time.sleep(3)
#         return True
#     except Exception as ex:
#         print(ex)
#         return False


@app.after_request
def after(resp):
    '''
    被after_request钩子函数装饰过的视图函数
    ，会在请求得到响应后返回给用户前调用，也就是说，这个时候，
    请求已经被app.route装饰的函数响应过了，已经形成了response，这个时
    候我们可以对response进行一些列操作，我们在这个钩子函数中添加headers，所有的url跨域请求都会允许！！！
    '''
    resp = make_response(resp)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'GET,POST'
    resp.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return resp


@app.route("/plc/<style>/<count>/<switch>/")
def write_data_plc(style, count, switch):
    try:
        count = int(count)
        switch = int(switch)
        STYLE1 = siemens1.WriteString("DB34.0", style + "1")
        countA1 = siemens1.WriteInt16("DB34.12", count)
        STYLEb1 = siemens1.WriteString("DB34.14", style + "2")
        Switch1 = siemens1.WriteInt16("DB34.26", switch)
        if STYLE1.IsSuccess:
            print("产品型号写入成功")
        else:
            print("产品型号写入错误：" + STYLE1.Message)
        if countA1.IsSuccess:
            print("当班加工数量写入成功")
        else:
            print("当班加工数量写入错误", countA1.Message)
        if STYLEb1.IsSuccess:
            print("产品型号2写入成功")
        else:
            print("产品型号2写入错误：" + STYLEb1.Message)
        if Switch1.IsSuccess:
            print("切换产线成功")
        else:
            print("切换产线错误：" + Switch1.Message)

        STYLE2 = siemens2.WriteString("DB34.0", style + "3")
        countA2 = siemens2.WriteInt16("DB34.12", count)
        STYLEb2 = siemens2.WriteString("DB34.14", style + "4")
        Switch2 = siemens2.WriteInt16("DB34.26", switch)
        if STYLE2.IsSuccess:
            print("产品型号写入成功")
        else:
            print("产品型号写入错误：" + STYLE2.Message)
        if countA2.IsSuccess:
            print("当班加工数量写入成功")
        else:
            print("当班加工数量写入错误", countA2.Message)
        if STYLEb2.IsSuccess:
            print("产品型号2写入成功")
        else:
            print("产品型号2写入错误：" + STYLEb2.Message)
        if Switch2.IsSuccess:
            print("切换产线成功")
        else:
            print("切换产线错误：" + Switch2.Message)

        STYLE3 = siemens3.WriteString("DB34.0", style + "5")
        countA3 = siemens3.WriteInt16("DB34.12", count)
        STYLEb3 = siemens3.WriteString("DB34.14", style + "6")
        Switch3 = siemens3.WriteInt16("DB34.26", switch)
        if STYLE3.IsSuccess:
            print("产品型号写入成功")
        else:
            print("产品型号写入错误：" + STYLE3.Message)
        if countA3.IsSuccess:
            print("当班加工数量写入成功")
        else:
            print("当班加工数量写入错误", countA3.Message)
        if STYLEb3.IsSuccess:
            print("产品型号2写入成功")
        else:
            print("产品型号2写入错误：" + STYLEb3.Message)
        if Switch3.IsSuccess:
            print("切换产线成功")
        else:
            print("切换产线错误：" + Switch3.Message)

        STYLE4 = siemens4.WriteString("DB34.0", style + "7")
        countA4 = siemens4.WriteInt16("DB34.12", count)
        STYLEb4 = siemens4.WriteString("DB34.14", style + "8")
        Switch4 = siemens4.WriteInt16("DB34.26", switch)
        if STYLE4.IsSuccess:
            print("产品型号写入成功")
        else:
            print("产品型号写入错误：" + STYLE4.Message)
        if countA4.IsSuccess:
            print("当班加工数量写入成功")
        else:
            print("当班加工数量写入错误", countA4.Message)
        if STYLEb4.IsSuccess:
            print("产品型号2写入成功")
        else:
            print("产品型号2写入错误：" + STYLEb4.Message)
        if Switch4.IsSuccess:
            print("切换产线成功")
        else:
            print("切换产线错误：" + Switch4.Message)

        STYLE5 = siemens5.WriteString("DB34.0", style + "9")
        countA5 = siemens5.WriteInt16("DB34.12", count)
        STYLEb5 = siemens5.WriteString("DB34.14", style + "10")
        Switch5 = siemens5.WriteInt16("DB34.26", switch)
        if STYLE5.IsSuccess:
            print("产品型号写入成功")
        else:
            print("产品型号写入错误：" + STYLE5.Message)
        if countA5.IsSuccess:
            print("当班加工数量写入成功")
        else:
            print("当班加工数量写入错误", countA5.Message)
        if STYLEb5.IsSuccess:
            print("产品型号2写入成功")
        else:
            print("产品型号2写入错误：" + STYLEb5.Message)
        if Switch5.IsSuccess:
            print("切换产线成功")
        else:
            print("切换产线错误：" + Switch5.Message)

        STYLE6 = siemens6.WriteString("DB34.0", style + "11")
        countA6 = siemens6.WriteInt16("DB34.12", count)
        STYLEb6 = siemens6.WriteString("DB34.14", style + "12")
        Switch6 = siemens6.WriteInt16("DB34.26", switch)
        if STYLE6.IsSuccess:
            print("产品型号写入成功")
        else:
            print("产品型号写入错误：" + STYLE6.Message)
        if countA6.IsSuccess:
            print("当班加工数量写入成功")
        else:
            print("当班加工数量写入错误", countA6.Message)
        if STYLEb6.IsSuccess:
            print("产品型号2写入成功")
        else:
            print("产品型号2写入错误：" + STYLEb6.Message)
        if Switch6.IsSuccess:
            print("切换产线成功")
        else:
            print("切换产线错误：" + Switch6.Message)
        return "success"
    except Exception as ex:
        print(ex)
        return "Faild"


def data_json(data):
    data_list = {"productType": data["product_type"],
                 "r1EquipmentStatus": data["r1_equipment_status"],
                 "failCode": data["fail_code"],
                 "prodNum": data["prod_num"],
                 "r1RobNo": data["r1_rob_no"],
                 "r1WeldLineNo": data["r1_weld_line_no"],
                 "r1Electric": data["r1_electric"],
                 "r1Voltage": data["r1_voltage"],
                 "r1Speed": data["r1_speed"],
                 "r1Job": data["r1_job"],
                 "r2RobNo": data["r2_rob_no"],
                 "r2WeldLineNo": data["r2_weld_line_no"],
                 "r2Electric": data["r2_electric"],
                 "r2Voltage": data["r2_voltage"],
                 "r2Speed": data["r2_speed"],
                 "r2Job": data["r2_job"],
                 "replaceStatus": data["replace_status"],
                 "r1ProtectiveGas": data["r1_protective_gas"],
                 "r2ProtectiveGas": data["r2_protective_gas"],
                 "r1WeldingWire": data["r1_welding_wire"],
                 "r2WeldingWire": data["r2_welding_wire"],
                 "loginId": data["login_id"],
                 "loginPassword": data["login_password"],
                 "partStatus": data["part_status"],
                 "recerve": data["recerve"],
                 "productType2": data["product_type2"],
                 "prodNumB": data["countB"],
                 "qualifed": data["Qualifed"],
                 "unaccepted": data["Unaccepted"]
                 # "switch": data["Switch"]
                 }
    return data_list


@app.route("/plc/<num>/")
def readdataplc(num):
    global plc_data
    try:
        num = int(num)
        data_list = {}
        if num == 0:
            if plc_data.state1[0] == 1:
                data1 = read_data_plc(siemens1)
                data_list1 = data_json(data1)
            else:
                data_list1 = None
            if plc_data.state1[1] == 1:
                data2 = read_data_plc(siemens2)
                data_list2 = data_json(data2)
            else:
                data_list2 = None
            if plc_data.state1[2] == 1:
                data3 = read_data_plc(siemens3)
                data_list3 = data_json(data3)
            else:
                data_list3 = None
            if plc_data.state1[3] == 1:
                data4 = read_data_plc(siemens4)
                data_list4 = data_json(data4)
            else:
                data_list4 = None
            if plc_data.state1[4] == 1:
                data5 = read_data_plc(siemens5)
                data_list5 = data_json(data5)
            else:
                data_list5 = None
            if plc_data.state1[5] == 1:
                data6 = read_data_plc(siemens6)
                data_list6 = data_json(data6)
            else:
                data_list6 = None
            data_list = {"1": data_list1, "2": data_list2, "3": data_list3, "4": data_list4, "5": data_list5,
                         "6": data_list6}
        elif num == 1:
            data = read_data_plc(siemens1)
            data_list = data_json(data)
        elif num == 2:
            data = read_data_plc(siemens2)
            data_list = data_json(data)
        elif num == 3:
            data = read_data_plc(siemens3)
            data_list = data_json(data)
        elif num == 4:
            data = read_data_plc(siemens4)
            data_list = data_json(data)
        elif num == 5:
            data = read_data_plc(siemens5)
            data_list = data_json(data)
        elif num == 6:
            data = read_data_plc(siemens6)
            data_list = data_json(data)
    except Exception as ex:
        # logging.info("路由读取plc数据错误：%s", ex)
        print("路由读取plc数据错误：", ex)
        data_list = {}
    return jsonify(data_list)


@app.route("/player/<ipadr>/<order>/")
def send_craftplayerorder(ipadr, order):
    print("&&&&&&&&&&")
    print(ipadr)
    print("*************&&&&&&&&&&&&&&&&&&&")
    print(order)
    return_data = udp_s.udp_send(order, ipadr)
    print(return_data)
    print(type(return_data))
    return str(return_data)


# def plc_write():
#     # http://127.0.0.1:5000/plc/产品型号/当班加工数量/
#     app.run(host="192.168.1.5", port=5000)
#     CORS(app)


if __name__ == "__main__":
    udp_s = UdpSend()
    udp_s.init()
    t1 = threading.Thread(target=plc_read)
    # t2 = threading.Thread(target=plc_write)
    t1.start()
    # t2.start()
