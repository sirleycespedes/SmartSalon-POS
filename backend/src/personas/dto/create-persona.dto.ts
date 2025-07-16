import { IsString, IsNotEmpty, IsEmail, IsOptional, IsObject, Matches, IsNumber, IsDateString, IsEnum } from "class-validator";

export class CreatePersonaDto {
  @IsString()
  @IsNotEmpty({ message: "Los nombres son requeridos" })
  nombres: string;

  @IsString()
  @IsNotEmpty({ message: "Los apellidos son requeridos" })
  apellidos: string;

  @IsOptional()
  @IsString()
  @Matches(/^\+?[0-9\s\-\(\)]{7,20}$/, { message: "El teléfono debe tener un formato válido" })
  telefono?: string;

  @IsOptional()
  @IsEmail({}, { message: "El email debe tener un formato válido" })
  email?: string;

  @IsOptional()
  @IsString()
  direccion?: string;

  @IsOptional()
  @IsDateString({}, { message: "La fecha de nacimiento debe ser una fecha válida" })
  fecha_nacimiento?: Date;

  @IsEnum(["cliente", "empleado", "proveedor"], { message: "El tipo de persona debe ser: cliente, empleado o proveedor" })
  @IsNotEmpty({ message: "El tipo de persona es requerido" })
  tipo: "cliente" | "empleado" | "proveedor";

  @IsOptional()
  @IsNumber({}, { message: "El ID del tipo de identificación debe ser un número" })
  tipo_identificacion_id?: number;

  @IsString()
  @IsNotEmpty({ message: "El número de identificación es requerido" })
  numero_identificacion: string;

  @IsOptional()
  @IsObject()
  datos_adicionales?: Record<string, any>;

  @IsOptional()
  @IsEnum(["activo", "inactivo", "suspendido"], { 
    message: "El estado debe ser: activo, inactivo o suspendido" 
  })
  estado?: "activo" | "inactivo" | "suspendido";
}

