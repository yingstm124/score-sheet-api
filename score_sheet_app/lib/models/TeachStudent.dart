class TeachStudent {
  final String FirstName;
  final String LastName;
  final String NickName;
  final int SecNo;
  final int StudentId;
  final int TeachStudentId;
  final bool? IsRegister;

  TeachStudent(
      {required this.FirstName,
        required this.LastName,
        required this.NickName,
        required this.SecNo,
        required this.StudentId,
        required this.TeachStudentId,
        this.IsRegister
      });

  factory TeachStudent.fromJson(Map<String, dynamic> json) {
    return TeachStudent(
        FirstName: json["FirstName"],
        LastName: json["LastName"],
        NickName: json["NickName"],
        SecNo: json["SecNo"],
        StudentId: json["StudentId"],
        TeachStudentId: json["TeachStudentId"],
        IsRegister: json["IsRegister"]
    );
  }
}
