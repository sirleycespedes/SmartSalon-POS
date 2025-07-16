import { Injectable, NotFoundException, ConflictException } from '@nestjs/common';
import { DatabaseService } from '../database/database.service';
import { CreateUsuarioDto } from './dto/create-usuario.dto';
import { UpdateUsuarioDto } from './dto/update-usuario.dto';
import { Usuario } from './entities/usuario.entity';
import * as bcrypt from 'bcryptjs';

@Injectable()
export class UsuariosService {
  constructor(private readonly databaseService: DatabaseService) {}

  async create(createUsuarioDto: CreateUsuarioDto): Promise<Usuario> {
    // Verificar si ya existe un usuario con el mismo username o email
    const existingUser = await this.findByUsernameOrEmail(createUsuarioDto.username);
    if (existingUser) {
      throw new ConflictException('Ya existe un usuario con este username o email');
    }

    const salt = await bcrypt.genSalt(10);
    const password_hash = await bcrypt.hash(createUsuarioDto.password, salt);

    const query = `
      INSERT INTO usuarios (
        persona_id, username, email, password_hash, salt, rol_id, compania_id,
        configuracion_usuario, estado
      )
      VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
      RETURNING *
    `;

    const values = [
      createUsuarioDto.persona_id,
      createUsuarioDto.username,
      createUsuarioDto.email,
      password_hash,
      salt,
      createUsuarioDto.rol_id || null,
      createUsuarioDto.compania_id || null,
      JSON.stringify(createUsuarioDto.configuracion_usuario || {}),
      createUsuarioDto.estado || 'activo',
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
      rol_id?: number;
      compania_id?: number;
    } = {},
  ): Promise<{ usuarios: Usuario[]; total: number; page: number; limit: number }> {
    const { page = 1, limit = 10, search, estado, rol_id, compania_id } = options;
    const offset = (page - 1) * limit;

    let whereClause = 'WHERE u.deleted_at IS NULL';
    const queryParams: any[] = [];
    let paramIndex = 1;

    if (search) {
      whereClause += ` AND (u.username ILIKE $${paramIndex} OR u.email ILIKE $${paramIndex})`;
      queryParams.push(`%${search}%`);
      paramIndex++;
    }

    if (estado) {
      whereClause += ` AND u.estado = $${paramIndex}`;
      queryParams.push(estado);
      paramIndex++;
    }

    if (rol_id) {
      whereClause += ` AND u.rol_id = $${paramIndex}`;
      queryParams.push(rol_id);
      paramIndex++;
    }

    if (compania_id) {
      whereClause += ` AND u.compania_id = $${paramIndex}`;
      queryParams.push(compania_id);
      paramIndex++;
    }

    // Query para contar total
    const countQuery = `SELECT COUNT(*) FROM usuarios u ${whereClause}`;
    const countResult = await this.databaseService.query(countQuery, queryParams);
    const total = parseInt(countResult.rows[0].count);

    // Query para obtener datos paginados
    const dataQuery = `
      SELECT 
        u.*,
        p.nombres, p.apellidos, p.nombre_completo, p.telefono, p.email as persona_email,
        r.nombre as rol_nombre,
        c.nombre as compania_nombre
      FROM usuarios u
      JOIN personas p ON u.persona_id = p.id
      LEFT JOIN roles r ON u.rol_id = r.id
      LEFT JOIN companias c ON u.compania_id = c.id
      ${whereClause}
      ORDER BY u.created_at DESC
      LIMIT $${paramIndex} OFFSET $${paramIndex + 1}
    `;

    queryParams.push(limit, offset);
    const dataResult = await this.databaseService.query(dataQuery, queryParams);

    return {
      usuarios: dataResult.rows,
      total,
      page,
      limit,
    };
  }

  async findOne(id: number): Promise<Usuario> {
    const query = `
      SELECT 
        u.*,
        p.nombres, p.apellidos, p.nombre_completo, p.telefono, p.email as persona_email,
        r.nombre as rol_nombre,
        c.nombre as compania_nombre
      FROM usuarios u
      JOIN personas p ON u.persona_id = p.id
      LEFT JOIN roles r ON u.rol_id = r.id
      LEFT JOIN companias c ON u.compania_id = c.id
      WHERE u.id = $1 AND u.deleted_at IS NULL
    `;
    const result = await this.databaseService.query(query, [id]);

    if (result.rows.length === 0) {
      throw new NotFoundException('Usuario no encontrado');
    }

    return result.rows[0];
  }

  async findByUsernameOrEmail(identifier: string): Promise<Usuario | null> {
    const query = `
      SELECT 
        u.*,
        p.nombres, p.apellidos, p.nombre_completo, p.telefono, p.email as persona_email,
        r.nombre as rol_nombre,
        c.nombre as compania_nombre
      FROM usuarios u
      JOIN personas p ON u.persona_id = p.id
      LEFT JOIN roles r ON u.rol_id = r.id
      LEFT JOIN companias c ON u.compania_id = c.id
      WHERE (u.username = $1 OR u.email = $1) AND u.deleted_at IS NULL
    `;
    const result = await this.databaseService.query(query, [identifier]);
    return result.rows[0] || null;
  }

  async findById(id: number): Promise<Usuario | null> {
    const query = `
      SELECT 
        u.*,
        p.nombres, p.apellidos, p.nombre_completo, p.telefono, p.email as persona_email,
        r.nombre as rol_nombre,
        c.nombre as compania_nombre
      FROM usuarios u
      JOIN personas p ON u.persona_id = p.id
      LEFT JOIN roles r ON u.rol_id = r.id
      LEFT JOIN companias c ON u.compania_id = c.id
      WHERE u.id = $1 AND u.deleted_at IS NULL
    `;
    const result = await this.databaseService.query(query, [id]);
    return result.rows[0] || null;
  }

  async update(id: number, updateUsuarioDto: UpdateUsuarioDto): Promise<Usuario> {
    const usuario = await this.findOne(id);

    // Si se actualiza username o email, verificar unicidad
    if (updateUsuarioDto.username && updateUsuarioDto.username !== usuario.username) {
      const existingUser = await this.findByUsernameOrEmail(updateUsuarioDto.username);
      if (existingUser && existingUser.id !== id) {
        throw new ConflictException('Ya existe un usuario con este username');
      }
    }
    if (updateUsuarioDto.email && updateUsuarioDto.email !== usuario.email) {
      const existingUser = await this.findByUsernameOrEmail(updateUsuarioDto.email);
      if (existingUser && existingUser.id !== id) {
        throw new ConflictException('Ya existe un usuario con este email');
      }
    }

    const updateFields: string[] = [];
    const values: any[] = [];
    let paramIndex = 1;

    if (updateUsuarioDto.password) {
      const salt = await bcrypt.genSalt(10);
      const password_hash = await bcrypt.hash(updateUsuarioDto.password, salt);
      updateFields.push(`password_hash = $${paramIndex}`);
      values.push(password_hash);
      paramIndex++;
      updateFields.push(`salt = $${paramIndex}`);
      values.push(salt);
      paramIndex++;
    }

    Object.keys(updateUsuarioDto).forEach((key) => {
      if (updateUsuarioDto[key] !== undefined && key !== 'password') {
        if (key === 'configuracion_usuario') {
          updateFields.push(`${key} = $${paramIndex}`);
          values.push(JSON.stringify(updateUsuarioDto[key]));
        } else {
          updateFields.push(`${key} = $${paramIndex}`);
          values.push(updateUsuarioDto[key]);
        }
        paramIndex++;
      }
    });

    if (updateFields.length === 0) {
      return usuario;
    }

    updateFields.push(`updated_at = CURRENT_TIMESTAMP`);
    values.push(id);

    const query = `
      UPDATE usuarios 
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
      UPDATE usuarios 
      SET deleted_at = CURRENT_TIMESTAMP, updated_at = CURRENT_TIMESTAMP
      WHERE id = $1
    `;

    await this.databaseService.query(query, [id]);
  }

  async restore(id: number): Promise<Usuario> {
    const query = `
      UPDATE usuarios 
      SET deleted_at = NULL, updated_at = CURRENT_TIMESTAMP
      WHERE id = $1
      RETURNING *
    `;

    const result = await this.databaseService.query(query, [id]);

    if (result.rows.length === 0) {
      throw new NotFoundException('Usuario no encontrado');
    }

    return result.rows[0];
  }

  async incrementFailedAttempts(userId: number): Promise<void> {
    const query = `
      UPDATE usuarios
      SET intentos_fallidos = intentos_fallidos + 1,
          bloqueado_hasta = CASE
              WHEN intentos_fallidos + 1 >= 5 THEN NOW() + INTERVAL '15 minutes'
              ELSE bloqueado_hasta
          END
      WHERE id = $1
    `;
    await this.databaseService.query(query, [userId]);
  }

  async resetFailedAttempts(userId: number): Promise<void> {
    const query = `
      UPDATE usuarios
      SET intentos_fallidos = 0,
          bloqueado_hasta = NULL
      WHERE id = $1
    `;
    await this.databaseService.query(query, [userId]);
  }

  async updateLastAccess(userId: number): Promise<void> {
    const query = `
      UPDATE usuarios
      SET ultimo_acceso = CURRENT_TIMESTAMP
      WHERE id = $1
    `;
    await this.databaseService.query(query, [userId]);
  }
}

