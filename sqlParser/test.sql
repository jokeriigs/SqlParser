       SELECT
              COL1 /* COL1 */
            , COL2 /* COL1 */
            , COL3 /* COL1 */
            , COL4 /* COL3 */
         FROM TAB2 ()
         (

         )
        WHERE COL4 != 'NOT GOOD'
          AND COL5 = 'GOOD'
          AND TAB LIKE '%'
