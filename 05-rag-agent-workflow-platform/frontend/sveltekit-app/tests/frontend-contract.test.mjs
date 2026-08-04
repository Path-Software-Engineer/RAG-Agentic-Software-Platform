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
