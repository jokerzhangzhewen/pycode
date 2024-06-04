# !/usr/bin/python3
# -*- coding: utf-8 -*-
# -------------------------------
# @Author : Code.K
# cron "59 59 23,10 * * *" script-path=xxx.py,tag=匹配cron用 定时建议一天2次
# const $ = new Env('联通阅读')
# 活动信息: 联通阅读专区 - 阅光宝盒(阅读得话费)、阅读打卡(抽5G流量和话费)
# 环境变量 名称 UnicomNumber 值填 手机号（没错，就是需要号码就行，不需要抓包！）
# 多账号 & 分开 , 最大支持5个号码 例如：15*******86&15*******87
# 

import random
import os
import sys
import platform
import subprocess
import time

from functools import partial
import concurrent.futures

file_url = 'https://mirror.ghproxy.com/https://raw.githubusercontent.com/Code-KKK/pycode/main/compiled/'

def check_environment(file_name):
    v, o, a = sys.version_info, platform.system(), platform.machine()
    print(f"Python版本: {v.major}.{v.minor}.{v.micro}, 操作系统类型: {o}, 处理器架构: {a}")
    if (v.minor in [8,9,10,11]) and o.lower() in ['linux'] and a.lower() in ['x86_64','aarch64']:
        print("当前环境符合运行要求")
        if o.lower() == 'linux':
            file_name += '.so'
            main_run(file_name, v.minor, o.lower(), a.lower())
    else:
        if not (v.minor in [8,9,10,11]):
            print("不符合运行要求: Python版本不是 3.8 ~ 3.11")
        if not (o.lower() in ['linux']):
            print(f"不符合运行要求: 操作系统类型[{o}] 支持：Linux")
        if not (a.lower() in ['x86_64','aarch64']):
            print(f"不符合运行要求: 当前处理器架构[{a}] 支持：x86_64 aarch64")

def main_run(file_name, py_v, os_info, cpu_info):
    if os.path.exists(file_name):
        file_name_ = os.path.splitext(file_name)[0]
        try:
            Code_module = __import__(file_name_)
            Code_module.run_main()
        except Exception as e:
            print(str(e)) #打印运行报错信息
            if 'ld-linux-aarch64.so' in str(e):
                print('检测当前系统环境缺失ld-linux-aarch64.so.1请在库里lib目录下载修复ld-linux-aarch64.so.1.sh运行')
    else:
        print(f"不存在{file_name}功能模块,准备下载模块文件")
        download_file(file_name, py_v, os_info, cpu_info,file_url)

def download_file(file_name, py_v, os_info, cpu_info, url):
    file_name_ = os.path.splitext(file_name)[0]
    if os_info == 'linux':
        url = url + f'{file_name_}/{file_name_}.cp3{py_v}-{cpu_info}-{os_info}.so'
    try:
        print(url)
        result = subprocess.run(['curl', '-I', '-s', '-o', '/dev/null', '-w', '%{http_code}', url], capture_output=True, text=True)
        if result.stdout.strip() == '404':
            print('服务器文件不存在,已停止下载')
        else:
            print('服务器文件存在，将开始下载')
            subprocess.run(["curl",'-#',"-o", file_name, url], check=True)
            print(f"{file_name}文件下载成功~开始执行~")
            check_environment(file_name_)
    except subprocess.CalledProcessError:
        print("下载失败，请检查 URL 或 网络问题。")

if __name__ == '__main__':
    print = partial(print, flush=True)
    check_environment("unicom")
    print('【联通阅读】运行完成！')
