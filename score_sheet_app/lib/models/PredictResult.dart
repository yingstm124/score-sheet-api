class PredictResult {
  int StudentId;
  List<dynamic> Scores;
  final String Message;

  PredictResult({
    required this.StudentId,
    required this.Scores,
    required this.Message
  });

  factory PredictResult.fromJson(Map<String, dynamic> json){
    return PredictResult(
        StudentId: json["StudentId"],
        Scores: json["Scores"],
        Message: json["Message"]
    );
  }
}