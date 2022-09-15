<script lang="ts">
  import IconButton, { Icon } from "@smui/icon-button";
  import "@smui/icon-button/bare.css"
  import Card, { Actions } from "@smui/card";
  import "@smui/card/bare.css"

  export let isRunning = false
</script>

<div>
  <Card>
    <Actions>
      <IconButton class="material-icons" title="Zurücksetzen">keyboard_double_arrow_left</IconButton>
      <IconButton class="material-icons" title="Schritt zurück">keyboard_arrow_left</IconButton>
      <IconButton class="material-icons" ariaLabelOn="Simulation pausieren" araiLabelOff="Simulation fortsetzen" bind:pressed={isRunning}>
        <Icon class="material-icons" title="Pause" on>pause</Icon>
        <Icon class="material-icons" title="Start" off>play_arrow</Icon>
      </IconButton>
      <IconButton class="material-icons" title="Schritt vor">keyboard_arrow_right</IconButton>
      <IconButton class="material-icons" title="Schnelldurchlauf">keyboard_double_arrow_right</IconButton>
    </Actions>
  </Card>
</div>
