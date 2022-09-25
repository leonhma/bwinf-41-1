<script lang="ts">
  import "wasm-tracing-allocator";
  import { onMount } from "svelte";
  import { get } from "svelte/store";

  import Canvas from "./components/Canvas.svelte";
  import Sidebar from "./components/Sidebar.svelte";
  import Buttons from "./components/Buttons.svelte";
  import Controls from "./components/Controls.svelte";
  import Settings from "./components/Settings.svelte";

  import { simulationProps, simulationData, HSVtoRGB } from "./index";
  import CircularProgress from "@smui/circular-progress";
  import Snackbar, { Label, SnackbarComponentDev } from "@smui/snackbar";

  import "@smui/snackbar/bare.css";
  import "@smui/circular-progress/bare.css";
  import "./reset.css";

  let loadingSnackbar: SnackbarComponentDev,
    loadingFinishedSnackbar: SnackbarComponentDev,
    secureContextSnackbar: SnackbarComponentDev;

  onMount(async () => {
    if (window.location.protocol !== "https:") {
      secureContextSnackbar.open();
    }

    let showsLoadingIndicator = false,
      finishedLoading = false,
      Simulation: typeof import("../pkg").Simulation;

    // asynchronously load the wasm module
    await Promise.all([
      (async function () {
        await import(/* webpackPreload: true */ "../pkg").then((module) => {
          Simulation = module.Simulation;
          finishedLoading = true;
          loadingSnackbar.close();
          if (showsLoadingIndicator) {
            loadingFinishedSnackbar.open();
          }
        });
      })(),
      new Promise<void>((resolve) => {
        setTimeout(() => {
          resolve();
        }, 500);
      }).then(() => {
        if (!finishedLoading) {
          showsLoadingIndicator = true;
          loadingSnackbar.open();
        }
      }),
    ]);

    let simulation: import("../pkg").Simulation;

    const props = get(simulationProps);

    simulationData.subscribe((data) => {
      if (data.canvas && simulation === undefined) {
        simulation = new Simulation(
          props.v_up_start,
          props.v_up_end,
          props.v_down_start,
          props.v_down_end,
          props.v_left_start,
          props.v_left_end,
          props.v_right_start,
          props.v_right_end,
          [255, 255, 255],
          1.0,
          data.canvas
        );
        console.log("created new instance of simulation");
        simulationProps.subscribe((props) => {
          simulation.updateSimulationProps(
            props.v_up_start,
            props.v_up_end,
            props.v_down_start,
            props.v_down_end,
            props.v_left_start,
            props.v_left_end,
            props.v_right_start,
            props.v_right_end,
            [
              ...Object.values(
                HSVtoRGB(props.color.h, props.color.s, props.color.v)
              ),
            ],
            props.color.a
          );
        });
      }
    });
  });
</script>

<div class="container">
  <Canvas />
  <Sidebar>
    <Settings />
    <Buttons />
    <Controls />
  </Sidebar>
  <Snackbar bind:this={loadingSnackbar} timeoutMs={-1}>
    <div style="display: flex; flex-direction: row; align-items: center">
      <CircularProgress
        style="height: 32px; width: 32px; margin-left: 12px"
        indeterminate
      />
      <Label>Runtime wird heruntergeladen</Label>
    </div>
  </Snackbar>
  <Snackbar bind:this={loadingFinishedSnackbar}>
    <Label>Runtime wurde heruntergeladen</Label>
  </Snackbar>
  <Snackbar bind:this={secureContextSnackbar}>
    <Label>Bitte nutze einen sicheren Kontext (https)</Label>
  </Snackbar>
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
