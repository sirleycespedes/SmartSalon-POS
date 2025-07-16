import { ExtractJwt, Strategy } from 'passport-jwt';
import { PassportStrategy } from '@nestjs/passport';
import { Injectable, UnauthorizedException } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { UsuariosService } from '../../usuarios/usuarios.service';

@Injectable()
export class JwtStrategy extends PassportStrategy(Strategy) {
  constructor(
    private configService: ConfigService,
    private usuariosService: UsuariosService,
  ) {
    super({
      jwtFromRequest: ExtractJwt.fromAuthHeaderAsBearerToken(),
      ignoreExpiration: false,
      secretOrKey: configService.get<string>('JWT_SECRET', 'smartsalon-pos-secret-key'),
    });
  }

  async validate(payload: any) {
    const user = await this.usuariosService.findById(payload.sub);
    
    if (!user || user.estado !== 'activo') {
      throw new UnauthorizedException('Usuario no válido');
    }

    return {
      id: user.id,
      username: user.username,
      email: user.email,
      rol_id: user.rol_id,
      compania_id: user.compania_id,
      persona: user.persona,
      rol: user.rol,
      compania: user.compania
    };
  }
}

