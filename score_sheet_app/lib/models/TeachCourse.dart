class TeachCourse {
  final int TeachCourseId;
  final int CourseId;
  final String CourseName;
  final int Term;
  final int Year;

  TeachCourse(
      {required this.TeachCourseId,
        required this.CourseId,
        required this.CourseName,
        required this.Term,
        required this.Year});

  factory TeachCourse.fromJson(Map<String, dynamic> json) {
    return TeachCourse(
        TeachCourseId: json["TeachCourseId"],
        CourseId: json["CourseId"],
        CourseName: json["CourseName"],
        Term: json["Term"],
        Year: json["Year"]);
  }
}