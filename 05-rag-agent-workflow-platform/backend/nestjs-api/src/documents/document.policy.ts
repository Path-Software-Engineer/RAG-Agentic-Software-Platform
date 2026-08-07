import { createHash } from 'node:crypto';
import { extname, basename } from 'node:path';
import { ApplicationError } from '../common/error.filter';

export interface ValidatedDocument {
  filename: string;
  mediaType: 'text/plain' | 'text/markdown';
  content: string;
  contentSha256: string;
  byteSize: number;
}

export function validateDocument(file: Express.Multer.File | undefined): ValidatedDocument {
  if (!file?.buffer?.length) {
    throw new ApplicationError('DOCUMENT_REQUIRED', 'Choose a non-empty .txt or .md file.', 400);
  }
  const maxBytes = Number(process.env.MAX_DOCUMENT_BYTES ?? 1_048_576);
  if (file.size !== file.buffer.length) {
    throw new ApplicationError('DOCUMENT_SIZE_MISMATCH', 'The upload metadata is inconsistent.', 400);
  }
  if (file.buffer.length > maxBytes) {
    throw new ApplicationError('DOCUMENT_TOO_LARGE', `Document exceeds ${maxBytes} bytes.`, 413);
  }
  const extension = extname(file.originalname).toLowerCase();
  if (!['.txt', '.md'].includes(extension)) {
    throw new ApplicationError('DOCUMENT_FORMAT_UNSUPPORTED', 'Only .txt and .md files are accepted.', 415);
  }
  if (file.buffer.includes(0)) {
    throw new ApplicationError('DOCUMENT_BINARY_REJECTED', 'The document must contain UTF-8 text.', 415);
  }
  const acceptedMimeTypes = new Set(['text/plain', 'text/markdown', 'text/x-markdown']);
  if (file.mimetype && file.mimetype !== 'application/octet-stream' && !acceptedMimeTypes.has(file.mimetype)) {
    throw new ApplicationError(
      'DOCUMENT_MIME_MISMATCH',
      'The declared MIME type is incompatible with controlled text ingestion.',
      415,
    );
  }
  const content = file.buffer.toString('utf8');
  if (content.includes('\uFFFD') || !content.trim()) {
    throw new ApplicationError('DOCUMENT_ENCODING_INVALID', 'The document must contain valid UTF-8 text.', 415);
  }
  const filename = basename(file.originalname)
    .normalize('NFKC')
    .replace(/[^A-Za-z0-9._-]+/g, '-')
    .replace(/^[-.]+|[-.]+$/g, '') || `document${extension}`;
  return {
    filename,
    mediaType: extension === '.md' ? 'text/markdown' : 'text/plain',
    content,
    contentSha256: createHash('sha256').update(Buffer.from(content, 'utf8')).digest('hex'),
    byteSize: Buffer.byteLength(content, 'utf8'),
  };
}
