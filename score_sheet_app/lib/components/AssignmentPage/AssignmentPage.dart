
import 'package:flutter/material.dart';
import 'package:flutter_speed_dial/flutter_speed_dial.dart';
import 'package:score_sheet_app/apis/AssignmentApi.dart';
import 'package:score_sheet_app/components/CourseHeader/CourseHeader.dart';
import 'package:score_sheet_app/components/StudentAssignmentPage/StudentAssignmentPage.dart';
import 'package:score_sheet_app/models/Assignment.dart';
import 'package:score_sheet_app/models/TeachCourse.dart';

import 'AssignmentAddForm.dart';

class AssignmentPage extends StatefulWidget {
  TeachCourse teachCourse;
  Function getTotalAssignment;
  AssignmentPage({required this.teachCourse, required this.getTotalAssignment});
  @override
  _AssignmentPage createState() => _AssignmentPage(teachCourse: teachCourse, getTotalAssignment: getTotalAssignment);
}

class _AssignmentPage extends State<AssignmentPage>{
  TeachCourse teachCourse;
  Function getTotalAssignment;
  _AssignmentPage({ required this.teachCourse, required this.getTotalAssignment});
  List<Assignment> _assignments = [];

  @override
  void initState() {
    super.initState();
    getAssignments();
  }

  void getAssignments()  async{
    final assignments = await AssignmentApi.getAssignments(this.teachCourse.TeachCourseId);
    setState(() {
      _assignments = assignments;
    });
  }

  Widget _getFAB() {
    return SpeedDial(
      animatedIcon: AnimatedIcons.menu_close,
      animatedIconTheme: IconThemeData(size: 22),
      backgroundColor: Color(0xFF801E48),
      visible: true,
      curve: Curves.bounceIn,
      children: [
        // FAB 1
        SpeedDialChild(
            child: Icon(Icons.assignment_turned_in),
            backgroundColor: Color(0xFF801E48),
            onTap: () {

            },
            label: 'Button 1',
            labelStyle: TextStyle(
                fontWeight: FontWeight.w500,
                color: Colors.white,
                fontSize: 16.0),
            labelBackgroundColor: Color(0xFF801E48)),
        // FAB 2
        SpeedDialChild(
            child: Icon(Icons.assignment_turned_in),
            backgroundColor: Color(0xFF801E48),
            onTap: () {
            },
            label: 'Button 2',
            labelStyle: TextStyle(
                fontWeight: FontWeight.w500,
                color: Colors.white,
                fontSize: 16.0),
            labelBackgroundColor: Color(0xFF801E48))
      ],

    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Semester ${teachCourse.Term}/${teachCourse.Year}')),
      body: Column(
          mainAxisSize: MainAxisSize.max,
          children: <Widget>[
            Container(
                margin: EdgeInsets.only(top: 30),
                child: CourseHeader(
                  teachCourse: teachCourse,
                )),
            Expanded(child: ListView(
              children: _assignments.map((e){
                return InkWell(
                  child: ListTile(
                      title: Text(
                          '${e.AssignmentName}'),
                      subtitle: Text('FullScore ${e.FullScore.toString()}'),
                      trailing: IconButton(
                        icon: const Icon(Icons.delete),
                        onPressed: () async{
                          print('Delete Assignment');
                          final _delAssignmentSuccess = await AssignmentApi.deleteAssignment(e.AssignmentId);
                          if(_delAssignmentSuccess){
                            print('del assignment success !');
                            getAssignments();
                            getTotalAssignment();
                          }
                        },
                      )
                  ),
                  onTap: (){
                    print('Look Student Assignments');
                    Navigator.push(
                        context,
                        MaterialPageRoute(
                            builder: (context) =>
                                StudentAssignmentPage(teachCourse: teachCourse,assignment: e,)
                        )
                    );
                  },
                );
              }).toList(),)
            )
          ],
      ),
      floatingActionButtonLocation: FloatingActionButtonLocation.centerDocked,
      floatingActionButton: Container(
        margin: EdgeInsets.all(10),
        child: FloatingActionButton(
          onPressed: () async{
            print('create assignment');
            return showDialog<void>(
                context: context,
                builder: (BuildContext context) {
                  return AlertDialog(
                      title: const Text('Section number'),
                      content: AssignmentAddForm(teachCourse: teachCourse, getAssignments: getAssignments, getTotalAssignment: getTotalAssignment,)
                  );
                }
            );
          },
          child: Icon(Icons.add),
        ),
      )
    );
  }

}