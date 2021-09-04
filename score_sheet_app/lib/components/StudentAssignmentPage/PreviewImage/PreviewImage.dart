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

  var _predictResult = new PredictResult(StudentId: 0, Scores: [], Message: "");

  _PreviewImage({
    required this.getStudentAssignment,
    this.image,
    required this.assignment,
    required this.teachCourse
  });

  void predictImage() async {
    final img = Io.File(image!.path);
    final predict = PredictApi.predict(assignment.AssignmentId, img)
        .then((value) => {
          setState(() {
          _predictResult = value;
          }),
        });
  }

  @override
  void initState() {
    // predict from image
    predictImage();
  }

  Widget getScoreWidget(List<dynamic> scores){
    List<Widget> list = [];
    int i = 1;
    scores.forEach((element) {
      list.add(new Text('Score ${i} : ${element.toString()}'));
      i++;
    });
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
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: <Widget>[
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: <Widget>[
                Column(
                  mainAxisAlignment: MainAxisAlignment.start,
                  children: <Widget>[
                    Text('${assignment.AssignmentName}'),
                    Text('${teachCourse.CourseName} (${teachCourse.CourseId})'),
                    Text('Semester ${teachCourse.Term}/${teachCourse.Year}')
                  ],
                )
              ],
            ),
            Image.file(File(image!.path)),
            Row(
              children: <Widget>[
                Column(
                  children: <Widget>[
                    Text('Student Id : ${_predictResult.StudentId.toString()}'),
                    getScoreWidget(_predictResult.Scores)
                  ],
                )
              ],
            ),
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
                    print('Submit');
                    predictImage();

                    // final _saveImageSuccess = await StudentAssignmentApi.saveImage(2, _image);
                    // if(_saveImageSuccess){
                    //   print('save image success !!');
                    //   await getStudentAssignment();
                    //   Navigator.of(context).pop();
                    // }
                  },
                  child: const Text('Submit'),
                ),
              ],
            ),
          ],
        ),

      ),

    );
  }

}