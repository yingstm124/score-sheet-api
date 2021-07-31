import 'package:flutter_easyloading/flutter_easyloading.dart';
import 'package:http/http.dart' as http;
import 'package:score_sheet_app/helpers/BaseApi.dart';
import 'package:score_sheet_app/models/TeachCourse.dart';
import 'dart:convert';


class TeachCourseApi {
  static final String _baseUrl = BaseApi.getBaseAPI();

  // get teach courses
  static Future<List<TeachCourse>> getTeachCourses() async {

    String url = _baseUrl + '/teachCourses';
    EasyLoading.show(status: 'loading..');
    final res = await http.get(Uri.parse(url));

    if (res.statusCode == 200) {
      final List<dynamic> result = jsonDecode(res.body);
      List<TeachCourse> lists =
      result.map((e) => TeachCourse.fromJson(e)).toList();
      EasyLoading.dismiss();
      return lists;
    } else {
      EasyLoading.showError('Failed with Error');
      EasyLoading.dismiss();
      throw Exception("Failed !");
    }
  }



}