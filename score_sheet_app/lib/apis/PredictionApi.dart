import 'dart:convert';
import 'dart:io';
import 'package:flutter_easyloading/flutter_easyloading.dart';
import 'package:score_sheet_app/helpers/BaseApi.dart';
import 'package:http/http.dart' as http;
import 'package:score_sheet_app/models/PredictResult.dart';

class PredictApi {

  static final String _baseUrl = BaseApi.getBaseAPI();

  static Future<PredictResult> predict(int _assignmentId, File _image) async {
    String url = _baseUrl + '/predict?assignmentId=${_assignmentId}';
    final headers = { "Content-Type": "multipart/form-data" };
    EasyLoading.show(status: 'loading..');
    final request = await http.MultipartRequest(
        "POST", Uri.parse(url)
    );

    request.files.add(http.MultipartFile(
        'image', _image.readAsBytes().asStream(), _image.lengthSync(),
        filename: _image.path.split('/').last
    ));
    PredictResult empty_answer = PredictResult(
        StudentId: 0,
        Scores: [],
        Message: ""
    );
    request.headers.addAll(headers);
    request.send().then((result) async{
      http.Response.fromStream(result)
          .then((response){
            if(response.statusCode == 200){
              EasyLoading.dismiss();
              final dynamic r = jsonDecode(response.body);
              PredictResult answer = PredictResult.fromJson(r);
              return answer;
            }
            else{
              EasyLoading.showError('Failed with Error');
              EasyLoading.dismiss();
              throw Exception("Failed !");
            }
      });
    });
    return empty_answer;

    // if(res.statusCode == 200){
    //   EasyLoading.dismiss();
    //   final dynamic result = res.stream.bytesToString();
    //   return true;
    // }
    // else{
    //   EasyLoading.showError('Failed with Error');
    //   EasyLoading.dismiss();
    //   return false;
    // }

  }

}