export interface Persona {
  id: number;
  uuid: string;
  nombres: string;
  apellidos: string;
  nombre_completo: string;
  telefono?: string;
  email?: string;
  direccion?: string;
  fecha_nacimiento?: Date;
  tipo: string;
  tipo_identificacion_id?: number;
  numero_identificacion: string;
  datos_adicionales?: Record<string, any>;
  estado: string;
  created_at: Date;
  updated_at: Date;
  deleted_at?: Date;

  // Propiedades de unión (opcionales)
  tipo_identificacion_nombre?: string;
}

