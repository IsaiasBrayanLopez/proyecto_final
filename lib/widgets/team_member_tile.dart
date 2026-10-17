import 'package:flutter/material.dart';
import '../theme/app_theme.dart';

class TeamMemberTile extends StatelessWidget {
  final String nombre;
  final String rol;
  final String githubUser;

  const TeamMemberTile({
    super.key,
    required this.nombre,
    required this.rol,
    required this.githubUser,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 0,
      color: Colors.white,
      margin: const EdgeInsets.only(bottom: 10),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(10),
        side: const BorderSide(color: Colors.black12),
      ),
      child: ListTile(
        leading: const CircleAvatar(
          backgroundColor: AppTheme.primaryColor,
          child: Icon(Icons.person, color: Colors.white),
        ),
        title: Text(
          nombre,
          style: const TextStyle(
            fontWeight: FontWeight.bold,
            color: AppTheme.textPrimary,
          ),
        ),
        subtitle: Text('$rol • @$githubUser'),
      ),
    );
  }
}