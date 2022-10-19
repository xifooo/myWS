import sqlite3
from urllib.parse import urlparse
import matplot.pyplot as plt
from matplotlib.font_manager import FontProperties

db_path = '/Users/zhangdongsheng/Library/Application Support/Google/Chrome/Default/History'
conn = sqlite3.connect(db_path)

sql = '''
select url from  urls where 
datetime(last_visit_time/1000000-11644473600,'unixepoch') 
> '2019-05-01'
'''
cursor = conn.execute(sql)