#coding=utf-8
from paramiko.py3compat import u
from core import configs, logs, filter
import sys, socket, termios, tty, select, traceback, re, time

def interactive(channel, command):
    # 获取原tty属性
    oldtty = termios.tcgetattr(sys.stdin)

    try:
        # 设置 tty 的属性
        tty.setraw(sys.stdin.fileno())
        tty.setcbreak(sys.stdin.fileno())
        channel.settimeout(0.0)

        # ssh连接进入主机后 执行命令 比如： 要进入docker 容器
        if command != "":
            channel.send(command + "\r")

        tm = 2
        input_cmd = ""

        while True:
            rlist, wlist, errlist = select.select([channel, sys.stdin], [], [])
            # 从标准输入和socket 获取数据然后写入标准输出
            if channel in rlist:
                try:
                    if tm > 0:
                        time.sleep(0.2)
                        tm = tm - 1
                    r = channel.recv(256)
                    output_string = u(r)

                    # 如果返回的长度为 0 (就是没有返回), 或者 返回的是exit 就退出程序(使用与进入第二层：比如在远程主机，进入了docker)
                    if len(output_string) == 0 or output_string == '\r\nexit\r\n':
                        sys.stdout.write('\r\nWelcome back again, Bye!\r\n')
                        break

                    (logger, fh) = logs.log(log_file=configs.CONFIG['logfile_debug'], log_fmode="a")
                    logger.debug("{out_string: %s}" % [output_string])
                    logger.removeHandler(fh)

                    ishow = filter.filter_channel(output_string)
                    if ishow == True:
                        sys.stdout.write(output_string)
                        sys.stdout.flush()
                except socket.timeout:
                    pass
            # 从标准输入获取输入的字符：然后，处理输入，对输入进行过滤
            if sys.stdin in rlist:
                input_string = funkey(stdinput=sys.stdin)
                # 命令过滤
                input_string, input_cmd = filter.filter_stdin(input_string=input_string, input_cmd=input_cmd)
                # 把输入的字符发送给 远程ssh (准确的说是：经过过滤过的输入)
                channel.send(input_string)
    except Exception as e:
        fe = traceback.format_exc()
        (logger, fh) = logs.log(log_file=configs.CONFIG['logfile_error'], log_fmode="a")
        logger.error("{ error }:%s \n %s" %(e, fe))
        logger.removeHandler(fh)
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldtty)

# 功能键处理
def funkey(stdinput):
    input_string = stdinput.read(1)
    # 如果是功能键
    if input_string == "\x1b":
        input_string = input_string + stdinput.read(2)
        # 只允许上下键 通过 其他的全当回车用
        if input_string in (configs.KEYS['UP_ARROW'], configs.KEYS['DOWN_ARROW']):
            #input_string = "\t"
            return input_string
        elif input_string in configs.KEYS['KEY_DENY1']:
            input_string = "\t"
            return input_string
        else:
            input_string = input_string + stdinput.read(1)
            if input_string in configs.KEYS['KEY_DENY2']:
                input_string = "\t"
                return input_string
            else:
                input_string = input_string + stdinput.read(1)
                if input_string in configs.KEYS['KEY_DENY3']:
                    input_string = "\t"
                    return input_string
                else:
                    input_string = "\t"
                    return input_string
    else:
        return input_string