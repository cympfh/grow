<script lang="ts">
  import { onMount } from "svelte";
  import { filetree } from "./filetree";
  import Folder from "./components/Folder.svelte";

  const pathname = location.pathname;
  const slug = pathname.replace(/^\/*/, "").replace(/\/*$/, "");
  const slug_decoded = decodeURIComponent(slug).replace(/\+/g, " ");
  console.log(slug, slug_decoded);
  let content = "";
  let error = "";
  let tree = null;

  function mathjax() {
    let script = document.createElement("script");
    script.src = "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js";
    document.head.append(script);
    script.onload = () => {
      MathJax = {
        tex: {
          inlineMath: [
            ["$", "$"],
            ["\\(", "\\)"],
          ],
        },
        svg: { fontCache: "global" },
      };
    };
  }

  /// read a markdown
  function show() {
    error = `Fetching ${slug}`;
    fetch(`/api/content?slug=${slug}`)
      .then((res) => res.json())
      .then((res) => {
        if (res.ok) {
          content = res.html;
          error = "";
          mathjax();
        } else {
          error = res.error;
        }
      });
  }

  /// list menu
  function list() {
    fetch("/api/list")
      .then((res) => res.json())
      .then((paths) => {
        tree = filetree(paths, slug_decoded);
      });
  }

  onMount(async () => {
    list();
    if (pathname === "/") {
      0;
    } else {
      show();
    }
  });
</script>

<section class="hero">
  <div class="hero-body">
    <p class="title">grow.md</p>
    <p class="subtitle">{slug_decoded}</p>
  </div>
</section>
<div class="section">
  <div class="container">
    <div class="columns">
      <div class="column is-two-fifths">
        {#if tree}
          <Folder {tree} />
        {/if}
      </div>
      <div class="column">
        {#if error}
          <div class="notification is-danger">
            <button class="delete" />
            {error}
          </div>
        {:else}
          <div class="content">
            {@html content}
          </div>
        {/if}
      </div>
    </div>
  </div>
</div>

<style global lang="scss">
  @import "main.scss";
  .menu-label {
    text-transform: none !important;
  }
  aside.menu svg {
    position: relative;
    top: 0.3rem;
  }
</style>
