import {
  ArgumentsHost,
  Catch,
  ExceptionFilter,
  HttpException,
  HttpStatus,
} from '@nestjs/common';
import { randomUUID } from 'node:crypto';
import { Request, Response } from 'express';

export class ApplicationError extends Error {
  constructor(
    readonly code: string,
    message: string,
    readonly status: number,
    readonly details: Record<string, unknown> = {},
  ) {
    super(message);
  }
}

@Catch()
export class ApiExceptionFilter implements ExceptionFilter {
  catch(exception: unknown, host: ArgumentsHost): void {
    const context = host.switchToHttp();
    const request = context.getRequest<Request>();
    const response = context.getResponse<Response>();
    const correlationId =
      String(request.headers['x-correlation-id'] ?? '').trim() || randomUUID();

    if (exception instanceof ApplicationError) {
      response.status(exception.status).json({
        code: exception.code,
        message: exception.message,
        details: exception.details,
        correlationId,
      });
      return;
    }

    if (exception instanceof HttpException) {
      const status = exception.getStatus();
      const payload = exception.getResponse();
      const message =
        typeof payload === 'object' && payload && 'message' in payload
          ? (payload as { message: string | string[] }).message
          : exception.message;
      response.status(status).json({
        code: status === HttpStatus.BAD_REQUEST ? 'VALIDATION_FAILED' : `HTTP_${status}`,
        message: Array.isArray(message) ? message.join('; ') : String(message),
        details: {},
        correlationId,
      });
      return;
    }

    response.status(500).json({
      code: 'INTERNAL_ERROR',
      message: 'The platform could not complete the operation.',
      details: {},
      correlationId,
    });
  }
}
