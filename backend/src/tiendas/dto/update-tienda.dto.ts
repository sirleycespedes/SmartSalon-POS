import { PartialType } from '@nestjs/mapped-types';
import { CreateTiendaDto } from './create-tienda.dto';
import { IsOptional, IsEnum, IsString, IsNumber, ValidateNested } from 'class-validator';
import { Type } from 'class-transformer';

class CoordenadasDto {
  @IsNumber()
  x: number;

  @IsNumber()
  y: number;
}

export class UpdateTiendaDto extends PartialType(CreateTiendaDto) {
  @IsOptional()
  @IsEnum(["activo", "inactivo", "suspendido"], { 
    message: "El estado debe ser: activo, inactivo o suspendido" 
  })
  estado?: "activo" | "inactivo" | "suspendido";

  @IsOptional()
  @IsString()
  codigo?: string;

  @IsOptional()
  @IsNumber()
  compania_id?: number;

  @IsOptional()
  @ValidateNested()
  @Type(() => CoordenadasDto)
  coordenadas?: CoordenadasDto;
}

