<script lang="ts">
  import Controls from "./components/Canvas.svelte";
  import Sidebar from "./components/Sidebar.svelte";
  import "@material/typography/dist/mdc.typography.min.css";
  import './reset.css';
</script>

<div class="container">
  <Controls />
  <Sidebar />
</div>

<style>
  :root {
    font-family: "Roboto", "Roboto Mono", "Helvetica", "Arial", sans-serif;
  }
  .container {
    width: 100%;
    height: 100%;
    display: grid;
    grid-template: 1fr / 1fr minmax(14em, min(35%, 22em));
  }
</style>
