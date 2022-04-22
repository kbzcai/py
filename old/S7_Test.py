#!/usr/bin/env python3.6
# -*- encoding: utf-8 -*-
"""
@File    :   S7_Test.py  
@Time   :  2020/12/6 15:34
@Author :   huxianming
"""

from HslCommunication import SiemensS7Net
from HslCommunication import SiemensPLCS


siemens = SiemensS7Net(SiemensPLCS.S1200, "192.168.1.30")
if not siemens.ConnectServer().IsSuccess:
    print("PLC连接失败")
else:
    print("PLC连接成功")

# result = siemens.WriteInt16("DB102.4",120)

# result = siemens.WriteInt32("DB33.18",20)
# result= siemens.ReadInt16("DB30.18")
result= siemens.ReadInt16("DB33.18")
# result =siemens.WriteString("DB34.0",'QWERTY')
print(result)
print(result.IsSuccess)
print(result.ErrorCode)
print(result.Message)
if result.IsSuccess:
    print("读取成功")
    print(result.Content)
else:
    print("读取失败")