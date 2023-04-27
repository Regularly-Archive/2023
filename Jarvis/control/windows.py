import os
import subprocess
 

# 关闭计算机
def shutdown():
    os.system('shutdown -s -t 60 ')

# 重启计算机
def restart():
    os.system('shutdown -r -t 100')

# 打开记事本
def notepad():
    subprocess.Popen('notepad.exe')

# 打开计算器
def calc():
    os.system("calc.exe")

