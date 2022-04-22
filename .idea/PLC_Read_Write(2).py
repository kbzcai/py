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
            Device_Status = self.siemens.ReadInt16("DB33.12")
            if Device_Status.IsSuccess:
                print("读取Device_Status成功", Device_Status.Content)
            else:
                print("读取Device_Status失败")
            Fault_Code = self.siemens.ReadInt16("DB33.14")
            if Fault_Code.IsSuccess:
                print("读取Fault_Code成功", Fault_Code.Content)
            else:
                print("读取Fault_Code失败")
            Reverse = self.siemens.ReadInt16("DB33.16")
            if Reverse.IsSuccess:
                print("读取Reverse成功", Reverse.Content)
            else:
                print("读取Reverse失败")
            countA = self.siemens.ReadInt16("DB33.18")
            if countA.IsSuccess:
                print("读取countA成功", countA.Content)
            else:
                print("读取countA失败")
            R1_JOB = self.siemens.ReadInt16("DB33.20")
            if R1_JOB.IsSuccess:
                print("读取R1_JOB成功", R1_JOB.Content)
            else:
                print("读取R1_JOB失败")
            Weld1_Code = self.siemens.ReadInt16("DB33.22")
            if Weld1_Code.IsSuccess:
                print("读取Weld1_Code成功", Weld1_Code.Content)
            else:
                print("读取Weld1_Code失败")
            W1_Current = self.siemens.ReadFloat("DB33.24")
            if W1_Current.IsSuccess:
                print("读取W1_Current成功", W1_Current.Content)
            else:
                print("读取W1_Current失败")
            W1_Voltage = self.siemens.ReadFloat("DB33.28")
            if W1_Voltage.IsSuccess:
                print("读取W1_Voltage成功", W1_Voltage.Content)
            else:
                print("读取W1_Voltage失败")
            W1_Speed = self.siemens.ReadFloat("DB33.32")
            if W1_Speed.IsSuccess:
                print("读取W1_Speed成功", W1_Speed.Content)
            else:
                print("读取W1_Speed失败")
            W1_JOB = self.siemens.ReadInt16("DB33.36")
            if W1_JOB.IsSuccess:
                print("读取W1_JOB成功", W1_JOB.Content)
            else:
                print("读取W1_JOB失败")
                print(W1_JOB.Message)
            R2_JOB = self.siemens.ReadInt16("DB33.38")
            if R2_JOB.IsSuccess:
                print("读取R2_JOB成功", R2_JOB.Content)
            else:
                print("读取R2_JOB失败")
                print(R2_JOB.Message)
            Weld2_Code = self.siemens.ReadInt16("DB33.40")
            if Weld2_Code.IsSuccess:
                print("读取Weld2_Code成功", Weld2_Code.Content)
            else:
                print("读取Weld2_Code失败")
                print(Weld2_Code.Message)
            W2_Current = self.siemens.ReadFloat("DB33.42")
            if W2_Current.IsSuccess:
                print("读取W2_Current成功", W2_Current.Content)
            else:
                print("读取W2_Current失败")
                print(W2_Current.Message)
            W2_Voltage = self.siemens.ReadFloat("DB33.46")
            if W2_Voltage.IsSuccess:
                print("读取W2_Voltage成功", W2_Voltage.Content)
            else:
                print("读取W2_Voltage失败")
            W2_Speed = self.siemens.ReadFloat("DB33.50")
            if W2_Speed.IsSuccess:
                print("读取W2_Speed成功", W2_Speed.Content)
            else:
                print("读取W2_Speed失败")
            W2_JOB = self.siemens.ReadInt16("DB33.54")
            if W2_JOB.IsSuccess:
                print("读取W2_JOB成功", W2_JOB.Content)
            else:
                print("读取W2_JOB失败")
            Gun_Status = self.siemens.ReadInt16("DB33.56")
            if Gun_Status.IsSuccess:
                print("读取Gun_Status成功", Gun_Status.Content)
            else:
                print("读取Gun_Status失败")
            Part_Status = self.siemens.ReadInt16("DB33.58")
            if Part_Status.IsSuccess:
                print("读取Part_Status成功", Part_Status.Content)
            else:
                print("读取Part_Status失败")
            W1_Gas = self.siemens.ReadInt16("DB33.60")
            if W1_Gas.IsSuccess:
                print("读取W1_Gas成功", W1_Gas.Content)
            else:
                print("读取W1_Gas失败")
            W1_Wire = self.siemens.ReadInt16("DB33.62")
            if W1_Wire.IsSuccess:
                print("读取W1_Wire成功", W1_Wire.Content)
            else:
                print("读取W1_Wire失败")
            W2_Gas = self.siemens.ReadInt16("DB33.64")
            if W2_Gas.IsSuccess:
                print("读取W2_Gas成功", W2_Gas.Content)
            else:
                print("读取W2_Gas失败")
            W2_Wire = self.siemens.ReadInt16("DB33.66")
            if W2_Wire.IsSuccess:
                print("读取W2_Wire成功", W2_Wire.Content)
            else:
                print("读取W2_Wire失败")
            User_ID = self.siemens.ReadString("DB33.68", 10)
            if User_ID.IsSuccess:
                print("读取User_ID成功", User_ID.Content)
            else:
                print("读取User_ID失败")
            User_Password = self.siemens.ReadString("DB33.80", 10)
            if User_Password.IsSuccess:
                print("读取User_Password成功", User_Password.Content)
            else:
                print("读取User_Password失败")
        except Exception as ex:
            print("读取失败错误", ex)

    def write_data(self, style, count):
        STYLE = self.siemens.WriteString("DB34.0", style)
        countA = self.siemens.WriteInt16("DB34.12", count)
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
    s7.read_data()
    s7.write_data("qwer",20)
