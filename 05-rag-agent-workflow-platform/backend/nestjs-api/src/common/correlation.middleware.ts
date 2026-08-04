import { Injectable, NestMiddleware } from '@nestjs/common';
import { randomUUID } from 'node:crypto';
import { NextFunction, Request, Response } from 'express';

@Injectable()
export class CorrelationMiddleware implements NestMiddleware {
  use(request: Request, response: Response, next: NextFunction): void {
    const incoming = String(request.headers['x-correlation-id'] ?? '').trim();
    const correlationId = /^[0-9a-f-]{36}$/i.test(incoming) ? incoming : randomUUID();
    request.headers['x-correlation-id'] = correlationId;
    response.setHeader('x-correlation-id', correlationId);
    next();
  }
}
