import os

params = [1,2,3,43,3]

def printErr(msg):

    if type(params) is str:
        print (params)
    elif type(params) is tuple or type(params) is list:
        for item in params:
            print(str(item))
    else:
        print('error')

printErr(params)