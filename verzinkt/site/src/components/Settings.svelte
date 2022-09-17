<script lang="ts">
  import Slider from "@smui/slider";
  import "@smui/slider/bare.css";

  const v_min = 0.1,
    v_max = 10,
    v_step = 0.1;

  let v_up_start = 4.5,
    v_up_end = 5.5,
    v_down_start = 4.5,
    v_down_end = 5.5,
    v_left_start = 4.5,
    v_left_end = 5.5,
    v_right_start = 4.5,
    v_right_end = 5.5;

  const d_t_min = 0,
    d_t_max = 200,
    d_t_step = 2;

  let d_t_start = 80,
    d_t_end = 120;
</script>

<div class="settings">
  <span class="name">v_up (px/s)</span>
  <Slider
    discrete
    range
    min={v_min}
    max={v_max}
    step={v_step}
    bind:start={v_up_start}
    bind:end={v_up_end}
    style="margin: 0"
  />

  <span class="name">v_down (px/s)</span>
  <Slider
    discrete
    range
    min={v_min}
    max={v_max}
    step={v_step}
    bind:start={v_down_start}
    bind:end={v_down_end}
    style="margin: 0"
  />

  <span class="name">v_left (px/s)</span>
  <Slider
    discrete
    range
    min={v_min}
    max={v_max}
    step={v_step}
    bind:start={v_left_start}
    bind:end={v_left_end}
    style="margin: 0"
  />

  <span class="name">v_right (px/s)</span>
  <Slider
    discrete
    range
    min={v_min}
    max={v_max}
    step={v_step}
    bind:start={v_right_start}
    bind:end={v_right_end}
    style="margin: 0"
  />

  <span class="name">d_t (ms)</span>
  <Slider
    discrete
    range
    min={d_t_min}
    max={d_t_max}
    step={d_t_step}
    bind:start={d_t_start}
    bind:end={d_t_end}
    style="margin: 0"
  />
</div>

<style>
  .settings {
    margin: 0 2.4em auto;
    padding-top: 1em;

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
