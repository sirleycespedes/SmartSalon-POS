import { IsString, IsNotEmpty, IsEmail, IsOptional, IsObject, Matches } from 'class-validator';

export class CreateCompaniaDto {
  @IsString()
  @IsNotEmpty({ message: 'El nombre de la compañía es requerido' })
  nombre: string;

  @IsString()
  @IsNotEmpty({ message: 'El NIT es requerido' })
  @Matches(/^[0-9\-]{5,20}$/, { message: 'El NIT debe tener un formato válido' })
  nit: string;

  @IsOptional()
  @IsString()
  direccion?: string;

  @IsString()
  @IsNotEmpty({ message: 'El teléfono es requerido' })
  @Matches(/^\+?[0-9\s\-\(\)]{7,20}$/, { message: 'El teléfono debe tener un formato válido' })
  telefono: string;

  @IsOptional()
  @IsEmail({}, { message: 'El email debe tener un formato válido' })
  email?: string;

  @IsOptional()
  @IsString()
  pais?: string;

  @IsOptional()
  @IsObject()
  configuracion?: Record<string, any>;
}

