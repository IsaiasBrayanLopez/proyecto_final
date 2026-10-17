import 'package:flutter/material.dart';
import '../theme/app_theme.dart';

class StatCounterCard extends StatelessWidget {
  final String title;
  final String count;
  final IconData icon;

  const StatCounterCard({
    super.key,
    required this.title,
    required this.count,
    required this.icon,
  });

  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: Card(
        elevation: 0,
        color: Colors.white,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(12),
          side: const BorderSide(color: Colors.black12),
        ),
        child: Padding(
          padding: const EdgeInsets.all(14.0),
          child: Column(
            children: [
              Icon(icon, color: AppTheme.primaryColor, size: 28),
              const SizedBox(height: 6),
              Text(
                count,
                style: const TextStyle(
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                  color: AppTheme.textPrimary,
                ),
              ),
              Text(
                title,
                textAlign: TextAlign.center,
                style: const TextStyle(
                  fontSize: 12,
                  color: AppTheme.textSecondary,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}