
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:score_sheet_app/apis/AssignmentApi.dart';
import 'package:score_sheet_app/components/AssignmentPage/AssignmentPage.dart';
import 'package:score_sheet_app/models/Counter.dart';
import 'package:score_sheet_app/models/TeachCourse.dart';

class AssignmentCard extends StatefulWidget {
  TeachCourse teachCourse;
  AssignmentCard({required this.teachCourse});

  @override
  _AssignmentCard createState() =>
      _AssignmentCard(teachCourse: teachCourse);
}

class _AssignmentCard extends State<AssignmentCard> {
  TeachCourse teachCourse;
  _AssignmentCard({required this.teachCourse});
  Counter _totalAssignments = new Counter(Count: 0);

  @override
  void initState() {
    super.initState();
    getTotalAssignments();
  }

  void getTotalAssignments() async {
    final assignments = await AssignmentApi.getTotalAssignments(this.teachCourse.TeachCourseId);
    setState(() {
      _totalAssignments = assignments;
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
                    Icons.school,
                    size: 40.0,
                  ),
                  Text('Assignment totals')
                ],
              ),
              Text(_totalAssignments.Count.toString())
            ],
          ),
          onTap: () {
            Navigator.push(
                context,
                MaterialPageRoute(
                    builder: (context) =>
                        AssignmentPage(teachCourse: teachCourse, getTotalAssignment: getTotalAssignments,)
                ));
          },
        ),
      )
    );
  }
}
