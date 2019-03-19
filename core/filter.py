#coding=utf-8
from core import configs, logs, special_cmd
import re, sys

def filter_stdin(input_string, input_cmd, yesno):
    (logger, fh) = logs.log(log_file=configs.CONFIG['logfile_debug'], log_fmode="a")
    return_cmd = input_cmd + input_string
    return_string = input_string

    logger.debug("{input_string: %s input_cmd: %s}" % ([input_string], [input_cmd]))

    # yes or no
    note = yesno
    # logger.debug("{3 note.yn: %s}" % note.yn)
    # if note.yn == True and input_string != 'q':
    #     return_cmd = input_cmd
    #     return_string = input_string
    #     logger.debug("{4 note.yn: %s}" % note.yn)
    #     logger.removeHandler(fh)
    #     return return_string, return_cmd

    if note.yn == True:
        return_cmd = input_cmd
        return_string = input_string
        if input_string == "q" or input_string == "n":
            note.yn = False
        # logger.debug("{5 note.yn: %s}" % note.yn)
        logger.removeHandler(fh)
        return return_string, return_cmd

    # 匹配 退格键
    if input_string == configs.KEYS['BACKSPACE']:
        return_cmd = input_cmd[:-1]
        #logger.debug("{return_string: %s return_cmd: %s}" % ([return_string], [return_cmd]))
        logger.removeHandler(fh)
        return return_string, return_cmd

    # 匹配 tab键, 向上键, 向下键
    if input_string == configs.KEYS['TAB']:
        return_cmd = input_cmd
        logger.removeHandler(fh)
        return return_string, return_cmd

    # 匹配 向上键, 向下键
    if input_string in (configs.KEYS['UP_ARROW'], configs.KEYS['DOWN_ARROW']):
        return_cmd = input_cmd
        logger.removeHandler(fh)
        return return_string, return_cmd

    if input_string == configs.KEYS['ENTER']:
        # 退出处理
        special_cmd.exit(input_cmd)

        if input_cmd == "":
            return_cmd = input_cmd
            #logger.debug("{return_string: %s return_cmd: %s}" % ([return_string], [return_cmd]))
            logger.removeHandler(fh)
            return return_string, return_cmd

        # s, c = special_cmd.help_cmd(input_cmd)
        # # 不等None 就是匹配到 help 命令
        # if s != None:
        #     return_string = s
        #     return_cmd = c
        #     #logger.debug("{return_string: %s return_cmd: %s}" % ([return_string], [return_cmd]))
        #     logger.removeHandler(fh)
        #     return  return_string, return_cmd

        s, c = allow_cmd(input_cmd)
        # 不等None 就是没有匹配到 允许的命令 (清除命令输入，然后回车)
        if s != None:
            return_string = s
            return_cmd = c
            #logger.debug("{return_string: %s return_cmd: %s}" % ([return_string], [return_cmd]))
            logger.removeHandler(fh)
            return  return_string, return_cmd

        s, c = deny_cmd(input_cmd)
        # 不等None 就是匹配到了 不允许的命令 (清除命令输入，然后回车)
        if s != None:
            return_string = s
            return_cmd = c
            #logger.debug("{return_string: %s return_cmd: %s}" % ([return_string], [return_cmd]))
            logger.removeHandler(fh)
            return  return_string, return_cmd

        return_cmd = ""
        #logger.debug("{return_string: %s return_cmd: %s}" % ([return_string], [return_cmd]))
        logger.removeHandler(fh)
        return return_string, return_cmd

    #logger.debug("{return_string: %s return_cmd: %s}" % ([return_string], [return_cmd]))
    logger.removeHandler(fh)
    return return_string, return_cmd

# 匹配 允许使用的命令
def allow_cmd(input_cmd):
    is_allow = False
    # 过滤命令： 只允许通过的
    cmd_allow = configs.CONFIG['cmd_allow']
    for allow in cmd_allow:
        r = re.findall(allow, input_cmd)
        (logger, fh) = logs.log(log_file=configs.CONFIG['logfile_debug'], log_fmode="a")
        #logger.debug("{from: %s re.findall: %s result: %s}" % ([input_cmd], [allow], [r]))
        logger.removeHandler(fh)
        if r != []:
            is_allow = True

    if is_allow == False:
        print("\r\n %s : 不是 - 允许使用的命令 ( 这玩意儿有 bug , 找作者！！！ ) \r\n" % [input_cmd])
        return_string = configs.KEYS['BACKSPACE'] * len(input_cmd) + configs.KEYS['ENTER']
        return_cmd = ""
        return return_string, return_cmd
    else:
        return None, None

def deny_cmd(input_cmd):
    is_allow = True
    cmd_deny = configs.CONFIG['cmd_deny']
    for deny in cmd_deny:
        r = re.findall(deny, input_cmd)
        (logger, fh) = logs.log(log_file=configs.CONFIG['logfile_debug'], log_fmode="a")
        #logger.debug("{from: %s re.findall: %s result: %s}" % ([input_cmd], [deny], [r]))
        logger.removeHandler(fh)
        if r != []:
            is_allow = False

    if is_allow == False:
        print("\r\n %s ：是 - 禁止使用的命令 \r\n" % [input_cmd])
        return_string = configs.KEYS['BACKSPACE'] * len(input_cmd) + configs.KEYS['ENTER']
        return_cmd = ""
        return return_string, return_cmd
    else:
        return None, None

def filter_channel(output_string):
    if re.findall(r'docker exec', output_string) == []:
        return True
    else:
        return False
