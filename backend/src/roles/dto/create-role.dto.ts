import { IsString, IsNotEmpty, IsOptional, IsObject, IsNumber, IsBoolean } from 'class-validator';

export class CreateRoleDto {
  @IsString()
  @IsNotEmpty({ message: 'El nombre del rol es requerido' })
  nombre: string;

  @IsOptional()
  @IsString()
  descripcion?: string;

  @IsOptional()
  @IsObject()
  permisos?: Record<string, any>;

  @IsOptional()
  @IsNumber()
  compania_id?: number;

  @IsOptional()
  @IsBoolean()
  es_sistema?: boolean;
}

