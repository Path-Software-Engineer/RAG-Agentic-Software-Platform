<script lang="ts">
  import { ArrowRight, Braces, FileStack, Fingerprint, SearchCheck } from '@lucide/svelte';
</script>

<section class="hero overview-hero">
  <div>
    <p class="eyebrow">TRACEABLE KNOWLEDGE RETRIEVAL</p>
    <h1>Search meaning.<br /><span>Inspect every source.</span></h1>
    <p class="lede">Atlas turns controlled documents into provenance-preserving chunks, exact vector rankings, and citations you can resolve without trusting generated prose.</p>
    <div class="hero-actions">
      <a class="button primary" href="/documents">Add documents <ArrowRight size={17} aria-hidden="true" /></a>
      <a class="button secondary" href="/search">Open search</a>
    </div>
  </div>
  <div class="signal-visual" aria-label="Document to evidence pipeline">
    <span class="orb orb-one"></span><span class="orb orb-two"></span>
    <div class="signal-core"><SearchCheck size={34} aria-hidden="true" /></div>
    <p>document <b>→</b> chunk <b>→</b> vector <b>→</b> citation</p>
  </div>
</section>

<section class="metric-grid" aria-label="Sprint 1 capabilities">
  <article><FileStack size={21} aria-hidden="true" /><span>01</span><h2>Controlled ingestion</h2><p>UTF-8 text, hash deduplication and durable status.</p></article>
  <article><Braces size={21} aria-hidden="true" /><span>02</span><h2>Exact retrieval</h2><p>Versioned 128-dimensional vectors with cosine ranking.</p></article>
  <article><Fingerprint size={21} aria-hidden="true" /><span>03</span><h2>Resolvable evidence</h2><p>Document, version, chunk and locator on every citation.</p></article>
</section>

<section class="notice-panel">
  <div><span class="status-dot"></span><strong>What this release proves</strong></div>
  <p>The complete product boundary works without an external model provider. It does not claim production semantic quality, answer generation, retrieval evaluation or agent behavior.</p>
</section>
