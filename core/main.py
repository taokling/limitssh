#coding=utf-8
from core import configs, logs, login, trigger
import traceback

def startapp():
    '''this "main" is application entry'''
    try:
        trigger.triggerman(protect=True)
        login.login()
    except Exception as e:
        ef = traceback.format_exc()
        (logger, fh) = logs.log(log_file=configs.CONFIG['logfile_error'], log_fmode="a")
        logger.error("{ error }:%s \n %s" %(e, ef))
        logger.removeHandler(fh)

