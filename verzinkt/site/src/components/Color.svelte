<script lang="ts">
  import { Color, ColorInput } from "color-picker-svelte";

  let color = new Color("#ffffff");
</script>

<div class="color">
  <ColorInput bind:color title="Farbe" />
</div>

<style>
  .color {
    margin-bottom: auto;
  }
</style>
