from ScoreSheet_api import app
from flask import Flask, request, jsonify, json
from ScoreSheet_api.config.database import getDb
from ScoreSheet_api.helpers.DbUtillity import Convert_to_Json, Handle_error

import pymysql

# initial database
cursor = getDb().cursor()


@app.route('/teachStudents', methods=['GET', 'POST'])
def getTeachStudents():
    
    teach_course_id = request.args.get('teachCourseId') 
    if(request.method == 'GET'):
        try: 
            query = "SELECT TS.TeachStudentId, S.StudentId, S.FirstName, S.LastName, S.NickName, TS.SecNo From TeachStudents TS INNER JOIN Students S ON TS.StudentId = S.StudentId WHERE TS.TeachCourseId = {0}".format(teach_course_id)
            cursor.execute(query)
            res = cursor.fetchall()
            
            if(res == None):
                print("No Content")
                return ('',204)
            
        
        except pymysql.Error as err:
            print(err)
            return Handle_error(err, 500)
    
    return jsonify(res), 200


@app.route('/countTeachStudents', methods=['GET'])
def getCountTeachStudents():
    
    teach_course_id = request.args.get('teachCourseId')
    if(request.method == 'GET'):
        
        try: 
            query = "Select COUNT(ts.TeachStudentId) AS Count FROM TeachCourses tc INNER JOIN TeachStudents ts ON tc.TeachCourseId = ts.TeachCourseId WHERE tc.TeachCourseId = {0}".format(teach_course_id)
            cursor.execute(query)
            res = cursor.fetchone()
            
            if(res == None):
                print("No Content")
                return ('',204)
        
        
        except pymysql.Error as err:
            print(err)
            return Handle_error(err, 500)
        
    return jsonify(res), 200

        

@app.route('/addTeachStudents', methods=['POST'])
def addTeachStudent():
    
    teach_course_id = request.args.get('teachCourseId') 
    if(request.method == 'POST'):
        students = request.json
        print(type(students))
        
        try:
            # find student in student system
            canInsert = True
            for std in students:
                print(type(std))
                
                if(not isinstance(std,dict)):
                    std = json.loads(std)
                
                print(std["StudentId"])
                query_find = "SELECT StudentId FROM Students WHERE StudentId = {0}".format(int(std["StudentId"]))
                cursor.execute(query_find)
                res = cursor.fetchone()
                
                if(res == None):
                    std["IsRegister"] = False
                    canInsert = False
                else:
                    std["IsRegister"] = True
                    
            #res = students
                
            # loop for insert
            if(canInsert == True):
                for std in students:
                    
                    if(not isinstance(std,dict)):
                        std = json.loads(std)

                    query = "INSERT INTO TeachStudents(StudentId, TeachCourseId, SecNo) VALUES(%s,%s,%s)"
                    res = cursor.execute(query,(int(std["StudentId"]), int(teach_course_id), int(std["SecNo"])))
                    std["TeachStudentId"] = cursor.lastrowid
                    getDb().commit()
                    
                    query = "INSERT INTO StudentAssignments (TeachStudentId) VALUES(%s)"
                    cursor.execute(query, int(std["TeachStudentId"]))
                    getDb().commit()
                
                getDb().close()
                res = students
            else:
                res = students
                return jsonify(res), 200

        except pymysql.Error as err:
            print(err)
            return Handle_error(err, 500)  
    
    return jsonify(res), 200


@app.route('/deleteTeachStudent', methods=['POST'])
def deleteTeachStudent():
    
    teachStudentId = request.args.get('teachStudentId')
    if(request.method == 'POST'):
        
        try:
            
            query = "Delete From StudentAssignments Where TeachStudentId = {0}".format(int(teachStudentId))
            cursor.execute(query)
            getDb().commit()
            
            query = "Delete From TeachStudents Where TeachStudentId = {0}".format(int(teachStudentId))
            cursor.execute(query)
            getDb().commit()
            
            return jsonify(True), 200
        
        except pymysql.Error as err:
            print(err)
            return Handle_error(err, 500)  
        
    return jsonify(False), 200