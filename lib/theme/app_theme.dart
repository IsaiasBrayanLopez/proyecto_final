import 'package:flutter/material.dart';

class AppTheme {

  static const Color primaryColor = Color(0xFF34495E);    // Azul pizarra sobrio
  static const Color accentColor = Color(0xFF5D6D7E);     // Gris azulado suave
  static const Color backgroundColor = Color(0xFFF4F6F8); // Fondo claro descansado
>>>>>>> 8cd39b0799eaae6c912a998cae086ac301a257fa
  static const Color cardColor = Colors.white;
  static const Color textPrimary = Color(0xFF2C3E50);
  static const Color textSecondary = Color(0xFF7F8C8D);

  static ThemeData get lightTheme {
    return ThemeData(
      useMaterial3: true,
      scaffoldBackgroundColor: backgroundColor,
      colorScheme: ColorScheme.fromSeed(
        seedColor: primaryColor,
        primary: primaryColor,
        secondary: accentColor,
      ),
      appBarTheme: const AppBarTheme(
        backgroundColor: primaryColor,
        foregroundColor: Colors.white,
        elevation: 0,
        centerTitle: true,
      ),
    );
  }
}