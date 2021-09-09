class AddStudent {
  final String StudentId;
  final bool IsRegister;
  final int SecNo;

  AddStudent(
  {
    required this.StudentId,
    required this.IsRegister,
    required this.SecNo
  });

  factory AddStudent.fromJson(Map<String, dynamic> json) {
    return AddStudent(
        StudentId: json["StudentId"],
        IsRegister: json["IsRegister"],
        SecNo: json["SecNo"]
    );

  }
}