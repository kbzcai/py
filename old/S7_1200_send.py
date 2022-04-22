#!/usr/bin/env python3.6
# -*- encoding: utf-8 -*-
"""
@File    :   S7_1200_send.py  
@Time   :  2020/11/21 14:35
@Author :   huxianming
"""

from HslCommunication import SiemensS7Net
from HslCommunication import SiemensPLCS


class ReadS71200():
    siemens = None

    def __int__(self, ip):
        self.siemens = SiemensS7Net(SiemensPLCS.S1200, ip)
        if not self.siemens.ConnectServer().IsSuccess:
            print("PLC连接失败")

    def read_data_int16(self, db_address):
        result = self.siemens.ReadInt16(db_address)
        if result.IsSuccess:
            print(result.Content)
            return result.Content
        else:
            print("错误：" + result.Message)
            return result.Message

    def write_data_int16(self, db_address, data):
        result = self.siemens.WriteInt16(db_address, data)
        if result.IsSuccess:
            print("写入成功!")
            return True
        else:
            print("错误：" + result.Message)
            return False

if __name__ == "main":
    ip_address = "192.168.1.10"
    s7: ReadS71200 = ReadS71200(ip_address)
    db_address = "DB26.6.0"
    s7.read_data_bool(db_address)
    # s7.write_data_int16(db_address, 100)





