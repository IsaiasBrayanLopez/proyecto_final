import 'package:flutter/material.dart';
import '../models/vehiculo.dart';
import '../widgets/custom_app_bar.dart';
import '../widgets/vehiculo_card.dart';
import '../widgets/empty_state_view.dart';
import 'detail_screen.dart';

class FavoritesScreen extends StatefulWidget {
  final List<Vehiculo> vehiculos;
  final Set<int> favoritosIds;
  final Function(int) onToggleFavorito;

  const FavoritesScreen({
    super.key,
    required this.vehiculos,
    required this.favoritosIds,
    required this.onToggleFavorito,
  });

  @override
  State<FavoritesScreen> createState() => _FavoritesScreenState();
}

class _FavoritesScreenState extends State<FavoritesScreen> {
  @override
  Widget build(BuildContext context) {
    final favoritos = widget.vehiculos
        .where((v) => widget.favoritosIds.contains(v.id))
        .toList();

    return Scaffold(
      appBar: const CustomAppBar(title: 'Vehículos Guardados'),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: favoritos.isEmpty
            ? const EmptyStateView(
                message: 'Aún no has guardado vehículos en tu lista.',
                icon: Icons.bookmark_border,
              )
            : ListView.builder(
                itemCount: favoritos.length,
                itemBuilder: (context, index) {
                  final item = favoritos[index];
                  return VehiculoCard(
                    vehiculo: item,
                    isFavorite: true,
                    onFavoriteToggle: () {
                      setState(() {
                        widget.onToggleFavorito(item.id);
                      });
                    },
                    onTap: () {
                      Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (context) => DetailScreen(vehiculo: item),
                        ),
                      );
                    },
                  );
                },
              ),
      ),
    );
  }
}