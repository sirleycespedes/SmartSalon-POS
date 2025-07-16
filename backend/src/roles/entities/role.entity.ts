export interface Role {
  id: number;
  nombre: string;
  descripcion?: string;
  permisos: Record<string, any>;
  compania_id?: number;
  es_sistema: boolean;
  created_at: Date;
  updated_at: Date;
}

