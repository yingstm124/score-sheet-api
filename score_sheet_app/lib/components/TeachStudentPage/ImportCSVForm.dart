import 'dart:convert';
import 'dart:io';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

import 'package:file_picker/file_picker.dart';
import 'package:score_sheet_app/components/TeachStudentPage/TeachStudentsPreview.dart';
import 'package:score_sheet_app/models/TeachCourse.dart';
import 'package:score_sheet_app/models/TeachStudent.dart';

class ImportCSVForm extends StatefulWidget{
  Function getTeachStudents;
  TeachCourse teachCourse;
  ImportCSVForm({required this.teachCourse, required this.getTeachStudents});
  @override
  _ImportCSVFormState createState() => _ImportCSVFormState(teachCourse: teachCourse, getTeachStudents: getTeachStudents);
}

class _ImportCSVFormState extends State<ImportCSVForm> {
  Function getTeachStudents;
  TeachCourse teachCourse;
  _ImportCSVFormState({required this.teachCourse, required this.getTeachStudents});
  final _formKey = GlobalKey<FormState>();
  final _sec = TextEditingController();

  pickFile() async {
    FilePickerResult? result = await FilePicker.platform.pickFiles();
    if(result != null){
      PlatformFile file = result.files.first;

      print("file ==> "+file.path.toString());
      var format  = file.path.toString().split('.').last;
      print(format);

      if(format == 'csv'){

        List<TeachStudent> teachStudents = [];

        Stream<List> _input = new File(file.path.toString()).openRead();
        _input
            .transform(utf8.decoder)
            .transform(new LineSplitter())
            .listen((String line) {

          List row = line.split(',');
          String id = row[0];
          String firstname = row[1];
          String lastname = row[2];
          String nickname = row[3];

          TeachStudent _teachStudent = new TeachStudent(FirstName: firstname, LastName: lastname, NickName: nickname, SecNo: int.parse(_sec.text), StudentId: int.parse(id), TeachStudentId: 0, IsRegister: true);

          teachStudents.add(_teachStudent);

          //print('$id, $firstname, $lastname, $nickname');

        }, onDone: () {
          // teachStudents_data.forEach((element) {
          //   element.forEach((e) {
          //     print('${e.FirstName}, ${e.SecNo}, ${e.TeachCourseId}');
          //   });
          // });
          Navigator.of(context).pop();
          Navigator.push(
              context,
              MaterialPageRoute(builder: (context) =>
                  TeachStudentsPreview(data: teachStudents, teachCourse: teachCourse, getTeachStudents: getTeachStudents,)
              )
          );
          print('File is now closed.');
        },
            onError: (e) {print(e.toString());}
        );
      }
      // other format ex .doc , .jpg
      else{
        // alert to user input again
        final snackBar = SnackBar(
          content: Text("other format ex .doc , .jpg"),
          action: SnackBarAction(
            label: 'Undo',
            onPressed: (){},
          ),
        );
        ScaffoldMessenger.of(context).showSnackBar(snackBar);
        print("other format ex .doc , .jpg");
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Form(
      key: _formKey,
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          TextFormField(
            controller: _sec,
            decoration: InputDecoration(labelText: "Enter your section number"),
              keyboardType: TextInputType.number,
              inputFormatters: <TextInputFormatter>[
                FilteringTextInputFormatter.digitsOnly
              ],
              validator: (value){
                if(value == null || value.isEmpty){
                  return 'Please enter sec no';
                }
                return null;
              }
          ),
          Row(
            mainAxisAlignment: MainAxisAlignment.end,
            children: <Widget>[
              Container(
                margin: EdgeInsets.only(left: 10.0, top: 20.0),
                child: OutlinedButton(
                    onPressed: () {
                      Navigator.of(context).pop();
                    },
                    child: Text(
                        'Cancel'
                    )
                ),
              ),
              Container(
                margin: EdgeInsets.only(left: 10.0, top: 20.0),
                child: ElevatedButton(
                    onPressed: () {

                      if(_formKey.currentState!.validate()){
                        pickFile();
                        // ScaffoldMessenger.of(context)
                        //     .showSnackBar(
                        //     SnackBar(
                        //         content: Text('import file csv')
                        //     )
                        // );
                      }
                    },
                    child: Text(
                        'Submit'
                    )
                ),
              )
            ],
          )
        ],
      )
    );
  }
}