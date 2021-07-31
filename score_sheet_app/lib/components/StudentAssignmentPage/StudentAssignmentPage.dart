import 'dart:io';

import 'package:flutter/cupertino.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:score_sheet_app/apis/StudentAssignmentApi.dart';
import 'package:score_sheet_app/components/CourseHeader/CourseHeader.dart';
import 'package:score_sheet_app/components/ExpandableFabCustom/ExpandableFab.dart';
import 'package:score_sheet_app/components/StudentAssignmentPage/PreviewImage/PreviewImage.dart';
import 'package:score_sheet_app/models/Assignment.dart';
import 'package:score_sheet_app/models/StudentAssignment.dart';
import 'package:score_sheet_app/models/TeachCourse.dart';

import 'package:camera/camera.dart';

class StudentAssignmentPage extends StatefulWidget {

  TeachCourse teachCourse;
  Assignment assignment;

  StudentAssignmentPage({required this.teachCourse, required this.assignment});

  @override
  _StudentAssignmentPage createState() => _StudentAssignmentPage(teachCourse: teachCourse, assignment: assignment);

}

class _StudentAssignmentPage extends State<StudentAssignmentPage> {
  TeachCourse teachCourse;
  Assignment assignment;

  _StudentAssignmentPage({required this.teachCourse, required this.assignment});

  List<CameraDescription> cameras = [];
  List<StudentAssignment> _studentAssignments = [];

  List<XFile>? _imageFileList;

  set _imageFile(XFile? value) {
    _imageFileList = value == null ? null : [value];
  }

  dynamic _pickImageError;
  bool isVideo = false;
  String? _retrieveDataError;

  final ImagePicker _picker = ImagePicker();
  final TextEditingController maxWidthController = TextEditingController();
  final TextEditingController maxHeightController = TextEditingController();
  final TextEditingController qualityController = TextEditingController();


  @override
  void initState() {
    super.initState();
    _getStudentAssignment();
  }


  Future _onImageButtonPressed(ImageSource source,
      {BuildContext? context}) async {
    try {
      final pickedFile = await _picker.pickImage(
          source: source
      );
      setState(() {
        _imageFile = pickedFile;
      });
    } catch (e) {
      setState(() {
        _pickImageError = e;
      });
    }
  }

  void _getStudentAssignment() async {
    final results = await StudentAssignmentApi.getStudentAssignment(
        teachCourse.TeachCourseId);
    setState(() {
      _studentAssignments = results;
    });
  }


  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
            title: Text('Semester ${teachCourse.Term}/${teachCourse.Year}')
        ),
        body: Column(
          mainAxisSize: MainAxisSize.max,
          children: <Widget>[
            Container(
                margin: EdgeInsets.only(top: 30),
                child: CourseHeader(
                  teachCourse: teachCourse,
                )),
            Expanded(
                child: ListView(
                    children: _studentAssignments.map((e) {
                      return InkWell(
                        child: Card(
                            child: Container(
                              margin: EdgeInsets.all(10),
                              child: Column(
                                mainAxisSize: MainAxisSize.min,
                                children: <Widget>[
                                  FadeInImage(
                                      placeholder: AssetImage(
                                          'placeholderImage.png'),
                                      image: AssetImage('placeholderImage.png'),
                                      height: 150,
                                      fit: BoxFit.fill
                                  ),
                                  ListTile(
                                    title: Text(
                                        '${e.FirstName} ${e.LastName} ( Sec ${e
                                            .SecNo.toString()})'),
                                    subtitle: Text(e.StudentId.toString()),
                                  )
                                ],
                              ),
                            )
                        ),
                        onTap: () {
                          print('click');
                        },
                      );
                    }).toList()
                )
            ),
          ],
        ),
        floatingActionButton: Container(
          margin: EdgeInsets.all(5),
          child: ExpandableFab(
            distance: 60.0,
            children: [
              ActionButton(
                icon: Icon(Icons.image),
                onPressed: () async {
                  print('uploade image');
                  await _onImageButtonPressed(ImageSource.gallery, context: context);
                  if(_imageFileList != null){
                    Navigator.push(
                        context,
                        MaterialPageRoute(
                            builder: (context) =>
                                PreviewImage(image: _imageFileList![0])
                        )
                    );
                  }
                },
              ),
              ActionButton(
                icon: Icon(Icons.camera_alt),
                onPressed: () async {
                  print('camera');
                  await _onImageButtonPressed(ImageSource.camera, context: context);
                  if(_imageFileList != null){
                    Navigator.push(
                        context,
                        MaterialPageRoute(
                            builder: (context) =>
                                PreviewImage(image: _imageFileList![0])
                        )
                    );
                  }
                },
              )
            ],
          ),
        )
    );
  }

}
