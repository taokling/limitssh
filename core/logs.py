#coding=utf-8
from core import configs
import logging, logging.handlers, re, os

# log_path 日志文件绝对路径
# log_fmode 文件打开模式  和 open 的模式相同 a 是追加 w 是重新写入
# log_level 日志级别
def log(log_file, log_fmode='w', log_level=configs.CONFIG['loglevel']):
    log_path = os.path.join(configs.CONFIG['logpath'], log_file)
    # 日志文件句柄
    fhandle = logging.FileHandler(log_path, mode=log_fmode, encoding='utf-8')
    # 初始化日志
    logger = logging.getLogger("test")
    # 设置日志级别
    logger.setLevel(log_level)
    # 设置日志 输出格式
    #fmt = logging.Formatter('%(asctime)s %(levelname)s %(pathname)s %(filename)s %(lineno)d  %(message)s')
    fmt = logging.Formatter('%(asctime)s %(levelname)s %(pathname)s { %(lineno)d } %(message)s\n')

    logger.addHandler(fhandle)
    fhandle.setFormatter(fmt)
    # 返回日志对象和文件句柄，用于调用后移除 logger.removeHandler(fhandle)
    return logger, fhandle

def create_logfile():
    # 创建日志文件路径
    logpath = configs.CONFIG['logpath']
    if not os.path.exists(logpath):
        os.makedirs(logpath)
    # 创建空的日志文件
    for k in configs.CONFIG:
        if re.findall('^logfile_', k) != []:
            f = open(os.path.join(logpath, configs.CONFIG[k]), 'w')
            f.close()
