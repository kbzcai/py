#!/usr/bin/env python3.6
# -*- encoding: utf-8 -*-
"""
@File    :   PLC_Read_Write.py
@Time   :  2021/1/16 13:43
@Author :   huxianming
"""

from HslCommunication import SiemensS7Net
from HslCommunication import SiemensPLCS


class ReadS71200(object):
    def __init__(self, ip):
        self.siemens = SiemensS7Net(SiemensPLCS.S1200, ip)
        if not self.siemens.ConnectServer().IsSuccess:
            print("PLC连接失败")
        else:
            print("PLC连接成功")

    def read_data(self):
        try:
            Device_Status = self.siemens.ReadInt16("Device_Status").Content
            print("Device_Status", Device_Status)
            Fault_Code = self.siemens.ReadInt16("Fault_Code").Content
            print("Fault_Code", Fault_Code)
            Reserve = self.siemens.ReadInt16("Reserve").Content
            print("Reserve", Reserve)
            R1_JOB = self.siemens.ReadInt16("R1_JOB").Content
            print("R1_JOB", R1_JOB)
            Weld1_Code = self.siemens.ReadInt16("Weld1_Code").Content
            print("Weld1_Code", Weld1_Code)
            W1_Current = self.siemens.ReadFloat("W1_Current").Content
            print("W1_Current", W1_Current)
            W1_Voltage = self.siemens.ReadFloat("W1_Voltage").Content
            print("W1_Voltage", W1_Voltage)
            W1_Speed = self.siemens.ReadFloat("W1_Speed").Content
            print("W1_Speed", W1_Speed)
            W1_JOB = self.siemens.ReadInt16("W1_JOB").Content
            print("W1_JOB", W1_JOB)
            R2_JOB = self.siemens.ReadInt16("R2_JOB").Content
            print("R2_JOB", R2_JOB)
            Weld2_Code = self.siemens.ReadInt16("Weld2_Code").Content
            print("Weld2_Code", Weld2_Code)
            W2_Current = self.siemens.ReadFloat("W2_Current").Content
            print("W2_Current", W2_Current)
            W2_Voltage = self.siemens.ReadFloat("W2_Voltage").Content
            print("W2_Voltage", W2_Voltage)
            W2_Speed = self.siemens.ReadFloat("W2_Speed").Content
            print("W2_Speed", W2_Speed)
            W2_JOB = self.siemens.ReadInt16("W2_JOB").Content
            print("W2_JOB", W2_JOB)
            Gun_Status = self.siemens.ReadInt16("Gun_Status").Content
            print("Gun_Status", Gun_Status)
            Part_Status = self.siemens.ReadInt16("Part_Status").Content
            print("Part_Status", Part_Status)
            W1_Gas = self.siemens.ReadInt16("W1_Gas").Content
            print("W1_Gas", W1_Gas)
            W1_Wire = self.siemens.ReadInt16("W1_Wire").Content
            print("W1_Wire", W1_Wire)
            W2_Gas = self.siemens.ReadInt16("W2_Gas").Content
            print("W2_Gas", W2_Gas)
            W2_Wire = self.siemens.ReadInt16("W2_Wire").Content
            print("W2_Wire", W2_Wire)
            User_ID = self.siemens.ReadString("User_ID", 10).Content
            print("User_ID", User_ID)
            User_Password = self.siemens.ReadString("User_Password", 10).Content
            print("User_Password", User_Password)
        except Exception as ex:
            print("读取失败错误", ex)

    def write_data(self, style, count):
        STYLE = self.siemens.WriteString("STYLE", style)
        countA = self.siemens.WriteInt16("countA", count)
        if STYLE.IsSuccess:
            print("产品型号写入成功")
        else:
            print("产品型号写入错误：" + STYLE.Message)
        if countA.IsSuccess:
            print("当班加工数量写入成功")
        else:
            print("当班加工数量写入错误", countA.Message)


if __name__ == "__main__":
    s7 = ReadS71200("192.168.1.20")
    s7.read_data()
    # s7.write_data("QWERTY",20)
