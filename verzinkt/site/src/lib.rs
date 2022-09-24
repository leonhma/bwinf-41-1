use wasm_bindgen::{prelude::*, Clamped, JsCast};
use web_sys::ImageData;

extern crate wee_alloc;

#[global_allocator]
static ALLOC: wee_alloc::WeeAlloc = wee_alloc::WeeAlloc::INIT;

#[allow(dead_code)]
fn main() {
    #[wasm_bindgen]
    pub struct Simulation {
        v_up_start: i8,
        v_up_end: i8,
        v_down_start: i8,
        v_down_end: i8,
        v_left_start: i8,
        v_left_end: i8,
        v_right_start: i8,
        v_right_end: i8,
        color: [u8; 4],

        context: web_sys::CanvasRenderingContext2d,
        data: [u8; 720 * 1080 * 4],
    }

    #[wasm_bindgen]
    impl Simulation {
        #[wasm_bindgen(constructor)]
        pub fn new(
            v_up_start: i8,
            v_up_end: i8,
            v_down_start: i8,
            v_down_end: i8,
            v_left_start: i8,
            v_left_end: i8,
            v_right_start: i8,
            v_right_end: i8,
            color: js_sys::Array,

            canvas: web_sys::HtmlCanvasElement,
        ) -> Result<Simulation, JsValue> {
            let context = canvas
                .get_context("2d")
                .unwrap()
                .unwrap()
                .dyn_into::<web_sys::CanvasRenderingContext2d>()
                .unwrap();
            context
                .put_image_data(
                    &ImageData::new_with_u8_clamped_array_and_sh(
                        Clamped(&[255; 720 * 1080 * 4]),
                        1080,
                        720,
                    )
                    .unwrap(),
                    0.0,
                    0.0,
                )
                .unwrap();
            Ok(Simulation {
                v_up_start,
                v_up_end,
                v_down_start,
                v_down_end,
                v_left_start,
                v_left_end,
                v_right_start,
                v_right_end,
                color: [
                    color.get(0).as_f64().unwrap() as u8,
                    color.get(1).as_f64().unwrap() as u8,
                    color.get(2).as_f64().unwrap() as u8,
                    color.get(3).as_f64().unwrap() as u8,
                ],
                context: context,
                data: [255; 720 * 1080 * 4],
            })
        }

        // rerender the canvas
        fn render(&self) -> Result<(), JsValue> {
            let image_data =
                ImageData::new_with_u8_clamped_array_and_sh(Clamped(&self.data), 1080, 720)
                    .unwrap();
            self.context.put_image_data(&image_data, 0.0, 0.0)
        }

        // delete contents of canvas
        #[wasm_bindgen]
        pub fn reset(&mut self) -> Result<(), JsValue> {
            self.data = [255; 720 * 1080 * 4];
            self.render()
        }

        #[wasm_bindgen(js_name = "updateSimulationProps")]
        pub fn update_simulation_props(
            &mut self,
            v_up_start: i8,
            v_up_end: i8,
            v_down_start: i8,
            v_down_end: i8,
            v_left_start: i8,
            v_left_end: i8,
            v_right_start: i8,
            v_right_end: i8,
            color: js_sys::Array,
        ) -> Result<(), JsValue> {
            self.v_up_start = v_up_start;
            self.v_up_end = v_up_end;
            self.v_down_start = v_down_start;
            self.v_down_end = v_down_end;
            self.v_left_start = v_left_start;
            self.v_left_end = v_left_end;
            self.v_right_start = v_right_start;
            self.v_right_end = v_right_end;
            self.color = [
                color.get(0).as_f64().unwrap() as u8,
                color.get(1).as_f64().unwrap() as u8,
                color.get(2).as_f64().unwrap() as u8,
                color.get(3).as_f64().unwrap() as u8,
            ];
            Ok(())
        }

        // return false if context is filled
    //    #[wasm_bindgen(js_name = "step")]
  //      pub fn step(&mut self) -> Result<bool, JsValue> {
//        }
    }
}
