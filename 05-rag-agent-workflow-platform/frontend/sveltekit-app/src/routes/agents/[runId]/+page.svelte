<script lang="ts">
  import { Activity, ArrowLeft, Braces, CircleAlert, ExternalLink, LockKeyhole, Network } from '@lucide/svelte';
  import { page } from '$app/stores';
  import { onDestroy, onMount } from 'svelte';
  import { agentEventsUrl, api, ApiError, formatScore } from '$lib/api';
  import type { AgentTraceResource } from '$lib/types';

  let trace: AgentTraceResource | null = null;
  let loading = true;
  let error = '';
  let streamState = 'replay';
  let eventSource: EventSource | null = null;
  const terminal = new Set(['completed', 'failed', 'cancelled', 'blocked']);
  const eventTypes = [
    'run_started', 'step_started', 'step_completed', 'step_failed', 'tool_called',
    'tool_completed', 'tool_failed', 'policy_blocked', 'run_completed', 'run_failed', 'run_cancelled'
  ];
  $: runId = $page.params.runId ?? '';

  onMount(async () => {
    await loadTrace();
    if (trace && !terminal.has(trace.run.status)) connectStream();
  });
  onDestroy(() => eventSource?.close());

  async function loadTrace() {
    error = '';
    try {
      trace = await api.agentTrace(runId);
      if (terminal.has(trace.run.status)) {
        streamState = 'reconciled';
        eventSource?.close();
      }
    } catch (reason) {
      error = reason instanceof ApiError
        ? `${reason.message} (${reason.correlationId})`
        : 'The trace could not be loaded.';
    } finally {
      loading = false;
    }
  }

  function connectStream() {
    streamState = 'connecting';
    eventSource = new EventSource(agentEventsUrl(runId));
    eventSource.onopen = () => (streamState = 'live');
    eventSource.onerror = () => (streamState = 'reconnecting');
    for (const eventType of eventTypes) {
      eventSource.addEventListener(eventType, () => void loadTrace());
    }
  }

  function eventLabel(value: string) {
    return value.replaceAll('_', ' ');
  }
</script>

<svelte:head><meta name="description" content="Inspect a sanitized governed-agent execution trace." /></svelte:head>

<a class="back-link" href="/agents"><ArrowLeft size={15} aria-hidden="true" /> Workflow runs</a>

{#if error}<p class="inline-message error large" role="alert">{error}</p>{/if}
{#if loading}
  <section class="results-loading" aria-live="polite"><i></i><span>Reconciling durable trace…</span></section>
{:else if trace}
  <section class="trace-heading">
    <div>
      <p class="eyebrow">RUN {trace.run.runId.slice(0, 13).toUpperCase()}</p>
      <h1>{trace.run.goal}</h1>
      <p>{trace.run.answer}</p>
    </div>
    <div class="trace-state">
      <span class={`run-status ${trace.run.status}`}>{trace.run.status}</span>
      <strong>{trace.run.outcome}</strong>
      <small><i></i>{streamState} · sequence {trace.events.at(-1)?.sequenceNumber ?? 0}</small>
    </div>
  </section>

  <section class="trace-metrics">
    <article><span>Graph steps</span><strong>{trace.run.usage.steps}/{trace.run.budget.maxSteps}</strong></article>
    <article><span>Tool calls</span><strong>{trace.run.usage.toolCalls}/{trace.run.budget.maxToolCalls}</strong></article>
    <article><span>Evidence</span><strong>{trace.run.citations.length}</strong></article>
    <article><span>Elapsed</span><strong>{trace.run.usage.elapsedMs.toFixed(1)} ms</strong></article>
  </section>

  <section class="panel trace-graph-panel">
    <div class="section-label"><span>01</span><div><strong>Executed graph</strong><small>Typed LangGraph path with server-owned transitions.</small></div></div>
    <div class="trace-graph" aria-label="Workflow graph">
      {#each trace.nodes as node, index}
        <article class:visited={trace.steps.some((step) => step.nodeId === node.nodeId)}>
          <span>{String(index + 1).padStart(2, '0')}</span>
          <Network size={16} aria-hidden="true" />
          <div><strong>{node.label}</strong><small>{node.kind}</small></div>
        </article>
        {#if index < trace.nodes.length - 1}<i aria-hidden="true"></i>{/if}
      {/each}
    </div>
  </section>

  <section class="trace-layout">
    <article class="panel">
      <div class="section-label"><span>02</span><div><strong>Event timeline</strong><small>Durable ordering; reconnect resumes after the last event ID.</small></div></div>
      <ol class="event-timeline">
        {#each trace.events as event}
          <li class:danger={event.eventType.includes('failed') || event.eventType === 'policy_blocked'}>
            <span>{String(event.sequenceNumber).padStart(2, '0')}</span>
            <i></i>
            <div><strong>{eventLabel(event.eventType)}</strong><small>{event.nodeId ?? 'run'} · {new Date(event.timestamp).toLocaleTimeString()}</small></div>
          </li>
        {/each}
      </ol>
    </article>

    <div class="trace-side-stack">
      <article class="panel">
        <div class="section-label"><span>03</span><div><strong>Sanitized tool calls</strong><small>Arguments and results are redacted and size-bounded.</small></div></div>
        {#if trace.toolCalls.length === 0}
          <p class="muted-copy">No tool implementation was reached.</p>
        {:else}
          <div class="tool-call-list">
            {#each trace.toolCalls as call}
              <details>
                <summary><LockKeyhole size={15} aria-hidden="true" /><strong>{call.toolName}</strong><span class={`run-status ${call.status}`}>{call.status}</span></summary>
                <div><p>Arguments</p><pre>{JSON.stringify(call.sanitizedArguments, null, 2)}</pre><p>Result boundary</p><pre>{JSON.stringify(call.sanitizedResult, null, 2)}</pre></div>
              </details>
            {/each}
          </div>
        {/if}
      </article>

      <article class="panel">
        <div class="section-label"><span>04</span><div><strong>Citation evidence</strong><small>Similarity ranks evidence; it is not confidence.</small></div></div>
        {#if trace.run.citations.length === 0}
          <p class="muted-copy">The run returned no supporting citations.</p>
        {:else}
          <div class="trace-citations">
            {#each trace.run.citations as citation}
              <a href={`/citations/${citation.citationId}`}>
                <span>#{citation.rank}</span><div><p>{citation.snippet}</p><small>{formatScore(citation.score)} similarity</small></div><ExternalLink size={14} aria-hidden="true" />
              </a>
            {/each}
          </div>
        {/if}
      </article>
    </div>
  </section>

  <aside class="private-reasoning-boundary">
    <CircleAlert size={18} aria-hidden="true" />
    <div><strong>Trace boundary</strong><p>This view exposes state, policy outcomes, sanitized inputs/outputs and citations. It never stores or displays chain-of-thought, system prompts or hidden model reasoning.</p></div>
    <Braces size={18} aria-hidden="true" />
  </aside>
{/if}
