import App from "./App.svelte";
import { writable } from "svelte/store";
import { Color } from "color-picker-svelte";

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
  color: new Color("#798f9d"),
});

export const simulationData = writable({
  canvas: undefined,
  simulation: undefined,
});

export function HSVtoRGB(h: number, s: number, v: number) {
  var r, g, b, i, f, p, q, t;
  i = Math.floor(h * 6);
  f = h * 6 - i;
  p = v * (1 - s);
  q = v * (1 - f * s);
  t = v * (1 - (1 - f) * s);
  switch (i % 6) {
    case 0:
      (r = v), (g = t), (b = p);
      break;
    case 1:
      (r = q), (g = v), (b = p);
      break;
    case 2:
      (r = p), (g = v), (b = t);
      break;
    case 3:
      (r = p), (g = q), (b = v);
      break;
    case 4:
      (r = t), (g = p), (b = v);
      break;
    case 5:
      (r = v), (g = p), (b = q);
      break;
  }
  return {
    r: Math.round(r * 255),
    g: Math.round(g * 255),
    b: Math.round(b * 255),
  };
}

new App({
  target: document.body,
});
