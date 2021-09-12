
from score_sheet_api import app
from flask import Flask, request, jsonify, json
from score_sheet_api.config.database import getDb
from score_sheet_api.helpers.DbUtillity import Convert_to_Json, Handle_error

import os
import pymysql

# initial database
cursor = getDb().cursor()

@app.route('/')
def hello():
    print(os.getcwd())
    return 'Hello Score Sheet !';

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
            
            if(res == None):
                print("No content")
                return ('',204)
            
        
        except pymysql.Error as err:
            print(err)
            return Handle_error(err, 500)
            
    return jsonify(res), 200

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
            row_headers=[x[0].lower() for x in cursor.description]
            res = cursor.fetchall()
            
            if(res == None):
                return ('',204)
        
        except pymysql.Error  as err:
            print(err)
            return Handle_error(err, 500)
        
    return jsonify(res), 200


    