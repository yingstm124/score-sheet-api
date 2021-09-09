
import 'dart:io';

import 'package:flutter_easyloading/flutter_easyloading.dart';
import 'package:score_sheet_app/helpers/BaseApi.dart';
import 'package:score_sheet_app/models/StudentAssignment.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class StudentAssignmentApi {

  static final String _baseUrl = BaseApi.getBaseAPI();

  static Future<List<StudentAssignment>> getStudentAssignment(int _assignmentId) async{
    String url = _baseUrl + '/studentAssignments?AssignmentId=${_assignmentId}';
    EasyLoading.show(status: 'loading..');

    final res = await  http.get(Uri.parse(url));
    if (res.statusCode == 200) {
      final List<dynamic> result = jsonDecode(res.body);
      List<StudentAssignment> lists =
      result.map((e) => StudentAssignment.fromJson(e)).toList();
      EasyLoading.dismiss();
      return lists;
    } else {
      EasyLoading.showError('Failed with Error');
      EasyLoading.dismiss();
      throw Exception("Failed !");
    }
  }

  static Future<bool> saveImage(int _teachStudentId, int _assignmentId ,File _image) async {
    String url = _baseUrl + '/saveImage?TeachStudentId=${_teachStudentId}&AssignmentId=${_assignmentId}';
    final headers = { "Content-Type": "multipart/form-data" };
    EasyLoading.show(status: 'loading..');
    final request = await http.MultipartRequest(
      "POST", Uri.parse(url)
    );

    request.files.add(http.MultipartFile(
      'image', _image.readAsBytes().asStream(), _image.lengthSync(),
      filename: _image.path.split('/').last
    ));

    request.headers.addAll(headers);
    final res = await request.send();

    if(res.statusCode == 200){
        EasyLoading.dismiss();
        return true;
    }
    else{
      EasyLoading.showError('Failed with Error');
      EasyLoading.dismiss();
      throw Exception("Failed !");
      return false;
    }
  }


}