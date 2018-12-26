import os

class FileMgr:
    
    def getFullList(self, dirname, filter = ''):
        
        filelist = []

        fulllist = os.listdir(dirname)
        itemname = ""

        for item in fulllist:
            
            itemname = os.path.join(dirname, item)        
            
            if os.path.isdir(itemname) == True:
                filelist = filelist + self.getFullList(itemname, filter)

            if filter == '' or itemname.find(filter) > -1:
                filelist.append(itemname)       
        
        return filelist