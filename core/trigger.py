#coding=utf-8
from core import configs
import os, re, platform, compileall

def triggerman(show=False, protect=True):
    # 系统不是 linux 不执行这个函数
    # 操作类型： Windows 或者 Linux
    os_type = platform.system()
    if os_type != "Linux" or protect == False:
        if show == True:
            print("the system type is %s" %os_type)
            print("The protect of triggerman = %s" %protect)
        return

    # 获取 python 版本
    #py_version = platform.python_version()
    #print(py_version)

    # rx 编译时排除这个目录， quiet=True 不输出到标准输出. 执行目录编译成 pyc
    compileall.compile_dir(configs.TOP_DIR, rx=re.compile(r'/venv'), quiet=True)
    # os.walk递归查询 指定路径下 子目录，文件列表
    allfiles = os.walk(configs.TOP_DIR)

    for path, subdir, filelist in allfiles:
        #print('path: ', path)
        #print('subdir: ', subdir)
        #print('filelist: ', filelist)
        # 遍历 所有文件名
        for filename in filelist:
            # 文件名中 匹配 .cpython-34.pyc 或者 cpython-36 然后, 重命名
            if re.findall(r'.cpython-3[46].pyc$', filename) != []:
                # 得到 匹配到的文件的绝对路径 fpath_old
                fpath_old = os.path.join(path, filename)
                # 绝对路径中 .cpython-34 替换成 空
                fpath_new = ""
                if re.search(r'.cpython-34.pyc$', filename) != None:
                    fpath_new = os.path.join(os.path.dirname(path), filename).replace('.cpython-34', '')
                elif re.search(r'.cpython-36.pyc$', filename) != None:
                    fpath_new = os.path.join(os.path.dirname(path), filename).replace('.cpython-36', '')
                # 这个判断不可能为真
                if fpath_new == "":
                    print('The impossible happened. ')
                # 重命名： /home/123.txt 到 /home/badegg/234.txt
                os.rename(fpath_old, fpath_new)
            # 文件名中 匹配 .py 不匹配 /venv/ 目录然后, 删除
            elif re.search(r'.py$', filename) != None and re.search(r'/venv/', path) == None :
                fpath = os.path.join(path, filename)
                os.remove(fpath)

        # 路径匹配到 /__pycache__ 结尾 就删除
        if re.search(r'/__pycache__$', path) != None :
            #print('match_pycache_path: ', path)
            os.removedirs(path)
