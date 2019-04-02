import os
from datetime import datetime
from time import time

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

        if logFilename == '':
            logFN = 'C:\\log\\' + datetime.now().strftime('LOG_%Y%m%d.log')
        else:
            logFN = logFilename

        f = open(logFN, 'a')
        f.write(datetime.now().strftime('[%Y-%m-%d %H:%M:%S] ') + msg + '\n')
        f.close()

instance = loger()
loger.logging('test')
loger.logging('test', 'c:\\l
    og\\test.log')