import threading
import requests
import json
from time import time, sleep


def printHello():
    params = {'name':'Kwon O Kung', 'job':'Engineer'}
    starttime = time()
    resp = requests.post('http://localhost/samples/jsonTest.php', data=params)
    endtime = time()

    print (endtime - starttime)

    # jsonData = resp.json()
    # print (jsonData['result'])


def loadManager(processingSecond):

    for i in range(1, processingSecond):
        t = threading.Thread(target=printHello)
        t.start()
        sleep(0.2)

    # if times == processingSecond:
    #     print ("Done !!!")
    # else:
    #     timer = threading.Timer(1, loadManager, args=(processingSecond, times))
    #     timer.start()

loadManager(3000)