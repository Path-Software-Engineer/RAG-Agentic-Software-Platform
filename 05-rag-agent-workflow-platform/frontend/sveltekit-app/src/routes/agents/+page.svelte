<script lang="ts">
  import { Activity, ArrowRight, Bot, LockKeyhole, Play, ShieldCheck } from '@lucide/svelte';
  import { goto } from '$app/navigation';
  import { onMount } from 'svelte';
  import { api, ApiError } from '$lib/api';
  import type {
    AgentRunSummaryResource,
    DocumentResource,
    SecurityEvaluationResource,
    ToolDefinitionResource
  } from '$lib/types';

  let documents: DocumentResource[] = [];
  let tools: ToolDefinitionResource[] = [];
  let runs: AgentRunSummaryResource[] = [];
  let security: SecurityEvaluationResource | null = null;
  let goal = 'How should retrieved instructions be treated?';
  let selectedVersions: string[] = [];
  let maxSteps = 8;
  let maxToolCalls = 3;
  let overallTimeoutMs = 8000;
  let running = false;
  let evaluating = false;
  let loading = true;
  let error = '';

  onMount(loadWorkspace);

  async function loadWorkspace() {
    loading = true;
    error = '';
    try {
      [documents, tools, runs] = await Promise.all([
        api.documents(),
        api.agentTools(),
        api.agentRuns()
      ]);
      documents = documents.filter((document) => document.status === 'completed');
      selectedVersions = documents.map((document) => document.documentVersionId);
    } catch (reason) {
      error = messageFor(reason, 'The governed workflow workspace could not be loaded.');
    } finally {
      loading = false;
    }
  }

  function messageFor(reason: unknown, fallback: string) {
    return reason instanceof ApiError ? `${reason.message} (${reason.correlationId})` : fallback;
  }

  function toggleVersion(versionId: string) {
    selectedVersions = selectedVersions.includes(versionId)
      ? selectedVersions.filter((item) => item !== versionId)
      : [...selectedVersions, versionId];
  }

  async function startRun(event: SubmitEvent) {
    event.preventDefault();
    running = true;
    error = '';
    try {
      const run = await api.createAgentRun({
        goal: goal.trim(),
        workflowId: 'bounded-research-v1',
        documentVersionIds: selectedVersions,
        allowedToolNames: ['semantic_search'],
        budget: {
          maxSteps: Number(maxSteps),
          maxToolCalls: Number(maxToolCalls),
          overallTimeoutMs: Number(overallTimeoutMs),
          perToolTimeoutMs: 3000
        },
        idempotencyKey: `atlas-${crypto.randomUUID()}`
      });
      await goto(`/agents/${run.runId}`);
    } catch (reason) {
      error = messageFor(reason, 'The governed run could not be started.');
    } finally {
      running = false;
    }
  }

  async function runSecurityEvaluation() {
    evaluating = true;
    error = '';
    try {
      security = await api.securityEvaluation();
    } catch (reason) {
      error = messageFor(reason, 'The security scenarios could not be evaluated.');
    } finally {
      evaluating = false;
    }
  }
</script>

<svelte:head>
  <meta
    name="description"
    content="Run a bounded evidence workflow and inspect its safe operational trace."
  />
</svelte:head>

<section class="agent-hero">
  <div>
    <p class="eyebrow">GOVERNED WORKFLOW / TRACE-FIRST</p>
    <h1>Observe the workflow.<br /><span>Trust only the evidence.</span></h1>
    <p class="lede">
      Run one deterministic research path across an approved corpus. Every state, tool call,
      policy decision and citation remains inspectable without exposing private reasoning.
    </p>
  </div>
  <div class="agent-hero-signal" aria-hidden="true">
    <Bot size={34} />
    <span>POLICY</span><i></i><span>RETRIEVE</span><i></i><span>TRACE</span>
  </div>
</section>

{#if error}<p class="inline-message error large" role="alert">{error}</p>{/if}

{#if loading}
  <section class="results-loading" aria-live="polite"><i></i><span>Loading workflow evidence…</span></section>
{:else}
  <section class="agent-workspace">
    <article class="panel agent-run-panel">
      <div class="section-label">
        <span>01</span>
        <div><strong>Start a bounded run</strong><small>The server owns the graph, policy and budgets.</small></div>
      </div>
      <form on:submit={startRun}>
        <label for="agent-goal">Evidence goal
          <textarea id="agent-goal" bind:value={goal} minlength="3" maxlength="500" required></textarea>
        </label>
        <fieldset class="selection-fieldset">
          <legend>Approved corpus versions</legend>
          {#if documents.length === 0}
            <small>Index at least one document before running the workflow.</small>
          {:else}
            {#each documents as document}
              <label class="check">
                <input
                  type="checkbox"
                  checked={selectedVersions.includes(document.documentVersionId)}
                  on:change={() => toggleVersion(document.documentVersionId)}
                />
                <span>{document.title}</span>
              </label>
            {/each}
          {/if}
        </fieldset>
        <div class="agent-budget-grid">
          <label for="max-steps">Graph steps<input id="max-steps" type="number" min="4" max="16" bind:value={maxSteps} /></label>
          <label for="max-tools">Tool calls<input id="max-tools" type="number" min="1" max="6" bind:value={maxToolCalls} /></label>
          <label for="timeout">Run timeout<input id="timeout" type="number" min="500" max="20000" step="500" bind:value={overallTimeoutMs} /></label>
        </div>
        <button class="button primary wide" disabled={running || selectedVersions.length === 0}>
          <Play size={16} aria-hidden="true" /> {running ? 'Running governed workflow…' : 'Run and inspect trace'}
        </button>
      </form>
      <p class="form-boundary">No shell · no arbitrary SQL · read-only tools · bounded output</p>
    </article>

    <aside class="agent-side-stack">
      <article class="panel">
        <div class="section-label">
          <span>02</span>
          <div><strong>Allowlisted tools</strong><small>Unknown tools never reach an implementation.</small></div>
        </div>
        <div class="tool-registry">
          {#each tools as tool}
            <article>
              <div><LockKeyhole size={15} aria-hidden="true" /><strong>{tool.name}</strong></div>
              <p>{tool.description}</p>
              <small>{tool.permission} · {tool.timeoutMs} ms · read only</small>
            </article>
          {/each}
        </div>
      </article>

      <article class="panel" id="security">
        <div class="section-label">
          <span>03</span>
          <div><strong>Security evidence</strong><small>Controlled fixtures, not a production red-team claim.</small></div>
        </div>
        <button class="button secondary wide" on:click={runSecurityEvaluation} disabled={evaluating}>
          <ShieldCheck size={16} aria-hidden="true" /> {evaluating ? 'Evaluating policies…' : 'Run five security scenarios'}
        </button>
        {#if security}
          <div class="security-result" class:passed={security.passed}>
            <Activity size={18} aria-hidden="true" />
            <div><strong>{security.passedCount}/{security.scenarioCount} scenarios passed</strong><small>{security.blockedCount} adversarial requests blocked · {security.policyVersion}</small></div>
          </div>
        {/if}
      </article>
    </aside>
  </section>

  <section class="agent-history">
    <div class="results-header">
      <div><p class="eyebrow">DURABLE POSTGRESQL HISTORY</p><h2>Recent workflow runs</h2></div>
      <div><span>{runs.length}</span><small>versioned traces</small></div>
    </div>
    {#if runs.length === 0}
      <div class="panel empty-trace">No agent runs have been recorded yet.</div>
    {:else}
      <div class="run-list">
        {#each runs as run}
          <a href={`/agents/${run.runId}`}>
            <span class={`run-status ${run.status}`}>{run.status}</span>
            <div><strong>{run.goal}</strong><small>{run.outcome ?? 'pending'} · {run.citationCount} citations · {new Date(run.createdAt).toLocaleString()}</small></div>
            <ArrowRight size={17} aria-hidden="true" />
          </a>
        {/each}
      </div>
    {/if}
  </section>
{/if}
