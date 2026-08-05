import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';
import { formatLocator, formatScore } from '../src/lib/formatting.ts';

test('formats similarity evidence without reinterpreting the score', () => {
  assert.equal(formatScore(0.89127), '0.891');
  assert.equal(
    formatLocator({ kind: 'character_range', start: 12, end: 44 }),
    'Characters 12-44'
  );
});

test('source cards expose score meaning and a resolvable citation route', async () => {
  const componentUrl = new URL('../src/lib/components/SourceCard.svelte', import.meta.url);
  const source = await readFile(fileURLToPath(componentUrl), 'utf8');

  assert.match(source, /formatScore\(result\.score\)/);
  assert.match(source, /vector similarity/);
  assert.match(source, /href=\{`\/citations\/\$\{result\.citationId\}`\}/);
  assert.match(source, /Resolve citation/);
});

test('evaluation dashboard uses API evidence and exposes auditable metric semantics', async () => {
  const pageUrl = new URL('../src/routes/evaluation/+page.svelte', import.meta.url);
  const apiUrl = new URL('../src/lib/api.ts', import.meta.url);
  const [page, api] = await Promise.all([
    readFile(fileURLToPath(pageUrl), 'utf8'),
    readFile(fileURLToPath(apiUrl), 'utf8')
  ]);

  assert.match(page, /api\.createEvaluationRun/);
  assert.match(page, /api\.labelEvaluationResult/);
  assert.match(page, /Precision@K/);
  assert.match(page, /Recall@K/);
  assert.match(page, /Similarity scores rank chunks; they are not confidence or probability/);
  assert.match(api, /\/api\/v1\/evaluations\/runs/);
  assert.doesNotMatch(page, /mock|fixture|Math\.random/i);
});
