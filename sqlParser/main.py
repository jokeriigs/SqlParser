import SqlStruct
import util
import ErrorManager

util = util.ParseUtil()
objError = ErrorManager.ErrorManager()
filename = "test.sql"

f = open(filename, 'r')

structs = []
bracketList = []
prevClauseNo = []
currFunction_list = []
groupList = ['SELECT', 'UPDATE', 'INSERT', 'DELETE']
partList = ['FROM', 'WHERE', 'GROUP', 'ORDER', 'SET', 'VALUES']
operatorList = ['+', '-', '*', '/', '=', '>', '<', '>=', '<=', '<>', '!=', '^=']

depth = 0
currClauseNo = 0 
lineCount = 0
itemCount = -1
oid = 0
group = ""
part = ""
prevChar = ""
nextChar = ""
lineRemovedComment = ""
line = ""

isPrevOpenBracket = False
isComment = False
isLikeAfter = False
LikeClause = ""

prevSelectPos = -1
prevOpenBracketPos = -1

while True:

    line = f.readline()
    
    if not line:
        break

    lineRemovedComment = util.removeComment(line)
    lineCount += 1    

    if lineRemovedComment.find(",") > 0 and lineRemovedComment.find(", ") < 0:
        objError.append("0007", filename, lineCount, "")

    if lineRemovedComment.find("EXECUTE IMMEDIATE") > 0:
        objError.append("0012", filename, lineCount, "")

    for item in operatorList:

        if lineRemovedComment.find(item) > 0:
            
            prevChar = util.getPrevChar(lineRemovedComment, item)
            nextChar = util.getNextChar(lineRemovedComment, item)
            
            if item == "<":
                if prevChar != " " or (nextChar != " " and nextChar != "=" and nextChar != ">"):
                    objError.append("0008", filename, lineCount, "1")
                    break
            elif (item == ">"  or item == "!" or item == "^") :
                if (prevChar != " " or (nextChar != " " and nextChar != "=")):
                    objError.append("0008", filename, lineCount, "2")
                    break
            elif item == "=" :
                if ((prevChar != " " and prevChar != "<" and prevChar != ">" and prevChar != "!" and prevChar != "^") \
                    or nextChar != " ") :
                    objError.append("0008", filename, lineCount, "4")
                    break
            elif prevChar != " " or nextChar != " ":
                objError.append("0008", filename, lineCount, "3")
                break

    tokens = util.tokenize(line)

    for item in tokens:

        if item == "/*":
            isComment = True

        #Check Group
        if groupList.count(item) > 0:
            group = item
            part = item
            
            # 이전 token이 "("일 경우 이전 문장 번호 저장
            if isPrevOpenBracket == True:
                prevClauseNo.append(currClauseNo)
                depth += 1

            currClauseNo = util.getClauseNo()

        if isPrevOpenBracket == True:
            bracketList.append(item)

        if item == "(":
            isPrevOpenBracket = True
        else:
            isPrevOpenBracket = False

        if item == ")" and len(bracketList) > 0:
            if groupList.count(bracketList.pop()) > 0:
                currClauseNo = prevClauseNo.pop()
                depth -= 1

        #Check Part
        if partList.count(item) > 0:
            part = item    

        pos = line.find(item)

        oid += 1
        structs.append(SqlStruct.SqlStruct(oid, group, part, item, lineCount, depth, currClauseNo, pos, isComment, filename))

        if item  == '*/':
            isComment = False

bracketList.clear()

#구문 체크
for struct in structs:

    itemCount += 1

    if struct.keyword == 'SELECT':
        prevSelectPos = struct.pos

        if len(bracketList) > 0:
            item = bracketList[len(bracketList) - 1]
            if struct.pos != item.pos:
                objError.append("0011", struct.filename, struct.line, struct.keyword)        

    elif struct.keyword == '(':
        bracketList.append(struct)

    if struct.keyword.islower() == True and struct.isComment == False:
        objError.append("0001", struct.filename, struct.line, struct.keyword)

    if struct.keyword == "--":
        objError.append("0003", struct.filename, struct.line, struct.keyword)

    if struct.keyword == ",":
        if struct.part == "SELECT":
            ### 괄호 안의 ',' 인지 검토 -- 코딩중
            i = 0
            isInBracket = False
                            
            while True:
                i += 1

                if itemCount - i < 0 or structs[itemCount - i].no != struct.no:
                    break

                if structs[itemCount - i].keyword == "(":
                    isInBracket = True
                    break
                
            if isInBracket == False and structs[itemCount - 1].keyword != "*/":
                objError.append("0004", struct.filename, struct.line, struct.keyword)

    if struct.keyword == "\t":
        objError.append("0006", struct.filename, struct.line, struct.keyword)

    if struct.keyword == "UNION" or struct.keyword == "MINUS" or struct.keyword == "INTERSECT":
        if prevSelectPos != struct.pos:
            objError.append("0009", struct.filename, struct.line, struct.keyword)

    if struct.keyword == ")":
        item = bracketList.pop()

        if struct.line != item.line and struct.pos != item.pos:
            objError.append("0010", struct.filename, struct.line, struct.keyword)

    if isLikeAfter == True:

        LikeClause += struct.keyword

        if LikeClause.count("'") > 1:
            LikeClause = LikeClause.replace("'", "")

            if len(LikeClause) <= 0:
                startChar = ""
                endChar = ""
            else:
                startChar = LikeClause[:1]
                endChar = LikeClause[len(LikeClause)-1:len(LikeClause)]
            
            if startChar != "%" and endChar != "%": 
                objError.append("0013", struct.filename, struct.line, struct.keyword)
            
            isLikeAfter = False

    if struct.keyword == 'LIKE':
        isLikeAfter = True

    if struct.keyword == 'MERGE':
        objError.append("0014", struct.filename, struct.line, struct.keyword)