       SELECT 
              COL1 /* COL1 */
            , COL2 /* COL1 */
            , COL3 /* COL1 */
            , COL4 AS COL5 /* COL3 */
         FROM TAB2
         LEFT JOIN (
                   SELECT
                          COL11 /* COL11 */
                        , COL22 /* COL22 */
                     FROM TAB3 TG
                     LEFT OUTER JOIN (
                                     SELECT
                                            COL1
                                          , COL2
                                       FROM TAB10
                                      WHERE COL1 = '1'
                                     ) TA
                   ) TB
        WHERE COL5 != 'NOT GOOD'
          AND COL6 = 'GOOD'
          AND COL7 IN (
                      SELECT
                             COL111
                        FROM TAB4
                      )
          AND COL8 = 'GOOD'
          AND COL9 EXISTS (
                          SELECT
                                 COL1111
                            FROM TAB5
                          )
       UNION
       SELECT
              COL1111
         FROM TAB7
        WHERE COL2222 = 'TEST'
          AND COL4444 = 'TEST2';
