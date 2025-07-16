import { Injectable, NotFoundException, ConflictException } from '@nestjs/common';
import { DatabaseService } from '../database/database.service';
import { CreateTiendaDto } from './dto/create-tienda.dto';
import { UpdateTiendaDto } from './dto/update-tienda.dto';
import { Tienda } from './entities/tienda.entity';

@Injectable()
export class TiendasService {
  constructor(private readonly databaseService: DatabaseService) {}

  async create(createTiendaDto: CreateTiendaDto): Promise<Tienda> {
    // Verificar si ya existe una tienda con el mismo código en la misma compañía
    const existingTienda = await this.findByCodigoAndCompania(createTiendaDto.codigo, createTiendaDto.compania_id);
    if (existingTienda) {
      throw new ConflictException(
        `Ya existe una tienda con el código ${createTiendaDto.codigo} para la compañía ${createTiendaDto.compania_id}`,
      );
    }

    const query = `
      INSERT INTO tiendas (
        nombre, codigo, direccion, ciudad, estado_provincia, codigo_postal,
        coordenadas, compania_id, telefono, email, horario_atencion, estado, configuracion
      )
      VALUES ($1, $2, $3, $4, $5, $6, POINT($7, $8), $9, $10, $11, $12, $13, $14)
      RETURNING *
    `;

    const values = [
      createTiendaDto.nombre,
      createTiendaDto.codigo,
      createTiendaDto.direccion || null,
      createTiendaDto.ciudad || null,
      createTiendaDto.estado_provincia || null,
      createTiendaDto.codigo_postal || null,
      createTiendaDto.coordenadas?.x || null,
      createTiendaDto.coordenadas?.y || null,
      createTiendaDto.compania_id,
      createTiendaDto.telefono || null,
      createTiendaDto.email || null,
      JSON.stringify(createTiendaDto.horario_atencion || {}),
      createTiendaDto.estado || 'activo',
      JSON.stringify(createTiendaDto.configuracion || {}),
    ];

    const result = await this.databaseService.query(query, values);
    return result.rows[0];
  }

  async findAll(
    options: {
      page?: number;
      limit?: number;
      search?: string;
      estado?: string;
      compania_id?: number;
    } = {},
  ): Promise<{ tiendas: Tienda[]; total: number; page: number; limit: number }> {
    const { page = 1, limit = 10, search, estado, compania_id } = options;
    const offset = (page - 1) * limit;

    let whereClause = 'WHERE deleted_at IS NULL';
    const queryParams: any[] = [];
    let paramIndex = 1;

    if (search) {
      whereClause += ` AND (nombre ILIKE $${paramIndex} OR codigo ILIKE $${paramIndex})`;
      queryParams.push(`%${search}%`);
      paramIndex++;
    }

    if (estado) {
      whereClause += ` AND estado = $${paramIndex}`;
      queryParams.push(estado);
      paramIndex++;
    }

    if (compania_id) {
      whereClause += ` AND compania_id = $${paramIndex}`;
      queryParams.push(compania_id);
      paramIndex++;
    }

    // Query para contar total
    const countQuery = `SELECT COUNT(*) FROM tiendas ${whereClause}`;
    const countResult = await this.databaseService.query(countQuery, queryParams);
    const total = parseInt(countResult.rows[0].count);

    // Query para obtener datos paginados
    const dataQuery = `
      SELECT * FROM tiendas 
      ${whereClause}
      ORDER BY created_at DESC
      LIMIT $${paramIndex} OFFSET $${paramIndex + 1}
    `;

    queryParams.push(limit, offset);
    const dataResult = await this.databaseService.query(dataQuery, queryParams);

    return {
      tiendas: dataResult.rows,
      total,
      page,
      limit,
    };
  }

  async findOne(id: number): Promise<Tienda> {
    const query = 'SELECT * FROM tiendas WHERE id = $1 AND deleted_at IS NULL';
    const result = await this.databaseService.query(query, [id]);

    if (result.rows.length === 0) {
      throw new NotFoundException('Tienda no encontrada');
    }

    return result.rows[0];
  }

  async findByCodigoAndCompania(codigo: string, compania_id: number): Promise<Tienda | null> {
    const query = 'SELECT * FROM tiendas WHERE codigo = $1 AND compania_id = $2 AND deleted_at IS NULL';
    const result = await this.databaseService.query(query, [codigo, compania_id]);
    return result.rows[0] || null;
  }

  async update(id: number, updateTiendaDto: UpdateTiendaDto): Promise<Tienda> {
    const tienda = await this.findOne(id);

    // Si se está actualizando el código o la compañía, verificar unicidad
    if (
      (updateTiendaDto.codigo && updateTiendaDto.codigo !== tienda.codigo) ||
      (updateTiendaDto.compania_id && updateTiendaDto.compania_id !== tienda.compania_id)
    ) {
      const existingTienda = await this.findByCodigoAndCompania(
        updateTiendaDto.codigo || tienda.codigo,
        updateTiendaDto.compania_id || tienda.compania_id,
      );
      if (existingTienda && existingTienda.id !== id) {
        throw new ConflictException(
          `Ya existe una tienda con el código ${updateTiendaDto.codigo || tienda.codigo} para la compañía ${updateTiendaDto.compania_id || tienda.compania_id}`,
        );
      }
    }

    const updateFields: string[] = [];
    const values: any[] = [];
    let paramIndex = 1;

    Object.keys(updateTiendaDto).forEach((key) => {
      if (updateTiendaDto[key] !== undefined) {
        if (key === 'horario_atencion' || key === 'configuracion') {
          updateFields.push(`${key} = $${paramIndex}`);
          values.push(JSON.stringify(updateTiendaDto[key]));
        } else if (key === 'coordenadas') {
          updateFields.push(`coordenadas = POINT($${paramIndex}, $${paramIndex + 1})`);
          values.push(updateTiendaDto[key].x, updateTiendaDto[key].y);
          paramIndex++; // Incrementa una vez más por el segundo parámetro de POINT
        } else {
          updateFields.push(`${key} = $${paramIndex}`);
          values.push(updateTiendaDto[key]);
        }
        paramIndex++;
      }
    });

    if (updateFields.length === 0) {
      return tienda;
    }

    updateFields.push(`updated_at = CURRENT_TIMESTAMP`);
    values.push(id);

    const query = `
      UPDATE tiendas 
      SET ${updateFields.join(', ')}
      WHERE id = $${paramIndex} AND deleted_at IS NULL
      RETURNING *
    `;

    const result = await this.databaseService.query(query, values);
    return result.rows[0];
  }

  async remove(id: number): Promise<void> {
    await this.findOne(id); // Verificar que existe

    const query = `
      UPDATE tiendas 
      SET deleted_at = CURRENT_TIMESTAMP, updated_at = CURRENT_TIMESTAMP
      WHERE id = $1
    `;

    await this.databaseService.query(query, [id]);
  }

  async restore(id: number): Promise<Tienda> {
    const query = `
      UPDATE tiendas 
      SET deleted_at = NULL, updated_at = CURRENT_TIMESTAMP
      WHERE id = $1
      RETURNING *
    `;

    const result = await this.databaseService.query(query, [id]);

    if (result.rows.length === 0) {
      throw new NotFoundException('Tienda no encontrada');
    }

    return result.rows[0];
  }
}

