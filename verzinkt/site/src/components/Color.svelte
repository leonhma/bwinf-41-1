<script lang="ts">
  import { Color, ColorInput } from "color-picker-svelte";

  let color = new Color("#79818f");
</script>

<div class="color">
  <ColorInput bind:color title="Farbe" showAlphaSlider/>
</div>

<style>
  .color {
    margin-bottom: auto;
  }
</style>
