
import pymysql

def getDb():

    # conn = pymysql.connect(

    #     user = 'root',
    #     host = 'localhost', 
    #     password = '27365410', 
    #     database = 'ScoreSheet', 
    #     autocommit = True, 
    #     charset = 'utf8mb4', 
    #     cursorclass = pymysql.cursors.DictCursor
    # )

    conn = pymysql.connect(

        user = 'b6308f2376f3a0',
        host = 'us-cdbr-east-04.cleardb.com', 
        password = 'fd4624b8', 
        database = 'heroku_27ddfa27b25fbc7', 
        autocommit = True, 
        charset = 'utf8mb4', 
        cursorclass = pymysql.cursors.DictCursor
    )


    return conn

    
