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
import { CompaniasService } from './companias.service';
import { CreateCompaniaDto } from './dto/create-compania.dto';
import { UpdateCompaniaDto } from './dto/update-compania.dto';
import { JwtAuthGuard } from '../auth/guards/jwt-auth.guard';

@Controller('companias')
@UseGuards(JwtAuthGuard)
export class CompaniasController {
  constructor(private readonly companiasService: CompaniasService) {}

  @Post()
  async create(@Body() createCompaniaDto: CreateCompaniaDto) {
    const compania = await this.companiasService.create(createCompaniaDto);
    return {
      message: 'Compañía creada exitosamente',
      compania
    };
  }

  @Get()
  async findAll(
    @Query('page') page: number = 1,
    @Query('limit') limit: number = 10,
    @Query('search') search?: string,
    @Query('estado') estado?: string
  ) {
    return this.companiasService.findAll({
      page: Number(page),
      limit: Number(limit),
      search,
      estado
    });
  }

  @Get(':id')
  async findOne(@Param('id', ParseIntPipe) id: number) {
    const compania = await this.companiasService.findOne(id);
    return {
      compania
    };
  }

  @Patch(':id')
  async update(
    @Param('id', ParseIntPipe) id: number, 
    @Body() updateCompaniaDto: UpdateCompaniaDto
  ) {
    const compania = await this.companiasService.update(id, updateCompaniaDto);
    return {
      message: 'Compañía actualizada exitosamente',
      compania
    };
  }

  @Delete(':id')
  async remove(@Param('id', ParseIntPipe) id: number) {
    await this.companiasService.remove(id);
    return {
      message: 'Compañía eliminada exitosamente'
    };
  }

  @Patch(':id/restore')
  async restore(@Param('id', ParseIntPipe) id: number) {
    const compania = await this.companiasService.restore(id);
    return {
      message: 'Compañía restaurada exitosamente',
      compania
    };
  }
}

