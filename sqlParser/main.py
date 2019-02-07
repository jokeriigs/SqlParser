
import SqlStruct
import util
import ErrorManager

util = util.ParseUtil()
objError = ErrorManager.ErrorManager()

filelist = util.getSQLFiles('C:\\log\\')

for fileitem in filelist:
    print(fileitem)

filename = "test.sql"

f = open(filename, 'r', encoding='UTF8')

structs = []
bracketList = []
prevClauseNo = []
currFunction_list = []
checkedLine = []
casePosList = []
existBracketList = []
prevGroupList = []
prevPartList = []
groupList = ['SELECT', 'UPDATE', 'INSERT', 'DELETE']
partList = ['FROM', 'WHERE', 'GROUP', 'ORDER', 'SET', 'VALUES']
joinList = ['INNER', 'LEFT', 'RIGHT', 'FULL']
operatorList = ['+', '-', '*', '/', '=', '>', '<', '>=', '<=', '<>', '!=', '^=']
symbolList = [',', '(', ')']

depth = 0
currClauseNo = 0 
lineCount = 0
itemCount = -1
objectLineOrder = -1
oid = 0
group = ""
part = ""
prevGroup = ""
prevPart = ""
prevChar = ""
nextChar = ""
lineRemovedComment = ""
line = ""

isPrevOpenBracket = False
isComment = False
isLikeAfter = False
LikeClause = ""

prevSelectPos = -1
prevSelectLine = -1
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
    objectLineOrder = 0

    for item in tokens:

        if item == "/*":
            isComment = True

        #Check Group
        if groupList.count(item) > 0:

            if item == 'SELECT' and part == 'SELECT':
                objError.append("0021", filename, lineCount, item)
            prevGroup = group
            prevPart = part

            if prevGroup == "":
                group = item
            part = item
            
            # 이전 token이 "("일 경우 이전 문장 번호 저장
            if isPrevOpenBracket == True:
                prevClauseNo.append(currClauseNo)
                prevGroupList.append(prevGroup)
                prevPartList.append(prevPart)
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
                group = prevGroupList.pop()
                part = prevPartList.pop()

        #Check Part
        if partList.count(item) > 0:
            part = item    

        pos = line.find(item)

        oid += 1

        if symbolList.count(item) == 0:
            objectLineOrder += 1
        
        structs.append(SqlStruct.SqlStruct(oid, group, part, item, lineCount, depth, currClauseNo, pos, isComment, filename, objectLineOrder))

        if item  == '*/':
            isComment = False
        

bracketList.clear()

#구문 체크

headerComment = []

headerComment = util.getHeaderComment(structs)

if len(headerComment) == 0:
    objError.append("0002", filename, 0, 'HEADER COMMENT')

elif headerComment[0].keyword != '/*':
    objError.append("0002", filename, 0, 'HEADER COMMENT')

elif util.getCountStruct(headerComment, 'SQL') == 0 or util.getCountStruct(headerComment, '설명') == 0:
     objError.append("0002", filename, 0, 'SQL 설명')

elif util.getCountStruct(headerComment, '@업무레벨1') == 0:
     objError.append("0002", filename, 0, '@업무레벨1')

elif util.getCountStruct(headerComment, '@업무레벨2') == 0:
     objError.append("0002", filename, 0, '@업무레벨2')

elif util.getCountStruct(headerComment, '@비즈니스명') == 0:
     objError.append("0002", filename, 0, '@비즈니스명')

elif util.getCountStruct(headerComment, '@작성자') == 0:
     objError.append("0002", filename, 0, '@작성자')


for struct in structs:

    itemCount += 1

    #if struct.objectLineOrder == 0:

    if struct.isComment == False:

        isInCase = False

        if struct.keyword == 'SELECT':
            prevSelectPos = struct.pos
            prevSelectLine = struct.line
            prevInsertPos = util.getPos(structs, struct.no - 1, "INSERT")

            if len(bracketList) > 0:
                item = bracketList[len(bracketList) - 1]
                if struct.pos != item.pos:
                    objError.append("0011", struct.filename, struct.line, struct.keyword)

            if prevInsertPos > -1 and prevInsertPos != struct.pos:
                objError.append("0038", struct.filename, struct.line, struct.keyword)

        

        elif struct.keyword == '(':
            bracketList.append(struct)

        if struct.keyword.islower() == True:
            objError.append("0001", struct.filename, struct.line, struct.keyword)

        if struct.keyword == "--":
            objError.append("0003", struct.filename, struct.line, struct.keyword)

        if struct.keyword == ",":
            if struct.part == "SELECT":
                ### 괄호 안의 ',' 인지 검토
                i = 0
                isInBracket = False
                                
                while True:
                    i += 1

                    if itemCount - i < 0 or structs[itemCount - i].no != struct.no:
                        break

                    if structs[itemCount - i].keyword == "(":
                        isInBracket = True
                        break
                """    
                if isInBracket == False and structs[itemCount - 1].keyword != "*/":
                    objError.append("0004", struct.filename, struct.line, struct.keyword)
                """

        if struct.keyword == "\t":
            objError.append("0006", struct.filename, struct.line, struct.keyword)

        if struct.keyword == "UNION" or struct.keyword == "MINUS" or struct.keyword == "INTERSECT":
            if util.getPos(structs, struct.no, "SELECT") != struct.pos:
                objError.append("0009", struct.filename, struct.line, struct.keyword)

        if struct.keyword == ")" and len(bracketList) > 0:
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

        if struct.part == "SELECT" and struct.keyword != "SELECT" and symbolList.count(struct.keyword) == 0:
            if struct.line == prevSelectLine:
                objError.append("0015", struct.filename, struct.line, struct.keyword)
            elif struct.objectLineOrder == 0 and struct.pos != prevSelectPos + 7:
                objError.append("0015", struct.filename, struct.line, struct.keyword)

        if struct.keyword == "*" and struct.objectLineOrder == 0:
            objError.append("0016", struct.filename, struct.line, struct.keyword)

        if struct.keyword == "DECODE":
            objError.append("0019", struct.filename, struct.line, struct.keyword)

        if struct.keyword == "CASE":
            isInCase = True
            casePosList.append(struct.pos)

        if struct.keyword == "END":
            isInCase = False
            if struct.pos != casePosList.pop():
                objError.append("0020", struct.filename, struct.line, struct.keyword)

        if struct.keyword == 'WHERE':
            if struct.pos - 1 != util.getPos(structs, struct.no, struct.group):
                objError.append("0030", struct.filename, struct.line, struct.keyword)

        if struct.keyword == 'FROM':
            fromLineList = util.getPartLines(structs, struct.no, struct.part)

            if struct.pos - 2 != util.getPos(structs, struct.no, struct.group):
                objError.append("0023", struct.filename, struct.line, struct.keyword)

            
            for lineNo in fromLineList:
                linestructs = util.getLineStruct(structs, lineNo, False)

                tmpval = ''

                if util.getCountStruct(linestructs, 'FROM') > 0 and len(linestructs) > 2:
                    tmpval = linestructs[2].keyword
                elif util.getCountStruct(linestructs, ')') > 0 :
                    if len(linestructs) > 1:
                        tmpval = linestructs[1].keyword
                    
                elif util.getCountStruct(linestructs, 'JOIN') > 0 and util.getCountStruct(linestructs, ('(')) == 0 and len(linestructs) > 3:
                    tmpval = linestructs[len(linestructs)-1].keyword

                if tmpval != '':
                    if tmpval[0] != 'T' or len(tmpval) < 2 :
                        objError.append("0022", struct.filename, linestructs[0].line, tmpval)

                if util.getCountStruct(linestructs, ',') > 0:
                    objError.append("0025", struct.filename, struct.line, struct.keyword)


        if struct.keyword == 'EXISTS':
            if util.checkKeyword(structs, ['AND', 'OR'], struct.oid, struct.no, 'after') == True:
                objError.append("0031", struct.filename, struct.line, struct.keyword)

        if struct.keyword == 'INTO':
            
            linestructs = util.getLineStruct(structs, struct.line, True)

            if util.getPos(structs, struct.no, "INSERT") + 2 != struct.pos:
                objError.append("0032", struct.filename, struct.line, struct.keyword)

            if len(linestructs) < 2:
                objError.append("0033", struct.filename, struct.line, struct.keyword)
            else :
                if linestructs[1].keyword == '/*':
                    objError.append("0033", struct.filename, struct.line, struct.keyword)
                elif linestructs[1].pos != linestructs[0].pos + 5:
                    objError.append("0033", struct.filename, struct.line, struct.keyword)

            if len(linestructs) < 4:
                objError.append("0034", struct.filename, struct.line, struct.keyword)
            else:
                if linestructs[2].keyword != '/*' or util.getCountStruct(linestructs, '*/') == 0:
                    objError.append("0034", struct.filename, struct.line, struct.keyword)

        if struct.keyword == 'VALUES':
            
            prevItem = util.getPrevStruct(structs, struct.oid)
            nextItem = util.getNextStruct(structs, struct.oid)
            
            if not prevItem :
                objError.append("0035", struct.filename, struct.line, struct.keyword)
            else:
                if prevItem.keyword != ')':
                    objError.append("0035", struct.filename, struct.line, struct.keyword)

            if util.getPos(structs, struct.no, "INSERT") != struct.pos:
                objError.append("0036", struct.filename, struct.line, struct.keyword)

            if not nextItem :
                objError.append("0037", struct.filename, struct.line, struct.keyword)
            else:
                if nextItem.keyword != '(' or nextItem.line != struct.line:
                    objError.append("0037", struct.filename, struct.line, struct.keyword)

        
        if checkedLine.count(struct.line) == 0:

            linestructs = util.getLineStruct(structs, struct.line, False)
            smallBracketList = []
            isSmallInBracket = False
            wordCount = util.getWordCount(linestructs)
            
            if util.getCountStruct(linestructs, ",") > 0:

                for item2 in linestructs:
                    
                    if item2.keyword == '(':
                        smallBracketList.append(item2)
                        isSmallInBracket = True
                    elif item2.keyword == ')':
                        smallBracketList.pop()
                        if smallBracketList.count(')') == 0:
                            isSmallInBracket = False
                    
                    if isSmallInBracket == False and item2.keyword == "," and item2.objectLineOrder > 0:
                        objError.append("0017", struct.filename, struct.line, struct.keyword)
                        break
            
            if wordCount > 1 and struct.part == "SELECT":
                if isInCase == False and util.getCountStruct(linestructs, "CASE") == 0 and util.getCountStruct(linestructs, "AS") == 0:
                    objError.append("0018", struct.filename, struct.line, struct.keyword)

            if struct.part == 'FROM':

                if util.getCountStruct(linestructs, 'JOIN') > 0:

                    if joinList.count(linestructs[0].keyword) == 0:
                        objError.append("0027", struct.filename, struct.line, struct.keyword)
                    elif linestructs[0].pos + len(linestructs[0].keyword) != util.getPos(structs, struct.no, "SELECT") + 6:
                        objError.append("0026", struct.filename, struct.line, struct.keyword)

                    if len(linestructs) < 3:
                        objError.append("0028", struct.filename, struct.line, struct.keyword)

                if util.getCountStruct(linestructs, 'ON') > 0:

                    if linestructs[0].pos + len(linestructs[0].keyword) != prevSelectPos + 6:
                        objError.append("0029", struct.filename, struct.line, "ON")

                if util.getCountStruct(linestructs, 'FROM') > 0:

                    tokenCount = len(linestructs)

                    if tokenCount == 1:
                        objError.append("0024", struct.filename, struct.line, struct.keyword)
                    elif linestructs[1].pos != linestructs[0].pos + 5:
                        objError.append("0024", struct.filename, struct.line, struct.keyword)

            if struct.group == 'UPDATE':
                
                prevUpdatePos = util.getPos(structs, struct.no, "UPDATE")

                prevItem = util.getPrevStruct(structs, struct.oid)
                nextItem = util.getNextStruct(structs, struct.oid)

                updateCheckList = ['SET', 'UPDATE', ',', 'SELECT', 'WHERE', '=']

                if struct.keyword == 'UPDATE' and len(linestructs) > 1:
                    objError.append("0039", struct.filename, struct.line, struct.keyword)
                elif updateCheckList.count(struct.keyword) == 0 and struct.pos != prevUpdatePos + 7:
                    objError.append("0039", struct.filename, struct.line, struct.keyword)
                elif struct.keyword == 'SET' :
                    
                    if struct.pos != prevUpdatePos + 3:
                        objError.append("0040", struct.filename, struct.line, struct.keyword)
                    
                    if len(linestructs) < 2:
                        objError.append("0041", struct.filename, struct.line, struct.keyword)
                    elif linestructs[1] == '(' and len(linestructs) > 2:
                        objError.append("0042", struct.filename, struct.line, struct.keyword)

                elif struct.keyword == '=':

                    if len(linestructs) > 1:
                        objError.append("0044", struct.filename, struct.line, struct.keyword)
                
                if linestructs.count('SELECT') > 0:
                    if linestructs[0].keyword != 'SELECT':
                        objError.append("0045", struct.filename, struct.line, struct.keyword)
                
                if struct.keyword == 'UPDATE':
                    
                    updateStructs = util.getPartStructs(structs, struct.no, struct.part, struct.group)

                    if util.getCountStruct(updateStructs, 'WHERE') == 0:
                        objError.append("0046", struct.filename, struct.line, struct.keyword)

            if struct.keyword == 'DELETE':
                
                deleteStructs = util.getPartStructs(structs, struct.no, struct.part, struct.group)

                util.printStruct(deleteStructs, "dddd.log")

                if util.getCountStruct(deleteStructs, 'WHERE') == 0:
                    objError.append("0050", struct.filename, struct.line, struct.keyword)
                    
            checkedLine.append(struct.line)

util.printStruct(structs, '')