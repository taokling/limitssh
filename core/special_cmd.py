#coding=utf-8
import re, sys


# 匹配 到("exit" "exit " "exit  "), 那么退出
def exit(input_cmd):
    r = re.findall(r'^exit *$|^exit$', input_cmd)
    if r != []:
        print('\r\nWelcome back again, Bye!\r\n')
        sys.exit(0)

# 匹配 到("help" "help " "help  "),  那么查看 help的帮助文档
def help_cmd(input_cmd):
    r = re.findall(r'^help *$|^help$', input_cmd)
    #logger.debug("{from: %s re.findall help: %s RS: %s}" %(rcmd, res, rs))
    if r != []:
        return_string = " help\r"
        retrun_cmd = ""
        return return_string, retrun_cmd
    else:
        return None, None