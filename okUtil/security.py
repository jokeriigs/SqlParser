import hashlib
import shutil
import os
from datetime import datetime, timedelta

valList = ['1afwefawf', '2awfawefawefawefw', '3www', '4sefa', '5qqqqwe', '6aasdfews', '7vvvvdsef']

def HashSHA256(val):

    hashSha = hashlib.sha256()
    hashSha.update(val.encode())

    rtn = hashSha.hexdigest()

    return rtn


a = (datetime.now() + timedelta(days = -14)).strftime('%Y%m%d')
b = (datetime.now() + timedelta(days = -8)).strftime('%Y%m%d')

print (a)
print (b)

fn = '20190410.ZIP'
comStr = fn[0:8]

if comStr >= a and comStr < b:
    print ('True')
else:
    print ('False')