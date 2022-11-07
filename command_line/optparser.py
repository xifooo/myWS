import sys
from optparse import OptionParser, IndentedHelpFormatter


class NoWrapFormatter(IndentedHelpFormatter) :
    def _format_text(self, text) :
        "[Does not] format a text, return the text as it is."
        return text

parser = OptionParser(
    prog = 'coolpython',
    usage = "%prog [OPTION]... FILE...",
    description = "酷python, 分享最专业的python技术",
    version = "1.1",
    formatter = NoWrapFormatter(),
    epilog = """\
这一段只是为了演示效果
    """)

parser.add_option("-n", "--name", action="store", help="姓名")

parser.add_option("-a", "--age", action="store", help="年龄")

parser.add_option('-o', "--out", action="store_true", help="是否输出")


if __name__ == '__main__':
    (options, args) = parser.parse_args(sys.argv[1:])
    print((options, args))
    print(options.age)