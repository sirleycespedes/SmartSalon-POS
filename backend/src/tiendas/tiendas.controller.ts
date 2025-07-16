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
import { TiendasService } from './tiendas.service';
import { CreateTiendaDto } from './dto/create-tienda.dto';
import { UpdateTiendaDto } from './dto/update-tienda.dto';
import { JwtAuthGuard } from '../auth/guards/jwt-auth.guard';

@Controller('tiendas')
@UseGuards(JwtAuthGuard)
export class TiendasController {
  constructor(private readonly tiendasService: TiendasService) {}

  @Post()
  async create(@Body() createTiendaDto: CreateTiendaDto) {
    const tienda = await this.tiendasService.create(createTiendaDto);
    return {
      message: 'Tienda creada exitosamente',
      tienda
    };
  }

  @Get()
  async findAll(
    @Query('page') page: number = 1,
    @Query('limit') limit: number = 10,
    @Query('search') search?: string,
    @Query('estado') estado?: string,
    @Query('compania_id', ParseIntPipe) compania_id?: number
  ) {
    return this.tiendasService.findAll({
      page: Number(page),
      limit: Number(limit),
      search,
      estado,
      compania_id
    });
  }

  @Get(':id')
  async findOne(@Param('id', ParseIntPipe) id: number) {
    const tienda = await this.tiendasService.findOne(id);
    return {
      tienda
    };
  }

  @Patch(':id')
  async update(
    @Param('id', ParseIntPipe) id: number, 
    @Body() updateTiendaDto: UpdateTiendaDto
  ) {
    const tienda = await this.tiendasService.update(id, updateTiendaDto);
    return {
      message: 'Tienda actualizada exitosamente',
      tienda
    };
  }

  @Delete(':id')
  async remove(@Param('id', ParseIntPipe) id: number) {
    await this.tiendasService.remove(id);
    return {
      message: 'Tienda eliminada exitosamente'
    };
  }

  @Patch(':id/restore')
  async restore(@Param('id', ParseIntPipe) id: number) {
    const tienda = await this.tiendasService.restore(id);
    return {
      message: 'Tienda restaurada exitosamente',
      tienda
    };
  }
}

