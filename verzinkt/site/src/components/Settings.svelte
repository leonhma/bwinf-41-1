<script lang="ts">
  import Slider from "@smui/slider";
  import "@smui/slider/bare.css";
  import { simulationProps } from "../index";
  import Color from "./Color.svelte";

  const v_min = 0.1,
    v_max = 10,
    v_step = 0.1;
</script>

<div class="settings">
  <span class="name">v_up (px/s)</span>
  <Slider
    discrete
    range
    min={v_min}
    max={v_max}
    step={v_step}
    bind:start={$simulationProps.v_up_start}
    bind:end={$simulationProps.v_up_end}
    style="margin: 0"
  />

  <span class="name">v_down (px/s)</span>
  <Slider
    discrete
    range
    min={v_min}
    max={v_max}
    step={v_step}
    bind:start={$simulationProps.v_down_start}
    bind:end={$simulationProps.v_down_end}
    style="margin: 0"
  />

  <span class="name">v_left (px/s)</span>
  <Slider
    discrete
    range
    min={v_min}
    max={v_max}
    step={v_step}
    bind:start={$simulationProps.v_left_start}
    bind:end={$simulationProps.v_left_end}
    style="margin: 0"
  />

  <span class="name">v_right (px/s)</span>
  <Slider
    discrete
    range
    min={v_min}
    max={v_max}
    step={v_step}
    bind:start={$simulationProps.v_right_start}
    bind:end={$simulationProps.v_right_end}
    style="margin: 0"
  />

  <Color />
</div>

<style>
  .settings {
    padding: 0 2.4em;
    padding-top: 1em;
    flex-grow: 3;

    background: #fefefe;
    display: grid;
    justify-content: center;
    align-content: flex-start;
    justify-items: stretch;
    align-items: center;
    grid-template-columns: 1fr;
    overflow: auto;
  }
  .settings .name {
    justify-self: start;
    overflow: hidden;
    word-wrap: normal;
    width: 100%;
  }
</style>
