class Assignment {
  final int AssignmentId;
  final String AssignmentName;
  final int FullScore;
  final int? TeachCourseId;

  Assignment(
      {required this.AssignmentId,
        required this.AssignmentName,
        required this.FullScore,
        this.TeachCourseId});

  factory Assignment.fromJson(Map<String, dynamic> json) {
    return Assignment(
        AssignmentId: json["AssignmentId"],
        AssignmentName: json["AssignmentName"],
        FullScore: json["FullScore"],
        TeachCourseId: json["TeachCourseId"]);
  }
}
