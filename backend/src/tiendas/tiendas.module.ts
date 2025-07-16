import { Module } from '@nestjs/common';
import { TiendasService } from './tiendas.service';
import { TiendasController } from './tiendas.controller';

@Module({
  controllers: [TiendasController],
  providers: [TiendasService],
  exports: [TiendasService],
})
export class TiendasModule {}

