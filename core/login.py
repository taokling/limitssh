#coding=utf-8
from core import interactive, auth, configs, logs
import paramiko, termios, traceback, os

def login():
    try:
        host, port, username, password, cmd = auth.auth()

        tran = paramiko.Transport((host, port))
        tran.start_client()
        tran.auth_password(username, password)

        # 打开一个通道
        chan = tran.open_session()
        # 终端配置： 类型，大小
        t = configs.CONFIG['term']
        ptype = configs.CONFIG['type'][t]
        term_size = os.get_terminal_size()
        w = term_size.columns
        h = term_size.lines
        # 获取一个终端
        chan.get_pty(term=ptype, width=w, height=h)
        # 激活器
        chan.invoke_shell()

        interactive.interactive(chan, cmd)

        chan.close()
        tran.close()
    except Exception as e:
        ef = traceback.format_exc()
        (logger, fh) = logs.log(log_file=configs.CONFIG['logfile_error'], log_fmode="a")
        logger.error("{ error }:%s \n %s" %(e, ef))
        logger.removeHandler(fh)

