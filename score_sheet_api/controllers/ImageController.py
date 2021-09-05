from score_sheet_api import app
from flask import Flask, request, jsonify, json
from score_sheet_api.config.database import getDb
from score_sheet_api.helpers.DbUtillity import Convert_to_Json, Handle_error

import os
import pymysql
import werkzeug

# initial database
cursor = getDb().cursor()


# @app.route('/saveImage', methods=['POST'])
# def uploadImage():
#     if request.method == "POST":
        
#         student_assignment_id = request.args.get('studentAssignmentId') 
#         img = request.json['image']
        
#         try:
#             query = "UPDATE studentassignments SET img=%s WHERE StudentAssignmentId=%s"
#             cursor.execute(query,(img, int(student_assignment_id)))
#             return jsonify(True), 200
        
#         except pymysql.Error as err:
#             print(err)
#             return Handle_error(False, 500)  


@app.route('/saveImage', methods=['POST'])
def uploadImage():
    if(request.method == "POST"):

        try:
            teach_std_id = request.args.get('TeachStudentId')
            assignment_id = request.args.get('AssignmentId')
            if(request.files['image']):
                image = request.files['image']
                filename = werkzeug.utils.secure_filename(image.filename)

                # Find Student Assignment Id
                query_select_id = "select SA.StudentAssignmentId from studentassignments SA Where TeachStudentId = {0} AND AssignmentId = {1}".format(teach_std_id,assignment_id)
                cursor.execute(query_select_id)
                res = cursor.fetchone()
                student_assign_id = res["StudentAssignmentId"]

                # Check duplicate image
                query_select = "SELECT S.img FROM studentassignments S  WHERE StudentAssignmentId={0}".format(student_assign_id)
                cursor.execute(query_select)
                res = cursor.fetchone()

                if(res['img'] != None):
                    os.remove(app.root_path+res['img'])

                query = "UPDATE studentassignments SET img=%s WHERE StudentAssignmentId=%s"
                cursor.execute(query,('/static/'+filename, int(student_assign_id)))
                

                print(app.root_path)
                pathImage = os.path.join(app.root_path,'./static/',filename)
                print(pathImage)
                image.save(pathImage)
            
                return jsonify(student_assign_id), 200

            else:
                return jsonify(0), 204
            
        
        except Exception as err:
            print(err)
            return Handle_error(0, 500)
             

        
         