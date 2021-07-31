class Counter {
  final int Count;

  Counter({required this.Count});

  factory Counter.fromJson(Map<String, dynamic> json) {
    return Counter(
        Count: json["Count"]
    );
  }
}

