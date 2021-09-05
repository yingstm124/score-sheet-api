class StudentScoreResponse {
  final String Message;

  StudentScoreResponse({
    required this.Message
  });

  factory StudentScoreResponse.fromJson(Map<String,dynamic> json){
    return StudentScoreResponse(
        Message: json["Message"]
    );
  }
}