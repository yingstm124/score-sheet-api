import 'package:flutter/material.dart';
import 'package:flutter_easyloading/flutter_easyloading.dart';
import 'package:score_sheet_app/components/HomePage/TeachCourseDetail.dart';
import 'package:score_sheet_app/components/Loading/Loading.dart';
import 'package:score_sheet_app/models/TeachCourse.dart';
import 'package:score_sheet_app/apis/TeachCourseApi.dart';

class TeachCourses extends StatefulWidget {
  @override
  _TeachCourses createState() => _TeachCourses();
}

class _TeachCourses extends State<TeachCourses> {
  List<TeachCourse> _teachCourses = [];

  @override
  void initState() {
    super.initState();
    getTeachCourses();
  }

  void getTeachCourses() async {
    final teachCourses = await TeachCourseApi.getTeachCourses();
    setState(() {
      _teachCourses = teachCourses;
    });
  }

  @override
  Widget build(BuildContext context) {
    return ListView.builder(
        itemCount: _teachCourses.length,
        itemBuilder: (context, index) {
          final teachCourse = _teachCourses[index];
          return TeachCourseDetail(teachcourse: teachCourse);
        });
  }
}