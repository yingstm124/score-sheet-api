
import 'package:flutter/material.dart';
import 'package:score_sheet_app/models/TeachCourse.dart';

class CourseHeader extends StatelessWidget {
  TeachCourse teachCourse;
  CourseHeader({required this.teachCourse});

  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisSize: MainAxisSize.min,
      children: <Widget>[
        Text(
          teachCourse.CourseName,
          style: TextStyle(fontSize: 20.0),
        ),
        Text(teachCourse.CourseId.toString()),
      ],
    );
  }
}
