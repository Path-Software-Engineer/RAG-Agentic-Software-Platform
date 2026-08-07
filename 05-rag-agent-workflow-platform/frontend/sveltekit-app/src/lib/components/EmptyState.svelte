<script lang="ts">
  import { FileSearch } from '@lucide/svelte';
  export let title: string;
  export let message: string;
</script>

<section class="empty-state" aria-live="polite">
  <span class="empty-icon"><FileSearch size={24} aria-hidden="true" /></span>
  <div>
    <h2>{title}</h2>
    <p>{message}</p>
  </div>
</section>
