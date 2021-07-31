import 'dart:convert';
import 'dart:io' as Io;
import 'dart:io';

import 'package:camera/camera.dart';
import 'package:flutter/material.dart';
import 'package:score_sheet_app/apis/StudentAssignmentApi.dart';

class PreviewImage extends StatelessWidget {

  Function getStudentAssignment;
  XFile? image ;
  PreviewImage({required this.getStudentAssignment, this.image});


  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(image!.name.toString()),
      ),
      body: Center(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: <Widget>[
            Image.file(File(image!.path)),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceAround,
              children: <Widget>[
                ElevatedButton(
                  onPressed: () {
                    Navigator.pop(context);
                    print('Cancel');
                  },
                  child: const Text('Cancel'),
                ),
                ElevatedButton(
                  onPressed: () async {
                    print('Submit');
                    final _image = Io.File(image!.path);
                    final _saveImageSuccess = await StudentAssignmentApi.saveImage(2, _image);
                    if(_saveImageSuccess){
                      print('save image success !!');
                      await getStudentAssignment();
                      Navigator.of(context).pop();
                    }
                  },
                  child: const Text('Submit'),
                ),
              ],
            )
          ],
        ),
      ),
    );
  }

}