<script lang="ts">
  import { BarChart3, Beaker, Check, CircleAlert, Database, Play, Tag } from '@lucide/svelte';
  import { onMount } from 'svelte';
  import { api, ApiError, formatScore } from '$lib/api';
  import EmptyState from '$lib/components/EmptyState.svelte';
  import type {
    DocumentResource,
    EvaluationHitResource,
    EvaluationRunResource,
    EvaluationRunSummaryResource,
    EvaluationStrategyResource,
    EvaluationTestCaseResource
  } from '$lib/types';

  let documents: DocumentResource[] = [];
  let strategies: EvaluationStrategyResource[] = [];
  let testCases: EvaluationTestCaseResource[] = [];
  let runSummaries: EvaluationRunSummaryResource[] = [];
  let selectedStrategyIds: string[] = [];
  let selectedTestCaseIds: string[] = [];
  let selectedDocumentVersionIds: string[] = [];
  let relevantDocumentIds: string[] = [];
  let query = '';
  let rationale = '';
  let topK = 3;
  let activeRun: EvaluationRunResource | null = null;
  let loading = true;
  let running = false;
  let creatingCase = false;
  let labellingResultId = '';
  let error = '';
  let notice = '';

  $: bestStrategy = activeRun
    ? [...activeRun.strategies].sort(
        (left, right) =>
          right.metrics.recallAtK - left.metrics.recallAtK ||
          right.metrics.precisionAtK - left.metrics.precisionAtK ||
          right.metrics.meanReciprocalRank - left.metrics.meanReciprocalRank
      )[0]
    : null;
  $: selectedCases = testCases.filter((item) => selectedTestCaseIds.includes(item.testCaseId));
  $: errorQueries = activeRun
    ? activeRun.strategies.flatMap((strategy) =>
        strategy.queries
          .filter((item) => item.recallAtK < 1)
          .map((item) => ({ strategy: strategy.metrics.strategyLabel, ...item }))
      )
    : [];

  onMount(loadWorkspace);

  async function loadWorkspace() {
    loading = true;
    error = '';
    try {
      [documents, strategies, testCases, runSummaries] = await Promise.all([
        api.documents(),
        api.evaluationStrategies(),
        api.evaluationTestCases(),
        api.evaluationRuns()
      ]);
      documents = documents.filter((document) => document.status === 'completed');
      selectedStrategyIds = strategies.map((strategy) => strategy.strategyId);
      selectedTestCaseIds = testCases.map((item) => item.testCaseId);
      selectedDocumentVersionIds = documents.map((document) => document.documentVersionId);
      if (runSummaries.length > 0) await openRun(runSummaries[0].runId);
    } catch (reason) {
      error = messageFor(reason, 'The evaluation workspace could not be loaded.');
    } finally {
      loading = false;
    }
  }

  function messageFor(reason: unknown, fallback: string) {
    return reason instanceof ApiError ? `${reason.message} (${reason.correlationId})` : fallback;
  }

  function toggle(value: string, values: string[]) {
    return values.includes(value) ? values.filter((item) => item !== value) : [...values, value];
  }

  async function createTestCase(event: SubmitEvent) {
    event.preventDefault();
    creatingCase = true;
    error = '';
    notice = '';
    try {
      const created = await api.createEvaluationTestCase(
        query.trim(),
        relevantDocumentIds,
        rationale.trim()
      );
      testCases = [created, ...testCases];
      selectedTestCaseIds = [created.testCaseId, ...selectedTestCaseIds];
      query = '';
      rationale = '';
      relevantDocumentIds = [];
      notice = 'The test case is now part of the reproducible evaluation set.';
    } catch (reason) {
      error = messageFor(reason, 'The test case could not be created.');
    } finally {
      creatingCase = false;
    }
  }

  async function runEvaluation() {
    running = true;
    error = '';
    notice = '';
    try {
      activeRun = await api.createEvaluationRun(
        selectedStrategyIds,
        selectedTestCaseIds,
        selectedDocumentVersionIds,
        Number(topK)
      );
      runSummaries = await api.evaluationRuns();
      notice = 'The immutable evaluation snapshot completed successfully.';
    } catch (reason) {
      error = messageFor(reason, 'The evaluation run could not be completed.');
    } finally {
      running = false;
    }
  }

  async function openRun(runId: string) {
    error = '';
    try {
      activeRun = await api.evaluationRun(runId);
    } catch (reason) {
      error = messageFor(reason, 'The selected run could not be loaded.');
    }
  }

  async function labelResult(hit: EvaluationHitResource, relevant: boolean) {
    if (!activeRun) return;
    labellingResultId = hit.resultId;
    error = '';
    try {
      activeRun = await api.labelEvaluationResult(
        activeRun.runId,
        hit.resultId,
        relevant,
        'Reviewed in the Sprint 2 evidence dashboard.'
      );
      runSummaries = await api.evaluationRuns();
      notice = `The result was labelled ${relevant ? 'relevant' : 'not relevant'} and metrics were recalculated.`;
    } catch (reason) {
      error = messageFor(reason, 'The relevance label could not be saved.');
    } finally {
      labellingResultId = '';
    }
  }

  function percentage(value: number) {
    return `${(value * 100).toFixed(1)}%`;
  }
</script>

<svelte:head>
  <meta
    name="description"
    content="Compare versioned retrieval strategies with explicit relevance judgments and reproducible metrics."
  />
</svelte:head>

<section class="evaluation-intro">
  <div>
    <p class="eyebrow">REPRODUCIBLE RETRIEVAL EVIDENCE</p>
    <h1>Compare the pipeline.<br /><span>Inspect every miss.</span></h1>
    <p class="lede">
      Define document-level ground truth, run the same queries against versioned chunking
      strategies, and review the evidence behind every metric.
    </p>
  </div>
  <div class="run-identity">
    <span>Active evidence snapshot</span>
    <strong>{activeRun ? activeRun.runId.slice(0, 13) : 'No run selected'}</strong>
    <small>{activeRun ? `${activeRun.strategies.length} strategies · top ${activeRun.topK}` : 'Create a test case, then run the lab.'}</small>
  </div>
</section>

{#if error}<p class="inline-message error large" role="alert">{error}</p>{/if}
{#if notice}<p class="inline-message success large" aria-live="polite">{notice}</p>{/if}

{#if loading}
  <section class="results-loading" aria-live="polite"><i></i><span>Loading evaluation evidence…</span></section>
{:else}
  <section class="evaluation-workflow">
    <div class="setup-stack">
      <article class="panel">
        <div class="section-label"><span>01</span><div><strong>Ground-truth test set</strong><small>Queries must point to at least one relevant document.</small></div></div>
        <form on:submit={createTestCase}>
          <label for="case-query">Evaluation query<input id="case-query" bind:value={query} minlength="2" maxlength="500" required placeholder="What must a retrieved instruction preserve?" /></label>
          <label for="case-rationale">Why this evidence is relevant<textarea id="case-rationale" bind:value={rationale} minlength="5" maxlength="500" required placeholder="Explain the expected evidence boundary."></textarea></label>
          <fieldset class="selection-fieldset">
            <legend>Relevant documents</legend>
            {#if documents.length === 0}
              <small>No completed documents are available. Add and index documents first.</small>
            {:else}
              {#each documents as document}
                <label class="check"><input type="checkbox" checked={relevantDocumentIds.includes(document.documentId)} on:change={() => relevantDocumentIds = toggle(document.documentId, relevantDocumentIds)} /><span>{document.title}</span></label>
              {/each}
            {/if}
          </fieldset>
          <button class="button secondary wide" disabled={creatingCase || relevantDocumentIds.length === 0}>{creatingCase ? 'Saving test case…' : 'Add to test set'}</button>
        </form>
        <div class="test-case-list" aria-label="Available test cases">
          {#each testCases as item}
            <label class="test-case">
              <input type="checkbox" checked={selectedTestCaseIds.includes(item.testCaseId)} on:change={() => selectedTestCaseIds = toggle(item.testCaseId, selectedTestCaseIds)} />
              <span><strong>{item.query}</strong><small>{item.relevantDocumentIds.length} relevant document{item.relevantDocumentIds.length === 1 ? '' : 's'} · {item.rationale}</small></span>
            </label>
          {/each}
        </div>
      </article>

      <article class="panel">
        <div class="section-label"><span>02</span><div><strong>Controlled experiment</strong><small>Run identical evidence through every selected strategy.</small></div></div>
        <div class="strategy-options">
          {#each strategies as strategy}
            <label class:selected={selectedStrategyIds.includes(strategy.strategyId)} class="strategy-option">
              <input type="checkbox" checked={selectedStrategyIds.includes(strategy.strategyId)} on:change={() => selectedStrategyIds = toggle(strategy.strategyId, selectedStrategyIds)} />
              <span><strong>{strategy.label}</strong><small>{strategy.description}</small></span>
              <code>{strategy.chunkSize}/{strategy.overlap}</code>
            </label>
          {/each}
        </div>
        <div class="evaluation-form-grid">
          <label for="run-history">Evidence snapshot<select id="run-history" value={activeRun?.runId ?? ''} on:change={(event) => event.currentTarget.value && openRun(event.currentTarget.value)}><option value="">Current setup</option>{#each runSummaries as run}<option value={run.runId}>{new Date(run.createdAt).toLocaleString()} · {percentage(run.bestRecallAtK)}</option>{/each}</select></label>
          <label for="top-k">Cutoff<select id="top-k" bind:value={topK}><option value={1}>Top 1</option><option value={3}>Top 3</option><option value={5}>Top 5</option><option value={10}>Top 10</option></select></label>
        </div>
        <fieldset class="selection-fieldset">
          <legend>Corpus versions</legend>
          {#each documents as document}
            <label class="check"><input type="checkbox" checked={selectedDocumentVersionIds.includes(document.documentVersionId)} on:change={() => selectedDocumentVersionIds = toggle(document.documentVersionId, selectedDocumentVersionIds)} /><span>{document.title}</span></label>
          {/each}
        </fieldset>
        <button class="button primary wide" on:click={runEvaluation} disabled={running || selectedStrategyIds.length === 0 || selectedTestCaseIds.length === 0 || selectedDocumentVersionIds.length === 0}>{running ? 'Evaluating retrieval…' : 'Run controlled evaluation'} <Play size={15} aria-hidden="true" /></button>
        <p class="form-boundary">{selectedStrategyIds.length} strategies · {selectedCases.length} queries · {selectedDocumentVersionIds.length} document versions</p>
      </article>
    </div>

    <div class="dashboard-stack">
      {#if !activeRun}
        <EmptyState title="No evaluation evidence yet" message="Select the test set, corpus and strategies to produce the first immutable comparison." />
      {:else}
        <section class="metric-strip" aria-label="Best strategy summary">
          <article><span>Best observed strategy</span><strong>{bestStrategy?.metrics.strategyLabel ?? '—'}</strong></article>
          <article><span>Recall@{activeRun.topK}</span><strong>{percentage(bestStrategy?.metrics.recallAtK ?? 0)}</strong></article>
          <article><span>Precision@{activeRun.topK}</span><strong>{percentage(bestStrategy?.metrics.precisionAtK ?? 0)}</strong></article>
          <article><span>Hit rate</span><strong>{percentage(bestStrategy?.metrics.hitRate ?? 0)}</strong></article>
        </section>

        <article class="panel">
          <div class="section-label"><BarChart3 size={17} aria-hidden="true" /><div><strong>Strategy comparison</strong><small>Macro averages across the selected ground-truth queries.</small></div></div>
          <div class="comparison-chart" aria-label={`Recall at ${activeRun.topK} comparison`}>
            {#each activeRun.strategies as strategy}
              <div class="chart-row"><strong>{strategy.metrics.strategyLabel}</strong><div class="bar-track"><i style={`width: ${strategy.metrics.recallAtK * 100}%`}></i></div><span>{percentage(strategy.metrics.recallAtK)}</span></div>
            {/each}
          </div>
          <div class="table-scroll">
            <table class="evaluation-table">
              <thead><tr><th>Strategy</th><th>Chunks</th><th>Precision@K</th><th>Recall@K</th><th>Hit rate</th><th>MRR</th><th>Errors</th></tr></thead>
              <tbody>{#each activeRun.strategies as strategy}<tr><th>{strategy.metrics.strategyLabel}</th><td>{strategy.metrics.chunkCount}</td><td>{percentage(strategy.metrics.precisionAtK)}</td><td>{percentage(strategy.metrics.recallAtK)}</td><td>{percentage(strategy.metrics.hitRate)}</td><td>{strategy.metrics.meanReciprocalRank.toFixed(3)}</td><td>{strategy.metrics.errorCount}</td></tr>{/each}</tbody>
            </table>
          </div>
        </article>

        <article class="panel error-analysis">
          <div class="section-label"><CircleAlert size={17} aria-hidden="true" /><div><strong>Error and relevance analysis</strong><small>Queries with incomplete recall remain visible; results can be reviewed without rewriting history.</small></div></div>
          {#if errorQueries.length === 0}
            <div class="evidence-note"><Check size={18} aria-hidden="true" /><p>Every evaluated query retrieved all expected documents within the selected cutoff. This result applies only to this test set and corpus snapshot.</p></div>
          {:else}
            {#each errorQueries as evaluationQuery}
              <details class="error-query">
                <summary><span><strong>{evaluationQuery.query}</strong><small>{evaluationQuery.strategy} · recall {percentage(evaluationQuery.recallAtK)}</small></span><CircleAlert size={16} aria-hidden="true" /></summary>
                <div class="result-list">
                  {#each evaluationQuery.results as hit}
                    <article class="result-row">
                      <span class="rank">{String(hit.rank).padStart(2, '0')}</span>
                      <div><strong>{hit.title}</strong><small>{hit.source} · similarity {formatScore(hit.score)}</small><p>{hit.snippet}</p></div>
                      <span class:complete={hit.relevant} class="status-badge">{hit.relevant ? 'Relevant' : 'Not relevant'}</span>
                      <div class="label-actions" aria-label={`Label ${hit.title}`}><button class="icon-button" title="Mark relevant" aria-label={`Mark ${hit.title} relevant`} disabled={labellingResultId === hit.resultId} on:click={() => labelResult(hit, true)}><Check size={15} /></button><button class="icon-button" title="Mark not relevant" aria-label={`Mark ${hit.title} not relevant`} disabled={labellingResultId === hit.resultId} on:click={() => labelResult(hit, false)}><Tag size={15} /></button></div>
                    </article>
                  {/each}
                </div>
              </details>
            {/each}
          {/if}
        </article>

        <aside class="evidence-note"><Beaker size={19} aria-hidden="true" /><p><strong>Evidence boundary.</strong> {activeRun.metricSemantics} Embedding version: <code>{activeRun.embeddingVersion}</code>. Similarity scores rank chunks; they are not confidence or probability. Manual labels update this run's auditable snapshot only.</p></aside>
      {/if}
    </div>
  </section>
{/if}
