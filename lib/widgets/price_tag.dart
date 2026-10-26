import 'package:flutter/material.dart';
import '../theme/app_theme.dart';

class PriceTag extends StatelessWidget {
  final double precio;

  const PriceTag({super.key, required this.precio});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
      decoration: BoxDecoration(
        color: AppTheme.backgroundColor,
        borderRadius: BorderRadius.circular(8),
      ),
<<<<<<< HEAD
 child: Text(
        '\$${precio.toStringAsFixed(0)} MXN',
=======
      child: Text(
        'Precio: \$${precio.toStringAsFixed(0)} MXN',
>>>>>>> origin/main
        style: const TextStyle(
          fontWeight: FontWeight.bold,
          color: AppTheme.primaryColor,
          fontSize: 13,
          letterSpacing: 0.4,
        ),
      ),
    );
  }
}