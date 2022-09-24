import App from "./App.svelte";
import { writable } from "svelte/store";
import "wasm-tracing-allocator";

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
  canvas: undefined,
  simulation: undefined,
});

new App({
  target: document.body,
});
