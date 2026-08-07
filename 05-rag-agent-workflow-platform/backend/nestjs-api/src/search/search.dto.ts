import { ApiProperty } from '@nestjs/swagger';
import { ArrayMaxSize, IsArray, IsInt, IsOptional, IsString, IsUUID, Length, Max, Min } from 'class-validator';

export class SearchRequestDto {
  @ApiProperty({ example: 'How should retrieved instructions be treated?' })
  @IsString()
  @Length(2, 500)
  query!: string;

  @ApiProperty({ default: 5, minimum: 1, maximum: 10 })
  @IsInt()
  @Min(1)
  @Max(10)
  topK = 5;

  @ApiProperty({ type: [String], required: false })
  @IsOptional()
  @IsArray()
  @ArrayMaxSize(50)
  @IsUUID('4', { each: true })
  documentIds: string[] = [];

  @ApiProperty({ type: [String], required: false })
  @IsOptional()
  @IsArray()
  @ArrayMaxSize(50)
  @IsUUID('4', { each: true })
  documentVersionIds: string[] = [];
}

export class SearchResultResource {
  @ApiProperty() rank!: number;
  @ApiProperty() score!: number;
  @ApiProperty() documentId!: string;
  @ApiProperty() documentVersionId!: string;
  @ApiProperty() chunkId!: string;
  @ApiProperty() citationId!: string;
  @ApiProperty() title!: string;
  @ApiProperty() source!: string;
  @ApiProperty() snippet!: string;
  @ApiProperty() locator!: Record<string, unknown>;
}

export class SearchResponseResource {
  @ApiProperty() query!: string;
  @ApiProperty() topK!: number;
  @ApiProperty() embeddingVersionId!: string;
  @ApiProperty() scoreSemantics!: string;
  @ApiProperty() elapsedMs!: number;
  @ApiProperty() correlationId!: string;
  @ApiProperty({ type: [SearchResultResource] }) results!: SearchResultResource[];
}

export class CitationResource {
  @ApiProperty() citationId!: string;
  @ApiProperty() documentId!: string;
  @ApiProperty() documentVersionId!: string;
  @ApiProperty() chunkId!: string;
  @ApiProperty() title!: string;
  @ApiProperty() source!: string;
  @ApiProperty() score!: number;
  @ApiProperty() snippet!: string;
  @ApiProperty() content!: string;
  @ApiProperty() locator!: Record<string, unknown>;
  @ApiProperty() correlationId!: string;
}
