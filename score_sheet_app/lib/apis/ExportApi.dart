import 'dart:io';

import 'package:excel/excel.dart';
import 'package:flutter_easyloading/flutter_easyloading.dart';
import 'package:open_file/open_file.dart';
import 'package:path_provider/path_provider.dart';
import 'package:score_sheet_app/helpers/BaseApi.dart';
import 'package:score_sheet_app/models/ExportScoreInfo.dart';
import 'package:http/http.dart' as http;
import 'package:score_sheet_app/models/TeachCourse.dart';
import 'dart:convert';

import 'package:syncfusion_flutter_xlsio/xlsio.dart';


class ExportApi {
  static final String _baseUrl = BaseApi.getBaseAPI();


  static Future<List<ExportScoreInfo>> getExportInfo(int _teachCourseId) async {
    String url = _baseUrl + '/exportScoreInfo?teachCourseId=${_teachCourseId}';
    EasyLoading.show(status: 'loading..');
    final res = await http.get(Uri.parse(url));

    if (res.statusCode == 200) {
      final List<dynamic> result = jsonDecode(res.body);
      List<ExportScoreInfo> lists =
      result.map((e) => ExportScoreInfo.fromJson(e)).toList();
      EasyLoading.dismiss();
      return lists;
    } else {
      EasyLoading.showError('Failed with Error');
      EasyLoading.dismiss();
      throw Exception("Failed !");
    }
  }

  static Future<void> createExcel(List<ExportScoreInfo> datas, TeachCourse teachCourse) async {
    final Workbook workbook = Workbook();
    final Worksheet sheet = workbook.worksheets[0];

    sheet.getRangeByName('A1').setText("รหัสนักศึกษา");
    sheet.getRangeByName('B1').setText("ชื่อนักศึกษา");
    sheet.getRangeByName('C1').setText("ชื่อการสอบย่อย");
    sheet.getRangeByName('D1').setText("คะแนนที่ได้");
    sheet.getRangeByName('E1').setText("คะแนนเต็ม");

    datas.asMap()
    .forEach((index, value) {
      sheet.getRangeByName('A${index+2}').setText(value.StudentId.toString());
      sheet.getRangeByName('B${index+2}').setText(value.FullName);
      sheet.getRangeByName('C${index+2}').setText(value.AssignmentName);
      sheet.getRangeByName('D${index+2}').setText(value.Score == null ? "0": value.Score.toString());
      sheet.getRangeByName('E${index+2}').setText(value.FullScore.toString());
    });

    final List<int> bytes = workbook.saveAsStream();
    workbook.dispose();

    final directory = await getExternalStorageDirectory();
    final path = directory!.path;
    File file = File('$path/Report.xlsx');
    await file.writeAsBytes(bytes, flush: true);
    OpenFile.open('$path/Report.xlsx');
  }
}