import requests as rs
# lxml模块可用于解析 HTML。
from lxml import html
# textwrap模块用于将文本包装到特定宽度。
import textwrap


term = 'dog'

url = "http://www.dictionary.com/browse/"

# 为了执行搜索，我们在 URL 的末尾附加了该词。
resp = rs.get(f'{url}term')

# 我们需要使用resp.content而不是resp.text，因为html.fromstring()隐式地希望字节作为输入。 
# （resp.content以字节为单位返回内容，而resp.text以 Unicode 文本形式返回。
root = html.fromstring(resp.content)

# 解析内容。 主要定义位于span标签内部，该标签具有one-click-content属性。 
# 我们通过消除多余的空白和杂散字符来改善格式。 文字宽度最大为 50 个字符。 
# 请注意，此类解析可能会更改。
x = "//span[contains(@class, 'one-click-content')]"
for sel in root.xpath(x):
    if sel.text:
        s = sel.text.strip()
        if(len(s) > 3):
            print(textwrap.fill(s, width=50))