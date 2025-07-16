import { PartialType } from '@nestjs/mapped-types';
import { CreateCompaniaDto } from './create-compania.dto';
import { IsOptional, IsEnum } from 'class-validator';

export class UpdateCompaniaDto extends PartialType(CreateCompaniaDto) {
  @IsOptional()
  @IsEnum(['activo', 'inactivo', 'suspendido'], { 
    message: 'El estado debe ser: activo, inactivo o suspendido' 
  })
  estado?: 'activo' | 'inactivo' | 'suspendido';
}

