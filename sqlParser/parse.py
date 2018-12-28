
class SQLParser:

    Errorlist   = []
    tableAliasList = []
    selPos = []
    CurFile     = ""
    CurLine     = 0

    def parseSQL(self, filename):
    
        f = open(filename, 'r')
        self.CurrFile = filename
        firstComment = ""
        line = ""
        lineRemovedComment = ""

        #flags
        firstBlockCommentEnd = False
        inSelect = False
        inFrom = False
        inWhere = False
        inInsert = False
        inUpdate = False
        inSet = False

        selDepth = 0
        casePos = []
        insertPos = -1
        updatePos = -1
        self.tableAliasList.clear()
        self.selPos.clear()
        
        prevBracketPos = -1

        while True:

            self.CurLine += 1
            prevline = line
            prevlineRemovedComment = lineRemovedComment
            prevlineTokens = self.tokenize(prevlineRemovedComment)

            line = f.readline()
            lineRemovedComment = self.removeComment(line)
            lineTokens = self.tokenize(lineRemovedComment)
            lastSelStartPos = self.getLastSelStartPos()
            lastSelEndPos = lastSelStartPos + 6

            #최초 SQL 주석 확인
            if firstBlockCommentEnd == False:
                firstComment += line

                if line.find('*/') > -1:
                    firstBlockCommentEnd = True
                    self.checkFirstBlock(firstComment)
            else:
                #모두 대문자로 작성되어 있는지 확인
                self.checkLowerCase(lineRemovedComment)

                #콤마, 연산자 공백 체크
                self.checkOperator(lineRemovedComment)

                #금지구문 확인
                self.checkRestrictCase(lineTokens, lineRemovedComment)

                #이전 구문의 종류 저장
                if inSelect == True:
                    prevStatus = "SELECT"
                elif inFrom == True:
                    prevStatus = "FROM"
                elif inWhere == True:
                    prevStatus = "WHERE"
                elif inInsert == True:
                    prevStatus = "INSERT"
                elif inUpdate == True:
                    prevStatus = "UPDATE" 

                if lineTokens.count("SELECT") > 0:
                    
                    inSelect = True
                    inFrom = False
                    inWhere = False
                    inInsert = False
                    inUpdate = False

                    selDepth += 1
                    self.selPos.append(lineRemovedComment.find('SELECT'))
                    bracketPos = lineRemovedComment.find('(')
                    prevLineBracketPos = prevline.find('(')

                    if line.find('(') > -1:
                        prevBracketPos = line.find('(')

                    if line.find(')') > -1 and prevBracketPos != line.find(')'):
                        self.appendError("0010", "시작괄호와 종료괄호가 한 라인에 없는 경우 시작괄호 위치와 종료괄호 위치는 동일해야 함")
                    
                    # SELECT 이외에 다른 구문이 있는지 확인
                    if self.getAfterString(line, "SELECT") != "":
                        self.appendError("0015", "SELECT 기술 후 한 라인을 비워야 함")

                    # SELECT와 서브쿼리 시작 괄호는 다음 라인의 동일 위치에 기술
                    if bracketPos < lastSelStartPos or (prevLineBracketPos != lastSelStartPos and prevLineBracketPos > -1):
                        self.appendError("011", "서브쿼리의 SELECT는 시작 괄호 다음 라인의 동일 위치에 기술되어야 함")

                    # INSERT ... SELECT 구문에서 SELECT의 마지막 위치는 INSERT의 마지막 위치와 동일하게 기술
                    if prevStatus == "INSERT" and insertPos != lastSelStartPos:
                        self.appendError("0038", "INSERT ... SELECT 구문에서 SELECT의 마지막 위치는 INSERT의 마지막 위치와 동일하게 기술")

                elif  lineTokens.count('FROM') > 0:
                    
                    inSelect = False
                    inFrom = True
                    inWhere = False
                    inInsert = False
                    inUpdate = False

                    fromPos = line.find("FROM")

                    if self.isHaveComment(line) != False:
                        self.appendError("0005", "테이블은 [테이블명] 주석이 존재해야함")

                    if line.find('FROM') != lastSelStartPos + 2:
                        self.appendError("0023", "FROM의 마지막 위치는 SELECT 마지막 위치와 동일하게 기술")
                    
                    # FROM 절의 테이블명은 FROM 다음에 공백을 한 칸 입력하고 기술
                    if len(line) > fromPos + 4 and line[fromPos+4:fromPos+5] != " ":
                        self.appendError("0024", "FROM 절의 테이블명은 FROM 다음에 공백을 한 칸 입력하고 기술")

                elif lineTokens.count('WHERE') > 0:
                    
                    inSelect = False
                    inFrom = False
                    inWhere = True
                    inInsert = False
                    inUpdate = False

                    # SELECT 구문의 WHERE의 마지막 위치는 SELECT 마지막 위치와 동일하게 기술
                    if lineRemovedComment.find("WHERE") != lastSelStartPos + 1:
                        self.appendError("0030", "SELECT 구문의 WHERE의 마지막 위치는 SELECT 마지막 위치와 동일하게 기술")


                # 집합연산자(UNION, MINUS, INTERSECT)는 동일 레벨의 SELECT 절 시작 위치에 기술
                elif (lineTokens.count("UNION") > 0 or lineTokens.count("MINUS") > 0 or lineTokens.count("INTERSECT") > 0):               
                    if (line.find("UNION") > -1 and lastSelStartPos != line.find("UNION")) or (line.find("MINUS") > -1 and lastSelStartPos != line.find("MINUS")) or (line.find("INTERSECT") > -1 and lastSelStartPos != line.find("INTERSECT")):
                        self.appendError("0009", "집합연산자(UNION, MINUS, INTERSECT)는 동일 레벨의 SELECT 절 시작 위치에 기술")

                elif lineTokens.count("INSERT") > 0:
                    
                    inSelect = False
                    inFrom = False
                    inWhere = False
                    inInsert = True
                    inUpdate = False

                    insertPos = lineRemovedComment.find("INSERT")

                    # INSERT 기술 후 한 라인을 비우고 INSERT 마지막 위치와 동일하게 INTO 기술
                    if self.isLastToken(lineTokens, "INSERT") != False:
                        self.appendError("0032", "INSERT 기술 후 한 라인을 비우고 INSERT 마지막 위치와 동일하게 INTO 기술")

                elif lineTokens.count("UPDATE") > 0:
                    
                    inSelect = False
                    inFrom = False
                    inWhere = False
                    inInsert = False
                    inUpdate = True

                    updatePos = lineRemovedComment.find("UPDATE")

                elif lineTokens.count("SET") > 0 :

                    inSelect = False
                    inFrom = False
                    inWhere = False
                    inInsert = False
                    inUpdate = False
                    inSet = True

                #  SELECT COLUMN CHECK
                if inSelect == True:

                    if lineTokens.count("CASE") > 0:
                        casePos.append(lineRemovedComment.find("CASE"))

                    if self.isHaveComment(line) != False:
                        self.appendError("0004", "컬럼은 컬럼명 주석이 존재해야 함")

                    # 컬럼 별칭은 AS를 사용해야 함
                    if self.checkColumnAlias(lineRemovedComment) == False:
                        self.appendError("0018", "컬럼의 별칭은 AS를 명시한 후 기술")

                    # SELECT 컬럼 리스트는 명시적으로 기술(* 사용 금지)
                    if lineTokens.count('*') > 0:
                        self.appendError("0016", "SELECT 컬럼 리스트는 명시적으로 기술(* 사용 금지)")

                    # SELECT 컬럼 리스트는 1라인에 1 컬럼만 기술
                    if lineTokens.count(",") > 1:
                        self.appendError("0017", "SELECT 컬럼 리스트는 1라인에 1 컬럼만 기술")

                    # CASE문의 CASE 시작 위치와 END 시작 위치는 동일
                    if lineTokens.count("END") > 0 and lineRemovedComment.find("END") != casePos.pop():
                        self.appendError("0020", "CASE문의 CASE 시작 위치와 END 시작 위치는 동일")

                    # 스칼라 서브 쿼리는 사용 지양
                    if lineTokens.count("SELECT") > 0:
                        self.appendError("0021", "스칼라 서브 쿼리는 사용 지양")

                if inFrom == True:
                    # FROM 절에 조인 테이블 서술 금지
                    if lineTokens.count(",") > 0:
                        self.appendError("0025", "FROM 절에 조인 테이블 서술 금지")

                    # 테이블 별칭은 T로 시작하고, 2자 이상이며 유일해야 함
                    if self.checkTableAlias(lineTokens) == False:
                        self.appendError("0022", "테이블 별칭은 T로 시작하고, 2자 이상이며 유일해야 함")

                    #JOIN 절의 INNER, LEFT, RIGHT, FULL의 마지막 위치는 SELECT 마지막 위치와 동일하게 기술
                    if self.checkIncludeValues(lineTokens, ["INNER", "LEFT", "RIGHT", "FULL", "ON"]) == True:
                        if self.checkEndPosition(lastSelEndPos, lineRemovedComment, ["INNER", "LEFT", "RIGHT", "FULL"]) == False:
                            self.appendError("0026", "JOIN 절의 INNER, LEFT, RIGHT, FULL의 마지막 위치는 SELECT 마지막 위치와 동일하게 기술")

                        #JOIN 절의 ON의 마지막 위치는 SELECT 마지막 위치와 동일하기 기술
                        if self.checkEndPosition(lastSelEndPos, lineRemovedComment, "ON") == False:
                            self.appendError("0029", "JOIN 절의 ON의 마지막 위치는 SELECT 마지막 위치와 동일하기 기술")

                    if self.checkIncludeValues(lineTokens, "JOIN") == True:
                        
                        #INNER JOIN 구문에서 INNER 생략 금지
                        if self.checkIncludeValues(lineTokens, ["INNER", "LEFT", "RIGHT", "FULL"]) == False:
                            self.appendError("0027", "INNER JOIN 구문에서 INNER 생략 금지")

                        #JOIN 절의 테이블명은 JOIN 다음에 공백을 한 칸 입력하고 기술
                        if self.isLastToken(lineTokens, "JOIN") == False:
                            strAfterJoin = self.getAfterString(lineRemovedComment, "JOIN")
                            if strAfterJoin[0] != " " or strAfterJoin[1] == " " :
                                self.appendError("0028", "JOIN 절의 테이블명은 JOIN 다음에 공백을 한 칸 입력하고 기술")
                                    

                if inWhere == True:
                    # LIKE 절은 %, _ 문자와 같이 사용되어야 함
                    if lineTokens.count("LIKE") > 0 and (lineTokens.count("%") == 0 or lineTokens.count("_") == 0):
                        self.appendError("0013", "LIKE 절은 %, _ 문자와 같이 사용되어야 함")
                
                if inInsert == True:
                    #INSERT 대상 테이블명은 INTO 다음에 공백을 한 칸 입력하고 기술
                    if lineTokens.count("INTO") > 0 and self.isLastToken(lineTokens, "INTO") == True:
                        self.appendError("0033", "INSERT 대상 테이블명은 INTO 다음에 공백을 한 칸 입력하고 기술")
                    
                    #INSERT 컬럼 리스트의 괄호는 테이블명 다음 라인의 테이블명 시작 위치에 기술
                    if lineTokens.count("INTO") > 0 and lineTokens.count(")") > 0:
                        self.appendError("0034", "INSERT 컬럼 리스트의 괄호는 테이블명 다음 라인의 테이블명 시작 위치에 기술")

                    #INSERT 컬럼 리스트는 명시적으로 기술(컬럼 리스트 생략 금지)
                    if lineTokens.count("VALUES") > 0 and prevlineTokens.count("INTO") > 0 :
                        self.appendError("0035", "INSERT 컬럼 리스트는 명시적으로 기술(컬럼 리스트 생략 금지)")

                    #INSERT ... VALUES 구문에서 VALUES 마지막 위치는 INSERT 마지막 위치와 동일하게 기술
                    if lineTokens.count("VALUES") > 0 and insertPos != lineRemovedComment.find("VALUES"):
                        self.appendError("0036", "INSERT ... VALUES 구문에서 VALUES 마지막 위치는 INSERT 마지막 위치와 동일하게 기술")

                    #INSERT ... VALUES 구문에서 VALUES 시작 괄호는 VALUES 다음에 공백을 한 칸 입력하고 이어서 기술
                    if lineTokens.count("VALUES") > 0 and lineTokens.count("(") == 0:
                        self.appendError("0037", "INSERT ... VALUES 구문에서 VALUES 시작 괄호는 VALUES 다음에 공백을 한 칸 입력하고 이어서 기술")

                if inUpdate == True:
                    updateNextToken = self.getNextToken(lineTokens, "UPDATE")

                    #UPDATE 테이블명은 UPDATE 기술 후 한 라인을 비우고 UPDATE 마지막 위치에서 공백을 한 칸 입력하고 기술
                    if lineTokens.count("UPDATE " + updateNextToken) > 0:
                        self.appendError("0039", "UPDATE 테이블명은 UPDATE 기술 후 한 라인을 비우고 UPDATE 마지막 위치에서 공백을 한 칸 입력하고 기술")

                if inSet == True:

                    #UPDATE 구문에서 SET은 테이블명 다음 라인에서 SET 마지막 위치와 UPDATE 마지막 위치와 동일하게 기술
                    if lineTokens.count("SET") > 0 and lineRemovedComment.find("SET") != (updatePos + 3):
                        self.appendError("0040", "UPDATE 구문에서 SET은 테이블명 다음 라인에서 SET 마지막 위치와 UPDATE 마지막 위치와 동일하게 기술")

                    #UPDATE 컬럼 리스트에 괄호가 필요한 경우에는 SET 다음에 공백을 한 칸 입력하고 기술
                    if lineTokens.count("(") > 0 and lineTokens.count("SET") == 0:
                        self.appendError("0041", "UPDATE 컬럼 리스트에 괄호가 필요한 경우에는 SET 다음에 공백을 한 칸 입력하고 기술")

                    #UPDATE 컬럼 리스트는 괄호가 없는 경우에는 SET 다음에 공백을 한 칸 입력하고 기술하고, 괄호가 있는 경우에는 시작 괄호의 다음 라인의 시작괄호와 동일한 위치에 기술
                    if lineTokens.count("(") > 0 and self.isLastToken(lineTokens, "(") == False:
                        self.appendError("0042", "UPDATE 컬럼 리스트는 괄호가 없는 경우에는 SET 다음에 공백을 한 칸 입력하고 기술하고, 괄호가 있는 경우에는 시작 괄호의 다음 라인의 시작괄호와 동일한 위치에 기술")

                    #UPDATE SET (...) = (SELECT 구문에서 = 은 SET 종료 괄호 다음 라인의 SET 마지막 위치에 기술
                    if lineTokens.count("=") > 0 and lineRemovedComment.find("=") != (updatePos + 6):
                        self.appendError("0043", "UPDATE SET (...) = (SELECT 구문에서 = 은 SET 종료 괄호 다음 라인의 SET 마지막 위치에 기술")

            if not line: 
                break

        f.close()


    def checkLowerCase(self, source):

        #바인드 변수 제외
        source = self.removeVariables(source)

        if source.islower() == True:
            self.appendError("0001", "SQL 문장은 모두 대문자로 통일하여 사용(바인드 변수 제외)")

    def checkRestrictCase(self, tokens, source):

        if source.find("--") > -1: 
            self.appendError("0003", "SQL 내부 주석은 블록주석(/*, */) 사용")

        if source.find("/t") > -1:
            self.appendError("0006", "탭(TAB)문자는 사용하지 않음")

        if tokens.count("EXECUTE") > 0:
            self.appendError("0012", "DYNAMIC SQL 사용 금지")

        if tokens.count("MERGE") > 0:
            self.appendError("0014", "MERGE문 사용 금지")

        if tokens.count("DECODE") > 0:
            self.appendError("0019", "DECODE문 사용 금지")

    def checkFirstBlock(self, source):

        if (source.find("* SQL 설명") < -1 or source.find("* @업무레벨1") < -1 or source.find("* @업무레벨2") < -1 or source.find("* @비즈니스명") < -1 or source.find("* @작성자") < -1) :
            self.appendError("0002", "SQL 상단 주석 형식")

    def appendError(self, pCode, pMsg):

        ErrorMsg = pCode + "$$$" + pMsg + "$$$" + self.CurFile + "$$$" + self.CurLine
        self.Errorlist.append(ErrorMsg)         

    def removeVariables(self, src):
        startidx = 0
        endidx = 0

        while True:
            startidx = src.find(':')

            if startidx == -1:
                break
            else:
                endidx = src.find(' ', startidx)

            if endidx == -1:
                src = src[:startidx]
            else:
                src = src[:startidx] + src[endidx:]
        
        return src

    def getAfterString(self, src, val):

        
        rtn = ""
        startpos = src.find(val)
        
        if startpos > -1:
            rtn = src[startpos + len(val):]

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

        return rtn.strip()

    def isHaveComment(self, src):

        commentStartPos = src.find('/*')
        commentEndPos = src.find('*/')

        if commentStartPos > -1 and commentEndPos > -1:
            return True
        else:
            return False

    def checkOperator(self, src):

        chars = []

        chars = self.getNextChars(src, ",")
        for item in chars:
            if item != " ":
                self.appendError("0007", "콤마 뒤에는 공백 입력")
        
        operatorList = ['+', '-', '*', '/', '=', '>', '<', '>=', '<=', '<>', '!=', '^=']
        
        for item in operatorList:

            chars.clear()
            chars = self.getPrevChars(src, item)
            for item2 in chars:
                if item2 != " ":
                    self.appendError("0008", "연산자 좌우에는 공백 입력")

            chars.clear()
            chars = self.getNextChars(src, item)
            for item2 in chars:
                if item2 != " ":
                    self.appendError("0008", "연산자 좌우에는 공백 입력")
            


    def getPrevChars(self, src, val):
        
        rtn = []
        startPos = -1 

        while True:
            startPos = src.find(val, startPos+1)

            if startPos == 0:
                rtn.append(" ")
            elif startPos > -1:
                rtn.append(src[startPos -1: startPos])
            else:
                break

        return rtn

    def getNextChars(self, src, val):

        rtn = []
        startPos = -1

        while True:
            startPos = src.find(val, startPos+1)

            if (startPos + len(val)) == len(src):
                rtn.append(" ")
            elif startPos > -1:
                rtn.append(src[startPos + len(val): startPos + len(val) + 1])
            else:
                break

        return rtn

    def checkColumnAlias(self, src):
        rtn = True
        tokens = src.split(" ")
        tokenLength = len(tokens)

        print(tokenLength)

        if ((tokenLength == 2 and tokens[0] != ",") or (tokenLength == 3 and tokens[1] != "AS") or (tokenLength == 4 and tokens[2] != "AS")):
            rtn = False

        return rtn

    def findPositions(self, src, val):
        
        rtn = []
        pos = 0

        while True:
            pos = src.find(val, pos)

            if pos > -1 :
                rtn.append(pos)
            else:
                break
        
        return rtn

    def tokenize(self, src):
        
        src = src.replace("\t", " ")
        src = src.replace("(", " ( ")
        src = src.replace(")", " ) ")
        src = src.replace("%", " % ")
        src = src.replace("_", " _ ")
        src = src.replace("\n", "")
        src = src.replace("\r", "")
        tokens = src.split(" ")
        loopcnt = len(tokens)

        while True:
            if tokens[loopcnt-1] == "":
                del tokens[loopcnt-1]
            loopcnt -= 1
            if loopcnt == 0 :
                break

        return tokens

    def checkTableAlias(self, tokens):
        rtn = True
        tableAlias = ""

        if tokens.count("(") == 0 and tokens.count("ON") == 0 and len(tokens) > 0:
            if tokens[0] == "FROM":
                tableAlias = tokens[2]
            else:
                tableAlias = tokens[len(tokens) - 1]

        if tableAlias[0] != "T" or self.tableAliasList.count(tableAlias) > 0:
            rtn = False

        self.tableAliasList.append(tableAlias)

        return rtn

    def checkIncludeValues(self, tokens, checkval):
        rtn = False

        if type(checkval) == list:
            for item in checkval:
                if tokens.count(item) > 0:
                    rtn = True
                    break
        else:
            if tokens.count(checkval) > 0:
                rtn = True

        return rtn

    def checkEndPosition(self, refPos, line, checkval):
        rtn = True

        if type(checkval) == list:
            for item in checkval:
                if (line.find(item) > -1) and (refPos != line.find(item) + len(item)):
                    rtn = False
                    break
        else:
            if (line.find(checkval) > -1) and (refPos != line.find(checkval) + len(checkval)):
                rtn = False

        return rtn

    def isLastToken(self, tokens, checkval):
        rtn = False

        if len(tokens) > 0:
            if tokens[len(tokens) - 1] == checkval:
                rtn = True

        return rtn

    def getLastSelStartPos(self):
        
        if len(self.selPos) > 0:
            return self.selPos[len(self.selPos) -1]
        else:
            return -1

    def getNextToken(self, tokens, checkval):
        rtn = ""
        isNextItem = False

        for item in tokens:
            if item == checkval:
                isNextItem == True
            if isNextItem == True:
                rtn = item
                isNextItem == False

        return rtn