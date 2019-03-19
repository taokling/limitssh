#coding=utf-8
import os

def test():
    result = "test"
    cmd2 = "echo " + result + " >> /home/badegg/oto/logs/tmp.log"

    os.system(cmd2)