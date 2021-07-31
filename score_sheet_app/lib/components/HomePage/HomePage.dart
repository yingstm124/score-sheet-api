import 'package:flutter/material.dart';
import 'package:score_sheet_app/components/HomePage/TeachCourses.dart';
import 'package:score_sheet_app/components/Loading/Loading.dart';

class HomePage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: TeachCourses(),
    );
  }
}