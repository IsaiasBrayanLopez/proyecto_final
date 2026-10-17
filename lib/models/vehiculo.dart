class Vehiculo {
  final int id;
  final String marca;
  final String modelo;
  final int anio;
  final String categoria;
  final double precio;
  final String motor;
  final String transmision;
  final String imagenUrl;
  final List<String> equipamiento;
  final List<String> pasosRevision;

  const Vehiculo({
    required this.id,
    required this.marca,
    required this.modelo,
    required this.anio,
    required this.categoria,
    required this.precio,
    required this.motor,
    required this.transmision,
    required this.imagenUrl,
    required this.equipamiento,
    required this.pasosRevision,
  });

  // Constructor Factory: Transforma el diccionario JSON en un Objeto Dart
  factory Vehiculo.fromJson(Map<String, dynamic> json) {
    return Vehiculo(
      id: json['id'],
      marca: json['marca'],
      modelo: json['modelo'],
      anio: json['anio'],
      categoria: json['categoria'],
      precio: (json['precio'] as num).toDouble(),
      motor: json['motor'],
      transmision: json['transmision'],
      imagenUrl: json['imagenUrl'],
      // Casteo seguro de listas dinámicas a listas de Strings
      equipamiento: List<String>.from(json['equipamiento']),
      pasosRevision: List<String>.from(json['pasosRevision']),
    );
  }
}