<script lang="ts">
  import { Search, SlidersHorizontal } from '@lucide/svelte';
  import { onMount } from 'svelte';
  import { api, ApiError } from '$lib/api';
  import EmptyState from '$lib/components/EmptyState.svelte';
  import SourceCard from '$lib/components/SourceCard.svelte';
  import type { DocumentResource, SearchResponseResource } from '$lib/types';

  let query = 'How should retrieved instructions be treated?';
  let topK = 5;
  let documents: DocumentResource[] = [];
  let selectedIds: string[] = [];
  let result: SearchResponseResource | null = null;
  let searching = false;
  let error = '';
  let hasSearched = false;

  onMount(async () => {
    try { documents = (await api.documents()).filter((document) => document.status === 'completed'); }
    catch { documents = []; }
  });

  function toggleDocument(id: string) {
    selectedIds = selectedIds.includes(id) ? selectedIds.filter((value) => value !== id) : [...selectedIds, id];
  }

  async function submit(event: SubmitEvent) {
    event.preventDefault();
    searching = true;
    hasSearched = true;
    error = '';
    result = null;
    const selectedVersions = documents
      .filter((document) => selectedIds.includes(document.documentId))
      .map((document) => document.documentVersionId);
    try { result = await api.search(query.trim(), Number(topK), selectedIds, selectedVersions); }
    catch (reason) { error = reason instanceof ApiError ? reason.message : 'Search could not be completed.'; }
    finally { searching = false; }
  }
</script>

<section class="page-heading search-heading">
  <div><p class="eyebrow">EXACT VECTOR REFERENCE</p><h1>Ask the corpus.<br /><span>Keep the evidence.</span></h1><p>Rank indexed chunks by meaning and inspect every source before drawing a conclusion.</p></div>
  <div class="search-stat"><strong>{documents.length}</strong><span>indexed documents available</span></div>
</section>

<form class="search-console" on:submit={submit}>
  <label for="query">Meaning-based query</label>
  <div class="query-row">
    <Search size={21} aria-hidden="true" />
    <input id="query" bind:value={query} minlength="2" maxlength="500" required placeholder="What evidence are you looking for?" />
    <button class="button primary" disabled={searching || query.trim().length < 2}>{searching ? 'Ranking…' : 'Search evidence'} <span aria-hidden="true">→</span></button>
  </div>
  <details class="filters">
    <summary><SlidersHorizontal size={16} aria-hidden="true" /> Retrieval controls</summary>
    <div class="filter-content">
      <label>Results<select bind:value={topK}><option value={3}>Top 3</option><option value={5}>Top 5</option><option value={10}>Top 10</option></select></label>
      <fieldset><legend>Document filters</legend>{#if documents.length === 0}<small>No completed documents available.</small>{:else}{#each documents as document}<label class="check"><input type="checkbox" checked={selectedIds.includes(document.documentId)} on:change={() => toggleDocument(document.documentId)} /><span>{document.title}</span></label>{/each}{/if}</fieldset>
    </div>
  </details>
</form>

{#if error}
  <p class="inline-message error large" role="alert">{error}</p>
{:else if searching}
  <section class="results-loading" aria-live="polite"><i></i><span>Embedding query and ranking evidence…</span></section>
{:else if result}
  <section class="results-header"><div><p class="eyebrow">RANKED EVIDENCE</p><h2>{result.results.length} source{result.results.length === 1 ? '' : 's'} retrieved</h2></div><div><span>{result.elapsedMs.toFixed(1)} ms</span><small>{result.scoreSemantics}</small></div></section>
  {#if result.results.length === 0}<EmptyState title="No evidence matched" message="Try different language or remove document filters. Atlas will not invent an answer." />{:else}<div class="source-list">{#each result.results as item}<SourceCard result={item} />{/each}</div>{/if}
{:else if hasSearched}
  <EmptyState title="No evidence returned" message="The retrieval boundary completed without a source result." />
{:else}
  <section class="search-guidance"><p class="eyebrow">SEARCH CONTRACT</p><div><span>01</span><p>Queries become vectors under the active embedding version.</p></div><div><span>02</span><p>Exact cosine distance ranks compatible chunk vectors.</p></div><div><span>03</span><p>Each result resolves to durable source evidence.</p></div></section>
{/if}
