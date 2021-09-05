import 'dart:convert';
import 'dart:io';
import 'package:flutter_easyloading/flutter_easyloading.dart';
import 'package:score_sheet_app/helpers/BaseApi.dart';
import 'package:http/http.dart' as http;
import 'package:score_sheet_app/models/PredictResult.dart';

class PredictApi {

  static final String _baseUrl = BaseApi.getBaseAPI();

  static Future<PredictResult> predict(int _assignmentId, int _teachCouseId, File _image) async {
    String url = _baseUrl + '/predict?assignmentId=${_assignmentId}&teachCourseId=${_teachCouseId}';
    final headers = { "Content-Type": "multipart/form-data" };
    EasyLoading.show(status: 'loading..');
    final request = http.MultipartRequest(
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
      final body = await res.stream.bytesToString();
      final dynamic result = jsonDecode(body);
      PredictResult answer = PredictResult.fromJson(result);
      print("Teach Student Id : ${answer.TeachStudentId}");
      return answer;
    }
    else {
      EasyLoading.showError('Can not Detect');
      EasyLoading.dismiss();
      throw Exception("Failed !");
    }

  }

}