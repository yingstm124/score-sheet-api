import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:score_sheet_app/apis/TeachStudentApi.dart';
import 'package:score_sheet_app/components/TeachStudentPage/TeachStudentPage.dart';
import 'package:score_sheet_app/models/Counter.dart';
import 'package:score_sheet_app/models/TeachCourse.dart';
import 'package:score_sheet_app/models/TeachStudent.dart';

class TeachStudentCard extends StatefulWidget {
  TeachCourse teachCourse;
  TeachStudentCard({required this.teachCourse});
  @override
  _TeachStudentCard createState() =>
      _TeachStudentCard(teachCourse: teachCourse);
}

class _TeachStudentCard extends State<TeachStudentCard> {
  TeachCourse teachCourse;
  _TeachStudentCard({required this.teachCourse});
  List<TeachStudent> _teachStudents = [];
  @override
  void initState() {
    super.initState();
    getTeachStudents();
  }

  void getTeachStudents() async {
    final teachStudents = await TeachStudentApi.getTeachStudents(this.teachCourse.TeachCourseId);
    setState(() {
      _teachStudents = teachStudents;
    });
  }


  @override
  Widget build(BuildContext context) {
    return Card(
      child: Container(
        padding: EdgeInsets.all(10.0),
        child: InkWell(
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceAround,
            children: <Widget>[
              Column(
                mainAxisSize: MainAxisSize.min,
                children: <Widget>[
                  Icon(
                    Icons.perm_identity,
                    size: 40.0,
                  ),
                  Text('Student totals')
                ],
              ),
              Text(_teachStudents.length.toString())
            ],
          ),
          onTap: () {
            Navigator.push(
                context,
                MaterialPageRoute(
                    builder: (context) =>
                        TeachStudentPage(teachCourse: teachCourse,getTeachStudents: getTeachStudents,))
            );
          },
        ),
      )
    );
  }
}