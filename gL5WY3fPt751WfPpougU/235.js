"use strict";(self.webpackChunkverzinkt=self.webpackChunkverzinkt||[]).push([[235],{235:(n,t,e)=>{e.a(n,(async(n,r)=>{try{e.r(t),e.d(t,{Simulation:()=>o.uL,__wbg_getContext_4d5e97892c1b206a:()=>o.qh,__wbg_get_57245cc7d7c7619d:()=>o.BO,__wbg_instanceof_CanvasRenderingContext2d_ff80c06d296e3622:()=>o.Ji,__wbg_newwithu8clampedarrayandsh_f7ef3a8f3fd04c8a:()=>o.iN,__wbg_onalloc_611aa284266001af:()=>o.RB,__wbg_onalloczeroed_86afad4ab69d2180:()=>o.tH,__wbg_ondealloc_d59c1d43c0a27c4a:()=>o.aP,__wbg_onrealloc_3ba44b7f074d28b9:()=>o.$u,__wbg_putImageData_23e0cc41d4fabcde:()=>o.QJ,__wbindgen_debug_string:()=>o.fY,__wbindgen_number_get:()=>o.M1,__wbindgen_object_drop_ref:()=>o.ug,__wbindgen_throw:()=>o.Or});var o=e(838),a=n([o]);o=(a.then?(await a)():a)[0],r()}catch(n){r(n)}}))},838:(n,t,e)=>{e.a(n,(async(r,o)=>{try{e.d(t,{$u:()=>L,BO:()=>z,Ji:()=>R,M1:()=>D,Or:()=>M,QJ:()=>q,RB:()=>S,aP:()=>B,fY:()=>F,iN:()=>P,qh:()=>E,tH:()=>J,uL:()=>j,ug:()=>I});var a=e(530);n=e.hmd(n);var _=r([a]);a=(_.then?(await _)():_)[0];const c=new Array(32).fill(void 0);function i(n){return c[n]}function u(n){return null==n}c.push(void 0,null,!0,!1);let d=new Float64Array,l=new Int32Array;function f(){return 0===l.byteLength&&(l=new Int32Array(a.memory.buffer)),l}let s=c.length;function g(n){n<36||(c[n]=s,s=n)}function b(n){const t=i(n);return g(n),t}function w(n){const t=typeof n;if("number"==t||"boolean"==t||null==n)return`${n}`;if("string"==t)return`"${n}"`;if("symbol"==t){const t=n.description;return null==t?"Symbol":`Symbol(${t})`}if("function"==t){const t=n.name;return"string"==typeof t&&t.length>0?`Function(${t})`:"Function"}if(Array.isArray(n)){const t=n.length;let e="[";t>0&&(e+=w(n[0]));for(let r=1;r<t;r++)e+=", "+w(n[r]);return e+="]",e}const e=/\[object ([^\]]+)\]/.exec(toString.call(n));let r;if(!(e.length>1))return toString.call(n);if(r=e[1],"Object"==r)try{return"Object("+JSON.stringify(n)+")"}catch(n){return"Object"}return n instanceof Error?`${n.name}: ${n.message}\n${n.stack}`:r}let y=0,h=new Uint8Array;function p(){return 0===h.byteLength&&(h=new Uint8Array(a.memory.buffer)),h}let m=new("undefined"==typeof TextEncoder?(0,n.require)("util").TextEncoder:TextEncoder)("utf-8");const v="function"==typeof m.encodeInto?function(n,t){return m.encodeInto(n,t)}:function(n,t){const e=m.encode(n);return t.set(e),{read:n.length,written:e.length}};function A(n,t,e){if(void 0===e){const e=m.encode(n),r=t(e.length);return p().subarray(r,r+e.length).set(e),y=e.length,r}let r=n.length,o=t(r);const a=p();let _=0;for(;_<r;_++){const t=n.charCodeAt(_);if(t>127)break;a[o+_]=t}if(_!==r){0!==_&&(n=n.slice(_)),o=e(o,r,r=_+3*n.length);const t=p().subarray(o+_,o+r);_+=v(n,t).written}return y=_,o}let x=new("undefined"==typeof TextDecoder?(0,n.require)("util").TextDecoder:TextDecoder)("utf-8",{ignoreBOM:!0,fatal:!0});function k(n,t){return x.decode(p().subarray(n,n+t))}function C(n){s===c.length&&c.push(c.length+1);const t=s;return s=c[t],c[t]=n,t}function O(n,t){try{return n.apply(this,t)}catch(n){a.__wbindgen_exn_store(C(n))}}x.decode();let T=new Uint8ClampedArray;function $(n,t){return(0===T.byteLength&&(T=new Uint8ClampedArray(a.memory.buffer)),T).subarray(n/1,n/1+t)}class j{static __wrap(n){const t=Object.create(j.prototype);return t.ptr=n,t}__destroy_into_raw(){const n=this.ptr;return this.ptr=0,n}free(){const n=this.__destroy_into_raw();a.__wbg_simulation_free(n)}constructor(n,t,e,r,o,_,c,i,u,d,l){try{const w=a.__wbindgen_add_to_stack_pointer(-16);a.simulation_new(w,n,t,e,r,o,_,c,i,C(u),d,C(l));var s=f()[w/4+0],g=f()[w/4+1];if(f()[w/4+2])throw b(g);return j.__wrap(s)}finally{a.__wbindgen_add_to_stack_pointer(16)}}reset(){try{const t=a.__wbindgen_add_to_stack_pointer(-16);a.simulation_reset(t,this.ptr);var n=f()[t/4+0];if(f()[t/4+1])throw b(n)}finally{a.__wbindgen_add_to_stack_pointer(16)}}updateSimulationProps(n,t,e,r,o,_,c,i,u,d){try{const s=a.__wbindgen_add_to_stack_pointer(-16);a.simulation_updateSimulationProps(s,this.ptr,n,t,e,r,o,_,c,i,C(u),d);var l=f()[s/4+0];if(f()[s/4+1])throw b(l)}finally{a.__wbindgen_add_to_stack_pointer(16)}}}function D(n,t){const e=i(t),r="number"==typeof e?e:void 0;(0===d.byteLength&&(d=new Float64Array(a.memory.buffer)),d)[n/8+1]=u(r)?0:r,f()[n/4+0]=!u(r)}function I(n){b(n)}function S(n,t,e){WasmTracingAllocator.on_alloc(n>>>0,t>>>0,e)}function B(n,t,e){WasmTracingAllocator.on_dealloc(n>>>0,t>>>0,e)}function J(n,t,e){WasmTracingAllocator.on_alloc_zeroed(n>>>0,t>>>0,e)}function L(n,t,e,r,o){WasmTracingAllocator.on_realloc(n,t,e>>>0,r>>>0,o>>>0)}function R(n){let t;try{t=i(n)instanceof CanvasRenderingContext2D}catch{t=!1}return t}function q(){return O((function(n,t,e,r){i(n).putImageData(i(t),e,r)}),arguments)}function E(){return O((function(n,t,e){const r=i(n).getContext(k(t,e));return u(r)?0:C(r)}),arguments)}function P(){return O((function(n,t,e,r){return C(new ImageData($(n,t),e>>>0,r>>>0))}),arguments)}function z(n,t){return C(i(n)[t>>>0])}function F(n,t){const e=A(w(i(t)),a.__wbindgen_malloc,a.__wbindgen_realloc),r=y;f()[n/4+1]=r,f()[n/4+0]=e}function M(n,t){throw new Error(k(n,t))}o()}catch(N){o(N)}}))},530:(n,t,e)=>{e.a(n,(async(r,o)=>{try{var a,_=r([a=e(838)]),[a]=_.then?(await _)():_;await e.v(t,n.id,"ee429ce16b5317c6c6d4",{"./index_bg.js":{__wbindgen_number_get:a.M1,__wbindgen_object_drop_ref:a.ug,__wbg_onalloc_611aa284266001af:a.RB,__wbg_ondealloc_d59c1d43c0a27c4a:a.aP,__wbg_onrealloc_3ba44b7f074d28b9:a.$u,__wbg_instanceof_CanvasRenderingContext2d_ff80c06d296e3622:a.Ji,__wbg_putImageData_23e0cc41d4fabcde:a.QJ,__wbg_getContext_4d5e97892c1b206a:a.qh,__wbg_newwithu8clampedarrayandsh_f7ef3a8f3fd04c8a:a.iN,__wbg_get_57245cc7d7c7619d:a.BO,__wbindgen_debug_string:a.fY,__wbindgen_throw:a.Or}}),o()}catch(n){o(n)}}),1)}}]);