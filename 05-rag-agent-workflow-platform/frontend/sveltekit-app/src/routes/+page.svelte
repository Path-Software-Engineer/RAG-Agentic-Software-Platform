<script lang="ts">
  import { ArrowRight, BarChart3, FileStack, Fingerprint, SearchCheck } from '@lucide/svelte';
</script>

<section class="hero overview-hero">
  <div>
    <p class="eyebrow">TRACEABLE KNOWLEDGE RETRIEVAL</p>
    <h1>Search meaning.<br /><span>Inspect every source.</span></h1>
    <p class="lede">Atlas turns controlled documents into provenance-preserving search evidence, then compares versioned retrieval strategies against explicit relevance judgments.</p>
    <div class="hero-actions">
      <a class="button primary" href="/documents">Add documents <ArrowRight size={17} aria-hidden="true" /></a>
      <a class="button secondary" href="/search">Open search</a>
      <a class="button secondary" href="/evaluation">Evaluate retrieval</a>
    </div>
  </div>
  <div class="signal-visual" aria-label="Document to evidence pipeline">
    <span class="orb orb-one"></span><span class="orb orb-two"></span>
    <div class="signal-core"><SearchCheck size={34} aria-hidden="true" /></div>
    <p>document <b>→</b> chunk <b>→</b> vector <b>→</b> citation</p>
  </div>
</section>

<section class="metric-grid" aria-label="Current platform capabilities">
  <article><FileStack size={21} aria-hidden="true" /><span>01</span><h2>Controlled ingestion</h2><p>UTF-8 text, hash deduplication and durable status.</p></article>
  <article><Fingerprint size={21} aria-hidden="true" /><span>02</span><h2>Resolvable evidence</h2><p>Versioned vectors plus document, chunk and locator on every citation.</p></article>
  <article><BarChart3 size={21} aria-hidden="true" /><span>03</span><h2>Retrieval evaluation</h2><p>Comparable strategies, explicit judgments, metrics and visible errors.</p></article>
</section>

<section class="notice-panel">
  <div><span class="status-dot"></span><strong>What this release proves</strong></div>
  <p>Semantic search and retrieval evaluation work without an external model provider. The release does not claim production semantic quality, answer generation or agent behavior.</p>
</section>
