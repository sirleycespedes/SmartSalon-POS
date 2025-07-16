import { Injectable, NotFoundException, ConflictException } from '@nestjs/common';
import { DatabaseService } from '../database/database.service';
import { CreatePersonaDto } from './dto/create-persona.dto';
import { UpdatePersonaDto } from './dto/update-persona.dto';
import { Persona } from './entities/persona.entity';

@Injectable()
export class PersonasService {
  constructor(private readonly databaseService: DatabaseService) {}

  async create(createPersonaDto: CreatePersonaDto): Promise<Persona> {
    // Verificar unicidad de identificación
    const existingPersona = await this.findByIdentificacion(
      createPersonaDto.tipo_identificacion_id,
      createPersonaDto.numero_identificacion,
    );
    if (existingPersona) {
      throw new ConflictException(
        `Ya existe una persona con el tipo y número de identificación ${createPersonaDto.numero_identificacion}`,
      );
    }

    const query = `
      INSERT INTO personas (
        nombres, apellidos, telefono, email, direccion, fecha_nacimiento, tipo,
        tipo_identificacion_id, numero_identificacion, datos_adicionales, estado
      )
      VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
      RETURNING *
    `;

    const values = [
      createPersonaDto.nombres,
      createPersonaDto.apellidos,
      createPersonaDto.telefono || null,
      createPersonaDto.email || null,
      createPersonaDto.direccion || null,
      createPersonaDto.fecha_nacimiento || null,
      createPersonaDto.tipo,
      createPersonaDto.tipo_identificacion_id || null,
      createPersonaDto.numero_identificacion,
      JSON.stringify(createPersonaDto.datos_adicionales || {}),
      createPersonaDto.estado || 'activo',
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
      tipo?: string;
      tipo_identificacion_id?: number;
    } = {},
  ): Promise<{ personas: Persona[]; total: number; page: number; limit: number }> {
    const { page = 1, limit = 10, search, estado, tipo, tipo_identificacion_id } = options;
    const offset = (page - 1) * limit;

    let whereClause = 'WHERE p.deleted_at IS NULL';
    const queryParams: any[] = [];
    let paramIndex = 1;

    if (search) {
      whereClause += ` AND (p.nombres ILIKE $${paramIndex} OR p.apellidos ILIKE $${paramIndex} OR p.numero_identificacion ILIKE $${paramIndex})`;
      queryParams.push(`%${search}%`);
      paramIndex++;
    }

    if (estado) {
      whereClause += ` AND p.estado = $${paramIndex}`;
      queryParams.push(estado);
      paramIndex++;
    }

    if (tipo) {
      whereClause += ` AND p.tipo = $${paramIndex}`;
      queryParams.push(tipo);
      paramIndex++;
    }

    if (tipo_identificacion_id) {
      whereClause += ` AND p.tipo_identificacion_id = $${paramIndex}`;
      queryParams.push(tipo_identificacion_id);
      paramIndex++;
    }

    // Query para contar total
    const countQuery = `SELECT COUNT(*) FROM personas p ${whereClause}`;
    const countResult = await this.databaseService.query(countQuery, queryParams);
    const total = parseInt(countResult.rows[0].count);

    // Query para obtener datos paginados
    const dataQuery = `
      SELECT 
        p.*,
        ti.nombre as tipo_identificacion_nombre
      FROM personas p
      LEFT JOIN tipos_identificacion ti ON p.tipo_identificacion_id = ti.id
      ${whereClause}
      ORDER BY p.created_at DESC
      LIMIT $${paramIndex} OFFSET $${paramIndex + 1}
    `;

    queryParams.push(limit, offset);
    const dataResult = await this.databaseService.query(dataQuery, queryParams);

    return {
      personas: dataResult.rows,
      total,
      page,
      limit,
    };
  }

  async findOne(id: number): Promise<Persona> {
    const query = `
      SELECT 
        p.*,
        ti.nombre as tipo_identificacion_nombre
      FROM personas p
      LEFT JOIN tipos_identificacion ti ON p.tipo_identificacion_id = ti.id
      WHERE p.id = $1 AND p.deleted_at IS NULL
    `;
    const result = await this.databaseService.query(query, [id]);

    if (result.rows.length === 0) {
      throw new NotFoundException('Persona no encontrada');
    }

    return result.rows[0];
  }

  async findByIdentificacion(tipo_identificacion_id: number, numero_identificacion: string): Promise<Persona | null> {
    const query = 'SELECT * FROM personas WHERE tipo_identificacion_id = $1 AND numero_identificacion = $2 AND deleted_at IS NULL';
    const result = await this.databaseService.query(query, [tipo_identificacion_id, numero_identificacion]);
    return result.rows[0] || null;
  }

  async update(id: number, updatePersonaDto: UpdatePersonaDto): Promise<Persona> {
    const persona = await this.findOne(id);

    // Si se actualiza la identificación, verificar unicidad
    if (
      (updatePersonaDto.tipo_identificacion_id && updatePersonaDto.tipo_identificacion_id !== persona.tipo_identificacion_id) ||
      (updatePersonaDto.numero_identificacion && updatePersonaDto.numero_identificacion !== persona.numero_identificacion)
    ) {
      const existingPersona = await this.findByIdentificacion(
        updatePersonaDto.tipo_identificacion_id || persona.tipo_identificacion_id,
        updatePersonaDto.numero_identificacion || persona.numero_identificacion,
      );
      if (existingPersona && existingPersona.id !== id) {
        throw new ConflictException(
          `Ya existe una persona con el tipo y número de identificación ${updatePersonaDto.numero_identificacion || persona.numero_identificacion}`,
        );
      }
    }

    const updateFields: string[] = [];
    const values: any[] = [];
    let paramIndex = 1;

    Object.keys(updatePersonaDto).forEach((key) => {
      if (updatePersonaDto[key] !== undefined) {
        if (key === 'datos_adicionales') {
          updateFields.push(`${key} = $${paramIndex}`);
          values.push(JSON.stringify(updatePersonaDto[key]));
        } else {
          updateFields.push(`${key} = $${paramIndex}`);
          values.push(updatePersonaDto[key]);
        }
        paramIndex++;
      }
    });

    if (updateFields.length === 0) {
      return persona;
    }

    updateFields.push(`updated_at = CURRENT_TIMESTAMP`);
    values.push(id);

    const query = `
      UPDATE personas 
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
      UPDATE personas 
      SET deleted_at = CURRENT_TIMESTAMP, updated_at = CURRENT_TIMESTAMP
      WHERE id = $1
    `;

    await this.databaseService.query(query, [id]);
  }

  async restore(id: number): Promise<Persona> {
    const query = `
      UPDATE personas 
      SET deleted_at = NULL, updated_at = CURRENT_TIMESTAMP
      WHERE id = $1
      RETURNING *
    `;

    const result = await this.databaseService.query(query, [id]);

    if (result.rows.length === 0) {
      throw new NotFoundException('Persona no encontrada');
    }

    return result.rows[0];
  }
}

