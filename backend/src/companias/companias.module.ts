import { Module } from '@nestjs/common';
import { CompaniasService } from './companias.service';
import { CompaniasController } from './companias.controller';

@Module({
  controllers: [CompaniasController],
  providers: [CompaniasService],
  exports: [CompaniasService],
})
export class CompaniasModule {}

