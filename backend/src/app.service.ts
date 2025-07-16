import { Injectable } from '@nestjs/common';

@Injectable()
export class AppService {
  getHello(): string {
    return 'SmartSalon POS API - Sistema de Punto de Venta para Peluquerías y Barberías';
  }
}

