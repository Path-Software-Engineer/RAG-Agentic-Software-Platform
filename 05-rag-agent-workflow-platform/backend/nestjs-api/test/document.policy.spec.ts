import { validate } from 'class-validator';
import { plainToInstance } from 'class-transformer';
import { ApplicationError } from '../src/common/error.filter';
import { validateDocument } from '../src/documents/document.policy';
import { SearchRequestDto } from '../src/search/search.dto';

function file(name: string, content: Buffer): Express.Multer.File {
  return {
    fieldname: 'file',
    originalname: name,
    encoding: '7bit',
    mimetype: 'text/plain',
    size: content.length,
    buffer: content,
    destination: '',
    filename: '',
    path: '',
    stream: undefined as never,
  };
}

describe('Sprint 1 validation contracts', () => {
  it('accepts and fingerprints controlled markdown', () => {
    const result = validateDocument(file('../Safety notes.md', Buffer.from('# Safe\nEvidence')));
    expect(result.filename).toBe('Safety-notes.md');
    expect(result.mediaType).toBe('text/markdown');
    expect(result.contentSha256).toHaveLength(64);
  });

  it('rejects unsupported files before persistence', () => {
    expect(() => validateDocument(file('payload.exe', Buffer.from('not binary')))).toThrow(
      ApplicationError,
    );
  });

  it('rejects a mismatched declared MIME type', () => {
    const upload = file('notes.md', Buffer.from('# Safe'));
    upload.mimetype = 'image/png';
    expect(() => validateDocument(upload)).toThrow(ApplicationError);
  });

  it('rejects invalid search bounds through DTO validation', async () => {
    const dto = plainToInstance(SearchRequestDto, { query: 'a', topK: 40, unknown: true });
    const errors = await validate(dto);
    expect(errors.map((error) => error.property)).toEqual(expect.arrayContaining(['query', 'topK']));
  });
});
