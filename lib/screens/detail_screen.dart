import 'package:flutter/material.dart';
import '../models/vehiculo.dart';
import '../theme/app_theme.dart';
import '../widgets/section_header.dart';
import '../widgets/spec_badge.dart';
import '../widgets/price_tag.dart';
import '../widgets/custom_action_button.dart';

class DetailScreen extends StatelessWidget {
  final Vehiculo vehiculo; // Exigimos la instancia completa por constructor

  const DetailScreen({super.key, required this.vehiculo});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppTheme.backgroundColor,
      // CustomScrollView permite efectos avanzados de scroll como el SliverAppBar
      body: CustomScrollView(
        slivers: [
          SliverAppBar(
            expandedHeight: 280.0,
            pinned: true,
            backgroundColor: AppTheme.primaryColor,
            foregroundColor: Colors.white,
            flexibleSpace: FlexibleSpaceBar(
              title: Text(
                '${vehiculo.marca} ${vehiculo.modelo}',
                style: const TextStyle(
                  fontWeight: FontWeight.bold,
                  fontSize: 16,
                  color: Colors.white,
                  backgroundColor: Colors.black45,
                ),
              ),
              background: Image.network(
                vehiculo.imagenUrl,
                fit: BoxFit.cover,
                errorBuilder: (context, error, stackTrace) => Container(
                  color: Colors.grey.shade300,
                  child: const Center(
                    child: Icon(Icons.directions_car, size: 60),
                  ),
                ),
              ),
            ),
          ),
          SliverToBoxAdapter(
            child: Padding(
              padding: const EdgeInsets.all(24.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Expanded(
                        child: SectionHeader(
                          title: 'Categoría: ${vehiculo.categoria}',
                          subtitle: 'Modelo año ${vehiculo.anio}',
                        ),
                      ),
                      PriceTag(precio: vehiculo.precio),
                    ],
                  ),
                  const SizedBox(height: 16),
                  SpecBadge(
                    icon: Icons.engineering,
                    label: 'Motorización',
                    value: vehiculo.motor,
                  ),
                  const SizedBox(height: 10),
                  SpecBadge(
                    icon: Icons.settings,
                    label: 'Transmisión',
                    value: vehiculo.transmision,
                  ),
                  const SizedBox(height: 28),
                  const Text(
                    'EQUIPAMIENTO',
                    style: TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                      letterSpacing: 2,
                      color: AppTheme.textPrimary,
                    ),
                  ),
                  const Divider(thickness: 2),
                  const SizedBox(height: 10),
                  // Mapeamos la lista de Strings a una lista de Widgets Text
                  ...vehiculo.equipamiento.map(
                    (item) => Padding(
                      padding: const EdgeInsets.symmetric(vertical: 4),
                      child: Row(
                        children: [
                          const Icon(
                            Icons.check_circle_outline,
                            size: 20,
                            color: Colors.grey,
                          ),
                          const SizedBox(width: 10),
                          Expanded(
                            child: Text(
                              item,
                              style: const TextStyle(fontSize: 16),
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                  const SizedBox(height: 36),
                  const Text(
                    'PROCEDIMIENTO DE REVISIÓN',
                    style: TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                      letterSpacing: 2,
                      color: AppTheme.textPrimary,
                    ),
                  ),
                  const Divider(thickness: 2),
                  const SizedBox(height: 10),
                  // Usamos .asMap() para obtener el índice y numerar los pasos
                  ...vehiculo.pasosRevision.asMap().entries.map(
                    (entrada) => Padding(
                      padding: const EdgeInsets.symmetric(vertical: 8),
                      child: Row(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            '${entrada.key + 1}. ',
                            style: const TextStyle(
                              fontSize: 16,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                          Expanded(
                            child: Text(
                              entrada.value,
                              style: const TextStyle(
                                fontSize: 16,
                                height: 1.5,
                              ),
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                  const SizedBox(height: 28),
                  CustomActionButton(
                    text: 'Regresar al Catálogo',
                    icon: Icons.arrow_back,
                    onPressed: () => Navigator.pop(context),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}