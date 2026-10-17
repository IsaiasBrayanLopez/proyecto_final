import 'dart:convert';
import 'package:flutter/services.dart';
import '../models/vehiculo.dart';

class VehiculoService {

  // Método asíncrono para leer el archivo JSON local
  Future<List<Vehiculo>> cargarVehiculos() async {
    final String respuesta =
        await rootBundle.loadString('assets/data/vehiculos.json');
    final List<dynamic> datosDecodificados = jsonDecode(respuesta);
    return datosDecodificados
        .map((json) => Vehiculo.fromJson(json))
        .toList();
  }
}