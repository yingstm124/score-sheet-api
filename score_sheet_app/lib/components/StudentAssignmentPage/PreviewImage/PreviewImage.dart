import 'dart:convert';
import 'dart:io' as Io;
import 'dart:io';

import 'package:camera/camera.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:score_sheet_app/apis/PredictionApi.dart';
import 'package:score_sheet_app/apis/StudentAssignmentApi.dart';
import 'package:score_sheet_app/apis/PredictionApi.dart';
import 'package:score_sheet_app/apis/StudentScoreApi.dart';
import 'package:score_sheet_app/helpers/ConvertType.dart';
import 'package:score_sheet_app/models/Assignment.dart';
import 'package:score_sheet_app/models/PredictResult.dart';
import 'package:score_sheet_app/models/TeachCourse.dart';


class PreviewImage extends StatefulWidget{

  Function getStudentAssignment;
  Assignment assignment;
  TeachCourse teachCourse;
  XFile? image ;

  PreviewImage({
    required this.getStudentAssignment,
    required this.assignment,
    required this.teachCourse,
    this.image
  });

  @override
  _PreviewImage createState() => _PreviewImage(
      getStudentAssignment: getStudentAssignment,
      assignment:assignment,
      teachCourse: teachCourse,
      image: image
  );
}


class _PreviewImage extends State<PreviewImage> {

  Function getStudentAssignment;
  Assignment assignment;
  TeachCourse teachCourse;
  XFile? image ;

  PredictResult _predictResult = new PredictResult(StudentId: null, Scores: [], Message: "");

  _PreviewImage({
    required this.getStudentAssignment,
    this.image,
    required this.assignment,
    required this.teachCourse
  });

  void predictImage() async {
    final img = Io.File(image!.path);
    final predict = PredictApi.predict(assignment.AssignmentId, teachCourse.TeachCourseId, img)
        .then((value) => {
          setState(() {
          _predictResult = value;
          }),
        });
  }

  void setStudentId(int studentId) async {
    setState(() {
      _predictResult.StudentId = studentId;
    });
  }

  void setScores(int score, int index) async {
    setState(() {
      print('${index.toString()} : ${score.toString()}');
      _predictResult.Scores[index] = score;
    });
  }

  @override
  void initState() {
    // predict from image
    predictImage();
  }

  Widget TextFormFieldStudentIdWidget(int studentId){
    return new TextFormField(
      keyboardType: TextInputType.number,
      decoration: InputDecoration(labelText:  "Student Id : ${studentId.toString()}"),
      initialValue: "${_predictResult.StudentId.toString()}",
      onChanged: (String value) async {
        print(value);
        setStudentId(int.parse(value));
      },
    );
  }

  Widget TextFormFieldScoreWidget(List<dynamic> scores){
    List<Widget> list = [];
    for(var i=0; i < scores.length; i++){
      list.add(
          new TextFormField(
            keyboardType: TextInputType.number,
            decoration: InputDecoration(labelText:  "Score ${i+1} : ${scores[i].toString()}"),
            initialValue: "${_predictResult.Scores[i].toString()}",
            onChanged: (String value) async {
              print(value);
              setScores(int.parse(value),i);
            },
          ));
    }
    return new Column(
      children: list,
    );
  }
  
  Widget TotalScoreWidget(List<int> scores){
    return Container(
      padding: EdgeInsets.all(20),
      child: Row(
        mainAxisSize: MainAxisSize.max,
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: <Widget>[
          Text(
            'Total Score',
            style: TextStyle(
              fontSize: 20
            ),
          ),
          Text(
              '${scores.reduce((value, element) => value + element)}',
              style: TextStyle(
              fontSize: 20
            ),
          )
        ],
      )
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(image!.name.toString()),
      ),
      body: Center(
        child: _predictResult.StudentId != null ? SingleChildScrollView(
          padding: EdgeInsets.all(20),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: <Widget>[
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: <Widget>[
                  Column(
                    mainAxisAlignment: MainAxisAlignment.start,
                    children: <Widget>[
                      Text('${_predictResult.Message}'),
                      Text('${assignment.AssignmentName}'),
                      Text('${teachCourse.CourseName} (${teachCourse.CourseId})'),
                      Text('Semester ${teachCourse.Term}/${teachCourse.Year}')
                    ],
                  )
                ],
              ),
              Image.file(File(image!.path)),
              TextFormFieldStudentIdWidget(_predictResult.StudentId!),
              TextFormFieldScoreWidget(_predictResult.Scores),
              TotalScoreWidget(_predictResult.Scores.map((e) => ConvertType.intOrStringValue(e)).toList()),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceAround,
                children: <Widget>[
                  Expanded(
                      flex: 1,
                      child: Container(
                        margin: EdgeInsets.all(10),
                        child: ElevatedButton(
                          onPressed: () {
                            Navigator.pop(context);
                            print('Cancel');
                          },
                          child: const Text('Cancel'),
                        ),
                      )
                  ),
                  Expanded(
                      flex: 1,
                      child: Container(
                        margin: EdgeInsets.all(10),
                        child: ElevatedButton(
                          onPressed: () async {
                            print('Save As');
                            // predictImage();
                            if(_predictResult.TeachStudentId != null){
                              final _image = Io.File(image!.path);
                              final _saveImageSuccess = await StudentAssignmentApi.saveImage(_predictResult.TeachStudentId!, assignment.AssignmentId, _image);
                              print('save image success');
                              if(_saveImageSuccess){
                                final _saveScoreSuccess = await StudentScoreApi.saveScore(
                                    _predictResult.Scores,
                                    _predictResult.StudentId.toString(),
                                    assignment.AssignmentId,
                                    teachCourse.TeachCourseId,
                                    _predictResult.TeachStudentId!
                                );
                                await showDialog(
                                    context: context,
                                    builder: (BuildContext context) => AlertDialog(
                                      title: Text('Save Score Success'),
                                      content: Text('${_saveScoreSuccess.Message}'),
                                      actions: <Widget>[
                                        TextButton(
                                            onPressed: () => Navigator.pop(context, 'Ok'),
                                            child: Text("OK")
                                        ),
                                      ],
                                    ));
                                Navigator.of(context).pop();
                                await getStudentAssignment();
                              }
                              print('save score sucess !');
                            }
                            print('no save');

                          },
                          child: const Text('Save As'),
                        ),
                      )
                  )
                ],
              ),
            ],
          ),
        ) : Center(
          child: Text('loading ....'),
        )
      ),

    );
  }

}