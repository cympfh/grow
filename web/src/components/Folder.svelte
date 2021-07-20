<script>
  export let tree;
  import FileTree from "./FileTree.svelte";
</script>

<aside class="menu">
  <ul class="menu-list">
    <li><FileTree {tree} /></li>
  </ul>
</aside>
