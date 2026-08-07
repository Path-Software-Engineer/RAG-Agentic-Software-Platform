<script lang="ts">
  import { RefreshCw, Upload } from '@lucide/svelte';
  import { onMount } from 'svelte';
  import { api, ApiError } from '$lib/api';
  import EmptyState from '$lib/components/EmptyState.svelte';
  import StatusBadge from '$lib/components/StatusBadge.svelte';
  import type { DocumentResource } from '$lib/types';

  let documents: DocumentResource[] = [];
  let loading = true;
  let submitting = false;
  let error = '';
  let title = '';
  let source = 'Controlled demo corpus';
  let selectedFile: File | null = null;
  let fileInput: HTMLInputElement;
  let success = '';

  async function loadDocuments() {
    loading = true;
    error = '';
    try {
      documents = await api.documents();
    } catch (reason) {
      error = reason instanceof ApiError ? reason.message : 'Documents could not be loaded.';
    } finally {
      loading = false;
    }
  }

  async function submit(event: SubmitEvent) {
    event.preventDefault();
    if (!selectedFile || !title.trim()) return;
    submitting = true;
    error = '';
    success = '';
    try {
      const document = await api.uploadDocument(title.trim(), source.trim(), selectedFile);
      success = document.deduplicated
        ? 'These bytes were already indexed; the existing evidence was reused.'
        : `${document.title} was indexed into ${document.chunkCount} traceable chunks.`;
      title = '';
      selectedFile = null;
      fileInput.value = '';
      await loadDocuments();
    } catch (reason) {
      error = reason instanceof ApiError ? reason.message : 'The upload could not be completed.';
    } finally {
      submitting = false;
    }
  }

  onMount(loadDocuments);
</script>

<section class="page-heading">
  <div><p class="eyebrow">DOCUMENT REGISTRY</p><h1>Build the evidence index.</h1><p>Only UTF-8 <code>.txt</code> and <code>.md</code> documents up to 1 MiB are accepted.</p></div>
  <button class="icon-button" on:click={loadDocuments} aria-label="Refresh documents"><RefreshCw size={17} aria-hidden="true" /></button>
</section>

<div class="split-layout">
  <form class="panel upload-panel" on:submit={submit}>
    <div class="section-label"><span>01</span><div><strong>Register a document</strong><small>Metadata and bytes are validated before persistence.</small></div></div>
    <label>Title<input bind:value={title} minlength="1" maxlength="200" required placeholder="Retrieval safety notes" /></label>
    <label>Source<input bind:value={source} minlength="1" maxlength="500" required /></label>
    <label class="file-drop">
      <Upload size={24} aria-hidden="true" />
      <strong>{selectedFile?.name ?? 'Choose a controlled document'}</strong>
      <span>{selectedFile ? `${selectedFile.size.toLocaleString()} bytes` : '.txt or .md · 1 MiB maximum'}</span>
      <input bind:this={fileInput} on:change={(event) => selectedFile = event.currentTarget.files?.[0] ?? null} type="file" accept=".txt,.md,text/plain,text/markdown" required />
    </label>
    <button class="button primary wide" type="submit" disabled={submitting || !selectedFile || !title.trim()}>{submitting ? 'Indexing evidence…' : 'Upload and index'} <span aria-hidden="true">→</span></button>
    {#if success}<p class="inline-message success" role="status">{success}</p>{/if}
    {#if error}<p class="inline-message error" role="alert">{error}</p>{/if}
  </form>

  <section class="panel registry-panel" aria-busy={loading}>
    <div class="section-label"><span>02</span><div><strong>Indexed documents</strong><small>{documents.length} durable resources in the active workspace.</small></div></div>
    {#if loading}
      <div class="loading-list" aria-label="Loading documents"><i></i><i></i><i></i></div>
    {:else if documents.length === 0}
      <EmptyState title="No documents yet" message="Upload a controlled fixture to create the first searchable evidence." />
    {:else}
      <div class="document-list">
        {#each documents as document}
          <article>
            <div class="file-monogram">{document.filename.split('.').pop()?.toUpperCase()}</div>
            <div><h2>{document.title}</h2><p>{document.filename} · {document.source}</p><small>{document.chunkCount} chunks · {new Date(document.createdAt).toLocaleString()}</small></div>
            <StatusBadge status={document.status} />
          </article>
        {/each}
      </div>
    {/if}
  </section>
</div>
