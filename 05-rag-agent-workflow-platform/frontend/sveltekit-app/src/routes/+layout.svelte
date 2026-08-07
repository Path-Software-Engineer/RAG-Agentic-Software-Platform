<script lang="ts">
  import {
    Activity,
    BarChart3,
    BookOpenText,
    Bot,
    Database,
    Search,
    ShieldCheck
  } from '@lucide/svelte';
  import { page } from '$app/stores';
  import '../styles.css';

  const semanticNavigation = [
    { href: '/documents', label: 'Documents', icon: Database },
    { href: '/search', label: 'Semantic search', icon: Search }
  ];
  const evaluationNavigation = [{ href: '/evaluation', label: 'Evaluation lab', icon: BarChart3 }];
  const agentNavigation = [
    { href: '/agents', label: 'Workflow runs', icon: Bot },
    { href: '/agents#security', label: 'Security evidence', icon: Activity }
  ];
  $: isEvaluation = $page.url.pathname.startsWith('/evaluation');
  $: isAgent = $page.url.pathname.startsWith('/agents');
</script>

<svelte:head>
  <title>Atlas | Governed Evidence</title>
</svelte:head>

<div class="app-shell">
  <aside class="sidebar">
    <a class="brand" href="/" aria-label="Atlas home">
      <span class="brand-mark"><BookOpenText size={22} aria-hidden="true" /></span>
      <span><strong>Atlas</strong><small>Evidence workspace</small></span>
    </a>

    <nav aria-label="Primary navigation">
      <a class:active={$page.url.pathname === '/'} href="/">
        <span class="nav-index">00</span>
        <ShieldCheck size={17} aria-hidden="true" />
        <span>Overview</span>
      </a>
      <details open>
        <summary><span>01</span> Semantic Search</summary>
        {#each semanticNavigation as item, index}
          <a class:active={$page.url.pathname.startsWith(item.href)} href={item.href}>
            <span class="nav-index">{String(index + 1).padStart(2, '0')}</span>
            <svelte:component this={item.icon} size={17} aria-hidden="true" />
            <span>{item.label}</span>
          </a>
        {/each}
      </details>
      <details open>
        <summary><span>02</span> Retrieval Evaluation</summary>
        {#each evaluationNavigation as item}
          <a class:active={$page.url.pathname.startsWith(item.href)} href={item.href}>
            <span class="nav-index">01</span>
            <svelte:component this={item.icon} size={17} aria-hidden="true" />
            <span>{item.label}</span>
          </a>
        {/each}
      </details>
      <details open>
        <summary><span>03</span> Agent Trace Viewer</summary>
        {#each agentNavigation as item, index}
          <a
            class:active={item.href.includes('#')
              ? $page.url.hash === '#security'
              : $page.url.pathname.startsWith('/agents') && $page.url.hash !== '#security'}
            href={item.href}
          >
            <span class="nav-index">{String(index + 1).padStart(2, '0')}</span>
            <svelte:component this={item.icon} size={17} aria-hidden="true" />
            <span>{item.label}</span>
          </a>
        {/each}
      </details>
    </nav>

    <section class="boundary-card">
      <p class="eyebrow">Evidence boundary</p>
      <strong>{isAgent ? 'Governed execution' : isEvaluation ? 'Macro evaluation' : 'Source-first retrieval'}</strong>
      <p>{isAgent ? 'Operational traces only. Private reasoning is never exposed.' : isEvaluation ? 'Metrics depend on explicit document-level judgments.' : 'No generated answers. Similarity is not confidence.'}</p>
    </section>
  </aside>

  <main>
    <header class="topbar">
      <div>
        <span class="crumb">PROJECT 05 / {isAgent ? 'SPRINT 03' : isEvaluation ? 'SPRINT 02' : 'SPRINT 01'}</span>
        <strong>{isAgent ? 'Agent Workflow Trace Viewer' : isEvaluation ? 'Retrieval Evaluation Dashboard' : 'Semantic Search Module'}</strong>
      </div>
      <span class="runtime"><i></i> Local evidence engine</span>
    </header>
    <div class="page-frame">
      <slot />
    </div>
  </main>
</div>
