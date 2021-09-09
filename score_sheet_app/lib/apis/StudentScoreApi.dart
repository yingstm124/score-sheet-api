import 'package:flutter_easyloading/flutter_easyloading.dart';
import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;
import 'package:score_sheet_app/helpers/BaseApi.dart';
import 'package:score_sheet_app/models/StudentScoreResponse.dart';

class StudentScoreApi {

  static final String _baseUrl = BaseApi.getBaseAPI();

  static Future<StudentScoreResponse> saveScore(
      List<dynamic> _scores,
      String _studentId,
      int _assignmentId,
      int _teachCourseId,
      int _teachStudentId) async {
    // var _queryStr = "";
    // _scores.forEach((element) {
    //   var _str = "Scores=";
    //   _str += element.toString();
    //   _queryStr += "&${_str}";
    // });
    // print(_queryStr);
    // String url = _baseUrl + '/saveScore?AssigmentId=${_assignmentId}${_queryStr}&StudentId=${_studentId}&TeachCourseId=${_teachCourseId}';
    String url = _baseUrl + '/saveScore';
    print(url);
    final headers = {
      "Content-Type": "application/json"
    };
    final jsonData = jsonEncode(<String,dynamic>{
      "AssignmentId": _assignmentId.toString(),
      "Scores": _scores,
      "StudentId": _studentId.toString(),
      "AssignmentId": _assignmentId.toString(),
      "TeachCourseId": _teachCourseId.toString(),
        "TeachStudentId": _teachStudentId.toString()
    });
    EasyLoading.show(status: 'loading..');
    final res = await http.post(Uri.parse(url),
        headers: {
          "Content-Type": "application/json"
        },
        body: jsonData
    );

    if(res.statusCode == 200){
      EasyLoading.dismiss();
      final dynamic result = jsonDecode(res.body);
      StudentScoreResponse response = StudentScoreResponse.fromJson(result);
      print("Msg : ${response.Message}");
      return response;
    }
    else {
      EasyLoading.showError('Can not Detect');
      EasyLoading.dismiss();
      throw Exception("Failed !");
    }

  }
}