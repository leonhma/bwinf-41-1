import App from "./App.svelte";
import { writable, get } from "svelte/store";
import { Simulation } from "../pkg";

export const simulationProps = writable({
  v_up_start: 4.5,
  v_up_end: 5.5,
  v_down_start: 4.5,
  v_down_end: 5.5,
  v_left_start: 4.5,
  v_left_end: 5.5,
  v_right_start: 4.5,
  v_right_end: 5.5,
  d_t_start: 80,
  d_t_end: 120,
  color: [255, 255, 255, 255],
});

export const simulationData = writable({
  canvas: null,
});

new App({
  target: document.body,
});

let simulation: Simulation;

simulationData.subscribe((data) => {
  if (data.canvas && simulation === undefined) {
    console.log('setting up simulation');
    const props = get(simulationProps);
    const data = get(simulationData);
    simulation = new Simulation(
      props.v_up_start,
      props.v_up_end,
      props.v_down_start,
      props.v_down_end,
      props.v_left_start,
      props.v_left_end,
      props.v_right_start,
      props.v_right_end,
      props.d_t_start,
      props.d_t_end,
      props.color,
      data.canvas
    );
  }
});
