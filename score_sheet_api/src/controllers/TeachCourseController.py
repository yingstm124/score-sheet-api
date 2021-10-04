
from score_sheet_api import app
from flask import Flask, request, jsonify, json
from score_sheet_api.src.config.database import getDb
from score_sheet_api.src.helpers.DbUtillity import Convert_to_Json, Handle_error

import os
import pymysql
import socket

# initial database
cursor = getDb().cursor()

@app.route('/')
def hello():
    print(os.getcwd())
    return 'Hello Score Sheet ! http://{0}:{1}'.format(socket.gethostbyname(socket.gethostname()),5000)

@app.route('/teachCourses', methods=['GET'])
def getTeachCourses():
    
    if request.method == 'GET':
        
        try:
            query = '''
                SELECT TC.TeachCourseId, C.CourseId , C.CourseName, TC.Term, TC.Year 
                FROM TeachCourses TC 
                INNER JOIN Courses C on C.CourseId = TC.CourseId'''
            cursor.execute(query)
            res = cursor.fetchall()
            headers = [c[0] for c in cursor.description ]
            
            if(len(res) == 0):
                print("No content")
                return ('',204)
        
        except pymysql.Error as err:
            print(err)
            return Handle_error(err, 500)
            
    return Convert_to_Json(headers, res)

@app.route('/teachCourse', methods=['GET'])
def getTeachCourse():
    
    teach_course_id = request.args.get('teachCourseId')
    if request.method == 'GET':
        
        try: 
            query = '''
                SELECT TC.TeachCourseId, C.CourseId , C.CourseName, TC.Term, TC.Year 
                FROM TeachCourses TC 
                INNER JOIN Courses C on C.CourseId = TC.CourseId 
                WHERE TC.TeachCourseId = {0}'''.format(teach_course_id)
            cursor.execute(query)
            headers= [x[0] for x in cursor.description]
            res = cursor.fetchall()
            
            if(len(res) == 0):
                return ('',204)
        
        except pymysql.Error  as err:
            print(err)
            return Handle_error(err, 500)
        
    return Convert_to_Json(headers, res)


    