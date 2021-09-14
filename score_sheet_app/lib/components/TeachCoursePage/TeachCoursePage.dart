
import 'package:flutter/material.dart';
import 'package:score_sheet_app/apis/ExportApi.dart';
import 'package:score_sheet_app/components/CourseHeader/CourseHeader.dart';
import 'package:score_sheet_app/components/TeachCoursePage/AssignmentCard.dart';
import 'package:score_sheet_app/components/TeachCoursePage/TeachStudentCard.dart';
import 'package:score_sheet_app/models/TeachCourse.dart';
import 'package:excel/excel.dart';

class TeachCoursePage extends StatelessWidget {
  TeachCourse teachCourse;
  TeachCoursePage({required this.teachCourse});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Semester ${teachCourse.Term}/${teachCourse.Year}'),
      ),
      body: Center(
        child: Column(
          mainAxisSize: MainAxisSize.max,
          children: <Widget>[
            Container(
              padding: EdgeInsets.all(20.0),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: <Widget>[
                  CourseHeader(teachCourse: teachCourse),
                  TeachStudentCard(teachCourse: teachCourse),
                  AssignmentCard(teachCourse: teachCourse)
                ],
              ),
            )
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () async {
          print('Export');
          final results = await ExportApi.getExportInfo(teachCourse.TeachCourseId);
          await ExportApi.createExcel(results, teachCourse);

        },
        child: Icon(
          Icons.file_download,
        ),
        backgroundColor: Colors.green,
      ),
    );
  }
}
