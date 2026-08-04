import { ApiProperty } from '@nestjs/swagger';
import { IsString, Length } from 'class-validator';

export class CreateDocumentDto {
  @ApiProperty({ example: 'Retrieval safety' })
  @IsString()
  @Length(1, 200)
  title!: string;

  @ApiProperty({ example: 'Controlled demo corpus' })
  @IsString()
  @Length(1, 500)
  source!: string;
}

export class DocumentResource {
  @ApiProperty() documentId!: string;
  @ApiProperty() documentVersionId!: string;
  @ApiProperty() jobId!: string;
  @ApiProperty() title!: string;
  @ApiProperty() source!: string;
  @ApiProperty() filename!: string;
  @ApiProperty({ enum: ['queued', 'running', 'completed', 'failed'] }) status!: string;
  @ApiProperty() chunkCount!: number;
  @ApiProperty({ nullable: true }) embeddingVersionId!: string | null;
  @ApiProperty() createdAt!: string;
  @ApiProperty() correlationId!: string;
  @ApiProperty() deduplicated!: boolean;
}
