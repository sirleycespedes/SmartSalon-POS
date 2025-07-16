import { PartialType } from '@nestjs/mapped-types';
import { CreateUsuarioDto } from './create-usuario.dto';
import { IsOptional, IsString, MinLength, IsEmail, IsNumber, IsEnum, IsObject } from 'class-validator';

export class UpdateUsuarioDto extends PartialType(CreateUsuarioDto) {
  @IsOptional()
  @IsString()
  @MinLength(6, { message: 'La contraseña debe tener al menos 6 caracteres' })
  password?: string;

  @IsOptional()
  @IsString()
  username?: string;

  @IsOptional()
  @IsEmail({}, { message: 'El email debe tener un formato válido' })
  email?: string;

  @IsOptional()
  @IsNumber()
  rol_id?: number;

  @IsOptional()
  @IsNumber()
  compania_id?: number;

  @IsOptional()
  @IsObject()
  configuracion_usuario?: Record<string, any>;

  @IsOptional()
  @IsEnum(['activo', 'inactivo', 'suspendido'], { 
    message: 'El estado debe ser: activo, inactivo o suspendido' 
  })
  estado?: 'activo' | 'inactivo' | 'suspendido';
}

