#coding=utf-8
import logging, os, yaml

TOP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CFG_PATH = os.path.join(TOP_DIR, 'bin', 'configs.yml')

f = open(CFG_PATH, encoding='utf-8')
configs = yaml.load(f)
f.close()

CONFIG = configs
CONFIG.update({'loglevel': logging.DEBUG})

# 使用时 注释掉
CONFIG = {'type': ('vt100', 'vt102', 'vt220', 'vt320', 'xterm', 'linux', 'ansi'),
          'term': 4,
          'logpath': os.path.join(TOP_DIR, "logs"),
          'logfile_error': 'error.log',
          'logfile_debug': 'debug.log',
          'loglevel': logging.DEBUG,
          'cmd_allow': ['^cat *', '^cd *', '^exit *', '^find *', '^grep *', '^head *', '^help *', '^history *',
                        '^ls *', '^pwd *', '^tail *', '^wc *', '^ping *', '^ifconfig *'],
          'cmd_deny': ['^chmod', ' chmod ', '\\|chmod', '\\| chmod', '&chmod', '& chmod',
                       '^chown', ' chown ', '\\|chown', '\\| chown', '&chown', '& chown',
                       # '^ifconfig *', '^ip *', '^mysql *',
                       '^mkdir', ' mkdir ', '\\|mkdir', '\\| mkdir', '&mkdir', '& mkdir',
                       '^rm', ' rm ', '\\|rm', '\\| rm', '&rm', '& rm',
                       '^touch ', ' touch ', '\\|touch', '\\| touch', '&touch', '& touch',
                       '^vim '],
          }

# 键盘按键对应的值： （都是功能键）
KEYS = {
    'BACKSPACE': '\x08',
    'TAB': '\t',
    'ENTER': '\r',
    'UP_ARROW': '\x1b[A',
    'DOWN_ARROW': '\x1b[B',
    'LEFT_ARROW': '\x1b[D',
    'RIGHT_ARROW': '\x1b[C',
    'KEY_DENY1': ('\x1b[C', '\x1b[D', '\x1bOP', '\x1bOQ', '\x1bOR', '\x1bOS'),
    'KEY_DENY2': ('\x1b[2~', '\x1b[1~', '\x1b[3~', '\x1b[4~', '\x1b[5~', '\x1b[6~'),
    'KEY_DENY3': ('\x1b[15~','\x1b[17~','\x1b[18~','\x1b[19~','\x1b[20~','\x1b[21~','\x1b[23~','\x1b[24~','\x1b[25~'),
}

# 这个字典：
# key 是服务名
# value 列表：
#           [ip, port, username, password, command]
# command ：
#           连接进入主机后要执行的命令
# SERVERS = {"ims": ["47.99.206.90", 22, "root", "R3IyMDE4MDNld2Vz", "docker exec -it ims /bin/bash"],
#            'ims2': ["47.99.205.235", 22, "root", "R3IyMDE4MDNld2Vz", "docker exec -it ims2 /bin/bash"],
#            "api": ["47.99.206.90", 22, "root", "R3IyMDE4MDNld2Vz", "docker exec -it api /bin/bash"],
#            'api2': ["47.99.205.235", 22, "root", "R3IyMDE4MDNld2Vz", "docker exec -it api2 /bin/bash"],
#            "xixi": ["47.110.242.178", 22, "root", "R3IyMDE4MDNld2Vz", ""],
#            'xixi2': ["47.110.240.145", 22, "root", "R3IyMDE4MDNld2Vz", ""],
#            "bsp": ["47.99.206.90", 22, "root", "R3IyMDE4MDNld2Vz", "docker exec -it bsp /bin/bash"],
#            'evcs': ["47.110.242.178", 22, "root", "R3IyMDE4MDNld2Vz", ""],
#            'evcs2': ["47.110.240.145", 22, "root", "R3IyMDE4MDNld2Vz", ""],
#            "dp": ["47.99.211.134", 22, "root", "R3IyMDE4MDNld2Vz", ""],
#            'ep': ["47.99.211.134", 22, "root", "R3IyMDE4MDNld2Vz", ""],
#            'ep2': ["47.99.215.129", 22, "root", "R3IyMDE4MDNld2Vz", ""],
#            "test": ["192.168.111.200", 22, "root", "LGIsYnosYg==", "docker exec -it centos7-latest /bin/bash"],
#            'test2': ["10.8.3.110", 22, "root", "LGIsYnosYg==", "docker exec -it wealth /bin/bash"],
#            }

# 提示： 密码转换成字符串：
# s = ',b,bz,b'
# ps = base64.b64encode(s.encode('utf-8')).decode('utf-8')
# ps 就是字符串: "LGIsYnosYg=="
# SERVERS 字典说明： key:主机标签 value:[IP地址, 端口号, 用户名, 密码, 进入主机后执行的命令]
SERVERS = {"ims": ["47.99.206.90", 22, "root", "aGpnZ2Zkc2Z2IyQwMzA1", "docker exec -it ims /bin/bash"],
           'ims2': ["47.99.205.235", 22, "root", "aGpnZ2Zkc2Z2IyQwMzA1", "docker exec -it ims2 /bin/bash"],
           "api": ["47.99.206.90", 22, "root", "aGpnZ2Zkc2Z2IyQwMzA1", "docker exec -it api /bin/bash"],
           'api2': ["47.99.205.235", 22, "root", "aGpnZ2Zkc2Z2IyQwMzA1", "docker exec -it api2 /bin/bash"],
           "xixi": ["47.110.242.178", 22, "root", "aGpnZ2Zkc2Z2IyQwMzA1", ""],
           'xixi2': ["47.110.240.145", 22, "root", "aGpnZ2Zkc2Z2IyQwMzA1", ""],
           "bsp": ["47.99.206.90", 22, "root", "aGpnZ2Zkc2Z2IyQwMzA1", "docker exec -it bsp /bin/bash"],
           'evcs': ["47.110.242.178", 22, "root", "aGpnZ2Zkc2Z2IyQwMzA1", ""],
           'evcs2': ["47.110.240.145", 22, "root", "aGpnZ2Zkc2Z2IyQwMzA1", ""],
           "dp": ["47.99.211.134", 22, "root", "aGpnZ2Zkc2Z2IyQwMzA1", ""],
           'ep': ["47.99.211.134", 22, "root", "aGpnZ2Zkc2Z2IyQwMzA1", ""],
           'ep2': ["47.99.215.129", 22, "root", "aGpnZ2Zkc2Z2IyQwMzA1", ""],
           '110': ["10.8.3.110", 22, "root", "LGIsYnosYg==", ""],
           "200": ["192.168.111.200", 22, "root", "LGIsYnosYg==", ""],
           '110docker': ["10.8.3.110", 22, "root", "LGIsYnosYg==", "docker exec -it wealth /bin/bash"],
           "200docker": ["192.168.111.200", 22, "root", "LGIsYnosYg==", "docker exec -it centos7-latest /bin/bash"],
           }

# 这个用于展示，所以格式要整齐
HOSTS = (["api", "api    ( 47. 99.206. 90)"], ["api2", "api2   ( 47. 99.205.235)"],
         ["ims", "ims    ( 47. 99.206. 90)"], ["ims2", "ims2   ( 47. 99.205.235)"],
         ["evcs", "evcs   ( 47.110.242.178)"], ["evcs2", "evcs2  ( 47.110.240.145)"],
         ["xixi", "xixi   ( 47.110.242.178)"], ["xixi2", "xixi2  ( 47.110.240.145)"],
         ["ep", "ep     ( 47. 99.211.134)"], ["ep2", "ep2    ( 47. 99.215.129)"],
         ["bsp", "bsp    ( 47. 99.206. 90)"], ["dp", "dp     ( 47. 99.211.134)"],
         ["110", "110    ( 10.  8.  3.110)"], ["200", "200    (192.168.111.200)"],
         ["110docker", "110dock( 10.  8.  3.110)"], ["200docker", "200dock(192.168.111.200)"])










































