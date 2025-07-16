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
import { UsuariosService } from './usuarios.service';
import { CreateUsuarioDto } from './dto/create-usuario.dto';
import { UpdateUsuarioDto } from './dto/update-usuario.dto';
import { JwtAuthGuard } from '../auth/guards/jwt-auth.guard';

@Controller('usuarios')
@UseGuards(JwtAuthGuard)
export class UsuariosController {
  constructor(private readonly usuariosService: UsuariosService) {}

  @Post()
  async create(@Body() createUsuarioDto: CreateUsuarioDto) {
    const usuario = await this.usuariosService.create(createUsuarioDto);
    return {
      message: 'Usuario creado exitosamente',
      usuario
    };
  }

  @Get()
  async findAll(
    @Query('page') page: number = 1,
    @Query('limit') limit: number = 10,
    @Query('search') search?: string,
    @Query('estado') estado?: string,
    @Query('rol_id', ParseIntPipe) rol_id?: number,
    @Query('compania_id', ParseIntPipe) compania_id?: number
  ) {
    return this.usuariosService.findAll({
      page: Number(page),
      limit: Number(limit),
      search,
      estado,
      rol_id,
      compania_id
    });
  }

  @Get(':id')
  async findOne(@Param('id', ParseIntPipe) id: number) {
    const usuario = await this.usuariosService.findOne(id);
    return {
      usuario
    };
  }

  @Patch(':id')
  async update(
    @Param('id', ParseIntPipe) id: number, 
    @Body() updateUsuarioDto: UpdateUsuarioDto
  ) {
    const usuario = await this.usuariosService.update(id, updateUsuarioDto);
    return {
      message: 'Usuario actualizado exitosamente',
      usuario
    };
  }

  @Delete(':id')
  async remove(@Param('id', ParseIntPipe) id: number) {
    await this.usuariosService.remove(id);
    return {
      message: 'Usuario eliminado exitosamente'
    };
  }

  @Patch(':id/restore')
  async restore(@Param('id', ParseIntPipe) id: number) {
    const usuario = await this.usuariosService.restore(id);
    return {
      message: 'Usuario restaurado exitosamente',
      usuario
    };
  }
}

