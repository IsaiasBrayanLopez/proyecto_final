import 'dart:convert';
import 'package:flutter/services.dart';
import '../models/vehiculo.dart';

class VehiculoService {
  Future<List<Vehiculo>> cargarVehiculos() async {
    final String respuesta = await rootBundle.loadString('assets/data/vehiculos.json');
    final List<dynamic> datos = json.decode(respuesta);
    return datos.map((item) => Vehiculo.fromJson(item)).toList();
  }
}