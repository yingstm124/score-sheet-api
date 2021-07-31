import 'package:flutter_easyloading/flutter_easyloading.dart';
import 'package:score_sheet_app/helpers/BaseApi.dart';
import 'package:score_sheet_app/models/Assignment.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

import 'package:score_sheet_app/models/Counter.dart';

class AssignmentApi {
  static final String _baseUrl = BaseApi.getBaseAPI();

  static Future<List<Assignment>> getAssignments(int _teachCourseId) async {
    String url = _baseUrl + '/assignments?teachCourseId=${_teachCourseId}';
    EasyLoading.show(status: 'loading..');
    final res = await http.get(Uri.parse(url));

    if (res.statusCode == 200) {
      final List<dynamic> result = jsonDecode(res.body);
      List<Assignment> lists =
      result.map((e) => Assignment.fromJson(e)).toList();
      EasyLoading.dismiss();
      return lists;
    } else {
      EasyLoading.showError('Failed with Error');
      EasyLoading.dismiss();
      throw Exception("Failed !");
    }
  }

  static Future<Counter> getTotalAssignments(int _teachCourseId) async{
    String url = _baseUrl + '/countAssignments?teachCourseId=${_teachCourseId}';
    EasyLoading.show(status: 'loading..');
    final res = await http.get(Uri.parse(url));

    if (res.statusCode == 200) {
      final dynamic result = jsonDecode(res.body);
      Counter totalAssignments = Counter.fromJson(result);
      EasyLoading.dismiss();
      return totalAssignments;
    } else {
      EasyLoading.showError('Failed with Error');
      EasyLoading.dismiss();
      throw Exception("Failed !");
    }
  }

  static Future<bool> addAssignment(int _teachCourseId, Assignment _data) async {
    String url = _baseUrl + '/addAssignment?teachCourseId=${_teachCourseId.toString()}';
    final jsonData = jsonEncode(<String,String>{
      "AssignmentName": _data.AssignmentName,
      "FullScore": _data.FullScore.toString()
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
      return true;
    }
    else{
      EasyLoading.showError('Failed with Error');
      EasyLoading.dismiss();
      throw Exception("Failed !");
    }
  }

  static Future<bool> deleteAssignment(int _assignmentId) async{
    String url = _baseUrl + '/deleteAssignment?AssignmentId=${_assignmentId}';
    EasyLoading.show(status: 'loading..');
    final res = await http.post(Uri.parse(url));

    if (res.statusCode == 200) {
      EasyLoading.dismiss();
      return true;
    } else {
      EasyLoading.showError('Failed with Error');
      EasyLoading.dismiss();
      throw Exception("Failed !");
    }
  }

}
