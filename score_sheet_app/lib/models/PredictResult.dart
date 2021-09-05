class PredictResult {
  int? StudentId;
  int? TeachStudentId;
  List<dynamic> Scores;
  final String Message;

  PredictResult({
    this.StudentId,
    this.TeachStudentId,
    required this.Scores,
    required this.Message
  });

  factory PredictResult.fromJson(Map<String, dynamic> json){
    return PredictResult(
        StudentId: json["StudentId"],
        TeachStudentId: json["TeachStudentId"],
        Scores: json["Scores"],
        Message: json["Message"]
    );
  }
}