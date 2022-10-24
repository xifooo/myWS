#!/usr/bin/env python3

import subprocess

cmd = [
    'git'
    ]
subprocess.call('ipconfig')

subprocess.call(['df', '-h']) # 数组作为参数运行命令
