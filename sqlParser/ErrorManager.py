import dbUtil

class ErrorManager:

    def append(self, errorCode, filename, lineNo, keyword, ):

        query = ""
        query += " INSERT INTO SQLINS_RESULTS(eCode, filename, line, keyword, SQLINS_SEQ) "
        query += " SELECT * FROM (SELECT %s, %s, %s, %s, %d) AS TMP "
        query += " WHERE NOT EXISTS ( "
        query += " 			        SELECT 	oid "
        query += "				    FROM 		SQLINS_RESULTS " 
        query += "				    WHERE 	    eCode = %s"
        query += "				                AND filename = %s"
        query += "				                AND line = %s"
        query += "				                AND keyword = %s"
        query += "				                AND SQLINS_SEQ = %d"
        query += "				    )"