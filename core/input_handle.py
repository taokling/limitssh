#coding=utf-8

class InputHandle(object):
    """ this is a class """
    def __init__(self):
        self.yn = False

    def set_yn(self, yn=False):
        if yn == True:
            self.yn = yn
        elif yn == False:
            self.yn = yn
        else:
            print("parameter must be True or False!!!")