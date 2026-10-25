import 'package:flutter/material.dart';

class AppTheme {


  static const Color primaryColor = Color(0xFF2C3E50);    // Azul marino sobrio
  static const Color accentColor = Color(0xFF4A6572);     // Azul acero suave  

  static const Color backgroundColor = Color(0xFFF4F6F8); // Fondo claro descansado
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