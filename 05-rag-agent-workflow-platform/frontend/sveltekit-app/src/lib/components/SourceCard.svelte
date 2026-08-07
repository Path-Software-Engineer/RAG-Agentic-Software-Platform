<script lang="ts">
  import { ArrowUpRight, FileText, MapPin } from '@lucide/svelte';
  import { formatLocator, formatScore } from '../api';
  import type { SearchResultResource } from '../types';

  export let result: SearchResultResource;
</script>

<article class="source-card">
  <header>
    <span class="rank" aria-label={`Result rank ${result.rank}`}>{String(result.rank).padStart(2, '0')}</span>
    <div>
      <p class="eyebrow"><FileText size={14} aria-hidden="true" /> Source evidence</p>
      <h2>{result.title}</h2>
      <p class="source">{result.source}</p>
    </div>
    <div class="score" aria-label={`Similarity score ${formatScore(result.score)}`}>
      <span>vector similarity</span>
      <strong>{formatScore(result.score)}</strong>
    </div>
  </header>
  <blockquote>{result.snippet}</blockquote>
  <footer>
    <span><MapPin size={14} aria-hidden="true" /> {formatLocator(result.locator)}</span>
    <a href={`/citations/${result.citationId}`}>
      Resolve citation <ArrowUpRight size={15} aria-hidden="true" />
    </a>
  </footer>
</article>
