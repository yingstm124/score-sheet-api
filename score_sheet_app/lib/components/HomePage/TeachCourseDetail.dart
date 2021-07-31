import 'package:flutter/material.dart';
import 'package:score_sheet_app/components/TeachCoursePage/TeachCoursePage.dart';
import 'package:score_sheet_app/models/TeachCourse.dart';

class TeachCourseDetail extends StatelessWidget {
  TeachCourse teachcourse;
  TeachCourseDetail({required this.teachcourse});

  @override
  Widget build(BuildContext context) {
    return Card(
        child: InkWell(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: <Widget>[
              ListTile(
                title: Text(
                    '${teachcourse.CourseName}  (${teachcourse.CourseId.toString()})'),
                subtitle: Text('Semester ${teachcourse.Term}/${teachcourse.Year}'),
              )
            ],
          ),
          onTap: () {
            Navigator.push(
                context,
                MaterialPageRoute(
                    builder: (context) =>
                        TeachCoursePage(teachCourse: teachcourse)));
          },
        ));
  }
}
