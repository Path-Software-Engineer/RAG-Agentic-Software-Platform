<script lang="ts">
  import { ArrowLeft, Fingerprint, MapPin, Quote } from '@lucide/svelte';
  import { page } from '$app/stores';
  import { api, ApiError, formatLocator, formatScore } from '$lib/api';
  import type { CitationResource } from '$lib/types';

  let citationPromise: Promise<CitationResource>;
  $: citationPromise = api.citation($page.params.citationId ?? '');
</script>

<a class="back-link" href="/search"><ArrowLeft size={16} aria-hidden="true" /> Back to results</a>
{#await citationPromise}
  <section class="citation-loading" aria-live="polite"><i></i><span>Resolving durable citation…</span></section>
{:then citation}
  <section class="page-heading citation-heading"><div><p class="eyebrow">RESOLVED SOURCE EVIDENCE</p><h1>{citation.title}</h1><p>{citation.source}</p></div><div class="score large"><span>similarity</span><strong>{formatScore(citation.score)}</strong></div></section>
  <article class="citation-document">
    <div class="citation-rail"><Quote size={23} aria-hidden="true" /><span>Verified fragment</span></div>
    <div class="citation-content"><blockquote>{citation.content}</blockquote><p><MapPin size={15} aria-hidden="true" /> {formatLocator(citation.locator)}</p></div>
  </article>
  <section class="identifier-grid" aria-label="Citation identifiers">
    <div><Fingerprint size={17} aria-hidden="true" /><span>Citation ID</span><code>{citation.citationId}</code></div>
    <div><span>Document ID</span><code>{citation.documentId}</code></div>
    <div><span>Version ID</span><code>{citation.documentVersionId}</code></div>
    <div><span>Chunk ID</span><code>{citation.chunkId}</code></div>
  </section>
  <section class="notice-panel"><div><span class="status-dot"></span><strong>Evidence resolved</strong></div><p>This view proves provenance within the controlled platform. It does not verify that the external source is true or that similarity implies correctness.</p></section>
{:catch reason}
  <section class="empty-state error-state" role="alert"><div><h2>Citation unavailable</h2><p>{reason instanceof ApiError ? reason.message : 'The evidence could not be resolved.'}</p><a class="button secondary" href="/search">Return to search</a></div></section>
{/await}
