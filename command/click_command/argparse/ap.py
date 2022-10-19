import argparse


p = argparse.ArgumentParser()

p.add_argument('text', help='print some text')
p.add_argument('-v', '--value', nargs = 2, type=int, help='the sum of 2 int')

a = p.parse_args()

# 输出两个部分
print(a.text)
if a.value:
    print(a.value[0] + a.value[1])