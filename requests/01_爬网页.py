import requests, re


url = "http://www.webcode.me"

resp = requests.get(url)

content = resp.text

# 剥离 www.webcode.me 网页的 HTML 标签。
rc = re.compile(r'<[^<]+?>')
stripped = rc.sub('', content)

print(stripped)

