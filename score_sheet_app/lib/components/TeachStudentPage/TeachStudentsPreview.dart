
import 'package:flutter/material.dart';
import 'package:score_sheet_app/apis/TeachStudentApi.dart';
import 'package:score_sheet_app/components/CourseHeader/CourseHeader.dart';
import 'package:score_sheet_app/components/TeachStudentPage/TeachStudentPage.dart';
import 'package:score_sheet_app/models/TeachCourse.dart';
import 'package:score_sheet_app/models/TeachStudent.dart';

class TeachStudentsPreview extends StatefulWidget {
  Function getTeachStudents;
  TeachCourse teachCourse;
  List<TeachStudent> data;
  TeachStudentsPreview({required this.data, required this.teachCourse, required this.getTeachStudents});
  @override
  _TeachStudentsPreview createState() => _TeachStudentsPreview(data: data, teachCourse: teachCourse, getTeachStudents: getTeachStudents);
}

class _TeachStudentsPreview extends State<TeachStudentsPreview>{
  Function getTeachStudents;
  TeachCourse teachCourse;
  List<TeachStudent> data;
  _TeachStudentsPreview({required this.data, required this.teachCourse, required this.getTeachStudents});


  @override
  Widget build(BuildContext context) {
    final ButtonStyle style =
    ElevatedButton.styleFrom(textStyle: const TextStyle(fontSize: 20));


    return Scaffold(
      appBar: AppBar(
        title: Text('Semester ${teachCourse.Term}/${teachCourse.Year}'),
      ),
      body: Column(
        children: [
          Container(
            padding: EdgeInsets.all(20.0),
            child: CourseHeader(teachCourse: teachCourse),
          ),
          Expanded(child: ListView(
            children: data.map((e) {
              return ListTile(
                title: Text(
                    '${e.FirstName} ${e.LastName} ( Sec ${e.SecNo.toString()})'),
                subtitle: Text(e.StudentId.toString()),
              );
            }).toList(),
          )),
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: <Widget>[
              Container(
                margin: EdgeInsets.only(left: 10.0, top: 20.0),
                child: OutlinedButton(
                  style: style,
                  onPressed: () {
                    Navigator.of(context).pop();
                  },
                  child: const Text('Cancel'),
                ),
              ),

              Container(
                margin: EdgeInsets.only(left: 10.0, top: 20.0),
                child: ElevatedButton(
                  style: style,
                  onPressed: () async {
                    print('import');
                    final _importSuccess = await TeachStudentApi.addTeachStudents(teachCourse.TeachCourseId, data);

                    if(_importSuccess){
                      print('success');
                      getTeachStudents();
                      Navigator.of(context).pop();

                    }

                  },
                  child: const Text('Import'),
                ),
              )

            ],
          )

        ],
      )
    );


  }

}