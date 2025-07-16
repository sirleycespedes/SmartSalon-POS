export interface Tienda {
  id: number;
  uuid: string;
  nombre: string;
  codigo: string;
  direccion?: string;
  ciudad?: string;
  estado_provincia?: string;
  codigo_postal?: string;
  coordenadas?: { x: number; y: number };
  compania_id: number;
  telefono?: string;
  email?: string;
  horario_atencion?: Record<string, any>;
  estado: string;
  configuracion?: Record<string, any>;
  created_at: Date;
  updated_at: Date;
  deleted_at?: Date;
}

