
import 'package:flutter_easyloading/flutter_easyloading.dart';
import 'package:score_sheet_app/helpers/BaseApi.dart';
import 'package:score_sheet_app/models/StudentAssignment.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class StudentAssignmentApi {

  static final String _baseUrl = BaseApi.getBaseAPI();

  static Future<List<StudentAssignment>> getStudentAssignment(int _teachCourseId) async{
    String url = _baseUrl + '/studentAssignments?teachCourseId=${_teachCourseId}';
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
}