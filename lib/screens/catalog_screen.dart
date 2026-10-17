import 'package:flutter/material.dart';
import '../models/vehiculo.dart';
import '../widgets/custom_app_bar.dart';
import '../widgets/category_chip.dart';
import '../widgets/vehiculo_card.dart';
import '../widgets/empty_state_view.dart';
import 'detail_screen.dart';

class CatalogScreen extends StatefulWidget {
  final List<Vehiculo> vehiculos;
  final Set<int> favoritosIds;
  final Function(int) onToggleFavorito;

  const CatalogScreen({
    super.key,
    required this.vehiculos,
    required this.favoritosIds,
    required this.onToggleFavorito,
  });

  @override
  State<CatalogScreen> createState() => _CatalogScreenState();
}

class _CatalogScreenState extends State<CatalogScreen> {
  String _categoriaSeleccionada = 'Todos';
  final List<String> _categorias = [
    'Todos',
    'Sedán',
    'SUV',
    'Motocicleta',
    'Pickup',
  ];

  @override
  Widget build(BuildContext context) {
    final listaFiltrada = _categoriaSeleccionada == 'Todos'
        ? widget.vehiculos
        : widget.vehiculos
            .where((v) => v.categoria == _categoriaSeleccionada)
            .toList();

    return Scaffold(
      appBar: const CustomAppBar(title: 'Catálogo de Vehículos'),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            SingleChildScrollView(
              scrollDirection: Axis.horizontal,
              child: Row(
                children: _categorias.map((cat) {
                  return CategoryChip(
                    label: cat,
                    isSelected: _categoriaSeleccionada == cat,
                    onTap: () {
                      setState(() {
                        _categoriaSeleccionada = cat;
                      });
                    },
                  );
                }).toList(),
              ),
            ),
            const SizedBox(height: 16),
            Expanded(
              child: listaFiltrada.isEmpty
                  ? const EmptyStateView(
                      message: 'No hay vehículos en esta categoría.',
                      icon: Icons.search_off,
                    )
                  : ListView.builder(
                      itemCount: listaFiltrada.length,
                      itemBuilder: (context, index) {
                        final item = listaFiltrada[index];
                        return VehiculoCard(
                          vehiculo: item,
                          isFavorite: widget.favoritosIds.contains(item.id),
                          onFavoriteToggle: () {
                            setState(() {
                              widget.onToggleFavorito(item.id);
                            });
                          },
                          onTap: () {
                            // Navegamos a la vista de detalle pasando el OBJETO completo
                            Navigator.push(
                              context,
                              MaterialPageRoute(
                                builder: (context) =>
                                    DetailScreen(vehiculo: item),
                              ),
                            );
                          },
                        );
                      },
                    ),
            ),
          ],
        ),
      ),
    );
  }
}