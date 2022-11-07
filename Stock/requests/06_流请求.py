import requests as rs


# 流式传输 PDF 文件并将其写入磁盘
url = "https://docs.oracle.com/javase/specs/jls/se8/jls8.pdf"

local_filename = url.split('/')[-1]

# 在发出请求时将 stream设置为True，除非我们消耗掉所有数据或调用Response.close()，否则请求无法释放回池的连接。
r = rs.get(url, stream=True)

# 按 1 KB 的块读取资源，并将其写入本地文件。
with open(local_filename, 'wb') as f:
    for chunk in r.iter_content(chunk_size=1024):
        f.write(chunk)