#coding=utf-8
import os, sys

def setenv():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if base_dir not in sys.path:
        sys.path.append(base_dir)
setenv()
from core import main

if __name__ == "__main__":
    main.startapp()


