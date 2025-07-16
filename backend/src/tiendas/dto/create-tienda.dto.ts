import { IsString, IsNotEmpty, IsEmail, IsOptional, IsObject, Matches, IsNumber, IsJSON, ValidateNested, IsEnum } from 'class-validator';
import { Type } from 'class-transformer';

class CoordenadasDto {
  @IsNumber()
  x: number;

  @IsNumber()
  y: number;
}

export class CreateTiendaDto {
  @IsString()
  @IsNotEmpty({ message: 'El nombre de la tienda es requerido' })
  nombre: string;

  @IsString()
  @IsNotEmpty({ message: 'El código de la tienda es requerido' })
  codigo: string;

  @IsOptional()
  @IsString()
  direccion?: string;

  @IsOptional()
  @IsString()
  ciudad?: string;

  @IsOptional()
  @IsString()
  estado_provincia?: string;

  @IsOptional()
  @IsString()
  codigo_postal?: string;

  @IsOptional()
  @ValidateNested()
  @Type(() => CoordenadasDto)
  coordenadas?: CoordenadasDto;

  @IsNumber()
  @IsNotEmpty({ message: 'El ID de la compañía es requerido' })
  compania_id: number;

  @IsOptional()
  @IsString()
  @Matches(/^\+?[0-9\s\-\(\)]{7,20}$/, { message: 'El teléfono debe tener un formato válido' })
  telefono?: string;

  @IsOptional()
  @IsEmail({}, { message: 'El email debe tener un formato válido' })
  email?: string;

  @IsOptional()
  @IsObject()
  horario_atencion?: Record<string, any>;

  @IsOptional()
  @IsEnum(['activo', 'inactivo', 'suspendido'], { 
    message: 'El estado debe ser: activo, inactivo o suspendido' 
  })
  estado?: 'activo' | 'inactivo' | 'suspendido';

  @IsOptional()
  @IsObject()
  configuracion?: Record<string, any>;
}

