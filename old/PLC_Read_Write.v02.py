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
            Device_Status = self.siemens.ReadInt16("Device_Status")
            if Device_Status.IsSuccess:
                print("读取Device_Status成功", Device_Status.Content)
            else:
                print("读取Device_Status失败")
            Fault_Code = self.siemens.ReadInt16("Fault_Code")
            if Fault_Code.IsSuccess:
                print("读取Fault_Code成功", Fault_Code.Content)
            else:
                print("读取Fault_Code失败")
            Reserve = self.siemens.ReadInt16("Reserve")
            if Reserve.IsSuccess:
                print("Reserve", Reserve.Content)
            else:
                print("读取Reserve失败")
            R1_JOB = self.siemens.ReadInt16("R1_JOB")
            if R1_JOB.IsSuccess:
                print("读取R1_JOB成功", R1_JOB.Content)
            else:
                print("读取R1_JOB失败")
            Weld1_Code = self.siemens.ReadInt16("Weld1_Code")
            if Weld1_Code.IsSuccess:
                print("读取Weld1_Code成功", Weld1_Code.Content)
            else:
                print("读取Weld1_Code失败")
            W1_Current = self.siemens.ReadFloat("W1_Current")
            if W1_Current.IsSuccess:
                print("读取W1_Current成功", W1_Current.Content)
            else:
                print("读取W1_Current失败")
            W1_Voltage = self.siemens.ReadFloat("W1_Voltage")
            if W1_Voltage.IsSuccess:
                print("读取W1_Voltage成功", W1_Voltage.Content)
            else:
                print("读取W1_Voltage失败")
            W1_Speed = self.siemens.ReadFloat("W1_Speed")
            if W1_Speed.IsSuccess:
                print("读取W1_Speed成功", W1_Speed.Content)
            else:
                print("读取W1_Speed失败")
            W1_JOB = self.siemens.ReadInt16("W1_JOB")
            if W1_JOB.IsSuccess:
                print("读取W1_JOB成功", W1_JOB.Content)
            else:
                print("读取W1_JOB失败")
            R2_JOB = self.siemens.ReadInt16("R2_JOB")
            if R2_JOB.IsSuccess:
                print("读取R2_JOB成功", R2_JOB.Content)
            else:
                print("读取R2_JOB失败")
            Weld2_Code = self.siemens.ReadInt16("Weld2_Code")
            if Weld2_Code.IsSuccess:
                print("读取Weld2_Code成功", Weld2_Code.Content)
            else:
                print("读取Weld2_Code失败")
            W2_Current = self.siemens.ReadFloat("W2_Current")
            if W2_Current.IsSuccess:
                print("读取W2_Current成功", W2_Current.Content)
            else:
                print("读取W2_Current失败")
            W2_Voltage = self.siemens.ReadFloat("W2_Voltage")
            if W2_Voltage.IsSuccess:
                print("读取W2_Voltage成功", W2_Voltage.Content)
            else:
                print("读取W2_Voltage失败")
            W2_Speed = self.siemens.ReadFloat("W2_Speed")
            if W2_Speed.IsSuccess:
                print("读取W2_Speed成功", W2_Speed.Content)
            else:
                print("读取W2_Speed失败")
            W2_JOB = self.siemens.ReadInt16("W2_JOB")
            if W2_JOB.IsSuccess:
                print("读取W2_JOB成功", W2_JOB.Content)
            else:
                print("读取W2_JOB失败")
            Gun_Status = self.siemens.ReadInt16("Gun_Status")
            if Gun_Status.IsSuccess:
                print("读取Gun_Status成功", Gun_Status.Content)
            else:
                print("读取Gun_Status失败")
            Part_Status = self.siemens.ReadInt16("Part_Status")
            if Part_Status.IsSuccess:
                print("读取Part_Status成功", Part_Status.Content)
            else:
                print("读取Part_Status失败")
            W1_Gas = self.siemens.ReadInt16("W1_Gas")
            if W1_Gas.IsSuccess:
                print("读取W1_Gas成功", W1_Gas.Content)
            else:
                print("读取W1_Gas失败")
            W1_Wire = self.siemens.ReadInt16("W1_Wire")
            if W1_Wire.IsSuccess:
                print("读取W1_Wire成功", W1_Wire.Content)
            else:
                print("读取W1_Wire失败")
            W2_Gas = self.siemens.ReadInt16("W2_Gas")
            if W2_Gas.IsSuccess:
                print("读取W2_Gas成功", W2_Gas.Content)
            else:
                print("读取W2_Gas失败")
            W2_Wire = self.siemens.ReadInt16("W2_Wire")
            if W2_Wire.IsSuccess:
                print("读取W2_Wire成功", W2_Wire.Content)
            else:
                print("读取W2_Wire失败")
            User_ID = self.siemens.ReadString("User_ID", 10)
            if User_ID.IsSuccess:
                print("读取User_ID成功", User_ID.Content)
            else:
                print("读取User_ID失败")
            User_Password = self.siemens.ReadString("User_Password", 10)
            if User_Password.IsSuccess:
                print("读取User_Password成功", User_Password.Content)
            else:
                print("读取User_Password失败")
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
    s7 = ReadS71200("192.168.1.30")
    s7.read_data()
