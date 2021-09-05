import 'dart:convert';
import 'dart:io' as Io;
import 'dart:io';

import 'package:camera/camera.dart';
import 'package:flutter/material.dart';
import 'package:score_sheet_app/apis/PredictionApi.dart';
import 'package:score_sheet_app/apis/StudentAssignmentApi.dart';
import 'package:score_sheet_app/apis/PredictionApi.dart';
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

  PredictResult _predictResult = new PredictResult(StudentId: 0, Scores: [], Message: "");

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
      print(studentId);
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

  Widget getScoreWidget(List<dynamic> scores){
    List<Widget> list = [];
    for(var i=0; i < scores.length; i++){
      list.add(
          new TextFormField(
            keyboardType: TextInputType.number,
            decoration: InputDecoration(labelText:  "Score ${i+1} : ${scores[i].toString()}"),
            initialValue: "${_predictResult.Scores[i].toString()}",
            onChanged: (String value) async {
              setScores(int.parse(value),i);
            },
          ));
    }
    return new Column(
      children: list,
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(image!.name.toString()),
      ),
      body: Center(
        child: SingleChildScrollView(
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
              TextFormField(
                keyboardType: TextInputType.number,
                decoration: InputDecoration(labelText:  "Student Id : ${_predictResult.StudentId.toString()}"),
                initialValue: "${_predictResult.StudentId.toString()}",
                onChanged: (String value) async {
                  if(value != null){
                    setStudentId(int.parse(value));
                  }
                },
              ),
              getScoreWidget(_predictResult.Scores),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceAround,
                children: <Widget>[
                  ElevatedButton(
                    onPressed: () {
                      Navigator.pop(context);
                      print('Cancel');
                    },
                    child: const Text('Cancel'),
                  ),
                  ElevatedButton(
                    onPressed: () async {
                      print('Save As');

                      // predictImage();
                      // final _saveImageSuccess = await StudentAssignmentApi.saveImage(2, _image);
                      // if(_saveImageSuccess){
                      //   print('save image success !!');
                      //   await getStudentAssignment();
                      //   Navigator.of(context).pop();
                      // }
                    },
                    child: const Text('Save As'),
                  ),
                ],
              ),
            ],
          ),
        )
      ),

    );
  }

}