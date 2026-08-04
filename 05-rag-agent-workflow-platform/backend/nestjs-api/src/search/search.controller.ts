import { Body, Controller, Get, Headers, Param, ParseUUIDPipe, Post } from '@nestjs/common';
import { ApiOkResponse, ApiTags } from '@nestjs/swagger';
import { CitationResource, SearchRequestDto, SearchResponseResource } from './search.dto';
import { SearchService } from './search.service';

@ApiTags('search')
@Controller('api/v1')
export class SearchController {
  constructor(private readonly searchService: SearchService) {}

  @Post('search')
  @ApiOkResponse({ type: SearchResponseResource })
  search(
    @Body() dto: SearchRequestDto,
    @Headers('x-correlation-id') correlationId: string,
  ) {
    return this.searchService.search(dto, correlationId);
  }

  @Get('citations/:citationId')
  @ApiOkResponse({ type: CitationResource })
  citation(
    @Param('citationId', new ParseUUIDPipe()) citationId: string,
    @Headers('x-correlation-id') correlationId: string,
  ) {
    return this.searchService.citation(citationId, correlationId);
  }
}
