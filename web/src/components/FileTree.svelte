<script>
  import Icon from "svelte-awesome";
  import { caretRight, caretDown } from "svelte-awesome/icons";
  export let tree;
</script>

{#if tree.nodes}
  <!-- directory -->
  <p class="menu-label" on:click={() => (tree.open ^= true)}>
    <a>
      <Icon data={tree.open ? caretDown : caretRight} />
      <span>{tree.name}/</span>
    </a>
  </p>
  <ul class="menu-list">
    {#if tree.open}
      {#each tree.nodes as node}
        <li><svelte:self tree={node} /></li>
      {/each}
    {/if}
  </ul>
{:else}
  <!-- file -->
  <a href={"/" + tree.fullpath}>{tree.name}</a>
{/if}
