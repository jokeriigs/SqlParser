import os
from datetime import datetime

class BaseClass:
    pass

class Singleton(object):

    _instance = None

    def __new__(cls, *args, **kwargs):

        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)

        return cls._instance

class loger(Singleton, BaseClass):

    def logging(msg, logFilename = ''):

        logFn = logFilename
        
        if logFilename == '':
            logFn = 'C:\\log\\' + datetime.now().strftime('log_%Y%m%d.log')

        f = open(logFn, 'a')

        if type(msg) is str:
            f.write(datetime.now().strftime('[%Y-%m-%d %H:%M:%S] ') + msg + '\n')
        elif type(msg) is  tuple or type(msg) is list:
            f.write(datetime.now().strftime('[%Y-%m-%d %H:%M:%S] ') + '\n')
            for item in msg:
                f.write(item + '\n')

        f.close() 