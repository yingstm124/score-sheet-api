class StudentAssignment {
  final int StudentAssignmentId;
  final int TeachStudentId;
  final int StudentId;
  final String FirstName;
  final String LastName;
  final String? Img;
  final int? Score;
  final int SecNo;

  StudentAssignment({
    required this.StudentAssignmentId,
    required this.TeachStudentId,
    required this.StudentId,
    required this.FirstName,
    required this.LastName,
    this.Img,
    this.Score,
    required this.SecNo
  });

  factory StudentAssignment.fromJson(Map<String, dynamic> json){
    return StudentAssignment(
        StudentAssignmentId: json["StudentAssignmentId"],
        TeachStudentId: json["TeachStudentId"],
        StudentId: json["StudentId"],
        FirstName: json["FirstName"],
        LastName: json["LastName"],
        Img: json["Img"] ,
        Score: json["Score"],
        SecNo: json["SecNo"]);
  }


}