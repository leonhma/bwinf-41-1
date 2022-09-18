<script lang="ts">
  import { simulationData } from "../index";

  
</script>

<div class="canvas">
  <canvas bind:this={$simulationData.canvas} id="simulationCanvas" width="1080" height="720" />
</div>

<style>
  .canvas {
    background: #dbdbdb;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  #simulationCanvas {
    box-shadow: 5px 5px 5px rgba(0, 0, 0, 0.1);
    width: 90%;
    aspect-ratio: 16 / 9;
    background: #ffffff;
  }
</style>
