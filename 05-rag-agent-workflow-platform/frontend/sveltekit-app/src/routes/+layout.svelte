<script lang="ts">
  import { BookOpenText, Database, Search, ShieldCheck } from '@lucide/svelte';
  import { page } from '$app/stores';
  import '../styles.css';

  const navigation = [
    { href: '/', label: 'Overview', icon: ShieldCheck },
    { href: '/documents', label: 'Documents', icon: Database },
    { href: '/search', label: 'Semantic search', icon: Search }
  ];
</script>

<svelte:head>
  <title>Atlas — Semantic Search</title>
</svelte:head>

<div class="app-shell">
  <aside class="sidebar">
    <a class="brand" href="/" aria-label="Atlas home">
      <span class="brand-mark"><BookOpenText size={22} aria-hidden="true" /></span>
      <span><strong>Atlas</strong><small>Evidence workspace</small></span>
    </a>

    <nav aria-label="Primary navigation">
      <p class="nav-label">Sprint 01</p>
      {#each navigation as item, index}
        <a class:active={$page.url.pathname === item.href || (item.href !== '/' && $page.url.pathname.startsWith(item.href))} href={item.href}>
          <span class="nav-index">{String(index + 1).padStart(2, '0')}</span>
          <svelte:component this={item.icon} size={17} aria-hidden="true" />
          <span>{item.label}</span>
        </a>
      {/each}
    </nav>

    <section class="boundary-card">
      <p class="eyebrow">Evidence boundary</p>
      <strong>Source-first retrieval</strong>
      <p>No generated answers. Similarity is not confidence.</p>
    </section>
  </aside>

  <main>
    <header class="topbar">
      <div>
        <span class="crumb">PROJECT 05 / SPRINT 01</span>
        <strong>Semantic Search Module</strong>
      </div>
      <span class="runtime"><i></i> Local evidence engine</span>
    </header>
    <div class="page-frame">
      <slot />
    </div>
  </main>
</div>
