from ScoreSheet_api import app
from flask import Flask, request, jsonify, json
from ScoreSheet_api.config.database import getDb
from ScoreSheet_api.helpers.DbUtillity import Convert_to_Json, Handle_error

import os
import pymysql

# initial database
cursor = getDb().cursor()


@app.route('/saveImage', methods=['POST'])
def uploadImage():
    if request.method == "POST":
        
        student_assignment_id = request.args.get('studentAssignmentId') 
        img = request.json['image']
        
        try:
            query = "UPDATE StudentAssignments SET Img=%s WHERE StudentAssignmentId=%s"
            cursor.execute(query,(img, student_assignment_id))
            return jsonify(True), 200
        
        except pymysql.Error as err:
            print(err)
            return Handle_error(err, 500)  

    
    
             

        
         