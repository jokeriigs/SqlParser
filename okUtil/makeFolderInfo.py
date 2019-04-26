import os

def getDirectories(dirname):

    rtn = []

    items = os.listdir(dirname)

    for item in items:
        
        fullName = os.path.join(dirname, item)
        if os.path.isdir(fullName):
            rtn.append(fullName)
            rtn.extend(getDirectories(fullName))
  
    return rtn

def getDirectorySize(dirname):

    rtn = 0

    items = os.listdir(dirname)

    for item in items:
        fullName = os.path.join(dirname, item)
        if os.path.isdir(fullName):
            rtn += getDirectorySize(fullName)
        else:
            rtn += os.path.getsize(fullName)

    return rtn

folderList = getDirectories('C:\\Apache24')

for item in folderList:
    print (item + ":" + str(getDirectorySize(item)))