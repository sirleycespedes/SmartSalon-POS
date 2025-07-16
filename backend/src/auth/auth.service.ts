import { Injectable, UnauthorizedException } from '@nestjs/common';
import { JwtService } from '@nestjs/jwt';
import * as bcrypt from 'bcryptjs';
import { UsuariosService } from '../usuarios/usuarios.service';

@Injectable()
export class AuthService {
  constructor(
    private usuariosService: UsuariosService,
    private jwtService: JwtService,
  ) {}

  async validateUser(username: string, password: string): Promise<any> {
    const user = await this.usuariosService.findByUsernameOrEmail(username);
    
    if (!user) {
      throw new UnauthorizedException('Credenciales inválidas');
    }

    if (user.estado !== 'activo') {
      throw new UnauthorizedException('Usuario inactivo');
    }

    const isPasswordValid = await bcrypt.compare(password, user.password_hash);
    
    if (!isPasswordValid) {
      // Incrementar intentos fallidos
      await this.usuariosService.incrementFailedAttempts(user.id);
      throw new UnauthorizedException('Credenciales inválidas');
    }

    // Resetear intentos fallidos en login exitoso
    await this.usuariosService.resetFailedAttempts(user.id);
    await this.usuariosService.updateLastAccess(user.id);

    const { password_hash, salt, ...result } = user;
    return result;
  }

  async login(user: any) {
    const payload = { 
      username: user.username, 
      sub: user.id,
      email: user.email,
      rol_id: user.rol_id,
      compania_id: user.compania_id
    };

    return {
      access_token: this.jwtService.sign(payload),
      usuario: {
        id: user.id,
        username: user.username,
        email: user.email,
        persona: user.persona,
        rol: user.rol,
        compania: user.compania
      }
    };
  }

  async refreshToken(refreshToken: string) {
    try {
      const payload = this.jwtService.verify(refreshToken);
      const user = await this.usuariosService.findById(payload.sub);
      
      if (!user || user.estado !== 'activo') {
        throw new UnauthorizedException('Token inválido');
      }

      return this.login(user);
    } catch (error) {
      throw new UnauthorizedException('Token inválido');
    }
  }
}

