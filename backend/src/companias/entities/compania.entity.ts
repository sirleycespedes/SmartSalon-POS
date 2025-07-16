export interface Compania {
  id: number;
  uuid: string;
  nombre: string;
  nit: string;
  direccion?: string;
  telefono: string;
  email?: string;
  pais: string;
  estado: 'activo' | 'inactivo' | 'suspendido';
  configuracion: Record<string, any>;
  created_at: Date;
  updated_at: Date;
  deleted_at?: Date;
}

