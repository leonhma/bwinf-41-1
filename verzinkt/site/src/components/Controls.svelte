<script lang="ts">
  import IconButton, { Icon } from "@smui/icon-button";
  import "@smui/icon-button/bare.css";

  let isPlaying = false;
</script>

<div class="wrapper">
  <div class="controls">
    <IconButton class="material-icons" disabled={isPlaying}
      >keyboard_double_arrow_left</IconButton
    >
    <IconButton class="material-icons" disabled={isPlaying}
      >keyboard_arrow_left</IconButton
    >

    <IconButton toggle bind:pressed={isPlaying}>
      <Icon class="material-icons" off>play_arrow</Icon>
      <Icon class="material-icons" on>pause</Icon>
    </IconButton>
    <IconButton class="material-icons" disabled={isPlaying}
      >keyboard_arrow_right</IconButton
    >
    <IconButton class="material-icons" disabled={isPlaying}
      >keyboard_double_arrow_right</IconButton
    >
  </div>
</div>

<style>
  .wrapper {
    width: 100%;
    box-shadow: 0px -5px 5px rgba(0, 0, 0, 0.1);
    position: relative;
    align-self: center;
    display: flex;
    flex-direction: row;
    justify-content: center;
  }
  .controls {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
  }
</style>
