import { 
  Controller, 
  Get, 
  Post, 
  Body, 
  Patch, 
  Param, 
  Delete, 
  UseGuards,
  Query,
  ParseIntPipe
} from '@nestjs/common';
import { PersonasService } from './personas.service';
import { CreatePersonaDto } from './dto/create-persona.dto';
import { UpdatePersonaDto } from './dto/update-persona.dto';
import { JwtAuthGuard } from '../auth/guards/jwt-auth.guard';

@Controller('personas')
@UseGuards(JwtAuthGuard)
export class PersonasController {
  constructor(private readonly personasService: PersonasService) {}

  @Post()
  async create(@Body() createPersonaDto: CreatePersonaDto) {
    const persona = await this.personasService.create(createPersonaDto);
    return {
      message: 'Persona creada exitosamente',
      persona
    };
  }

  @Get()
  async findAll(
    @Query('page') page: number = 1,
    @Query('limit') limit: number = 10,
    @Query('search') search?: string,
    @Query('estado') estado?: string,
    @Query('tipo') tipo?: string,
    @Query('tipo_identificacion_id', ParseIntPipe) tipo_identificacion_id?: number
  ) {
    return this.personasService.findAll({
      page: Number(page),
      limit: Number(limit),
      search,
      estado,
      tipo,
      tipo_identificacion_id
    });
  }

  @Get(':id')
  async findOne(@Param('id', ParseIntPipe) id: number) {
    const persona = await this.personasService.findOne(id);
    return {
      persona
    };
  }

  @Patch(':id')
  async update(
    @Param('id', ParseIntPipe) id: number, 
    @Body() updatePersonaDto: UpdatePersonaDto
  ) {
    const persona = await this.personasService.update(id, updatePersonaDto);
    return {
      message: 'Persona actualizada exitosamente',
      persona
    };
  }

  @Delete(':id')
  async remove(@Param('id', ParseIntPipe) id: number) {
    await this.personasService.remove(id);
    return {
      message: 'Persona eliminada exitosamente'
    };
  }

  @Patch(':id/restore')
  async restore(@Param('id', ParseIntPipe) id: number) {
    const persona = await this.personasService.restore(id);
    return {
      message: 'Persona restaurada exitosamente',
      persona
    };
  }
}

