import {
  Body,
  Controller,
  Get,
  Headers,
  Param,
  ParseUUIDPipe,
  Post,
  UploadedFile,
  UseInterceptors,
} from '@nestjs/common';
import { FileInterceptor } from '@nestjs/platform-express';
import { ApiBody, ApiConsumes, ApiCreatedResponse, ApiOkResponse, ApiTags } from '@nestjs/swagger';
import { CreateDocumentDto, DocumentResource } from './document.dto';
import { DocumentsService } from './documents.service';

@ApiTags('documents')
@Controller('api/v1/documents')
export class DocumentsController {
  constructor(private readonly documents: DocumentsService) {}

  @Post()
  @UseInterceptors(FileInterceptor('file', { limits: { fileSize: 1_048_576, files: 1 } }))
  @ApiConsumes('multipart/form-data')
  @ApiBody({
    schema: {
      type: 'object',
      required: ['title', 'source', 'file'],
      properties: {
        title: { type: 'string', maxLength: 200 },
        source: { type: 'string', maxLength: 500 },
        file: { type: 'string', format: 'binary' },
      },
    },
  })
  @ApiCreatedResponse({ type: DocumentResource })
  create(
    @Body() dto: CreateDocumentDto,
    @UploadedFile() file: Express.Multer.File | undefined,
    @Headers('x-correlation-id') correlationId: string,
  ) {
    return this.documents.create(dto, file, correlationId);
  }

  @Get()
  @ApiOkResponse({ type: [DocumentResource] })
  list(@Headers('x-correlation-id') correlationId: string) {
    return this.documents.list(correlationId);
  }

  @Get(':documentId')
  @ApiOkResponse({ type: DocumentResource })
  detail(
    @Param('documentId', new ParseUUIDPipe()) documentId: string,
    @Headers('x-correlation-id') correlationId: string,
  ) {
    return this.documents.detail(documentId, correlationId);
  }

  @Post(':documentId/index')
  @ApiOkResponse({ type: DocumentResource })
  index(
    @Param('documentId', new ParseUUIDPipe()) documentId: string,
    @Headers('x-correlation-id') correlationId: string,
  ) {
    return this.documents.index(documentId, correlationId);
  }
}
