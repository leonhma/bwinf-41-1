<script lang="ts">
  import { ColorInput } from "color-picker-svelte";
  import {simulationProps} from "../index";
</script>

<div class="color">
  <ColorInput bind:color={$simulationProps.color} title={$simulationProps.color.toHexString()} showAlphaSlider/>
</div>

<style>
  .color {
    margin-bottom: auto;
  }
</style>
