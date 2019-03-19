#coding=utf-8
from paramiko.py3compat import u
from core import configs, logs, filter
import sys

def output(receive):
    r = receive
    # 接收的字节码，分割成列表。
    rlist = r.split(b'\r\n')

    # (logger, fh) = logs.log(log_file=configs.CONFIG['logfile_debug'], log_fmode="a")
    # logger.debug("{receive length: %s}" % len(r))
    # logger.debug("{receive: %s}" % r)
    # logger.debug("{rlist : %s}" % [rlist])
    # logger.debug("{rlist[-1] : %s}" % rlist[-1])
    # logger.removeHandler(fh)

    rlist_rump = rlist[-1]
    rlist_len = len(rlist)
    # 如果 列表长度 1 而且 为空，这种情况发生了，那就意味着接收到的是空（那就可以退出了）
    if rlist_rump == "" and rlist_len == 1:
        sys.stdout.write('\r\nWelcome back again, Bye!\r\n')
        return "exit"
    # 如果 列表长度 > 1 而且 最后一个元素为空，那就说明 接收到的字节码 是以 b"\r\n" 结尾的
    # 在为每个元素结尾补回 b"\r\n" 时，就不用区别对待了。
    elif rlist_rump == b"" and rlist_len > 1:
        # 因为下面在每个元素后面补回b"\r\n", 所以最后的空元素应该删掉(因为原来的b"\r\n"会补回到前面每个元素后面)
        # 不删除就会多出一个b"\r\n"
        rlist = rlist[:-1]
        i = 0
        for rb in rlist:
            rlist[i] = rb + b"\r\n"
            #output_string = u(rlist[i])
            output_string = u_reconsitution(rlist[i])
            i = i + 1

            # (logger, fh) = logs.log(log_file=configs.CONFIG['logfile_debug'], log_fmode="a")
            # logger.debug("{rlist: %s}" % [rlist])
            # logger.debug("{output_string: %s}" % [output_string])
            # logger.removeHandler(fh)

            # 如果返回的长度为 0 (就是没有返回), 或者 返回的是exit 就退出程序(使用与进入第二层：比如在远程主机，进入了docker)
            if len(output_string) == 0 or output_string == 'exit\r\n':
                sys.stdout.write('\r\nWelcome back again, Bye!\r\n')
                return "exit"

            ishow = filter.filter_channel(output_string)
            if ishow == True:
                sys.stdout.write(output_string)
                sys.stdout.flush()
    # 如果 最后一个元素不为空，那就说明 接收到的字节码 不是以 b"\r\n" 结尾的
    # 在为每个元素结尾补回 b"\r\n" 时， 结尾的那个 元素就要不能 补回 b"\r\n"
    else:
        i = 0
        for rb in rlist:
            if i < rlist_len - 1:
                rlist[i] = rb + b"\r\n"
            else:
                rlist[i] = rb
            #output_string = u(rlist[i])
            output_string = u_reconsitution(rlist[i])
            i = i + 1

            # (logger, fh) = logs.log(log_file=configs.CONFIG['logfile_debug'], log_fmode="a")
            # logger.debug("{rlist: %s}" % [rlist])
            # logger.debug("{i: %s}" % i)
            # logger.debug("{output_string: %s}" % [output_string])
            # logger.removeHandler(fh)

            # 如果返回的长度为 0 (就是没有返回), 或者 返回的是exit 就退出程序(使用与进入第二层：比如在远程主机，进入了docker)
            if len(output_string) == 0 or output_string == '\r\nexit\r\n':
                sys.stdout.write('\r\nWelcome back again, Bye!\r\n')
                return "exit"
            # 过滤显示
            ishow = filter.filter_channel(output_string)
            if ishow == True:
                sys.stdout.write(output_string)
                sys.stdout.flush()
    return None

# 重新构造一个 和 paramiko.py3compat.u 一样的函数; 忽略非法字符 decode 使用非严格模式：strict
def u_reconsitution(s, encoding="utf8"):
    """cast bytes or unicode to unicode"""
    if isinstance(s, bytes):
        return s.decode(encoding, "ignore")
    elif isinstance(s, str):
        return s
    else:
        raise TypeError("Expected unicode or bytes, got {!r}".format(s))