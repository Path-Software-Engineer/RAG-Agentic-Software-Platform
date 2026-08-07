<script lang="ts">
  import { CircleCheck, CircleEllipsis, CircleX } from '@lucide/svelte';
  import type { DocumentStatus } from '../types';

  export let status: DocumentStatus;
</script>

<span class:complete={status === 'completed'} class:failed={status === 'failed'} class="status-badge">
  {#if status === 'completed'}
    <CircleCheck size={14} aria-hidden="true" />
  {:else if status === 'failed'}
    <CircleX size={14} aria-hidden="true" />
  {:else}
    <CircleEllipsis size={14} aria-hidden="true" />
  {/if}
  <span>{status}</span>
</span>
