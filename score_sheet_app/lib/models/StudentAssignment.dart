class StudentAssignment {
  final int StudentAssignmentId;
  final int TeachStudentId;
  final int StudentId;
  final String FirstName;
  final String LastName;
  final String? Img;
  final int SecNo;

  StudentAssignment({
    required this.StudentAssignmentId,
    required this.TeachStudentId,
    required this.StudentId,
    required this.FirstName,
    required this.LastName,
    this.Img,
    required this.SecNo
  });

  factory StudentAssignment.fromJson(Map<String, dynamic> json){
    return StudentAssignment(
        StudentAssignmentId: json["StudentAssignmentId"],
        TeachStudentId: json["TeachStudentId"],
        StudentId: json["StudentId"],
        FirstName: json["FirstName"],
        LastName: json["LastName"],
        Img: json["Img"],
        SecNo: json["SecNo"]);
  }


}