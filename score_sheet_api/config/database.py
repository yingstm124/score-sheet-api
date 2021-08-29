
import pymysql
import pymssql

def getDb():
    
    # conn = pymysql.connect(

    #     user = 'root',
    #     host = 'localhost', 
    #     password = '1234567890', 
    #     database = 'ScoreSheet', 
    #     autocommit = True, 
    #     charset = 'utf8mb4', 
    #     cursorclass = pymysql.cursors.DictCursor
    # )

    conn = pymysql.connect(

        user = 'root',
        host = 'localhost', 
        password = '27365410', 
        database = 'ScoreSheet', 
        autocommit = True, 
        charset = 'utf8mb4', 
        cursorclass = pymysql.cursors.DictCursor
    )

    return conn

    
