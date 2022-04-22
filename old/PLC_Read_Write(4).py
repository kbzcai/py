#!/usr/bin/env python3.6
# -*- encoding: utf-8 -*-
"""
@File    :   PLC_Read_Write.py
@Time   :  2021/1/16 13:43
@Author :   huxianming
"""

from HslCommunication import SiemensS7Net
from HslCommunication import SiemensPLCS
import pymysql


class ReadS71200(object):
    def __init__(self, ip):
        self.db = None
        self.cursor = None
        self.siemens = SiemensS7Net(SiemensPLCS.S1200, ip)
        if not self.siemens.ConnectServer().IsSuccess:
            print("PLC连接失败")
        else:
            print("PLC连接成功")

    def sql_connect(self, ip, user, password, db_name):
        try:
            self.db = pymysql.connect(ip, user, password, db_name)
            self.cursor = self.db.cursor()
            print("数据库连接成功！")
        except Exception as ex:
            print(ex)

    def select_data(self):
        self.cursor.execute("select version()")
        data = self.cursor.fetchone()
        print(data)

    def insert_data(self, data):
        sql = "insert into mes_plc(product_type, r1_equipment_status, r2_equipment_status,\
                 fail_code, prod_num, r1_rob_no, r1_weld_line_no, r1_electric, r1_voltage,\
                 r1_speed, r1_job, r2_rob_no, r2_weld_line_no, r2_electric, r2_voltage,\
                 r2_speed, r2_job, replace_status, r1_protective_gas, r2_protective_gas,\
                 r1_welding_wire, r2_welding_wire, login_id, login_password, part_status) values (\
                 '%s', '%s', '%s', '%s', %s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s',\
                 '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
              (data["product_type"], data["r1_equipment_status"], data["r2_equipment_status"],
               data["fail_code"], data["prod_num"], data["r1_rob_no"], data["r1_weld_line_no"], data["r1_electric"],
               data["r1_voltage"], data["r1_speed"], data["r1_job"], data["r2_rob_no"], data["r2_weld_line_no"],
               data["r2_electric"], data["r2_voltage"], data["r2_speed"], data["r2_job"], data["replace_status"],
               data["r1_protective_gas"], data["r2_protective_gas"], data["r1_welding_wire"], data["r2_welding_wire"],
               data["login_id"], data["login_password"], data["part_status"])
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as ex:
            print(ex)
            self.db.rollback()


    def read_data(self):
        try:
            data_list = {}
            STYLE = self.siemens.ReadString("DB33.0", 10)
            #产品型号
            if STYLE.IsSuccess:
                print("读取STYLE成功", STYLE.Content)
                data_list["product_type"] = str(STYLE.Content)
            else:
                print("读取STYLE失败")
            Device_Status = self.siemens.ReadInt16("DB33.12")
            #设备状态
            if Device_Status.IsSuccess:
                print("读取Device_Status成功", Device_Status.Content)
                data_list["r1_equipment_status"] = str(Device_Status.Content)
            else:
                print("读取Device_Status失败")
            Fault_Code = self.siemens.ReadInt16("DB33.14")
            #错误代码
            if Fault_Code.IsSuccess:
                print("读取Fault_Code成功", Fault_Code.Content)
                data_list["fail_code"] = str(Fault_Code.Content)
            else:
                print("读取Fault_Code失败")
            Recvrve = self.siemens.ReadInt16("DB33.16")
            #预留
            if Recvrve.IsSuccess:
                print("读取Recvrve成功", Recvrve.Content)
                data_list["r2_equipment_status"] = str(Recvrve.Content)
            else:
                print("读取Recvrve失败")
            countA = self.siemens.ReadInt16("DB33.18")
            #当前加工数量
            if countA.IsSuccess:
                print("读取countA成功", countA.Content)
                data_list["prod_num"] = countA.Content
            else:
                print("读取countA失败")
            R1_JOB = self.siemens.ReadInt16("DB33.20")
            #机器人1程序号
            if R1_JOB.IsSuccess:
                print("读取R1_JOB成功", R1_JOB.Content)
                data_list["r1_rob_no"] = str(R1_JOB.Content)
            else:
                print("读取R1_JOB失败")
            Weld1_Code = self.siemens.ReadInt16("DB33.22")
            #w1焊缝号
            if Weld1_Code.IsSuccess:
                print("读取Weld1_Code成功", Weld1_Code.Content)
                data_list["r1_weld_line_no"] = str(Weld1_Code.Content)
            else:
                print("读取Weld1_Code失败")
            W1_Current = self.siemens.ReadFloat("DB33.24")
            #w1焊接电流
            if W1_Current.IsSuccess:
                print("读取W1_Current成功", W1_Current.Content)
                data_list["r1_electric"] = str(W1_Current.Content)
            else:
                print("读取W1_Current失败")
            W1_Voltage = self.siemens.ReadFloat("DB33.28")
            #w1焊接电压
            if W1_Voltage.IsSuccess:
                print("读取W1_Voltage成功", W1_Voltage.Content)
                data_list["r1_voltage"] = str(W1_Voltage.Content)
            else:
                print("读取W1_Voltage失败")
            W1_Speed = self.siemens.ReadFloat("DB33.32")
            #w1焊接速度
            if W1_Speed.IsSuccess:
                print("读取W1_Speed成功", W1_Speed.Content)
                data_list["r1_speed"] = str(W1_Speed.Content)
            else:
                print("读取W1_Speed失败")
            W1_JOB = self.siemens.ReadInt16("DB33.36")
            #w1焊接号
            if W1_JOB.IsSuccess:
                print("读取W1_JOB成功", W1_JOB.Content)
                data_list["r1_job"] = str(W1_JOB.Content)
            else:
                print("读取W1_JOB失败")
            R2_JOB = self.siemens.ReadInt16("DB33.38")
            #机器人2程序号
            if R2_JOB.IsSuccess:
                print("读取R2_JOB成功", R2_JOB.Content)
                data_list["r2_rob_no"] = str(R2_JOB.Content)
            else:
                print("读取R2_JOB失败")
            Weld2_Code = self.siemens.ReadInt16("DB33.40")
            #w2焊缝号
            if Weld2_Code.IsSuccess:
                print("读取Weld2_Code成功", Weld2_Code.Content)
                data_list["r2_weld_line_no"] = str(Weld2_Code.Content)
            else:
                print("读取Weld2_Code失败")
            W2_Current = self.siemens.ReadFloat("DB33.42")
            #w2焊接电流
            if W2_Current.IsSuccess:
                print("读取W2_Current成功", W2_Current.Content)
                data_list["r2_electric"] = str(W2_Current.Content)
            else:
                print("读取W2_Current失败")
            W2_Voltage = self.siemens.ReadFloat("DB33.46")
            #w2焊接电压
            if W2_Voltage.IsSuccess:
                print("读取W2_Voltage成功", W2_Voltage.Content)
                data_list["r2_voltage"] = str(W2_Voltage.Content)
            else:
                print("读取W2_Voltage失败")
            W2_Speed = self.siemens.ReadFloat("DB33.50")
            #w2焊接速度
            if W2_Speed.IsSuccess:
                print("读取W2_Speed成功", W2_Speed.Content)
                data_list["r2_speed"] = str(W2_Speed.Content)
            else:
                print("读取W2_Speed失败")
            W2_JOB = self.siemens.ReadInt16("DB33.54")
            #w2焊接号
            if W2_JOB.IsSuccess:
                print("读取W2_JOB成功", W2_JOB.Content)
                data_list["r2_job"] = str(W2_JOB.Content)
            else:
                print("读取W2_JOB失败")
            Gun_Status = self.siemens.ReadInt16("DB33.56")
            #焊接状态
            if Gun_Status.IsSuccess:
                print("读取Gun_Status成功", Gun_Status.Content)
                data_list["replace_status"] = str(Gun_Status.Content)
            else:
                print("读取Gun_Status失败")
            Part_Status = self.siemens.ReadInt16("DB33.58")
            #零件状态
            if Part_Status.IsSuccess:
                print("读取Part_Status成功", Part_Status.Content)
                data_list["part_status"] = str(Part_Status.Content)
            else:
                print("读取Part_Status失败")
            W1_Gas = self.siemens.ReadInt16("DB33.60")
            #枪1气体用量
            if W1_Gas.IsSuccess:
                print("读取W1_Gas成功", W1_Gas.Content)
                data_list["r1_protective_gas"] = str(W1_Gas.Content)
            else:
                print("读取W1_Gas失败")
            W1_Wire = self.siemens.ReadInt16("DB33.62")
            #枪1焊丝用量
            if W1_Wire.IsSuccess:
                print("读取W1_Wire成功", W1_Wire.Content)
                data_list["r1_welding_wire"] = str(W1_Wire.Content)
            else:
                print("读取W1_Wire失败")
            W2_Gas = self.siemens.ReadInt16("DB33.64")
            #枪2气体用量
            if W2_Gas.IsSuccess:
                print("读取W2_Gas成功", W2_Gas.Content)
                data_list["r2_protective_gas"] = str(W2_Gas.Content)
            else:
                print("读取W2_Gas失败")
            W2_Wire = self.siemens.ReadInt16("DB33.66")
            #枪2焊丝用量
            if W2_Wire.IsSuccess:
                print("读取W2_Wire成功", W2_Wire.Content)
                data_list["r2_welding_wire"] = str(W2_Wire.Content)
            else:
                print("读取W2_Wire失败")
            User_ID = self.siemens.ReadString("DB33.68", 10)
            #用户ID
            if User_ID.IsSuccess:
                print("读取User_ID成功", User_ID.Content)
                data_list["login_id"] = str(User_ID.Content)
            else:
                print("读取User_ID失败")
            User_Password = self.siemens.ReadString("DB33.80", 10)
            #用户密码
            if User_Password.IsSuccess:
                print("读取User_Password成功", User_Password.Content)
                data_list["login_password"] = str(User_Password.Content)
            else:
                print("读取User_Password失败")

            self.insert_data(data_list)
        except Exception as ex:
            print("读取失败错误", ex)

    def write_data(self, style, count):
        STYLE = self.siemens.WriteString("DB34.0", style)
        countA = self.siemens.WriteInt16("DB34.18", count)
        if STYLE.IsSuccess:
            print("产品型号写入成功")
        else:
            print("产品型号写入错误：" + STYLE.Message)
        if countA.IsSuccess:
            print("当班加工数量写入成功")
        else:
            print("当班加工数量写入错误", countA.Message)


if __name__ == "__main__":
    s7 = ReadS71200("192.168.1.10")
    s7.sql_connect("192.168.1.5", "root", "rootroot", "mes")
    s7.read_data()
