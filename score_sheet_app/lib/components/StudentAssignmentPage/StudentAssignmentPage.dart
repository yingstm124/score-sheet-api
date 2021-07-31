import 'dart:io';

import 'package:flutter/cupertino.dart';
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
  CameraController? controller;
  bool openCameraPreview = false;
  //File? _image;

  late ImagePicker _image = ImagePicker();

  @override
  void initState() {
    super.initState();
    _getStudentAssignment();

  }

  void initialCamera() async{
    // allow first camera
    WidgetsFlutterBinding.ensureInitialized();
    final cameras = await availableCameras();

    // access to camera
    controller = CameraController(cameras[0], ResolutionPreset.max);
    controller?.initialize().then((_) {
      if (!mounted) {
        return;
      }
      setState(() {
        openCameraPreview = true;
      });
    });

  }

  Future _getImage() async{
    final image = await ImagePicker.platform.pickImage(source: ImageSource.camera);
    try {
      setState(() {
        _image = image as ImagePicker;
      });

        print('Preview image');


    }
    catch(e) {
      print(e);
    }
  }

  @override
  void dispose() {
    controller?.dispose();
    setState(() {
      openCameraPreview = false;
    });
    super.dispose();
  }

  void _getStudentAssignment() async {
    final results = await StudentAssignmentApi.getStudentAssignment(teachCourse.TeachCourseId);
    setState(() {
      _studentAssignments = results;
    });
  }


  @override
  Widget build(BuildContext context) {
    if(!openCameraPreview){
      return  Scaffold(
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
                      children: _studentAssignments.map((e){
                        return InkWell(
                          child: Card(
                              child: Container(
                                margin: EdgeInsets.all(10),
                                child: Column(
                                  mainAxisSize: MainAxisSize.min,
                                  children: <Widget>[
                                    FadeInImage(
                                        placeholder: AssetImage('placeholderImage.png'),
                                        image: AssetImage('placeholderImage.png'),
                                        height: 150,
                                        fit:BoxFit.fill
                                    ),
                                    ListTile(
                                      title: Text(
                                          '${e.FirstName} ${e.LastName} ( Sec ${e.SecNo.toString()})'),
                                      subtitle: Text(e.StudentId.toString()),
                                    )
                                  ],
                                ),
                              )
                          ),
                          onTap: (){
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
                  onPressed: (){
                    print('uploade image');
                  },
                ),
                ActionButton(
                  icon: Icon(Icons.camera),
                  onPressed: () async {
                    //initialCamera();
                    _getImage();
                    print('camera');

                  },
                )
              ],
            ),
          )
      );
    }else {
      return CameraPreview(controller!);
    }
  }
}