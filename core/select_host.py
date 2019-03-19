#coding=utf-8
from core import configs, logs
import os, sys, curses

def setenv():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if base_dir not in sys.path:
        sys.path.append(base_dir)
setenv()
from core import configs, logs

# 改变 屏幕有显示的 一个区域的颜色
def change_color(stdscr, position, lines):
    p = position
    # 与众不同的那个字符串的开始位置的 x, y 坐标
    y = p['y']*2 + 8
    x = p['x']*28 + 10
    # 比如：主机列表中的序号： 第 4 行 第 1个 那就是 3 * 2 + 0 = 6
    id = p['y']*2 + p['x']
    #(logger, fh) = logs.log(log_file=configs.CONFIG['logfile_debug'], log_fmode='a')
    #logger.debug("{y: %s x: %s }" %(y, x))
    #logger.removeHandler(fh)

    # 所有的都是 白色
    for i in range(lines):
        stdscr.addstr(i*2+8, 10, configs.HOSTS[i*2][1], curses.color_pair(1))
        stdscr.addstr(i*2+8, 38, configs.HOSTS[i*2+1][1], curses.color_pair(1))
    # 重新设置 被选中的 那个位置 显示的字符串 和 颜色对
    stdscr.addstr(y, x, configs.HOSTS[id][1], curses.color_pair(2))

# 这里的 stdscr 只是一个形式参数 用于接受 wrapper 传递过来的 window 对象
def screen_init(stdscr):
    (logger, fh) = logs.log(log_file=configs.CONFIG['logfile_debug'], log_fmode='a')
    stdscr.clear()
    stdscr.refresh()
    stdscr.scrollok(1)
    #height, width = stdscr.getmaxyx()
    #logger.debug("{height: %s width: %s screen }" %(height, width))
    curses.start_color()
    # 设置颜色对 下面设置了 3 个颜色对 黑底白字 黑底红字 黑底青蓝字
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)

    # 这个部分不需要 每次都改变，只需要显示一次，不刷新就不会消失
    stdscr.addstr(3, 33, "日志查看器", curses.color_pair(3))
    stdscr.addstr(6, 10, "请选择要查看日志的项目:", curses.color_pair(1))

    lines = int(len(configs.HOSTS)/2)
    position = {"x":0, "y":0}
    change_color(stdscr, position, lines)
    while True:
        # 获取键盘输入
        key = stdscr.getch()
        #logger.debug("{key: %s key type: %s color: %s}" % ([key], type(key), position))
        if key == 259 and position['y'] > 0:
            position['y'] = position['y'] - 1
        elif key == 258 and position['y'] < lines - 1:
            position['y'] = position['y'] + 1
        elif key == 260 and position['x'] > 0:
            position['x'] = position['x'] - 1
        elif key == 261 and position['x'] < 1:
            position['x'] = position['x'] + 1

        # 如果是方向键 就改变 颜色
        if key in [258, 259, 260, 261]:
            change_color(stdscr, position, lines)
        # 如果是确定键 就跳出循环 返回位置信息
        elif key == 10:
            #logger.debug("{key: %s type: %s}" % ([key], type(key)))
            break
        # 如果输入: q/Q 表示退出
        elif key == ord('q') or key == ord('Q'):
            stdscr.refresh()
            curses.endwin()
            logger.removeHandler(fh)
            sys.exit(0)

    stdscr.refresh()
    curses.endwin()
    logger.removeHandler(fh)
    return position

def select():
    # http://www.cnblogs.com/starof/p/4703820.html
    # curses.wrapper(screen_init) 这个函数会初始化 stdscr = initscr() 返回一个window对象：stdscr
    # 把 stdscr 传递给 函数 screen_init(stdscr) 的第一个参数：stdscr
    # screen_init(stdscr) 中的 stdscr 只是一个用于接受 wrapper的 window 对象的形式参数
    position = curses.wrapper(screen_init)
    (logger, fh) = logs.log(log_file=configs.CONFIG['logfile_debug'], log_fmode='a')

    host_id = position['y']*2 + position['x']
    #logger.debug("{position: %s host id: %s}" %(position, host_id))
    logger.removeHandler(fh)
    return host_id

if (__name__ == "__main__"):
    host_id = select()
