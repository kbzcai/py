#!/usr/bin/env python3.6
# -*- encoding: utf-8 -*-
"""
@File    :   PLC_Read_Write2.py  
@Time   :  2021/1/22 10:19
@Author :   huxianming
"""
import time
from HslCommunication import SiemensS7Net
from HslCommunication import SiemensPLCS
import pymysql
import datetime


class ReadS71200(object):
    siemens1 = None
    siemens2 = None
    siemens3 = None
    siemens4 = None
    siemens5 = None
    siemens6 = None

    def __init__(self, ip, user, password, db_name):
        try:
            self.db = pymysql.connect(ip, user, password, db_name)
            self.cursor = self.db.cursor()
            print("数据库连接成功！")
        except Exception as ex:
            print(ex)

    def insertData(self, tablename, *key, **kwargs):  # *key返回的是元组(),**返回的是字典
        values = []
        for value in kwargs.values():
            values.append(value)
        print(tuple(values))
        sql = 'insert into {} {}'.format(tablename, key).replace("'", "") + ' VALUES {}'.format(tuple(values))
        print(sql)
        try:
            self.cursor.execute(sql)
            self.db.commit()
            print("成功添加数据")
            print("插入数据的ID：", self.cursor.lastrowid)
        except Exception as e:
            print(e)
            # 发生错误时候回滚
            self.db.rollback()

    def plc_connect(self, plc_ip1, plc_ip2, plc_ip3, plc_ip4, plc_ip5, plc_ip6):
        self.siemens1 = SiemensS7Net(SiemensPLCS.S1200, plc_ip1)
        if not self.siemens1.ConnectServer().IsSuccess:
            print("PLC1连接失败")
        else:
            print("PLC1连接成功")
        self.siemens2 = SiemensS7Net(SiemensPLCS.S1200, plc_ip2)
        if not self.siemens2.ConnectServer().IsSuccess:
            print("PLC2连接失败")
        else:
            print("PLC2连接成功")
        self.siemens3 = SiemensS7Net(SiemensPLCS.S1200, plc_ip3)
        if not self.siemens3.ConnectServer().IsSuccess:
            print("PLC3连接失败")
        else:
            print("PLC3连接成功")
        self.siemens4 = SiemensS7Net(SiemensPLCS.S1200, plc_ip4)
        if not self.siemens4.ConnectServer().IsSuccess:
            print("PLC4连接失败")
        else:
            print("PLC4连接成功")
        self.siemens5 = SiemensS7Net(SiemensPLCS.S1200, plc_ip5)
        if not self.siemens5.ConnectServer().IsSuccess:
            print("PLC5连接失败")
        else:
            print("PLC5连接成功")
        self.siemens6 = SiemensS7Net(SiemensPLCS.S1200, plc_ip6)
        if not self.siemens6.ConnectServer().IsSuccess:
            print("PLC6连接失败")
        else:
            print("PLC6连接成功")

    def write_data_plc(self, plc, style, count):
        STYLE = plc.WriteString("DB34.0", style)
        countA = plc.WriteInt16("DB34.18", count)
        if STYLE.IsSuccess:
            print("产品型号写入成功")
        else:
            print("产品型号写入错误：" + STYLE.Message)
        if countA.IsSuccess:
            print("当班加工数量写入成功")
        else:
            print("当班加工数量写入错误", countA.Message)

    def read_data_plc(self, plc, table_name):
        try:
            data_list = {}
            STYLE = plc.ReadString("DB33.0", 10)
            # 产品型号
            if STYLE.IsSuccess:
                print("读取STYLE成功", STYLE.Content)
                data_list["product_type"] = str(STYLE.Content)
            else:
                print("读取STYLE失败")
            Device_Status = plc.ReadInt16("DB33.12")
            # 设备状态
            if Device_Status.IsSuccess:
                print("读取Device_Status成功", Device_Status.Content)
                data_list["r1_equipment_status"] = str(Device_Status.Content)
            else:
                print("读取Device_Status失败")
            Fault_Code = plc.ReadInt16("DB33.14")
            # 错误代码
            if Fault_Code.IsSuccess:
                print("读取Fault_Code成功", Fault_Code.Content)
                data_list["fail_code"] = str(Fault_Code.Content)
            else:
                print("读取Fault_Code失败")
            Recerve = plc.ReadInt16("DB33.16")
            # 预留
            if Recerve.IsSuccess:
                print("读取Recvrve成功", Recerve.Content)
                data_list["recerve"] = str(Recerve.Content)
            else:
                print("读取Recvrve失败")
            countA = plc.ReadInt16("DB33.18")
            # 当前加工数量
            if countA.IsSuccess:
                print("读取countA成功", countA.Content)
                data_list["prod_num"] = countA.Content
            else:
                print("读取countA失败")
            R1_JOB = plc.ReadInt16("DB33.20")
            # 机器人1程序号
            if R1_JOB.IsSuccess:
                print("读取R1_JOB成功", R1_JOB.Content)
                data_list["r1_rob_no"] = str(R1_JOB.Content)
            else:
                print("读取R1_JOB失败")
            Weld1_Code = plc.ReadInt16("DB33.22")
            # w1焊缝号
            if Weld1_Code.IsSuccess:
                print("读取Weld1_Code成功", Weld1_Code.Content)
                data_list["r1_weld_line_no"] = str(Weld1_Code.Content)
            else:
                print("读取Weld1_Code失败")
            W1_Current = plc.ReadFloat("DB33.24")
            # w1焊接电流
            if W1_Current.IsSuccess:
                print("读取W1_Current成功", W1_Current.Content)
                data_list["r1_electric"] = str(W1_Current.Content)
            else:
                print("读取W1_Current失败")
            W1_Voltage = plc.ReadFloat("DB33.28")
            # w1焊接电压
            if W1_Voltage.IsSuccess:
                print("读取W1_Voltage成功", W1_Voltage.Content)
                data_list["r1_voltage"] = str(W1_Voltage.Content)
            else:
                print("读取W1_Voltage失败")
            W1_Speed = plc.ReadFloat("DB33.32")
            # w1焊接速度
            if W1_Speed.IsSuccess:
                print("读取W1_Speed成功", W1_Speed.Content)
                data_list["r1_speed"] = str(W1_Speed.Content)
            else:
                print("读取W1_Speed失败")
            W1_JOB = plc.ReadInt16("DB33.36")
            # w1焊接号
            if W1_JOB.IsSuccess:
                print("读取W1_JOB成功", W1_JOB.Content)
                data_list["r1_job"] = str(W1_JOB.Content)
            else:
                print("读取W1_JOB失败")
            R2_JOB = plc.ReadInt16("DB33.38")
            # 机器人2程序号
            if R2_JOB.IsSuccess:
                print("读取R2_JOB成功", R2_JOB.Content)
                data_list["r2_rob_no"] = str(R2_JOB.Content)
            else:
                print("读取R2_JOB失败")
            Weld2_Code = plc.ReadInt16("DB33.40")
            # w2焊缝号
            if Weld2_Code.IsSuccess:
                print("读取Weld2_Code成功", Weld2_Code.Content)
                data_list["r2_weld_line_no"] = str(Weld2_Code.Content)
            else:
                print("读取Weld2_Code失败")
            W2_Current = plc.ReadFloat("DB33.42")
            # w2焊接电流
            if W2_Current.IsSuccess:
                print("读取W2_Current成功", W2_Current.Content)
                data_list["r2_electric"] = str(W2_Current.Content)
            else:
                print("读取W2_Current失败")
            W2_Voltage = plc.ReadFloat("DB33.46")
            # w2焊接电压
            if W2_Voltage.IsSuccess:
                print("读取W2_Voltage成功", W2_Voltage.Content)
                data_list["r2_voltage"] = str(W2_Voltage.Content)
            else:
                print("读取W2_Voltage失败")
            W2_Speed = plc.ReadFloat("DB33.50")
            # w2焊接速度
            if W2_Speed.IsSuccess:
                print("读取W2_Speed成功", W2_Speed.Content)
                data_list["r2_speed"] = str(W2_Speed.Content)
            else:
                print("读取W2_Speed失败")
            W2_JOB = plc.ReadInt16("DB33.54")
            # w2焊接号
            if W2_JOB.IsSuccess:
                print("读取W2_JOB成功", W2_JOB.Content)
                data_list["r2_job"] = str(W2_JOB.Content)
            else:
                print("读取W2_JOB失败")
            Gun_Status = plc.ReadInt16("DB33.56")
            # 焊接状态
            if Gun_Status.IsSuccess:
                print("读取Gun_Status成功", Gun_Status.Content)
                data_list["replace_status"] = str(Gun_Status.Content)
            else:
                print("读取Gun_Status失败")
            Part_Status = plc.ReadInt16("DB33.58")
            # 零件状态
            if Part_Status.IsSuccess:
                print("读取Part_Status成功", Part_Status.Content)
                data_list["part_status"] = str(Part_Status.Content)
            else:
                print("读取Part_Status失败")
            W1_Gas = plc.ReadInt16("DB33.60")
            # 枪1气体用量
            if W1_Gas.IsSuccess:
                print("读取W1_Gas成功", W1_Gas.Content)
                data_list["r1_protective_gas"] = str(W1_Gas.Content)
            else:
                print("读取W1_Gas失败")
            W1_Wire = plc.ReadInt16("DB33.62")
            # 枪1焊丝用量
            if W1_Wire.IsSuccess:
                print("读取W1_Wire成功", W1_Wire.Content)
                data_list["r1_welding_wire"] = str(W1_Wire.Content)
            else:
                print("读取W1_Wire失败")
            W2_Gas = plc.ReadInt16("DB33.64")
            # 枪2气体用量
            if W2_Gas.IsSuccess:
                print("读取W2_Gas成功", W2_Gas.Content)
                data_list["r2_protective_gas"] = str(W2_Gas.Content)
            else:
                print("读取W2_Gas失败")
            W2_Wire = plc.ReadInt16("DB33.66")
            # 枪2焊丝用量
            if W2_Wire.IsSuccess:
                print("读取W2_Wire成功", W2_Wire.Content)
                data_list["r2_welding_wire"] = str(W2_Wire.Content)
            else:
                print("读取W2_Wire失败")
            User_ID = plc.ReadString("DB33.68", 10)
            # 用户ID
            if User_ID.IsSuccess:
                print("读取User_ID成功", User_ID.Content)
                data_list["login_id"] = str(User_ID.Content)
            else:
                print("读取User_ID失败")
            User_Password = plc.ReadString("DB33.80", 10)
            # 用户密码
            if User_Password.IsSuccess:
                print("读取User_Password成功", User_Password.Content)
                data_list["login_password"] = str(User_Password.Content)
            else:
                print("读取User_Password失败")

            self.insertData(table_name, "product_type", "r1_equipment_status",
                            "fail_code", "prod_num", "r1_rob_no", "r1_weld_line_no", "r1_electric",
                            "r1_voltage", "r1_speed", "r1_job", "r2_rob_no", "r2_weld_line_no",
                            "r2_electric", "r2_voltage", "r2_speed", "r2_job", "replace_status",
                            "r1_protective_gas", "r2_protective_gas", "r1_welding_wire", "r2_welding_wire",
                            "login_id", "login_password", "part_status", "recerve", "create_time",
                            product_type=data_list["product_type"],
                            r1_equipment_status=data_list["r1_equipment_status"],
                            fail_code=data_list["fail_code"], prod_num=data_list["prod_num"],
                            r1_rob_no=data_list["r1_rob_no"], r1_weld_line_no=data_list["r1_weld_line_no"],
                            r1_electric=data_list["r1_electric"], r1_voltage=data_list["r1_voltage"],
                            r1_speed=data_list["r1_speed"],
                            r1_job=data_list["r1_job"], r2_rob_no=data_list["r2_rob_no"],
                            r2_weld_line_no=data_list["r2_weld_line_no"],
                            r2_electric=data_list["r2_electric"], r2_voltage=data_list["r2_voltage"],
                            r2_speed=data_list["r2_speed"], r2_job=data_list["r2_job"],
                            replace_status=data_list["replace_status"],
                            r1_protective_gas=data_list["r1_protective_gas"],
                            r2_protective_gas=data_list["r2_protective_gas"],
                            r1_welding_wire=data_list["r1_welding_wire"], r2_welding_wire=data_list["r2_welding_wire"],
                            login_id=data_list["login_id"], login_password=data_list["login_password"],
                            part_status=data_list["part_status"],
                            recerve=data_list["recerve"],
                            create_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        except Exception as ex:
            print("读取插入数据库失败错误", ex)

    def main(self):
        self.read_data_plc(self.siemens1, "mes_plc")
        self.read_data_plc(self.siemens2, "mes_plc_r2")
        self.read_data_plc(self.siemens3, "mes_plc_r3")
        self.read_data_plc(self.siemens4, "mes_plc_r4")
        self.read_data_plc(self.siemens5, "mes_plc_r5")
        self.read_data_plc(self.siemens6, "mes_plc_r6")


if __name__ == "__main__":
    plc_data = ReadS71200("192.168.1.5", "root", "rootroot", "mes")
    plc_data.plc_connect("192.168.1.10", "192.168.1.20", "192.168.1.30",
                         "192.168.1.40", "192.168.1.50", "192.168.1.60")
    while True:
        plc_data.main()
        time.sleep(60)
