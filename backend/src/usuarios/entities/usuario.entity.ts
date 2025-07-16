export interface Usuario {
  id: number;
  uuid: string;
  persona_id: number;
  username: string;
  email: string;
  password_hash: string;
  salt: string;
  rol_id?: number;
  compania_id?: number;
  ultimo_acceso?: Date;
  intentos_fallidos: number;
  bloqueado_hasta?: Date;
  configuracion_usuario?: Record<string, any>;
  estado: string;
  created_at: Date;
  updated_at: Date;
  deleted_at?: Date;
  
  // Propiedades de unión (opcionales)
  nombres?: string;
  apellidos?: string;
  nombre_completo?: string;
  telefono?: string;
  persona_email?: string;
  rol_nombre?: string;
  compania_nombre?: string;
  persona?: any; // Añadido para jwt.strategy.ts
  rol?: any; // Añadido para jwt.strategy.ts
  compania?: any; // Añadido para jwt.strategy.ts
}

