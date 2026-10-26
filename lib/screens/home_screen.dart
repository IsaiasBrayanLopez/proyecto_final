import 'package:flutter/material.dart';
import '../models/vehiculo.dart';
import '../services/vehiculo_service.dart';
import '../widgets/custom_app_bar.dart';
import '../widgets/section_header.dart';
import '../widgets/stat_counter_card.dart';
import '../widgets/custom_action_button.dart';
import 'catalog_screen.dart';
import 'favorites_screen.dart';
import 'about_screen.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final VehiculoService _service = VehiculoService();
  late Future<List<Vehiculo>> _futureVehiculos;
  final Set<int> _favoritosIds = {};

  @override
  void initState() {
    super.initState();
    _futureVehiculos = _service.cargarVehiculos();
  }

  void _toggleFavorito(int id) {
    setState(() {
      if (_favoritosIds.contains(id)) {
        _favoritosIds.remove(id);
      } else {
        _favoritosIds.add(id);
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: const CustomAppBar(title: 'Directorio Automotriz'),
      body: FutureBuilder<List<Vehiculo>>(
        future: _futureVehiculos,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }
          if (snapshot.hasError) {
            return const Center(child: Text('Error al cargar datos del JSON'));
          }

          final vehiculos = snapshot.data!;

          return SingleChildScrollView(
            padding: const EdgeInsets.all(16.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const SectionHeader(
                  title: 'Catálogo Automotriz Digital',
                  subtitle: 'Explora fichas técnicas, equipamiento y precios.',
                ),
                const SizedBox(height: 16),
                Row(
                  children: [
                    StatCounterCard(
                      title: 'Unidades en JSON',
                      count: '${vehiculos.length}',
                      icon: Icons.directions_car_filled,
                    ),
                    const SizedBox(width: 10),
                    StatCounterCard(
                      title: 'Guardados',
                      count: '${_favoritosIds.length}',
                      icon: Icons.bookmark,
                    ),
                  ],
                ),
                const SizedBox(height: 24),
                CustomActionButton(
                  text: 'Explorar Catálogo Completo',
                  icon: Icons.list_alt,
                  onPressed: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (context) => CatalogScreen(
                          vehiculos: vehiculos,
                          favoritosIds: _favoritosIds,
                          onToggleFavorito: _toggleFavorito,
                        ),
                      ),
                    ).then((_) => setState(() {}));
                  },
                ),
                const SizedBox(height: 12),
                CustomActionButton(
                  text: 'Ver Mis Vehículos Guardados',
                  icon: Icons.bookmarks_outlined,
                  onPressed: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (context) => FavoritesScreen(
                          vehiculos: vehiculos,
                          favoritosIds: _favoritosIds,
                          onToggleFavorito: _toggleFavorito,
                        ),
                      ),
                    ).then((_) => setState(() {}));
                  },
                ),
                const SizedBox(height: 12),
                CustomActionButton(
                  text: 'Acerca del Proyecto y Bina',
                  icon: Icons.info_outline,
                  onPressed: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (context) => const AboutScreen(),
                      ),
                    );
                  },
                ),
              ],
            ),
          );
        },
      ),
    );
  }
}