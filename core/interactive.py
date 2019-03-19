#coding=utf-8
from core import configs, logs, filter, output, input_handle
import sys, socket, termios, tty, select, traceback, time, os

def interactive(channel, command):
    # 获取原tty属性
    oldtty = termios.tcgetattr(sys.stdin)

    try:
        # 设置 tty 的属性
        tty.setraw(sys.stdin.fileno())
        tty.setcbreak(sys.stdin.fileno())
        channel.settimeout(1.5)

        # ssh连接进入主机后 执行命令 比如： 要进入docker 容器
        if command != "":
            channel.send(command + "\r")

        # 获取终端大小
        term_size = os.get_terminal_size()
        w_old = term_size.columns
        h_old = term_size.lines

        tm = 2
        input_cmd = ""
        input_string = "\r"
        note = input_handle.InputHandle()
        left_arrow_count = 0
        right_arrow_count = 0
        while True:
            # 获取终端大小
            term_size = os.get_terminal_size()
            w = term_size.columns
            h = term_size.lines
            # 如果窗口大小变了，更更改
            if w != w_old or h != h_old:
                w_old = w
                h_old = h
                # 重置 虚拟终端的大小
                channel.resize_pty(w, h)
                continue
            # 更改 channel 会发生 InterruptedError 异常。
            try:
                rlist, wlist, errlist = select.select([channel, sys.stdin], [], [])
            except InterruptedError:
                continue

            # (logger, fh) = logs.log(log_file=configs.CONFIG['logfile_debug'], log_fmode="a")
            # logger.debug("{channel len: %s}" % dir(channel.in_buffer._buffer))
            # logger.debug("{dir(channel.recv): %s}" % help(channel.recv))
            # logger.debug("{channel : %s}" % channel.in_buffer._buffer)
            # logger.debug("{channel len: %s}" % len(channel.in_buffer._buffer))
            # logger.removeHandler(fh)

            # 从标准输入和socket 获取数据然后写入标准输出
            if channel in rlist:
                try:
                    # 启动交互 头两次等待一小会儿，然数据接受完整（为了登录时不显示 docker exec -it 进入容器这一步）
                    if tm > 0:
                        time.sleep(0.2*tm)
                        tm = tm - 1
                    # 接收多少个字节
                    r = channel.recv(1024)

                    # tab 补全
                    if input_string == '\t' and r[:2] != b"\r\n" and r[:1] != b"\x07" and r[-23:] != b"possibilities? (y or n)":
                        input_cmd = input_cmd + output.u_reconsitution(r)

                        # (logger, fh) = logs.log(log_file=configs.CONFIG['logfile_debug'], log_fmode="a")
                        # logger.debug("{input_string: %s r[:1]: %s }" % ([input_string], r[:1]))
                        # logger.debug("{input_cmd: %s r[:3]: %s }" % ([input_cmd], r[:3]))
                        # logger.removeHandler(fh)

                    # (logger, fh) = logs.log(log_file=configs.CONFIG['logfile_debug'], log_fmode="a")
                    # logger.debug("{1 note.yn: %s}" % note.yn)
                    recv_list = r.split(b'\r\n')
                    # logger.debug("{rlist : %s}" % recv_list)
                    # logger.debug("{r length : %s}" % len(r))
                    # logger.debug("{rlist[-1] : %s}" % rlist[-1])

                    # 更改 补全提示状态
                    if recv_list[-1] != b"--More--" and len(r) < 1024:
                        note.yn = False
                    elif recv_list[-1] == b"--More--":
                        note.yn = True
                    # logger.debug("{6 note.yn : %s}" % note.yn)
                    # logger.removeHandler(fh)

                    if input_string == "\t" and r[-23:] == b"possibilities? (y or n)":
                        note.yn = True

                    # (logger, fh) = logs.log(log_file=configs.CONFIG['logfile_debug'], log_fmode="a")
                    # logger.debug("{2 note.yn: %s}" % note.yn)
                    # logger.removeHandler(fh)

                    status = output.output(r)
                    if status == "exit":
                        break
                    elif status == None:
                        pass
                except socket.timeout:
                    pass
            # 从标准输入获取输入的字符：然后，处理输入，对输入进行过滤
            if sys.stdin in rlist:
                input_string = funkey(stdinput=sys.stdin)
                if input_string == "break":
                    break
                # elif input_string == "left_arrow\x1b[D":
                #     left_arrow_count = left_arrow_count + 1
                #     input_string = '\x1b[D'
                # elif input_string == "right_arrow\x1b[C":
                #     right_arrow_count = right_arrow_count + 1
                #     input_string = '\x1b[C'
                #
                # if len(input_cmd) == 0:
                #     pass
                # else:
                #     cursor_position = left_arrow_count - right_arrow_count
                #     if cursor_position <= 0:
                #         cursor_position = 0
                #     elif cursor_position >= len(input_cmd):
                #         cursor_position = len(input_cmd)
                #
                #     if input_string == "\x08" and cursor_position < len(input_cmd):
                #         input_cmd = input_cmd[:-(cursor_position + 1)] + input_cmd[-cursor_position:]

                # 命令过滤
                input_string, input_cmd = filter.filter_stdin(input_string=input_string, input_cmd=input_cmd, yesno=note)
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

    (logger, fh) = logs.log(log_file=configs.CONFIG['logfile_debug'], log_fmode="a")
    logger.debug("{ stdin.read(1): %s}" % [input_string])
    logger.removeHandler(fh)

    if len(input_string) == 0:
        return "break"
    # 如果是功能键
    if input_string == "\x1b":
        input_string = input_string + stdinput.read(2)

        (logger, fh) = logs.log(log_file=configs.CONFIG['logfile_debug'], log_fmode="a")
        logger.debug("{ stdin.read(2): %s}" % [input_string])
        logger.removeHandler(fh)

        # 只允许上下键 通过 其他的全当回车用
        if input_string in (configs.KEYS['UP_ARROW'], configs.KEYS['DOWN_ARROW']):
            #input_string = "\t"
            return input_string
        # elif input_string in (configs.KEYS['LEFT_ARROW']):
        #     #print("\r\n 不支持：左键，你输入的是：%s \r\n" %[input_string])
        #     input_string = 'left_arrow' + input_string
        #     return input_string
        # elif input_string in (configs.KEYS['RIGHT_ARROW']):
        #     #print("\r\n 不支持：右键，你输入的是：%s \r\n" %[input_string])
        #     input_string = 'right_arrow' + input_string
        #     return input_string
        elif input_string in configs.KEYS['KEY_DENY1']:
            print("\r\n 不支持：左右键，功能键 = (F1~F12、Home、Insert、Delete、End、PageUp、PageDown)，你输入的是：%s \r\n"
                  %[input_string])
            input_string = "\r"
            return input_string
        else:
            input_string = input_string + stdinput.read(1)
            if input_string in configs.KEYS['KEY_DENY2']:
                print(
                    "\r\n 不支持：左右键，功能键 = (F1~F12、Home、Insert、Delete、End、PageUp、PageDown)，你输入的是：%s \r\n"
                    % [input_string])
                input_string = "\r"
                return input_string
            else:
                input_string = input_string + stdinput.read(1)
                if input_string in configs.KEYS['KEY_DENY3']:
                    print(
                        "\r\n 不支持：左右键，功能键 = (F1~F12、Home、Insert、Delete、End、PageUp、PageDown)，你输入的是：%s \r\n"
                        % [input_string])
                    input_string = "\r"
                    return input_string
                else:
                    print(
                        "\r\n 不支持：左右键，功能键 = (F1~F12、Home、Insert、Delete、End、PageUp、PageDown)，你输入的是：%s \r\n"
                        % [input_string])
                    input_string = "\r"
                    return input_string
    else:
        return input_string