import { Injectable, NotFoundException, ConflictException } from '@nestjs/common';
import { DatabaseService } from '../database/database.service';
import { CreateCompaniaDto } from './dto/create-compania.dto';
import { UpdateCompaniaDto } from './dto/update-compania.dto';
import { Compania } from './entities/compania.entity';

@Injectable()
export class CompaniasService {
  constructor(private readonly databaseService: DatabaseService) {}

  async create(createCompaniaDto: CreateCompaniaDto): Promise<Compania> {
    // Verificar si ya existe una compañía con el mismo NIT
    const existingCompania = await this.findByNit(createCompaniaDto.nit);
    if (existingCompania) {
      throw new ConflictException('Ya existe una compañía con este NIT');
    }

    const query = `
      INSERT INTO companias (nombre, nit, direccion, telefono, email, pais, configuracion)
      VALUES ($1, $2, $3, $4, $5, $6, $7)
      RETURNING *
    `;

    const values = [
      createCompaniaDto.nombre,
      createCompaniaDto.nit,
      createCompaniaDto.direccion || null,
      createCompaniaDto.telefono,
      createCompaniaDto.email || null,
      createCompaniaDto.pais || 'Colombia',
      JSON.stringify(createCompaniaDto.configuracion || {})
    ];

    const result = await this.databaseService.query(query, values);
    return result.rows[0];
  }

  async findAll(options: {
    page?: number;
    limit?: number;
    search?: string;
    estado?: string;
  } = {}): Promise<{ companias: Compania[]; total: number; page: number; limit: number }> {
    const { page = 1, limit = 10, search, estado } = options;
    const offset = (page - 1) * limit;

    let whereClause = 'WHERE deleted_at IS NULL';
    const queryParams: any[] = [];
    let paramIndex = 1;

    if (search) {
      whereClause += ` AND (nombre ILIKE $${paramIndex} OR nit ILIKE $${paramIndex})`;
      queryParams.push(`%${search}%`);
      paramIndex++;
    }

    if (estado) {
      whereClause += ` AND estado = $${paramIndex}`;
      queryParams.push(estado);
      paramIndex++;
    }

    // Query para contar total
    const countQuery = `SELECT COUNT(*) FROM companias ${whereClause}`;
    const countResult = await this.databaseService.query(countQuery, queryParams);
    const total = parseInt(countResult.rows[0].count);

    // Query para obtener datos paginados
    const dataQuery = `
      SELECT * FROM companias 
      ${whereClause}
      ORDER BY created_at DESC
      LIMIT $${paramIndex} OFFSET $${paramIndex + 1}
    `;
    
    queryParams.push(limit, offset);
    const dataResult = await this.databaseService.query(dataQuery, queryParams);

    return {
      companias: dataResult.rows,
      total,
      page,
      limit
    };
  }

  async findOne(id: number): Promise<Compania> {
    const query = 'SELECT * FROM companias WHERE id = $1 AND deleted_at IS NULL';
    const result = await this.databaseService.query(query, [id]);
    
    if (result.rows.length === 0) {
      throw new NotFoundException('Compañía no encontrada');
    }
    
    return result.rows[0];
  }

  async findByNit(nit: string): Promise<Compania | null> {
    const query = 'SELECT * FROM companias WHERE nit = $1 AND deleted_at IS NULL';
    const result = await this.databaseService.query(query, [nit]);
    return result.rows[0] || null;
  }

  async update(id: number, updateCompaniaDto: UpdateCompaniaDto): Promise<Compania> {
    const compania = await this.findOne(id);

    // Si se está actualizando el NIT, verificar que no exista otro con el mismo
    if (updateCompaniaDto.nit && updateCompaniaDto.nit !== compania.nit) {
      const existingCompania = await this.findByNit(updateCompaniaDto.nit);
      if (existingCompania) {
        throw new ConflictException('Ya existe una compañía con este NIT');
      }
    }

    const updateFields: string[] = [];
    const values: any[] = [];
    let paramIndex = 1;

    Object.keys(updateCompaniaDto).forEach(key => {
      if (updateCompaniaDto[key] !== undefined) {
        if (key === 'configuracion') {
          updateFields.push(`${key} = $${paramIndex}`);
          values.push(JSON.stringify(updateCompaniaDto[key]));
        } else {
          updateFields.push(`${key} = $${paramIndex}`);
          values.push(updateCompaniaDto[key]);
        }
        paramIndex++;
      }
    });

    if (updateFields.length === 0) {
      return compania;
    }

    updateFields.push(`updated_at = CURRENT_TIMESTAMP`);
    values.push(id);

    const query = `
      UPDATE companias 
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
      UPDATE companias 
      SET deleted_at = CURRENT_TIMESTAMP, updated_at = CURRENT_TIMESTAMP
      WHERE id = $1
    `;
    
    await this.databaseService.query(query, [id]);
  }

  async restore(id: number): Promise<Compania> {
    const query = `
      UPDATE companias 
      SET deleted_at = NULL, updated_at = CURRENT_TIMESTAMP
      WHERE id = $1
      RETURNING *
    `;
    
    const result = await this.databaseService.query(query, [id]);
    
    if (result.rows.length === 0) {
      throw new NotFoundException('Compañía no encontrada');
    }
    
    return result.rows[0];
  }
}

