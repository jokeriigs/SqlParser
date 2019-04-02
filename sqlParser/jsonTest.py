import requests
import json
from time import time, sleep

params = {'name':'Kwon O Kung', 'job':'Engineer'}
starttime = time()
resp = requests.post('http://localhost/samples/jsonTest.php', data=params)
endtime = time()

print (endtime - starttime)

jsonData = resp.json()
print (jsonData['result'])