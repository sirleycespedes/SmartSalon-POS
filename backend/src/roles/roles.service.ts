import { Injectable, NotFoundException, ConflictException } from '@nestjs/common';
import { DatabaseService } from '../database/database.service';
import { CreateRoleDto } from './dto/create-role.dto';
import { UpdateRoleDto } from './dto/update-role.dto';
import { Role } from './entities/role.entity';

@Injectable()
export class RolesService {
  constructor(private readonly databaseService: DatabaseService) {}

  async create(createRoleDto: CreateRoleDto): Promise<Role> {
    // Verificar si ya existe un rol con el mismo nombre para la misma compañía
    const existingRole = await this.findByNameAndCompania(
      createRoleDto.nombre,
      createRoleDto.compania_id,
    );
    if (existingRole) {
      throw new ConflictException(
        `Ya existe un rol con el nombre ${createRoleDto.nombre} para la compañía ${createRoleDto.compania_id || 'global'}`,
      );
    }

    const query = `
      INSERT INTO roles (nombre, descripcion, permisos, compania_id, es_sistema)
      VALUES ($1, $2, $3, $4, $5)
      RETURNING *
    `;

    const values = [
      createRoleDto.nombre,
      createRoleDto.descripcion || null,
      JSON.stringify(createRoleDto.permisos || {}),
      createRoleDto.compania_id || null,
      createRoleDto.es_sistema || false,
    ];

    const result = await this.databaseService.query(query, values);
    return result.rows[0];
  }

  async findAll(
    options: {
      page?: number;
      limit?: number;
      search?: string;
      compania_id?: number;
    } = {},
  ): Promise<{ roles: Role[]; total: number; page: number; limit: number }> {
    const { page = 1, limit = 10, search, compania_id } = options;
    const offset = (page - 1) * limit;

    let whereClause = 'WHERE 1=1';
    const queryParams: any[] = [];
    let paramIndex = 1;

    if (search) {
      whereClause += ` AND nombre ILIKE $${paramIndex}`;
      queryParams.push(`%${search}%`);
      paramIndex++;
    }

    if (compania_id) {
      whereClause += ` AND compania_id = $${paramIndex}`;
      queryParams.push(compania_id);
      paramIndex++;
    }

    // Query para contar total
    const countQuery = `SELECT COUNT(*) FROM roles ${whereClause}`;
    const countResult = await this.databaseService.query(countQuery, queryParams);
    const total = parseInt(countResult.rows[0].count);

    // Query para obtener datos paginados
    const dataQuery = `
      SELECT * FROM roles 
      ${whereClause}
      ORDER BY created_at DESC
      LIMIT $${paramIndex} OFFSET $${paramIndex + 1}
    `;

    queryParams.push(limit, offset);
    const dataResult = await this.databaseService.query(dataQuery, queryParams);

    return {
      roles: dataResult.rows,
      total,
      page,
      limit,
    };
  }

  async findOne(id: number): Promise<Role> {
    const query = 'SELECT * FROM roles WHERE id = $1';
    const result = await this.databaseService.query(query, [id]);

    if (result.rows.length === 0) {
      throw new NotFoundException('Rol no encontrado');
    }

    return result.rows[0];
  }

  async findByNameAndCompania(nombre: string, compania_id?: number): Promise<Role | null> {
    let query = 'SELECT * FROM roles WHERE nombre = $1';
    const values: (string | number | null)[] = [nombre];
    
    if (compania_id !== undefined && compania_id !== null) {
      query += ' AND compania_id = $2';
      values.push(compania_id);
    } else {
      query += ' AND compania_id IS NULL';
    }

    const result = await this.databaseService.query(query, values);
    return result.rows[0] || null;
  }

  async update(id: number, updateRoleDto: UpdateRoleDto): Promise<Role> {
    const role = await this.findOne(id);

    // Si se actualiza el nombre o la compañía, verificar unicidad
    if (
      (updateRoleDto.nombre && updateRoleDto.nombre !== role.nombre) ||
      (updateRoleDto.compania_id !== undefined && updateRoleDto.compania_id !== role.compania_id)
    ) {
      const existingRole = await this.findByNameAndCompania(
        updateRoleDto.nombre || role.nombre,
        updateRoleDto.compania_id !== undefined ? updateRoleDto.compania_id : role.compania_id,
      );
      if (existingRole && existingRole.id !== id) {
        throw new ConflictException(
          `Ya existe un rol con el nombre ${updateRoleDto.nombre || role.nombre} para la compañía ${updateRoleDto.compania_id !== undefined ? updateRoleDto.compania_id : role.compania_id}`,
        );
      }
    }

    const updateFields: string[] = [];
    const values: any[] = [];
    let paramIndex = 1;

    Object.keys(updateRoleDto).forEach((key) => {
      if (updateRoleDto[key] !== undefined) {
        if (key === 'permisos') {
          updateFields.push(`${key} = $${paramIndex}`);
          values.push(JSON.stringify(updateRoleDto[key]));
        } else {
          updateFields.push(`${key} = $${paramIndex}`);
          values.push(updateRoleDto[key]);
        }
        paramIndex++;
      }
    });

    if (updateFields.length === 0) {
      return role;
    }

    updateFields.push(`updated_at = CURRENT_TIMESTAMP`);
    values.push(id);

    const query = `
      UPDATE roles 
      SET ${updateFields.join(', ')}
      WHERE id = $${paramIndex}
      RETURNING *
    `;

    const result = await this.databaseService.query(query, values);
    return result.rows[0];
  }

  async remove(id: number): Promise<void> {
    await this.findOne(id); // Verificar que existe

    const query = 'DELETE FROM roles WHERE id = $1';
    await this.databaseService.query(query, [id]);
  }
}

