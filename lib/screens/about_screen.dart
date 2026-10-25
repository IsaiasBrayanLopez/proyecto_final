import 'package:flutter/material.dart';
import '../widgets/custom_app_bar.dart';
import '../widgets/section_header.dart';
import '../widgets/team_member_tile.dart';
import '../widgets/custom_action_button.dart';

class AboutScreen extends StatelessWidget {
  const AboutScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: const CustomAppBar(title: 'Información del Proyecto'),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const SectionHeader(
              title: 'Desarrollo de Aplicaciones Móviles',
              subtitle: 'Unidad 3: Manejo de Estados, Arquitectura y Servicios',
            ),
            const SizedBox(height: 16),
            const SectionHeader(
              title: 'Integrantes de la Bina',
              subtitle: 'Flujo colaborativo con Ramas y Pull Requests',
            ),
            const SizedBox(height: 8),
            const TeamMemberTile(
              nombre: 'Programador A Lopez Domínguez Isaías Brayan',
              rol: 'Modelos, Widgets Bloque 1 y Pantallas Principales',
              githubUser: 'IsaíasBrayanLópez',
            ),
            const TeamMemberTile(
              nombre: 'Programador B Barrios Velasco Jazlynn',
              rol: 'Servicios JSON, Tema, Widgets Bloque 2 y Pantallas Finales',
              githubUser: 'usuario_programador_b',
            ),
            const SizedBox(height: 24),
            CustomActionButton(
              text: 'Volver al Inicio',
              icon: Icons.home_outlined,
              onPressed: () => Navigator.pop(context),
            ),
          ],
        ),
      ),
    );
  }
}