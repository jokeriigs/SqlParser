class ParseUtil:
    
    clauseNo = 0
    function_list = ['ROUND', 'TRUNC', 'MOD', 'UPPER', 'LOWER', 'INITCAP', 'LENGTH', 'INSTR', 'SUBSTR' \
    , 'LPAD', 'RPAD', 'LTRIM', 'RTRIM', 'TRIM', 'MONTHS_BETWEEN', 'IN', 'ADD_MONTHS', 'LAST_DAY', 'NEXT_DAY' \
    , 'TO_DATE', 'TO_NUMBER', 'TO_CHAR', 'NVL', 'DECODE', 'SUM', 'AVG', 'MIN', 'MAX', 'COUNT', 'EXIST']

    def tokenize(self, src):
            
            src = src.replace("\t", " \t ")
            src = src.replace("(", " ( ")
            src = src.replace(")", " ) ")
            src = src.replace("%", " % ")
            src = src.replace("_", " _ ")
            src = src.replace("\n", "")
            src = src.replace("\r", "")
            src = src.replace("/*", " /* ")
            src = src.replace("*/", " */ ")

            tokens = src.split(" ")
            loopcnt = len(tokens)

            while True:
                if tokens[loopcnt-1] == "":
                    del tokens[loopcnt-1]
                loopcnt -= 1
                if loopcnt == 0 :
                    break

            return tokens

    def getClauseNo(self):
        self.clauseNo += 1
        return self.clauseNo

    def getPrevChar(self, src, val):
        
        rtn = ""
        startPos = src.find(val) 

        if startPos > 0:
            rtn = src[startPos -1: startPos]

        return rtn

    def getNextChar(self, src, val):

        rtn = ""
        startPos = src.find(val) + len(val)

        if startPos > 0 and len(src) > startPos + 1:
            rtn = src[startPos:startPos + 1]            

        return rtn

    def removeComment(self, src):
        
        rtn = ""
        commentStartPos = src.find('/*')
        commentEndPos = src.find('*/')

        if commentStartPos > -1 :
            if commentEndPos > -1:
                rtn = src[:commentStartPos] + src[commentEndPos + 3:]
            else:
                rtn = src[:commentStartPos]

        return rtn

    def getLineStruct(self, structs, lineNo, isIncludeComment):

        rtn = []

        for item in structs:
            if item.line == lineNo:
                if isIncludeComment == True or (isIncludeComment == False and item.isComment == False):
                    rtn.append(item)

        return rtn

    def getPartLines(self, structList, clauseNo, part):
        rtn = []

        for item in structList:
            if item.no == clauseNo and item.part == part and rtn.count(item.line) == 0:
                rtn.append(item.line)

        return rtn 

    def getCountStruct(self, structList, val):

        rtn = 0

        for item in structList:
            
            if item.keyword == val:
                rtn += 1

        return rtn

    def getWordCount(self, structList):
        
        rtn = 0

        for item in structList:
            char = item.keyword[0]

            if char >= 'A' and char <= 'Z':
                rtn += 1

        return rtn

    def getPos(self, structList, no, keyword):
        rtn = -1

        for item in structList:
            if item.no == no and item.keyword == keyword:
                rtn = item.pos
                break

        return rtn

    def checkKeyword(self, structList, keyword, oid, clauseNo, option):
        rtn = False
        isSkip = False

        for item in structList:

            if option == 'before' and item.oid > oid:
                break

            if option == 'after' and item.oid < oid:
                isSkip = True
            else:
                isSkip = False

            if isSkip == False and item.no == clauseNo: 

                if type(keyword) is list:
                    if keyword.count(item.keyword) > 0:
                        rtn = True
                elif item.keyword == keyword:
                    rtn = True

        return rtn

    def getPrevStruct(self, structList, oid):

        rtn = None

        search_oid = oid - 1

        for item in structList:
            if item.oid == search_oid:
                rtn = item
                break

        return rtn

    def getNextStruct(self, structList, oid):

        rtn = None

        search_oid = oid + 1

        for item in structList:
            if item.oid == search_oid:
                rtn = item
                break

        return rtn   



    def printStruct(self, structList):

        f = open("C:\\Log\\SqlParseStruct.log", "w")

        for item in structList:
            f.write(str(item.line) + " : " + item.group + " : " + item.part + " : " + item.keyword + " : " + str(item.depth) + " : " + str(item.no) + "\r\n" )

        f.close()
        
        
