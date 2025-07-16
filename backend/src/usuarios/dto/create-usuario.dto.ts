import { IsString, IsNotEmpty, IsEmail, IsOptional, IsObject, IsNumber, MinLength, IsEnum } from 'class-validator';

export class CreateUsuarioDto {
  @IsNumber()
  @IsNotEmpty({ message: 'El ID de la persona es requerido' })
  persona_id: number;

  @IsString()
  @IsNotEmpty({ message: 'El username es requerido' })
  username: string;

  @IsEmail({}, { message: 'El email debe tener un formato válido' })
  @IsNotEmpty({ message: 'El email es requerido' })
  email: string;

  @IsString()
  @IsNotEmpty({ message: 'La contraseña es requerida' })
  @MinLength(6, { message: 'La contraseña debe tener al menos 6 caracteres' })
  password: string;

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

