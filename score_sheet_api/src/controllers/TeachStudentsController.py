from score_sheet_api import app
from flask import Flask, request, jsonify, json
from score_sheet_api.src.config.database import getDb
from score_sheet_api.src.helpers.DbUtillity import Convert_to_Json, Handle_error, Covert_to_Object_Json

import pymysql

# initial database
cursor = getDb().cursor()

@app.route('/teachStudents', methods=['GET'])
def getTeachStudents():
    
    teach_course_id = request.args.get('teachCourseId') 
    if(request.method == 'GET'):
        try: 
            query = '''SELECT TS.TeachStudentId, S.StudentId, S.FirstName, S.LastName, S.NickName, TS.SecNo 
                    From TeachStudents TS 
                    INNER JOIN Students S ON TS.StudentId = S.StudentId 
                    WHERE TS.TeachCourseId = {0}'''.format(teach_course_id)
            cursor.execute(query)
            res = cursor.fetchall()
            headers = [ x[0] for x in cursor.description]
        
        except Exception as err:
            print(err)
            return Handle_error(err, 500)
            
    return Convert_to_Json(headers, res)


@app.route('/countTeachStudents', methods=['GET'])
def getCountTeachStudents():
    
    teach_course_id = request.args.get('teachCourseId')
    if(request.method == 'GET'):
        
        try: 
            query = '''Select COUNT(ts.TeachStudentId) AS Count FROM TeachCourses tc 
                    INNER JOIN TeachStudents ts ON tc.TeachCourseId = ts.TeachCourseId 
                    WHERE tc.TeachCourseId = {0}'''.format(teach_course_id)
            cursor.execute(query)
            res = Covert_to_Object_Json(cursor.description[0], cursor.fetchone())
        
        except pymysql.Error as err:
            print(err)
            return Handle_error(err, 500)
        
    return jsonify(res), 200

        

@app.route('/addTeachStudents', methods=['POST'])
def addTeachStudent():
    
    teach_course_id = request.args.get('teachCourseId') 
    if(request.method == 'POST'):
        '''
            => input body 
            {
                "StudentId": int
                "SecNo": int
            }
            => output body
            [
                {
                    "StudentId": int
                    "IsRegister": boolean
                    "SecNo":int
                }
            ]
        '''
        students = request.json
        
        
        try:
            insert_students = []
            for std in students:
                print(type(std))
                
                if(not isinstance(std,dict)):
                    std = json.loads(std)

                std_obj = {
                    "StudentId": std["StudentId"],
                    "IsRegister": False,
                    "SecNo": int(std["SecNo"])
                }

                # check student in system ?
                query_find = '''
                    SELECT StudentId 
                    FROM Students 
                    WHERE StudentId = {0}'''.format(int(std["StudentId"]))
                cursor.execute(query_find)
                res = cursor.fetchone()
                    
                if(res != None):
                    # check student duplicate on teach student ?
                    query_find = ''' 
                        SELECT T.TeachStudentId
                        FROM TeachStudents T
                        WHERE T.StudentId = {0} AND T.TeachCourseId = {1}
                    '''.format(std["StudentId"], teach_course_id)
                    cursor.execute(query_find)
                    teachStudent = cursor.fetchone()

                    if(teachStudent == None): 
                        std_obj["IsRegister"] = True
                
                insert_students.append(std_obj)
                
            # loop for insert
            for insert_student in insert_students:

                if(insert_student["IsRegister"]):
                    query = '''
                                INSERT INTO TeachStudents(StudentId, TeachCourseId, SecNo) 
                                VALUES(?,?,?)'''
                    cursor.execute(query,[int(insert_student["StudentId"]), int(teach_course_id), int(insert_student["SecNo"])])
                    cursor.commit()

                    cursor.execute("SELECT @@IDENTITY AS ID")
                    teachStudentId = cursor.fetchone().ID

                    # check assignment from teach course id
                    query = ''' 
                                SELECT AssignmentId 
                                FROM Assignments
                                WHERE TeachCourseId = {0}'''.format(teach_course_id)
                    cursor.execute(query)
                    assignmentIds = cursor.fetchall()

                    if(assignmentIds != None):
                        for assignmentId in assignmentIds:
                            q = '''
                                    INSERT INTO StudentAssignments (TeachStudentId,AssignmentId) 
                                    VALUES(?,?)'''
                            cursor.execute(q, (teachStudentId,assignmentId.AssignmentId))
                            cursor.commit()

            response = jsonify(insert_students)
            return jsonify(insert_students), 200

        except pymysql.Error as err:
            print(err)
            return Handle_error(err, 500)  


@app.route('/deleteTeachStudent', methods=['POST'])
def deleteTeachStudent():
    
    teachStudentId = request.args.get('teachStudentId')
    if(request.method == 'POST'):
        
        try:
            
            query = '''Delete From StudentAssignments 
                    Where TeachStudentId = ?'''
            cursor.execute(query, teachStudentId)
            cursor.commit()
            
            query = '''Delete From TeachStudents 
                    Where TeachStudentId = ?'''
            cursor.execute(query, teachStudentId)
            cursor.commit()
            
            return jsonify(True), 200
        
        except pymysql.Error as err:
            print(err)
            return Handle_error(err, 500)  
        
    return jsonify(False), 200