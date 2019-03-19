#coding=utf-8
from core import configs, logs, select_host, sendemail
import traceback, base64

def auth():
    try:
        host_id = select_host.select()
        # (logger, fh) = logs.log(log_file=configs.CONFIG['logfile_debug'], log_fmode="a")
        # logger.debug("{host id: %s}" % host_id)
        # logger.removeHandler(fh)
        host, port, username, password, cmd = confirm_host(host_id)

        return (host, port, username, password, cmd)
    except Exception as e:
        ef = traceback.format_exc()
        (logger, fh) = logs.log(log_file=configs.CONFIG['logfile_error'], log_fmode="a")
        logger.error("{ error }:%s \n %s" %(e, ef))
        logger.removeHandler(fh)

def confirm_host(host_id):
    k = configs.HOSTS[host_id][0]

    host = configs.SERVERS[k][0]
    port = configs.SERVERS[k][1]
    username = configs.SERVERS[k][2]
    password = base64.b64decode(configs.SERVERS[k][3].encode('utf-8')).decode('utf-8')
    cmd = configs.SERVERS[k][4]

    # 此处发送邮件：这是用户已经选择了主机，可以知道用户使用了哪个服务
    #sendemail.send_mail(host=k)
    return host, port, username, password, cmd

# password = getpass.getpass("%s@%s's password: " % (username, host))