class ConvertType {
  static int intOrStringValue(dynamic o) {
    if (o is String) o = int.tryParse(o);
    return o ?? 0;
  }
}