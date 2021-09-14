
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:score_sheet_app/apis/AssignmentApi.dart';
import 'package:score_sheet_app/components/AssignmentPage/AssignmentPage.dart';
import 'package:score_sheet_app/components/Loading/Loading.dart';
import 'package:score_sheet_app/models/Assignment.dart';
import 'package:score_sheet_app/models/TeachCourse.dart';

class AssignmentAddForm extends StatefulWidget {
  Function getAssignments;
  Function getTotalAssignment;
  TeachCourse teachCourse;
   AssignmentAddForm({
     required this.teachCourse,
     required this.getAssignments,
     required this.getTotalAssignment });
  @override
  _AssignmentAddForm createState() => _AssignmentAddForm(teachCourse: teachCourse, getAssignments: getAssignments, getTotalAssignment: getTotalAssignment);
}

class _AssignmentAddForm extends State<AssignmentAddForm> {
  Function getAssignments;
  Function getTotalAssignment;
  TeachCourse teachCourse;
  _AssignmentAddForm({ required this.teachCourse, required this.getAssignments, required this.getTotalAssignment });

  final _formKey = GlobalKey<FormState>();
  final _assignmentName = TextEditingController();
  final _fullscore = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Form(
        key: _formKey,
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: <Widget>[
            TextFormField(
              controller: _assignmentName,
              decoration: InputDecoration(labelText:  "Enter Assignment name"),
              validator: (value){
                if(value == null || value.isEmpty){
                  return 'Please enter assignment name';
                }
                return null;
              },
            ),
            TextFormField(
              controller: _fullscore,
              decoration: InputDecoration(labelText: "Enter Full Score"),
              keyboardType: TextInputType.number,
              inputFormatters: <TextInputFormatter>[
                FilteringTextInputFormatter.digitsOnly
              ],
              validator: (value){
                if(value == null || value.isEmpty){
                  return 'Please enter score';
                }
                return null;
              },
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.end,
              children: <Widget>[
                Container(
                  margin: EdgeInsets.only(left: 10.0, top: 20.0),
                  child: OutlinedButton(
                      onPressed: () {
                        Navigator.of(context).pop();
                      },
                      child: Text(
                          'Cancel'
                      )
                  ),
                ),
                Container(
                  margin: EdgeInsets.only(left: 10.0, top: 20.0),
                  child: ElevatedButton(
                      onPressed: () async{

                        if(_formKey.currentState!.validate()){
                          print('add assignment');
                          final assignment = new Assignment(AssignmentId: 0, AssignmentName: _assignmentName.text, FullScore: int.parse(_fullscore.text));
                          final _addAssignmentSuccess = await AssignmentApi.addAssignment(teachCourse.TeachCourseId, assignment);

                          if(_addAssignmentSuccess){
                            print('add assignment sucess !');
                            getAssignments();
                            getTotalAssignment();
                            Navigator.of(context).pop();
                          }
                        }

                      },
                      child: Text(
                          'Submit'
                      )
                  ),
                )
              ],
            )
          ],
        )
    );
  }
}