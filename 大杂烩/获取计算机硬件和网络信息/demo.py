#!/usr/bin/env python
# -*- encoding: utf-8 -*-
''' 
@File    :   demo.py
@Time    :   2022/11/02 21:34:50
'''
import platform as pf
import socket, re, uuid, json, psutil, logging


def get_computer_info():
    try:
        info = {}
        info['platform'] = pf.system()
        info['platform-release'] = pf.release()
        info['platform-version'] = pf.version()
        info['architecture'] = pf.machine()
        
        info['hostname'] = socket.gethostname()
        info['ip-address'] = socket.gethostbyname(socket.gethostname())
        
        info['mac-address'] = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
        
        info['processor'] = pf.processor()
        
        info['RAM'] = f"{str(round(psutil.virtual_memory().total / (1024.0 **3)))} GB"
        
        return json.dumps(info)
    
    except Exception as e:
        logging.exception(e)


# def main():
#     g = get_computer_info()
#     print(json.loads(g))


if __name__ == "__main__":
    # main()
    json.loads(get_computer_info())
