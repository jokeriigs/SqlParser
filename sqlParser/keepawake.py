import time
import sys
import os

import ctypes

ES_CONTINUOUS        = 0x80000000
ES_AWAYMODE_REQUIRED = 0x00000040
ES_SYSTEM_REQUIRED   = 0x00000001
ES_DISPLAY_REQUIRED  = 0x00000002

ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED | ES_AWAYMODE_REQUIRED)

p = ['|', '/', '-', '\\']

os.system('cls')
while True:
	for i in range(0, 4):
		print('\r' + p[i] + ' Press Ctrl-C to allow computer to sleep', end='')
		try:
			time.sleep(2)
		except(KeyboardInterrupt):
			print('\nGoodbye')
			sys.exit()