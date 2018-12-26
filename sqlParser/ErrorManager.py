import datetime

class ErrorManager:

    errorQuery = ''

    def append(self, errorCode, filename, lineNo, keyword):
        query = "VALUES ('" + errorCode + "'" \
        + ", '" + filename + "'" \
        + ", '" + str(lineNo) + "'" \
        + ", '" + keyword + "');"

        f = open("C:\\Log\\SqlParse.log", "a")
        now = datetime.datetime.now()
        f.write("[" + now.strftime('%Y-%m-%d %H-%M-%S') + "] :" + query + "\n")

        f.close()

        self.errorQuery += query