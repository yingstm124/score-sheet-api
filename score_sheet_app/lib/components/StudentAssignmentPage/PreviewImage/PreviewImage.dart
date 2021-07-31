import 'dart:io';

import 'package:flutter/material.dart';

class PreviewImage extends StatelessWidget {

  File? image ;
  PreviewImage({this.image});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Image.file(image!),
    );
  }

}