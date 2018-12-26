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

