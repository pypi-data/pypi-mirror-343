var Wn = Object.defineProperty;
var Bn = (e, t, n) => t in e ? Wn(e, t, { enumerable: !0, configurable: !0, writable: !0, value: n }) : e[t] = n;
var F = (e, t, n) => Bn(e, typeof t != "symbol" ? t + "" : t, n);
import * as Ln from "vue";
import { unref as B, watch as G, nextTick as ke, isRef as Ut, shallowRef as Q, ref as J, watchEffect as Kt, computed as L, readonly as Un, provide as Pe, inject as ee, customRef as ut, toValue as H, shallowReactive as Kn, defineComponent as W, reactive as Gn, h as A, getCurrentInstance as Gt, toRaw as Ht, normalizeStyle as Hn, normalizeClass as ze, toDisplayString as qt, onUnmounted as Ae, Fragment as $e, vModelDynamic as qn, vShow as zn, resolveDynamicComponent as lt, normalizeProps as Jn, withDirectives as Qn, onErrorCaptured as Yn, openBlock as de, createElementBlock as Se, createElementVNode as Xn, createVNode as Zn, withCtx as er, renderList as tr, createBlock as nr, TransitionGroup as zt, KeepAlive as rr } from "vue";
let Jt;
function or(e) {
  Jt = e;
}
function Je() {
  return Jt;
}
function ye() {
  const { queryPath: e, pathParams: t, queryParams: n } = Je();
  return {
    path: e,
    ...t === void 0 ? {} : { params: t },
    ...n === void 0 ? {} : { queryParams: n }
  };
}
var oe;
((e) => {
  function t(i) {
    return i.type === "ref";
  }
  e.isRef = t;
  function n(i) {
    return i.type === "vComputed";
  }
  e.isVueComputed = n;
  function r(i) {
    return i.type === "jsComputed";
  }
  e.isJsComputed = r;
  function o(i) {
    return i.type === "webComputed";
  }
  e.isWebComputed = o;
  function s(i) {
    return i.type === "data";
  }
  e.isConstData = s;
})(oe || (oe = {}));
var N;
((e) => {
  function t(g) {
    return g.type === "ref" || g.type === "computed" || g.type === "webComputed" || g.type === "data";
  }
  e.isVar = t;
  function n(g) {
    return g.type === "ref";
  }
  e.isRef = n;
  function r(g) {
    return g.type === "routePar";
  }
  e.isRouterParams = r;
  function o(g) {
    return g.type === "routeAct";
  }
  e.isRouterAction = o;
  function s(g) {
    return g.type === "data";
  }
  e.isConstData = s;
  function i(g) {
    return g.type === "computed";
  }
  e.isComputed = i;
  function a(g) {
    return g.type === "webComputed";
  }
  e.isWebComputed = a;
  function l(g) {
    return g.type === "js";
  }
  e.isJs = l;
  function d(g) {
    return g.type === "jsOutput";
  }
  e.isJsOutput = d;
  function u(g) {
    return g.type === "vf";
  }
  e.isVForItem = u;
  function c(g) {
    return g.type === "vf-i";
  }
  e.isVForIndex = c;
  function f(g) {
    return g.type === "sp";
  }
  e.isSlotProp = f;
  function h(g) {
    return g.type === "event";
  }
  e.isEventContext = h;
  function v(g) {
    return g.type === "ele_ref";
  }
  e.isElementRef = v;
  function p(g) {
    return g.type !== void 0;
  }
  e.IsBinding = p;
})(N || (N = {}));
var Qe;
((e) => {
  function t(n) {
    return n.type === "web";
  }
  e.isWebEventHandler = t;
})(Qe || (Qe = {}));
class sr extends Map {
  constructor(t) {
    super(), this.factory = t;
  }
  getOrDefault(t) {
    if (!this.has(t)) {
      const n = this.factory();
      return this.set(t, n), n;
    }
    return super.get(t);
  }
}
function we(e) {
  return new sr(e);
}
function he(e) {
  return typeof e == "function" ? e() : B(e);
}
typeof WorkerGlobalScope < "u" && globalThis instanceof WorkerGlobalScope;
const Ye = () => {
};
function Xe(e, t = !1, n = "Timeout") {
  return new Promise((r, o) => {
    setTimeout(t ? () => o(n) : r, e);
  });
}
function Ze(e, t = !1) {
  function n(c, { flush: f = "sync", deep: h = !1, timeout: v, throwOnTimeout: p } = {}) {
    let g = null;
    const _ = [new Promise((b) => {
      g = G(
        e,
        (S) => {
          c(S) !== t && (g ? g() : ke(() => g == null ? void 0 : g()), b(S));
        },
        {
          flush: f,
          deep: h,
          immediate: !0
        }
      );
    })];
    return v != null && _.push(
      Xe(v, p).then(() => he(e)).finally(() => g == null ? void 0 : g())
    ), Promise.race(_);
  }
  function r(c, f) {
    if (!Ut(c))
      return n((S) => S === c, f);
    const { flush: h = "sync", deep: v = !1, timeout: p, throwOnTimeout: g } = f ?? {};
    let w = null;
    const b = [new Promise((S) => {
      w = G(
        [e, c],
        ([D, x]) => {
          t !== (D === x) && (w ? w() : ke(() => w == null ? void 0 : w()), S(D));
        },
        {
          flush: h,
          deep: v,
          immediate: !0
        }
      );
    })];
    return p != null && b.push(
      Xe(p, g).then(() => he(e)).finally(() => (w == null || w(), he(e)))
    ), Promise.race(b);
  }
  function o(c) {
    return n((f) => !!f, c);
  }
  function s(c) {
    return r(null, c);
  }
  function i(c) {
    return r(void 0, c);
  }
  function a(c) {
    return n(Number.isNaN, c);
  }
  function l(c, f) {
    return n((h) => {
      const v = Array.from(h);
      return v.includes(c) || v.includes(he(c));
    }, f);
  }
  function d(c) {
    return u(1, c);
  }
  function u(c = 1, f) {
    let h = -1;
    return n(() => (h += 1, h >= c), f);
  }
  return Array.isArray(he(e)) ? {
    toMatch: n,
    toContains: l,
    changed: d,
    changedTimes: u,
    get not() {
      return Ze(e, !t);
    }
  } : {
    toMatch: n,
    toBe: r,
    toBeTruthy: o,
    toBeNull: s,
    toBeNaN: a,
    toBeUndefined: i,
    changed: d,
    changedTimes: u,
    get not() {
      return Ze(e, !t);
    }
  };
}
function ir(e) {
  return Ze(e);
}
function ar(e, t, n) {
  let r;
  Ut(n) ? r = {
    evaluating: n
  } : r = n || {};
  const {
    lazy: o = !1,
    evaluating: s = void 0,
    shallow: i = !0,
    onError: a = Ye
  } = r, l = J(!o), d = i ? Q(t) : J(t);
  let u = 0;
  return Kt(async (c) => {
    if (!l.value)
      return;
    u++;
    const f = u;
    let h = !1;
    s && Promise.resolve().then(() => {
      s.value = !0;
    });
    try {
      const v = await e((p) => {
        c(() => {
          s && (s.value = !1), h || p();
        });
      });
      f === u && (d.value = v);
    } catch (v) {
      a(v);
    } finally {
      s && f === u && (s.value = !1), h = !0;
    }
  }), o ? L(() => (l.value = !0, d.value)) : d;
}
function cr(e, t, n) {
  const {
    immediate: r = !0,
    delay: o = 0,
    onError: s = Ye,
    onSuccess: i = Ye,
    resetOnExecute: a = !0,
    shallow: l = !0,
    throwError: d
  } = {}, u = l ? Q(t) : J(t), c = J(!1), f = J(!1), h = Q(void 0);
  async function v(w = 0, ..._) {
    a && (u.value = t), h.value = void 0, c.value = !1, f.value = !0, w > 0 && await Xe(w);
    const b = typeof e == "function" ? e(..._) : e;
    try {
      const S = await b;
      u.value = S, c.value = !0, i(S);
    } catch (S) {
      if (h.value = S, s(S), d)
        throw S;
    } finally {
      f.value = !1;
    }
    return u.value;
  }
  r && v(o);
  const p = {
    state: u,
    isReady: c,
    isLoading: f,
    error: h,
    execute: v
  };
  function g() {
    return new Promise((w, _) => {
      ir(f).toBe(!1).then(() => w(p)).catch(_);
    });
  }
  return {
    ...p,
    then(w, _) {
      return g().then(w, _);
    }
  };
}
function K(e, t) {
  t = t || {};
  const n = [...Object.keys(t), "__Vue"], r = [...Object.values(t), Ln];
  try {
    return new Function(...n, `return (${e})`)(...r);
  } catch (o) {
    throw new Error(o + " in function code: " + e);
  }
}
function ur(e) {
  if (e.startsWith(":")) {
    e = e.slice(1);
    try {
      return K(e);
    } catch (t) {
      throw new Error(t + " in function code: " + e);
    }
  }
}
function Qt(e) {
  return e.constructor.name === "AsyncFunction";
}
function lr(e, t) {
  return J(e.value);
}
function fr(e, t, n) {
  const { bind: r = {}, code: o, const: s = [] } = e, i = Object.values(r).map((u, c) => s[c] === 1 ? u : t.getVueRefObjectOrValue(u));
  if (Qt(new Function(o)))
    return ar(
      async () => {
        const u = Object.fromEntries(
          Object.keys(r).map((c, f) => [c, i[f]])
        );
        return await K(o, u)();
      },
      null,
      { lazy: !0 }
    );
  const a = Object.fromEntries(
    Object.keys(r).map((u, c) => [u, i[c]])
  ), l = K(o, a);
  return L(l);
}
function dr(e, t, n) {
  const {
    inputs: r = [],
    code: o,
    slient: s,
    data: i,
    asyncInit: a = null
  } = e, l = s || Array(r.length).fill(0), d = i || Array(r.length).fill(0), u = r.filter((p, g) => l[g] === 0 && d[g] === 0).map((p) => t.getVueRefObject(p));
  function c() {
    return r.map(
      (p, g) => d[g] === 1 ? p : t.getObjectToValue(p)
    );
  }
  const f = K(o), h = Q(null), v = { immediate: !0, deep: !0 };
  return Qt(f) ? (h.value = a, G(
    u,
    async () => {
      h.value = await f(...c());
    },
    v
  )) : G(
    u,
    () => {
      h.value = f(...c());
    },
    v
  ), Un(h);
}
function hr(e, t) {
  const { init: n } = e;
  return Q(n ?? null);
}
function pr() {
  return [];
}
const Ee = we(pr);
function Yt(e, t) {
  const n = Ee.getOrDefault(e.id), r = /* @__PURE__ */ new Map();
  return n.push(r), t.replaceSnapshot({
    scopeSnapshot: Xt()
  }), (e.vars || []).forEach((o) => {
    r.set(o.id, vr(o, t));
  }), (e.web_computed || []).forEach((o) => {
    const { init: s } = o;
    r.set(o.id, J(s));
  }), n.length - 1;
}
function Xt() {
  const e = /* @__PURE__ */ new Map();
  for (const [n, r] of Ee) {
    const o = r[r.length - 1];
    e.set(n, [o]);
  }
  function t(n) {
    return Zt(n, e);
  }
  return {
    getVueRef: t
  };
}
function mr(e) {
  return Zt(e, Ee);
}
function Zt(e, t) {
  const n = t.get(e.sid);
  if (!n)
    throw new Error(`Scope ${e.sid} not found`);
  const o = n[n.length - 1].get(e.id);
  if (!o)
    throw new Error(`Var ${e.id} not found in scope ${e.sid}`);
  return o;
}
function gr(e) {
  Ee.delete(e);
}
function en(e, t) {
  const n = Ee.get(e);
  n && n.splice(t, 1);
}
function vr(e, t, n) {
  if (oe.isRef(e))
    return lr(e);
  if (oe.isVueComputed(e))
    return fr(
      e,
      t
    );
  if (oe.isJsComputed(e))
    return dr(
      e,
      t
    );
  if (oe.isWebComputed(e))
    return hr(e);
  if (oe.isConstData(e))
    return e.value;
  throw new Error(`Invalid var config: ${e}`);
}
const Ne = we(() => []);
function yr(e) {
  const t = Q();
  Ne.getOrDefault(e.sid).push(t);
}
function wr(e) {
  Ne.has(e) && Ne.delete(e);
}
function tn() {
  const e = new Map(
    Array.from(Ne.entries()).map(([n, r]) => [
      n,
      r[r.length - 1]
    ])
  );
  function t(n) {
    return e.get(n.sid);
  }
  return {
    getRef: t
  };
}
const Te = we(() => []);
function Er(e) {
  const t = Te.getOrDefault(e);
  return t.push(Q({})), t.length - 1;
}
function _r(e, t, n) {
  Te.get(e)[t].value = n;
}
function br(e) {
  Te.delete(e);
}
function Rr() {
  const e = /* @__PURE__ */ new Map();
  for (const [n, r] of Te) {
    const o = r[r.length - 1];
    e.set(n, o);
  }
  function t(n) {
    return e.get(n.id).value[n.name];
  }
  return {
    getPropsValue: t
  };
}
function Et(e, t) {
  Object.entries(e).forEach(([n, r]) => t(r, n));
}
function je(e, t) {
  return nn(e, {
    valueFn: t
  });
}
function nn(e, t) {
  const { valueFn: n, keyFn: r } = t;
  return Object.fromEntries(
    Object.entries(e).map(([o, s]) => [
      r ? r(o, s) : o,
      n(s, o)
    ])
  );
}
function rn(e, t, n) {
  if (Array.isArray(t)) {
    const [o, ...s] = t;
    switch (o) {
      case "!":
        return !e;
      case "+":
        return e + s[0];
      case "~+":
        return s[0] + e;
    }
  }
  const r = on(t, n);
  return e[r];
}
function on(e, t) {
  if (typeof e == "string" || typeof e == "number")
    return e;
  if (!Array.isArray(e))
    throw new Error(`Invalid path ${e}`);
  const [n, ...r] = e;
  switch (n) {
    case "bind":
      if (!t)
        throw new Error("No bindable function provided");
      return t(r[0]);
    default:
      throw new Error(`Invalid flag ${n} in array at ${e}`);
  }
}
function _e(e, t, n) {
  return t.reduce(
    (r, o) => rn(r, o, n),
    e
  );
}
function et(e, t, n, r) {
  t.reduce((o, s, i) => {
    if (i === t.length - 1)
      o[on(s, r)] = n;
    else
      return rn(o, s, r);
  }, e);
}
const sn = /* @__PURE__ */ new Map(), ft = we(() => /* @__PURE__ */ new Map()), an = /* @__PURE__ */ new Set(), cn = Symbol("vfor");
function Or(e) {
  const t = un() ?? {};
  Pe(cn, { ...t, [e.fid]: e.key });
}
function un() {
  return ee(cn, void 0);
}
function Sr() {
  const e = un(), t = /* @__PURE__ */ new Map();
  return e === void 0 || Object.keys(e).forEach((n) => {
    t.set(n, e[n]);
  }), t;
}
function Vr(e, t, n, r) {
  if (r) {
    an.add(e);
    return;
  }
  let o;
  if (n)
    o = new $r(t);
  else {
    const s = Array.isArray(t) ? t : Object.entries(t).map(([i, a], l) => [a, i, l]);
    o = new Ar(s);
  }
  sn.set(e, o);
}
function Pr(e, t, n) {
  const r = ft.getOrDefault(e);
  r.has(t) || r.set(t, J(n)), r.get(t).value = n;
}
function kr(e) {
  const t = /* @__PURE__ */ new Set();
  function n(o) {
    t.add(o);
  }
  function r() {
    const o = ft.get(e);
    o !== void 0 && o.forEach((s, i) => {
      t.has(i) || o.delete(i);
    });
  }
  return {
    add: n,
    removeUnusedKeys: r
  };
}
function Nr(e) {
  const t = e, n = Sr();
  function r(o) {
    const s = n.get(o) ?? t;
    return ft.get(o).get(s).value;
  }
  return {
    getVForIndex: r
  };
}
function Ir(e) {
  return sn.get(e.binding.fid).createRefObjectWithPaths(e);
}
function Cr(e) {
  return an.has(e);
}
class Ar {
  constructor(t) {
    this.array = t;
  }
  createRefObjectWithPaths(t) {
    const { binding: n } = t, { snapshot: r } = t, { path: o = [] } = n, s = [...o], i = r.getVForIndex(n.fid);
    return s.unshift(i), ut(() => ({
      get: () => _e(
        this.array,
        s,
        r.getObjectToValue
      ),
      set: () => {
        throw new Error("Cannot set value to a constant array");
      }
    }));
  }
}
class $r {
  constructor(t) {
    F(this, "_isDictSource");
    this.binding = t;
  }
  isDictSource(t) {
    if (this._isDictSource === void 0) {
      const n = H(t);
      this._isDictSource = n !== null && !Array.isArray(n);
    }
    return this._isDictSource;
  }
  createRefObjectWithPaths(t) {
    const { binding: n } = t, { path: r = [] } = n, o = [...r], { snapshot: s } = t, i = s.getVueRefObject(this.binding), a = this.isDictSource(i), l = s.getVForIndex(n.fid), d = a && o.length === 0 ? [0] : [];
    return o.unshift(l, ...d), ut(() => ({
      get: () => {
        const u = H(i), c = a ? Object.entries(u).map(([f, h], v) => [
          h,
          f,
          v
        ]) : u;
        try {
          return _e(
            H(c),
            o,
            s.getObjectToValue
          );
        } catch {
          return;
        }
      },
      set: (u) => {
        const c = H(i);
        if (a) {
          const f = Object.keys(c);
          if (l >= f.length)
            throw new Error("Cannot set value to a non-existent key");
          const h = f[l];
          et(
            c,
            [h],
            u,
            s.getObjectToValue
          );
          return;
        }
        et(
          c,
          o,
          u,
          s.getObjectToValue
        );
      }
    }));
  }
}
function Tr(e, t, n = !1) {
  return n && (e = `$computed(${e})`, t = { ...t, $computed: L }), K(e, t);
}
function _t(e, t, n) {
  const { paths: r, getBindableValueFn: o } = t, { paths: s, getBindableValueFn: i } = t;
  return r === void 0 || r.length === 0 ? e : ut(() => ({
    get() {
      try {
        return _e(
          H(e),
          r,
          o
        );
      } catch {
        return;
      }
    },
    set(a) {
      et(
        H(e),
        s || r,
        a,
        i
      );
    }
  }));
}
function bt(e) {
  return e == null;
}
function jr() {
  return ln().__VUE_DEVTOOLS_GLOBAL_HOOK__;
}
function ln() {
  return typeof navigator < "u" && typeof window < "u" ? window : typeof globalThis < "u" ? globalThis : {};
}
const xr = typeof Proxy == "function", Dr = "devtools-plugin:setup", Mr = "plugin:settings:set";
let ae, tt;
function Fr() {
  var e;
  return ae !== void 0 || (typeof window < "u" && window.performance ? (ae = !0, tt = window.performance) : typeof globalThis < "u" && (!((e = globalThis.perf_hooks) === null || e === void 0) && e.performance) ? (ae = !0, tt = globalThis.perf_hooks.performance) : ae = !1), ae;
}
function Wr() {
  return Fr() ? tt.now() : Date.now();
}
class Br {
  constructor(t, n) {
    this.target = null, this.targetQueue = [], this.onQueue = [], this.plugin = t, this.hook = n;
    const r = {};
    if (t.settings)
      for (const i in t.settings) {
        const a = t.settings[i];
        r[i] = a.defaultValue;
      }
    const o = `__vue-devtools-plugin-settings__${t.id}`;
    let s = Object.assign({}, r);
    try {
      const i = localStorage.getItem(o), a = JSON.parse(i);
      Object.assign(s, a);
    } catch {
    }
    this.fallbacks = {
      getSettings() {
        return s;
      },
      setSettings(i) {
        try {
          localStorage.setItem(o, JSON.stringify(i));
        } catch {
        }
        s = i;
      },
      now() {
        return Wr();
      }
    }, n && n.on(Mr, (i, a) => {
      i === this.plugin.id && this.fallbacks.setSettings(a);
    }), this.proxiedOn = new Proxy({}, {
      get: (i, a) => this.target ? this.target.on[a] : (...l) => {
        this.onQueue.push({
          method: a,
          args: l
        });
      }
    }), this.proxiedTarget = new Proxy({}, {
      get: (i, a) => this.target ? this.target[a] : a === "on" ? this.proxiedOn : Object.keys(this.fallbacks).includes(a) ? (...l) => (this.targetQueue.push({
        method: a,
        args: l,
        resolve: () => {
        }
      }), this.fallbacks[a](...l)) : (...l) => new Promise((d) => {
        this.targetQueue.push({
          method: a,
          args: l,
          resolve: d
        });
      })
    });
  }
  async setRealTarget(t) {
    this.target = t;
    for (const n of this.onQueue)
      this.target.on[n.method](...n.args);
    for (const n of this.targetQueue)
      n.resolve(await this.target[n.method](...n.args));
  }
}
function Lr(e, t) {
  const n = e, r = ln(), o = jr(), s = xr && n.enableEarlyProxy;
  if (o && (r.__VUE_DEVTOOLS_PLUGIN_API_AVAILABLE__ || !s))
    o.emit(Dr, e, t);
  else {
    const i = s ? new Br(n, o) : null;
    (r.__VUE_DEVTOOLS_PLUGINS__ = r.__VUE_DEVTOOLS_PLUGINS__ || []).push({
      pluginDescriptor: n,
      setupFn: t,
      proxy: i
    }), i && t(i.proxiedTarget);
  }
}
var O = {};
const z = typeof document < "u";
function fn(e) {
  return typeof e == "object" || "displayName" in e || "props" in e || "__vccOpts" in e;
}
function Ur(e) {
  return e.__esModule || e[Symbol.toStringTag] === "Module" || // support CF with dynamic imports that do not
  // add the Module string tag
  e.default && fn(e.default);
}
const I = Object.assign;
function Ke(e, t) {
  const n = {};
  for (const r in t) {
    const o = t[r];
    n[r] = U(o) ? o.map(e) : e(o);
  }
  return n;
}
const ve = () => {
}, U = Array.isArray;
function V(e) {
  const t = Array.from(arguments).slice(1);
  console.warn.apply(console, ["[Vue Router warn]: " + e].concat(t));
}
const dn = /#/g, Kr = /&/g, Gr = /\//g, Hr = /=/g, qr = /\?/g, hn = /\+/g, zr = /%5B/g, Jr = /%5D/g, pn = /%5E/g, Qr = /%60/g, mn = /%7B/g, Yr = /%7C/g, gn = /%7D/g, Xr = /%20/g;
function dt(e) {
  return encodeURI("" + e).replace(Yr, "|").replace(zr, "[").replace(Jr, "]");
}
function Zr(e) {
  return dt(e).replace(mn, "{").replace(gn, "}").replace(pn, "^");
}
function nt(e) {
  return dt(e).replace(hn, "%2B").replace(Xr, "+").replace(dn, "%23").replace(Kr, "%26").replace(Qr, "`").replace(mn, "{").replace(gn, "}").replace(pn, "^");
}
function eo(e) {
  return nt(e).replace(Hr, "%3D");
}
function to(e) {
  return dt(e).replace(dn, "%23").replace(qr, "%3F");
}
function no(e) {
  return e == null ? "" : to(e).replace(Gr, "%2F");
}
function ce(e) {
  try {
    return decodeURIComponent("" + e);
  } catch {
    O.NODE_ENV !== "production" && V(`Error decoding "${e}". Using original value`);
  }
  return "" + e;
}
const ro = /\/$/, oo = (e) => e.replace(ro, "");
function Ge(e, t, n = "/") {
  let r, o = {}, s = "", i = "";
  const a = t.indexOf("#");
  let l = t.indexOf("?");
  return a < l && a >= 0 && (l = -1), l > -1 && (r = t.slice(0, l), s = t.slice(l + 1, a > -1 ? a : t.length), o = e(s)), a > -1 && (r = r || t.slice(0, a), i = t.slice(a, t.length)), r = ao(r ?? t, n), {
    fullPath: r + (s && "?") + s + i,
    path: r,
    query: o,
    hash: ce(i)
  };
}
function so(e, t) {
  const n = t.query ? e(t.query) : "";
  return t.path + (n && "?") + n + (t.hash || "");
}
function Rt(e, t) {
  return !t || !e.toLowerCase().startsWith(t.toLowerCase()) ? e : e.slice(t.length) || "/";
}
function Ot(e, t, n) {
  const r = t.matched.length - 1, o = n.matched.length - 1;
  return r > -1 && r === o && te(t.matched[r], n.matched[o]) && vn(t.params, n.params) && e(t.query) === e(n.query) && t.hash === n.hash;
}
function te(e, t) {
  return (e.aliasOf || e) === (t.aliasOf || t);
}
function vn(e, t) {
  if (Object.keys(e).length !== Object.keys(t).length)
    return !1;
  for (const n in e)
    if (!io(e[n], t[n]))
      return !1;
  return !0;
}
function io(e, t) {
  return U(e) ? St(e, t) : U(t) ? St(t, e) : e === t;
}
function St(e, t) {
  return U(t) ? e.length === t.length && e.every((n, r) => n === t[r]) : e.length === 1 && e[0] === t;
}
function ao(e, t) {
  if (e.startsWith("/"))
    return e;
  if (O.NODE_ENV !== "production" && !t.startsWith("/"))
    return V(`Cannot resolve a relative location without an absolute path. Trying to resolve "${e}" from "${t}". It should look like "/${t}".`), e;
  if (!e)
    return t;
  const n = t.split("/"), r = e.split("/"), o = r[r.length - 1];
  (o === ".." || o === ".") && r.push("");
  let s = n.length - 1, i, a;
  for (i = 0; i < r.length; i++)
    if (a = r[i], a !== ".")
      if (a === "..")
        s > 1 && s--;
      else
        break;
  return n.slice(0, s).join("/") + "/" + r.slice(i).join("/");
}
const X = {
  path: "/",
  // TODO: could we use a symbol in the future?
  name: void 0,
  params: {},
  query: {},
  hash: "",
  fullPath: "/",
  matched: [],
  meta: {},
  redirectedFrom: void 0
};
var ue;
(function(e) {
  e.pop = "pop", e.push = "push";
})(ue || (ue = {}));
var se;
(function(e) {
  e.back = "back", e.forward = "forward", e.unknown = "";
})(se || (se = {}));
const He = "";
function yn(e) {
  if (!e)
    if (z) {
      const t = document.querySelector("base");
      e = t && t.getAttribute("href") || "/", e = e.replace(/^\w+:\/\/[^\/]+/, "");
    } else
      e = "/";
  return e[0] !== "/" && e[0] !== "#" && (e = "/" + e), oo(e);
}
const co = /^[^#]+#/;
function wn(e, t) {
  return e.replace(co, "#") + t;
}
function uo(e, t) {
  const n = document.documentElement.getBoundingClientRect(), r = e.getBoundingClientRect();
  return {
    behavior: t.behavior,
    left: r.left - n.left - (t.left || 0),
    top: r.top - n.top - (t.top || 0)
  };
}
const xe = () => ({
  left: window.scrollX,
  top: window.scrollY
});
function lo(e) {
  let t;
  if ("el" in e) {
    const n = e.el, r = typeof n == "string" && n.startsWith("#");
    if (O.NODE_ENV !== "production" && typeof e.el == "string" && (!r || !document.getElementById(e.el.slice(1))))
      try {
        const s = document.querySelector(e.el);
        if (r && s) {
          V(`The selector "${e.el}" should be passed as "el: document.querySelector('${e.el}')" because it starts with "#".`);
          return;
        }
      } catch {
        V(`The selector "${e.el}" is invalid. If you are using an id selector, make sure to escape it. You can find more information about escaping characters in selectors at https://mathiasbynens.be/notes/css-escapes or use CSS.escape (https://developer.mozilla.org/en-US/docs/Web/API/CSS/escape).`);
        return;
      }
    const o = typeof n == "string" ? r ? document.getElementById(n.slice(1)) : document.querySelector(n) : n;
    if (!o) {
      O.NODE_ENV !== "production" && V(`Couldn't find element using selector "${e.el}" returned by scrollBehavior.`);
      return;
    }
    t = uo(o, e);
  } else
    t = e;
  "scrollBehavior" in document.documentElement.style ? window.scrollTo(t) : window.scrollTo(t.left != null ? t.left : window.scrollX, t.top != null ? t.top : window.scrollY);
}
function Vt(e, t) {
  return (history.state ? history.state.position - t : -1) + e;
}
const rt = /* @__PURE__ */ new Map();
function fo(e, t) {
  rt.set(e, t);
}
function ho(e) {
  const t = rt.get(e);
  return rt.delete(e), t;
}
let po = () => location.protocol + "//" + location.host;
function En(e, t) {
  const { pathname: n, search: r, hash: o } = t, s = e.indexOf("#");
  if (s > -1) {
    let a = o.includes(e.slice(s)) ? e.slice(s).length : 1, l = o.slice(a);
    return l[0] !== "/" && (l = "/" + l), Rt(l, "");
  }
  return Rt(n, e) + r + o;
}
function mo(e, t, n, r) {
  let o = [], s = [], i = null;
  const a = ({ state: f }) => {
    const h = En(e, location), v = n.value, p = t.value;
    let g = 0;
    if (f) {
      if (n.value = h, t.value = f, i && i === v) {
        i = null;
        return;
      }
      g = p ? f.position - p.position : 0;
    } else
      r(h);
    o.forEach((w) => {
      w(n.value, v, {
        delta: g,
        type: ue.pop,
        direction: g ? g > 0 ? se.forward : se.back : se.unknown
      });
    });
  };
  function l() {
    i = n.value;
  }
  function d(f) {
    o.push(f);
    const h = () => {
      const v = o.indexOf(f);
      v > -1 && o.splice(v, 1);
    };
    return s.push(h), h;
  }
  function u() {
    const { history: f } = window;
    f.state && f.replaceState(I({}, f.state, { scroll: xe() }), "");
  }
  function c() {
    for (const f of s)
      f();
    s = [], window.removeEventListener("popstate", a), window.removeEventListener("beforeunload", u);
  }
  return window.addEventListener("popstate", a), window.addEventListener("beforeunload", u, {
    passive: !0
  }), {
    pauseListeners: l,
    listen: d,
    destroy: c
  };
}
function Pt(e, t, n, r = !1, o = !1) {
  return {
    back: e,
    current: t,
    forward: n,
    replaced: r,
    position: window.history.length,
    scroll: o ? xe() : null
  };
}
function go(e) {
  const { history: t, location: n } = window, r = {
    value: En(e, n)
  }, o = { value: t.state };
  o.value || s(r.value, {
    back: null,
    current: r.value,
    forward: null,
    // the length is off by one, we need to decrease it
    position: t.length - 1,
    replaced: !0,
    // don't add a scroll as the user may have an anchor, and we want
    // scrollBehavior to be triggered without a saved position
    scroll: null
  }, !0);
  function s(l, d, u) {
    const c = e.indexOf("#"), f = c > -1 ? (n.host && document.querySelector("base") ? e : e.slice(c)) + l : po() + e + l;
    try {
      t[u ? "replaceState" : "pushState"](d, "", f), o.value = d;
    } catch (h) {
      O.NODE_ENV !== "production" ? V("Error with push/replace State", h) : console.error(h), n[u ? "replace" : "assign"](f);
    }
  }
  function i(l, d) {
    const u = I({}, t.state, Pt(
      o.value.back,
      // keep back and forward entries but override current position
      l,
      o.value.forward,
      !0
    ), d, { position: o.value.position });
    s(l, u, !0), r.value = l;
  }
  function a(l, d) {
    const u = I(
      {},
      // use current history state to gracefully handle a wrong call to
      // history.replaceState
      // https://github.com/vuejs/router/issues/366
      o.value,
      t.state,
      {
        forward: l,
        scroll: xe()
      }
    );
    O.NODE_ENV !== "production" && !t.state && V(`history.state seems to have been manually replaced without preserving the necessary values. Make sure to preserve existing history state if you are manually calling history.replaceState:

history.replaceState(history.state, '', url)

You can find more information at https://router.vuejs.org/guide/migration/#Usage-of-history-state`), s(u.current, u, !0);
    const c = I({}, Pt(r.value, l, null), { position: u.position + 1 }, d);
    s(l, c, !1), r.value = l;
  }
  return {
    location: r,
    state: o,
    push: a,
    replace: i
  };
}
function _n(e) {
  e = yn(e);
  const t = go(e), n = mo(e, t.state, t.location, t.replace);
  function r(s, i = !0) {
    i || n.pauseListeners(), history.go(s);
  }
  const o = I({
    // it's overridden right after
    location: "",
    base: e,
    go: r,
    createHref: wn.bind(null, e)
  }, t, n);
  return Object.defineProperty(o, "location", {
    enumerable: !0,
    get: () => t.location.value
  }), Object.defineProperty(o, "state", {
    enumerable: !0,
    get: () => t.state.value
  }), o;
}
function vo(e = "") {
  let t = [], n = [He], r = 0;
  e = yn(e);
  function o(a) {
    r++, r !== n.length && n.splice(r), n.push(a);
  }
  function s(a, l, { direction: d, delta: u }) {
    const c = {
      direction: d,
      delta: u,
      type: ue.pop
    };
    for (const f of t)
      f(a, l, c);
  }
  const i = {
    // rewritten by Object.defineProperty
    location: He,
    // TODO: should be kept in queue
    state: {},
    base: e,
    createHref: wn.bind(null, e),
    replace(a) {
      n.splice(r--, 1), o(a);
    },
    push(a, l) {
      o(a);
    },
    listen(a) {
      return t.push(a), () => {
        const l = t.indexOf(a);
        l > -1 && t.splice(l, 1);
      };
    },
    destroy() {
      t = [], n = [He], r = 0;
    },
    go(a, l = !0) {
      const d = this.location, u = (
        // we are considering delta === 0 going forward, but in abstract mode
        // using 0 for the delta doesn't make sense like it does in html5 where
        // it reloads the page
        a < 0 ? se.back : se.forward
      );
      r = Math.max(0, Math.min(r + a, n.length - 1)), l && s(this.location, d, {
        direction: u,
        delta: a
      });
    }
  };
  return Object.defineProperty(i, "location", {
    enumerable: !0,
    get: () => n[r]
  }), i;
}
function yo(e) {
  return e = location.host ? e || location.pathname + location.search : "", e.includes("#") || (e += "#"), O.NODE_ENV !== "production" && !e.endsWith("#/") && !e.endsWith("#") && V(`A hash base must end with a "#":
"${e}" should be "${e.replace(/#.*$/, "#")}".`), _n(e);
}
function Ie(e) {
  return typeof e == "string" || e && typeof e == "object";
}
function bn(e) {
  return typeof e == "string" || typeof e == "symbol";
}
const ot = Symbol(O.NODE_ENV !== "production" ? "navigation failure" : "");
var kt;
(function(e) {
  e[e.aborted = 4] = "aborted", e[e.cancelled = 8] = "cancelled", e[e.duplicated = 16] = "duplicated";
})(kt || (kt = {}));
const wo = {
  1({ location: e, currentLocation: t }) {
    return `No match for
 ${JSON.stringify(e)}${t ? `
while being at
` + JSON.stringify(t) : ""}`;
  },
  2({ from: e, to: t }) {
    return `Redirected from "${e.fullPath}" to "${_o(t)}" via a navigation guard.`;
  },
  4({ from: e, to: t }) {
    return `Navigation aborted from "${e.fullPath}" to "${t.fullPath}" via a navigation guard.`;
  },
  8({ from: e, to: t }) {
    return `Navigation cancelled from "${e.fullPath}" to "${t.fullPath}" with a new navigation.`;
  },
  16({ from: e, to: t }) {
    return `Avoided redundant navigation to current location: "${e.fullPath}".`;
  }
};
function le(e, t) {
  return O.NODE_ENV !== "production" ? I(new Error(wo[e](t)), {
    type: e,
    [ot]: !0
  }, t) : I(new Error(), {
    type: e,
    [ot]: !0
  }, t);
}
function q(e, t) {
  return e instanceof Error && ot in e && (t == null || !!(e.type & t));
}
const Eo = ["params", "query", "hash"];
function _o(e) {
  if (typeof e == "string")
    return e;
  if (e.path != null)
    return e.path;
  const t = {};
  for (const n of Eo)
    n in e && (t[n] = e[n]);
  return JSON.stringify(t, null, 2);
}
const Nt = "[^/]+?", bo = {
  sensitive: !1,
  strict: !1,
  start: !0,
  end: !0
}, Ro = /[.+*?^${}()[\]/\\]/g;
function Oo(e, t) {
  const n = I({}, bo, t), r = [];
  let o = n.start ? "^" : "";
  const s = [];
  for (const d of e) {
    const u = d.length ? [] : [
      90
      /* PathScore.Root */
    ];
    n.strict && !d.length && (o += "/");
    for (let c = 0; c < d.length; c++) {
      const f = d[c];
      let h = 40 + (n.sensitive ? 0.25 : 0);
      if (f.type === 0)
        c || (o += "/"), o += f.value.replace(Ro, "\\$&"), h += 40;
      else if (f.type === 1) {
        const { value: v, repeatable: p, optional: g, regexp: w } = f;
        s.push({
          name: v,
          repeatable: p,
          optional: g
        });
        const _ = w || Nt;
        if (_ !== Nt) {
          h += 10;
          try {
            new RegExp(`(${_})`);
          } catch (S) {
            throw new Error(`Invalid custom RegExp for param "${v}" (${_}): ` + S.message);
          }
        }
        let b = p ? `((?:${_})(?:/(?:${_}))*)` : `(${_})`;
        c || (b = // avoid an optional / if there are more segments e.g. /:p?-static
        // or /:p?-:p2
        g && d.length < 2 ? `(?:/${b})` : "/" + b), g && (b += "?"), o += b, h += 20, g && (h += -8), p && (h += -20), _ === ".*" && (h += -50);
      }
      u.push(h);
    }
    r.push(u);
  }
  if (n.strict && n.end) {
    const d = r.length - 1;
    r[d][r[d].length - 1] += 0.7000000000000001;
  }
  n.strict || (o += "/?"), n.end ? o += "$" : n.strict && !o.endsWith("/") && (o += "(?:/|$)");
  const i = new RegExp(o, n.sensitive ? "" : "i");
  function a(d) {
    const u = d.match(i), c = {};
    if (!u)
      return null;
    for (let f = 1; f < u.length; f++) {
      const h = u[f] || "", v = s[f - 1];
      c[v.name] = h && v.repeatable ? h.split("/") : h;
    }
    return c;
  }
  function l(d) {
    let u = "", c = !1;
    for (const f of e) {
      (!c || !u.endsWith("/")) && (u += "/"), c = !1;
      for (const h of f)
        if (h.type === 0)
          u += h.value;
        else if (h.type === 1) {
          const { value: v, repeatable: p, optional: g } = h, w = v in d ? d[v] : "";
          if (U(w) && !p)
            throw new Error(`Provided param "${v}" is an array but it is not repeatable (* or + modifiers)`);
          const _ = U(w) ? w.join("/") : w;
          if (!_)
            if (g)
              f.length < 2 && (u.endsWith("/") ? u = u.slice(0, -1) : c = !0);
            else
              throw new Error(`Missing required param "${v}"`);
          u += _;
        }
    }
    return u || "/";
  }
  return {
    re: i,
    score: r,
    keys: s,
    parse: a,
    stringify: l
  };
}
function So(e, t) {
  let n = 0;
  for (; n < e.length && n < t.length; ) {
    const r = t[n] - e[n];
    if (r)
      return r;
    n++;
  }
  return e.length < t.length ? e.length === 1 && e[0] === 80 ? -1 : 1 : e.length > t.length ? t.length === 1 && t[0] === 80 ? 1 : -1 : 0;
}
function Rn(e, t) {
  let n = 0;
  const r = e.score, o = t.score;
  for (; n < r.length && n < o.length; ) {
    const s = So(r[n], o[n]);
    if (s)
      return s;
    n++;
  }
  if (Math.abs(o.length - r.length) === 1) {
    if (It(r))
      return 1;
    if (It(o))
      return -1;
  }
  return o.length - r.length;
}
function It(e) {
  const t = e[e.length - 1];
  return e.length > 0 && t[t.length - 1] < 0;
}
const Vo = {
  type: 0,
  value: ""
}, Po = /[a-zA-Z0-9_]/;
function ko(e) {
  if (!e)
    return [[]];
  if (e === "/")
    return [[Vo]];
  if (!e.startsWith("/"))
    throw new Error(O.NODE_ENV !== "production" ? `Route paths should start with a "/": "${e}" should be "/${e}".` : `Invalid path "${e}"`);
  function t(h) {
    throw new Error(`ERR (${n})/"${d}": ${h}`);
  }
  let n = 0, r = n;
  const o = [];
  let s;
  function i() {
    s && o.push(s), s = [];
  }
  let a = 0, l, d = "", u = "";
  function c() {
    d && (n === 0 ? s.push({
      type: 0,
      value: d
    }) : n === 1 || n === 2 || n === 3 ? (s.length > 1 && (l === "*" || l === "+") && t(`A repeatable param (${d}) must be alone in its segment. eg: '/:ids+.`), s.push({
      type: 1,
      value: d,
      regexp: u,
      repeatable: l === "*" || l === "+",
      optional: l === "*" || l === "?"
    })) : t("Invalid state to consume buffer"), d = "");
  }
  function f() {
    d += l;
  }
  for (; a < e.length; ) {
    if (l = e[a++], l === "\\" && n !== 2) {
      r = n, n = 4;
      continue;
    }
    switch (n) {
      case 0:
        l === "/" ? (d && c(), i()) : l === ":" ? (c(), n = 1) : f();
        break;
      case 4:
        f(), n = r;
        break;
      case 1:
        l === "(" ? n = 2 : Po.test(l) ? f() : (c(), n = 0, l !== "*" && l !== "?" && l !== "+" && a--);
        break;
      case 2:
        l === ")" ? u[u.length - 1] == "\\" ? u = u.slice(0, -1) + l : n = 3 : u += l;
        break;
      case 3:
        c(), n = 0, l !== "*" && l !== "?" && l !== "+" && a--, u = "";
        break;
      default:
        t("Unknown state");
        break;
    }
  }
  return n === 2 && t(`Unfinished custom RegExp for param "${d}"`), c(), i(), o;
}
function No(e, t, n) {
  const r = Oo(ko(e.path), n);
  if (O.NODE_ENV !== "production") {
    const s = /* @__PURE__ */ new Set();
    for (const i of r.keys)
      s.has(i.name) && V(`Found duplicated params with name "${i.name}" for path "${e.path}". Only the last one will be available on "$route.params".`), s.add(i.name);
  }
  const o = I(r, {
    record: e,
    parent: t,
    // these needs to be populated by the parent
    children: [],
    alias: []
  });
  return t && !o.record.aliasOf == !t.record.aliasOf && t.children.push(o), o;
}
function Io(e, t) {
  const n = [], r = /* @__PURE__ */ new Map();
  t = Tt({ strict: !1, end: !0, sensitive: !1 }, t);
  function o(c) {
    return r.get(c);
  }
  function s(c, f, h) {
    const v = !h, p = At(c);
    O.NODE_ENV !== "production" && To(p, f), p.aliasOf = h && h.record;
    const g = Tt(t, c), w = [p];
    if ("alias" in c) {
      const S = typeof c.alias == "string" ? [c.alias] : c.alias;
      for (const D of S)
        w.push(
          // we need to normalize again to ensure the `mods` property
          // being non enumerable
          At(I({}, p, {
            // this allows us to hold a copy of the `components` option
            // so that async components cache is hold on the original record
            components: h ? h.record.components : p.components,
            path: D,
            // we might be the child of an alias
            aliasOf: h ? h.record : p
            // the aliases are always of the same kind as the original since they
            // are defined on the same record
          }))
        );
    }
    let _, b;
    for (const S of w) {
      const { path: D } = S;
      if (f && D[0] !== "/") {
        const x = f.record.path, T = x[x.length - 1] === "/" ? "" : "/";
        S.path = f.record.path + (D && T + D);
      }
      if (O.NODE_ENV !== "production" && S.path === "*")
        throw new Error(`Catch all routes ("*") must now be defined using a param with a custom regexp.
See more at https://router.vuejs.org/guide/migration/#Removed-star-or-catch-all-routes.`);
      if (_ = No(S, f, g), O.NODE_ENV !== "production" && f && D[0] === "/" && xo(_, f), h ? (h.alias.push(_), O.NODE_ENV !== "production" && $o(h, _)) : (b = b || _, b !== _ && b.alias.push(_), v && c.name && !$t(_) && (O.NODE_ENV !== "production" && jo(c, f), i(c.name))), On(_) && l(_), p.children) {
        const x = p.children;
        for (let T = 0; T < x.length; T++)
          s(x[T], _, h && h.children[T]);
      }
      h = h || _;
    }
    return b ? () => {
      i(b);
    } : ve;
  }
  function i(c) {
    if (bn(c)) {
      const f = r.get(c);
      f && (r.delete(c), n.splice(n.indexOf(f), 1), f.children.forEach(i), f.alias.forEach(i));
    } else {
      const f = n.indexOf(c);
      f > -1 && (n.splice(f, 1), c.record.name && r.delete(c.record.name), c.children.forEach(i), c.alias.forEach(i));
    }
  }
  function a() {
    return n;
  }
  function l(c) {
    const f = Do(c, n);
    n.splice(f, 0, c), c.record.name && !$t(c) && r.set(c.record.name, c);
  }
  function d(c, f) {
    let h, v = {}, p, g;
    if ("name" in c && c.name) {
      if (h = r.get(c.name), !h)
        throw le(1, {
          location: c
        });
      if (O.NODE_ENV !== "production") {
        const b = Object.keys(c.params || {}).filter((S) => !h.keys.find((D) => D.name === S));
        b.length && V(`Discarded invalid param(s) "${b.join('", "')}" when navigating. See https://github.com/vuejs/router/blob/main/packages/router/CHANGELOG.md#414-2022-08-22 for more details.`);
      }
      g = h.record.name, v = I(
        // paramsFromLocation is a new object
        Ct(
          f.params,
          // only keep params that exist in the resolved location
          // only keep optional params coming from a parent record
          h.keys.filter((b) => !b.optional).concat(h.parent ? h.parent.keys.filter((b) => b.optional) : []).map((b) => b.name)
        ),
        // discard any existing params in the current location that do not exist here
        // #1497 this ensures better active/exact matching
        c.params && Ct(c.params, h.keys.map((b) => b.name))
      ), p = h.stringify(v);
    } else if (c.path != null)
      p = c.path, O.NODE_ENV !== "production" && !p.startsWith("/") && V(`The Matcher cannot resolve relative paths but received "${p}". Unless you directly called \`matcher.resolve("${p}")\`, this is probably a bug in vue-router. Please open an issue at https://github.com/vuejs/router/issues/new/choose.`), h = n.find((b) => b.re.test(p)), h && (v = h.parse(p), g = h.record.name);
    else {
      if (h = f.name ? r.get(f.name) : n.find((b) => b.re.test(f.path)), !h)
        throw le(1, {
          location: c,
          currentLocation: f
        });
      g = h.record.name, v = I({}, f.params, c.params), p = h.stringify(v);
    }
    const w = [];
    let _ = h;
    for (; _; )
      w.unshift(_.record), _ = _.parent;
    return {
      name: g,
      path: p,
      params: v,
      matched: w,
      meta: Ao(w)
    };
  }
  e.forEach((c) => s(c));
  function u() {
    n.length = 0, r.clear();
  }
  return {
    addRoute: s,
    resolve: d,
    removeRoute: i,
    clearRoutes: u,
    getRoutes: a,
    getRecordMatcher: o
  };
}
function Ct(e, t) {
  const n = {};
  for (const r of t)
    r in e && (n[r] = e[r]);
  return n;
}
function At(e) {
  const t = {
    path: e.path,
    redirect: e.redirect,
    name: e.name,
    meta: e.meta || {},
    aliasOf: e.aliasOf,
    beforeEnter: e.beforeEnter,
    props: Co(e),
    children: e.children || [],
    instances: {},
    leaveGuards: /* @__PURE__ */ new Set(),
    updateGuards: /* @__PURE__ */ new Set(),
    enterCallbacks: {},
    // must be declared afterwards
    // mods: {},
    components: "components" in e ? e.components || null : e.component && { default: e.component }
  };
  return Object.defineProperty(t, "mods", {
    value: {}
  }), t;
}
function Co(e) {
  const t = {}, n = e.props || !1;
  if ("component" in e)
    t.default = n;
  else
    for (const r in e.components)
      t[r] = typeof n == "object" ? n[r] : n;
  return t;
}
function $t(e) {
  for (; e; ) {
    if (e.record.aliasOf)
      return !0;
    e = e.parent;
  }
  return !1;
}
function Ao(e) {
  return e.reduce((t, n) => I(t, n.meta), {});
}
function Tt(e, t) {
  const n = {};
  for (const r in e)
    n[r] = r in t ? t[r] : e[r];
  return n;
}
function st(e, t) {
  return e.name === t.name && e.optional === t.optional && e.repeatable === t.repeatable;
}
function $o(e, t) {
  for (const n of e.keys)
    if (!n.optional && !t.keys.find(st.bind(null, n)))
      return V(`Alias "${t.record.path}" and the original record: "${e.record.path}" must have the exact same param named "${n.name}"`);
  for (const n of t.keys)
    if (!n.optional && !e.keys.find(st.bind(null, n)))
      return V(`Alias "${t.record.path}" and the original record: "${e.record.path}" must have the exact same param named "${n.name}"`);
}
function To(e, t) {
  t && t.record.name && !e.name && !e.path && V(`The route named "${String(t.record.name)}" has a child without a name and an empty path. Using that name won't render the empty path child so you probably want to move the name to the child instead. If this is intentional, add a name to the child route to remove the warning.`);
}
function jo(e, t) {
  for (let n = t; n; n = n.parent)
    if (n.record.name === e.name)
      throw new Error(`A route named "${String(e.name)}" has been added as a ${t === n ? "child" : "descendant"} of a route with the same name. Route names must be unique and a nested route cannot use the same name as an ancestor.`);
}
function xo(e, t) {
  for (const n of t.keys)
    if (!e.keys.find(st.bind(null, n)))
      return V(`Absolute path "${e.record.path}" must have the exact same param named "${n.name}" as its parent "${t.record.path}".`);
}
function Do(e, t) {
  let n = 0, r = t.length;
  for (; n !== r; ) {
    const s = n + r >> 1;
    Rn(e, t[s]) < 0 ? r = s : n = s + 1;
  }
  const o = Mo(e);
  return o && (r = t.lastIndexOf(o, r - 1), O.NODE_ENV !== "production" && r < 0 && V(`Finding ancestor route "${o.record.path}" failed for "${e.record.path}"`)), r;
}
function Mo(e) {
  let t = e;
  for (; t = t.parent; )
    if (On(t) && Rn(e, t) === 0)
      return t;
}
function On({ record: e }) {
  return !!(e.name || e.components && Object.keys(e.components).length || e.redirect);
}
function Fo(e) {
  const t = {};
  if (e === "" || e === "?")
    return t;
  const r = (e[0] === "?" ? e.slice(1) : e).split("&");
  for (let o = 0; o < r.length; ++o) {
    const s = r[o].replace(hn, " "), i = s.indexOf("="), a = ce(i < 0 ? s : s.slice(0, i)), l = i < 0 ? null : ce(s.slice(i + 1));
    if (a in t) {
      let d = t[a];
      U(d) || (d = t[a] = [d]), d.push(l);
    } else
      t[a] = l;
  }
  return t;
}
function jt(e) {
  let t = "";
  for (let n in e) {
    const r = e[n];
    if (n = eo(n), r == null) {
      r !== void 0 && (t += (t.length ? "&" : "") + n);
      continue;
    }
    (U(r) ? r.map((s) => s && nt(s)) : [r && nt(r)]).forEach((s) => {
      s !== void 0 && (t += (t.length ? "&" : "") + n, s != null && (t += "=" + s));
    });
  }
  return t;
}
function Wo(e) {
  const t = {};
  for (const n in e) {
    const r = e[n];
    r !== void 0 && (t[n] = U(r) ? r.map((o) => o == null ? null : "" + o) : r == null ? r : "" + r);
  }
  return t;
}
const Bo = Symbol(O.NODE_ENV !== "production" ? "router view location matched" : ""), xt = Symbol(O.NODE_ENV !== "production" ? "router view depth" : ""), De = Symbol(O.NODE_ENV !== "production" ? "router" : ""), ht = Symbol(O.NODE_ENV !== "production" ? "route location" : ""), it = Symbol(O.NODE_ENV !== "production" ? "router view location" : "");
function pe() {
  let e = [];
  function t(r) {
    return e.push(r), () => {
      const o = e.indexOf(r);
      o > -1 && e.splice(o, 1);
    };
  }
  function n() {
    e = [];
  }
  return {
    add: t,
    list: () => e.slice(),
    reset: n
  };
}
function Z(e, t, n, r, o, s = (i) => i()) {
  const i = r && // name is defined if record is because of the function overload
  (r.enterCallbacks[o] = r.enterCallbacks[o] || []);
  return () => new Promise((a, l) => {
    const d = (f) => {
      f === !1 ? l(le(4, {
        from: n,
        to: t
      })) : f instanceof Error ? l(f) : Ie(f) ? l(le(2, {
        from: t,
        to: f
      })) : (i && // since enterCallbackArray is truthy, both record and name also are
      r.enterCallbacks[o] === i && typeof f == "function" && i.push(f), a());
    }, u = s(() => e.call(r && r.instances[o], t, n, O.NODE_ENV !== "production" ? Lo(d, t, n) : d));
    let c = Promise.resolve(u);
    if (e.length < 3 && (c = c.then(d)), O.NODE_ENV !== "production" && e.length > 2) {
      const f = `The "next" callback was never called inside of ${e.name ? '"' + e.name + '"' : ""}:
${e.toString()}
. If you are returning a value instead of calling "next", make sure to remove the "next" parameter from your function.`;
      if (typeof u == "object" && "then" in u)
        c = c.then((h) => d._called ? h : (V(f), Promise.reject(new Error("Invalid navigation guard"))));
      else if (u !== void 0 && !d._called) {
        V(f), l(new Error("Invalid navigation guard"));
        return;
      }
    }
    c.catch((f) => l(f));
  });
}
function Lo(e, t, n) {
  let r = 0;
  return function() {
    r++ === 1 && V(`The "next" callback was called more than once in one navigation guard when going from "${n.fullPath}" to "${t.fullPath}". It should be called exactly one time in each navigation guard. This will fail in production.`), e._called = !0, r === 1 && e.apply(null, arguments);
  };
}
function qe(e, t, n, r, o = (s) => s()) {
  const s = [];
  for (const i of e) {
    O.NODE_ENV !== "production" && !i.components && !i.children.length && V(`Record with path "${i.path}" is either missing a "component(s)" or "children" property.`);
    for (const a in i.components) {
      let l = i.components[a];
      if (O.NODE_ENV !== "production") {
        if (!l || typeof l != "object" && typeof l != "function")
          throw V(`Component "${a}" in record with path "${i.path}" is not a valid component. Received "${String(l)}".`), new Error("Invalid route component");
        if ("then" in l) {
          V(`Component "${a}" in record with path "${i.path}" is a Promise instead of a function that returns a Promise. Did you write "import('./MyPage.vue')" instead of "() => import('./MyPage.vue')" ? This will break in production if not fixed.`);
          const d = l;
          l = () => d;
        } else l.__asyncLoader && // warn only once per component
        !l.__warnedDefineAsync && (l.__warnedDefineAsync = !0, V(`Component "${a}" in record with path "${i.path}" is defined using "defineAsyncComponent()". Write "() => import('./MyPage.vue')" instead of "defineAsyncComponent(() => import('./MyPage.vue'))".`));
      }
      if (!(t !== "beforeRouteEnter" && !i.instances[a]))
        if (fn(l)) {
          const u = (l.__vccOpts || l)[t];
          u && s.push(Z(u, n, r, i, a, o));
        } else {
          let d = l();
          O.NODE_ENV !== "production" && !("catch" in d) && (V(`Component "${a}" in record with path "${i.path}" is a function that does not return a Promise. If you were passing a functional component, make sure to add a "displayName" to the component. This will break in production if not fixed.`), d = Promise.resolve(d)), s.push(() => d.then((u) => {
            if (!u)
              throw new Error(`Couldn't resolve component "${a}" at "${i.path}"`);
            const c = Ur(u) ? u.default : u;
            i.mods[a] = u, i.components[a] = c;
            const h = (c.__vccOpts || c)[t];
            return h && Z(h, n, r, i, a, o)();
          }));
        }
    }
  }
  return s;
}
function Dt(e) {
  const t = ee(De), n = ee(ht);
  let r = !1, o = null;
  const s = L(() => {
    const u = B(e.to);
    return O.NODE_ENV !== "production" && (!r || u !== o) && (Ie(u) || (r ? V(`Invalid value for prop "to" in useLink()
- to:`, u, `
- previous to:`, o, `
- props:`, e) : V(`Invalid value for prop "to" in useLink()
- to:`, u, `
- props:`, e)), o = u, r = !0), t.resolve(u);
  }), i = L(() => {
    const { matched: u } = s.value, { length: c } = u, f = u[c - 1], h = n.matched;
    if (!f || !h.length)
      return -1;
    const v = h.findIndex(te.bind(null, f));
    if (v > -1)
      return v;
    const p = Mt(u[c - 2]);
    return (
      // we are dealing with nested routes
      c > 1 && // if the parent and matched route have the same path, this link is
      // referring to the empty child. Or we currently are on a different
      // child of the same parent
      Mt(f) === p && // avoid comparing the child with its parent
      h[h.length - 1].path !== p ? h.findIndex(te.bind(null, u[c - 2])) : v
    );
  }), a = L(() => i.value > -1 && qo(n.params, s.value.params)), l = L(() => i.value > -1 && i.value === n.matched.length - 1 && vn(n.params, s.value.params));
  function d(u = {}) {
    if (Ho(u)) {
      const c = t[B(e.replace) ? "replace" : "push"](
        B(e.to)
        // avoid uncaught errors are they are logged anyway
      ).catch(ve);
      return e.viewTransition && typeof document < "u" && "startViewTransition" in document && document.startViewTransition(() => c), c;
    }
    return Promise.resolve();
  }
  if (O.NODE_ENV !== "production" && z) {
    const u = Gt();
    if (u) {
      const c = {
        route: s.value,
        isActive: a.value,
        isExactActive: l.value,
        error: null
      };
      u.__vrl_devtools = u.__vrl_devtools || [], u.__vrl_devtools.push(c), Kt(() => {
        c.route = s.value, c.isActive = a.value, c.isExactActive = l.value, c.error = Ie(B(e.to)) ? null : 'Invalid "to" value';
      }, { flush: "post" });
    }
  }
  return {
    route: s,
    href: L(() => s.value.href),
    isActive: a,
    isExactActive: l,
    navigate: d
  };
}
function Uo(e) {
  return e.length === 1 ? e[0] : e;
}
const Ko = /* @__PURE__ */ W({
  name: "RouterLink",
  compatConfig: { MODE: 3 },
  props: {
    to: {
      type: [String, Object],
      required: !0
    },
    replace: Boolean,
    activeClass: String,
    // inactiveClass: String,
    exactActiveClass: String,
    custom: Boolean,
    ariaCurrentValue: {
      type: String,
      default: "page"
    }
  },
  useLink: Dt,
  setup(e, { slots: t }) {
    const n = Gn(Dt(e)), { options: r } = ee(De), o = L(() => ({
      [Ft(e.activeClass, r.linkActiveClass, "router-link-active")]: n.isActive,
      // [getLinkClass(
      //   props.inactiveClass,
      //   options.linkInactiveClass,
      //   'router-link-inactive'
      // )]: !link.isExactActive,
      [Ft(e.exactActiveClass, r.linkExactActiveClass, "router-link-exact-active")]: n.isExactActive
    }));
    return () => {
      const s = t.default && Uo(t.default(n));
      return e.custom ? s : A("a", {
        "aria-current": n.isExactActive ? e.ariaCurrentValue : null,
        href: n.href,
        // this would override user added attrs but Vue will still add
        // the listener, so we end up triggering both
        onClick: n.navigate,
        class: o.value
      }, s);
    };
  }
}), Go = Ko;
function Ho(e) {
  if (!(e.metaKey || e.altKey || e.ctrlKey || e.shiftKey) && !e.defaultPrevented && !(e.button !== void 0 && e.button !== 0)) {
    if (e.currentTarget && e.currentTarget.getAttribute) {
      const t = e.currentTarget.getAttribute("target");
      if (/\b_blank\b/i.test(t))
        return;
    }
    return e.preventDefault && e.preventDefault(), !0;
  }
}
function qo(e, t) {
  for (const n in t) {
    const r = t[n], o = e[n];
    if (typeof r == "string") {
      if (r !== o)
        return !1;
    } else if (!U(o) || o.length !== r.length || r.some((s, i) => s !== o[i]))
      return !1;
  }
  return !0;
}
function Mt(e) {
  return e ? e.aliasOf ? e.aliasOf.path : e.path : "";
}
const Ft = (e, t, n) => e ?? t ?? n, zo = /* @__PURE__ */ W({
  name: "RouterView",
  // #674 we manually inherit them
  inheritAttrs: !1,
  props: {
    name: {
      type: String,
      default: "default"
    },
    route: Object
  },
  // Better compat for @vue/compat users
  // https://github.com/vuejs/router/issues/1315
  compatConfig: { MODE: 3 },
  setup(e, { attrs: t, slots: n }) {
    O.NODE_ENV !== "production" && Qo();
    const r = ee(it), o = L(() => e.route || r.value), s = ee(xt, 0), i = L(() => {
      let d = B(s);
      const { matched: u } = o.value;
      let c;
      for (; (c = u[d]) && !c.components; )
        d++;
      return d;
    }), a = L(() => o.value.matched[i.value]);
    Pe(xt, L(() => i.value + 1)), Pe(Bo, a), Pe(it, o);
    const l = J();
    return G(() => [l.value, a.value, e.name], ([d, u, c], [f, h, v]) => {
      u && (u.instances[c] = d, h && h !== u && d && d === f && (u.leaveGuards.size || (u.leaveGuards = h.leaveGuards), u.updateGuards.size || (u.updateGuards = h.updateGuards))), d && u && // if there is no instance but to and from are the same this might be
      // the first visit
      (!h || !te(u, h) || !f) && (u.enterCallbacks[c] || []).forEach((p) => p(d));
    }, { flush: "post" }), () => {
      const d = o.value, u = e.name, c = a.value, f = c && c.components[u];
      if (!f)
        return Wt(n.default, { Component: f, route: d });
      const h = c.props[u], v = h ? h === !0 ? d.params : typeof h == "function" ? h(d) : h : null, g = A(f, I({}, v, t, {
        onVnodeUnmounted: (w) => {
          w.component.isUnmounted && (c.instances[u] = null);
        },
        ref: l
      }));
      if (O.NODE_ENV !== "production" && z && g.ref) {
        const w = {
          depth: i.value,
          name: c.name,
          path: c.path,
          meta: c.meta
        };
        (U(g.ref) ? g.ref.map((b) => b.i) : [g.ref.i]).forEach((b) => {
          b.__vrv_devtools = w;
        });
      }
      return (
        // pass the vnode to the slot as a prop.
        // h and <component :is="..."> both accept vnodes
        Wt(n.default, { Component: g, route: d }) || g
      );
    };
  }
});
function Wt(e, t) {
  if (!e)
    return null;
  const n = e(t);
  return n.length === 1 ? n[0] : n;
}
const Jo = zo;
function Qo() {
  const e = Gt(), t = e.parent && e.parent.type.name, n = e.parent && e.parent.subTree && e.parent.subTree.type;
  if (t && (t === "KeepAlive" || t.includes("Transition")) && typeof n == "object" && n.name === "RouterView") {
    const r = t === "KeepAlive" ? "keep-alive" : "transition";
    V(`<router-view> can no longer be used directly inside <transition> or <keep-alive>.
Use slot props instead:

<router-view v-slot="{ Component }">
  <${r}>
    <component :is="Component" />
  </${r}>
</router-view>`);
  }
}
function me(e, t) {
  const n = I({}, e, {
    // remove variables that can contain vue instances
    matched: e.matched.map((r) => as(r, ["instances", "children", "aliasOf"]))
  });
  return {
    _custom: {
      type: null,
      readOnly: !0,
      display: e.fullPath,
      tooltip: t,
      value: n
    }
  };
}
function Ve(e) {
  return {
    _custom: {
      display: e
    }
  };
}
let Yo = 0;
function Xo(e, t, n) {
  if (t.__hasDevtools)
    return;
  t.__hasDevtools = !0;
  const r = Yo++;
  Lr({
    id: "org.vuejs.router" + (r ? "." + r : ""),
    label: "Vue Router",
    packageName: "vue-router",
    homepage: "https://router.vuejs.org",
    logo: "https://router.vuejs.org/logo.png",
    componentStateTypes: ["Routing"],
    app: e
  }, (o) => {
    typeof o.now != "function" && console.warn("[Vue Router]: You seem to be using an outdated version of Vue Devtools. Are you still using the Beta release instead of the stable one? You can find the links at https://devtools.vuejs.org/guide/installation.html."), o.on.inspectComponent((u, c) => {
      u.instanceData && u.instanceData.state.push({
        type: "Routing",
        key: "$route",
        editable: !1,
        value: me(t.currentRoute.value, "Current Route")
      });
    }), o.on.visitComponentTree(({ treeNode: u, componentInstance: c }) => {
      if (c.__vrv_devtools) {
        const f = c.__vrv_devtools;
        u.tags.push({
          label: (f.name ? `${f.name.toString()}: ` : "") + f.path,
          textColor: 0,
          tooltip: "This component is rendered by &lt;router-view&gt;",
          backgroundColor: Sn
        });
      }
      U(c.__vrl_devtools) && (c.__devtoolsApi = o, c.__vrl_devtools.forEach((f) => {
        let h = f.route.path, v = kn, p = "", g = 0;
        f.error ? (h = f.error, v = rs, g = os) : f.isExactActive ? (v = Pn, p = "This is exactly active") : f.isActive && (v = Vn, p = "This link is active"), u.tags.push({
          label: h,
          textColor: g,
          tooltip: p,
          backgroundColor: v
        });
      }));
    }), G(t.currentRoute, () => {
      l(), o.notifyComponentUpdate(), o.sendInspectorTree(a), o.sendInspectorState(a);
    });
    const s = "router:navigations:" + r;
    o.addTimelineLayer({
      id: s,
      label: `Router${r ? " " + r : ""} Navigations`,
      color: 4237508
    }), t.onError((u, c) => {
      o.addTimelineEvent({
        layerId: s,
        event: {
          title: "Error during Navigation",
          subtitle: c.fullPath,
          logType: "error",
          time: o.now(),
          data: { error: u },
          groupId: c.meta.__navigationId
        }
      });
    });
    let i = 0;
    t.beforeEach((u, c) => {
      const f = {
        guard: Ve("beforeEach"),
        from: me(c, "Current Location during this navigation"),
        to: me(u, "Target location")
      };
      Object.defineProperty(u.meta, "__navigationId", {
        value: i++
      }), o.addTimelineEvent({
        layerId: s,
        event: {
          time: o.now(),
          title: "Start of navigation",
          subtitle: u.fullPath,
          data: f,
          groupId: u.meta.__navigationId
        }
      });
    }), t.afterEach((u, c, f) => {
      const h = {
        guard: Ve("afterEach")
      };
      f ? (h.failure = {
        _custom: {
          type: Error,
          readOnly: !0,
          display: f ? f.message : "",
          tooltip: "Navigation Failure",
          value: f
        }
      }, h.status = Ve("❌")) : h.status = Ve("✅"), h.from = me(c, "Current Location during this navigation"), h.to = me(u, "Target location"), o.addTimelineEvent({
        layerId: s,
        event: {
          title: "End of navigation",
          subtitle: u.fullPath,
          time: o.now(),
          data: h,
          logType: f ? "warning" : "default",
          groupId: u.meta.__navigationId
        }
      });
    });
    const a = "router-inspector:" + r;
    o.addInspector({
      id: a,
      label: "Routes" + (r ? " " + r : ""),
      icon: "book",
      treeFilterPlaceholder: "Search routes"
    });
    function l() {
      if (!d)
        return;
      const u = d;
      let c = n.getRoutes().filter((f) => !f.parent || // these routes have a parent with no component which will not appear in the view
      // therefore we still need to include them
      !f.parent.record.components);
      c.forEach(Cn), u.filter && (c = c.filter((f) => (
        // save matches state based on the payload
        at(f, u.filter.toLowerCase())
      ))), c.forEach((f) => In(f, t.currentRoute.value)), u.rootNodes = c.map(Nn);
    }
    let d;
    o.on.getInspectorTree((u) => {
      d = u, u.app === e && u.inspectorId === a && l();
    }), o.on.getInspectorState((u) => {
      if (u.app === e && u.inspectorId === a) {
        const f = n.getRoutes().find((h) => h.record.__vd_id === u.nodeId);
        f && (u.state = {
          options: es(f)
        });
      }
    }), o.sendInspectorTree(a), o.sendInspectorState(a);
  });
}
function Zo(e) {
  return e.optional ? e.repeatable ? "*" : "?" : e.repeatable ? "+" : "";
}
function es(e) {
  const { record: t } = e, n = [
    { editable: !1, key: "path", value: t.path }
  ];
  return t.name != null && n.push({
    editable: !1,
    key: "name",
    value: t.name
  }), n.push({ editable: !1, key: "regexp", value: e.re }), e.keys.length && n.push({
    editable: !1,
    key: "keys",
    value: {
      _custom: {
        type: null,
        readOnly: !0,
        display: e.keys.map((r) => `${r.name}${Zo(r)}`).join(" "),
        tooltip: "Param keys",
        value: e.keys
      }
    }
  }), t.redirect != null && n.push({
    editable: !1,
    key: "redirect",
    value: t.redirect
  }), e.alias.length && n.push({
    editable: !1,
    key: "aliases",
    value: e.alias.map((r) => r.record.path)
  }), Object.keys(e.record.meta).length && n.push({
    editable: !1,
    key: "meta",
    value: e.record.meta
  }), n.push({
    key: "score",
    editable: !1,
    value: {
      _custom: {
        type: null,
        readOnly: !0,
        display: e.score.map((r) => r.join(", ")).join(" | "),
        tooltip: "Score used to sort routes",
        value: e.score
      }
    }
  }), n;
}
const Sn = 15485081, Vn = 2450411, Pn = 8702998, ts = 2282478, kn = 16486972, ns = 6710886, rs = 16704226, os = 12131356;
function Nn(e) {
  const t = [], { record: n } = e;
  n.name != null && t.push({
    label: String(n.name),
    textColor: 0,
    backgroundColor: ts
  }), n.aliasOf && t.push({
    label: "alias",
    textColor: 0,
    backgroundColor: kn
  }), e.__vd_match && t.push({
    label: "matches",
    textColor: 0,
    backgroundColor: Sn
  }), e.__vd_exactActive && t.push({
    label: "exact",
    textColor: 0,
    backgroundColor: Pn
  }), e.__vd_active && t.push({
    label: "active",
    textColor: 0,
    backgroundColor: Vn
  }), n.redirect && t.push({
    label: typeof n.redirect == "string" ? `redirect: ${n.redirect}` : "redirects",
    textColor: 16777215,
    backgroundColor: ns
  });
  let r = n.__vd_id;
  return r == null && (r = String(ss++), n.__vd_id = r), {
    id: r,
    label: n.path,
    tags: t,
    children: e.children.map(Nn)
  };
}
let ss = 0;
const is = /^\/(.*)\/([a-z]*)$/;
function In(e, t) {
  const n = t.matched.length && te(t.matched[t.matched.length - 1], e.record);
  e.__vd_exactActive = e.__vd_active = n, n || (e.__vd_active = t.matched.some((r) => te(r, e.record))), e.children.forEach((r) => In(r, t));
}
function Cn(e) {
  e.__vd_match = !1, e.children.forEach(Cn);
}
function at(e, t) {
  const n = String(e.re).match(is);
  if (e.__vd_match = !1, !n || n.length < 3)
    return !1;
  if (new RegExp(n[1].replace(/\$$/, ""), n[2]).test(t))
    return e.children.forEach((i) => at(i, t)), e.record.path !== "/" || t === "/" ? (e.__vd_match = e.re.test(t), !0) : !1;
  const o = e.record.path.toLowerCase(), s = ce(o);
  return !t.startsWith("/") && (s.includes(t) || o.includes(t)) || s.startsWith(t) || o.startsWith(t) || e.record.name && String(e.record.name).includes(t) ? !0 : e.children.some((i) => at(i, t));
}
function as(e, t) {
  const n = {};
  for (const r in e)
    t.includes(r) || (n[r] = e[r]);
  return n;
}
function cs(e) {
  const t = Io(e.routes, e), n = e.parseQuery || Fo, r = e.stringifyQuery || jt, o = e.history;
  if (O.NODE_ENV !== "production" && !o)
    throw new Error('Provide the "history" option when calling "createRouter()": https://router.vuejs.org/api/interfaces/RouterOptions.html#history');
  const s = pe(), i = pe(), a = pe(), l = Q(X);
  let d = X;
  z && e.scrollBehavior && "scrollRestoration" in history && (history.scrollRestoration = "manual");
  const u = Ke.bind(null, (m) => "" + m), c = Ke.bind(null, no), f = (
    // @ts-expect-error: intentionally avoid the type check
    Ke.bind(null, ce)
  );
  function h(m, E) {
    let y, R;
    return bn(m) ? (y = t.getRecordMatcher(m), O.NODE_ENV !== "production" && !y && V(`Parent route "${String(m)}" not found when adding child route`, E), R = E) : R = m, t.addRoute(R, y);
  }
  function v(m) {
    const E = t.getRecordMatcher(m);
    E ? t.removeRoute(E) : O.NODE_ENV !== "production" && V(`Cannot remove non-existent route "${String(m)}"`);
  }
  function p() {
    return t.getRoutes().map((m) => m.record);
  }
  function g(m) {
    return !!t.getRecordMatcher(m);
  }
  function w(m, E) {
    if (E = I({}, E || l.value), typeof m == "string") {
      const P = Ge(n, m, E.path), $ = t.resolve({ path: P.path }, E), re = o.createHref(P.fullPath);
      return O.NODE_ENV !== "production" && (re.startsWith("//") ? V(`Location "${m}" resolved to "${re}". A resolved location cannot start with multiple slashes.`) : $.matched.length || V(`No match found for location with path "${m}"`)), I(P, $, {
        params: f($.params),
        hash: ce(P.hash),
        redirectedFrom: void 0,
        href: re
      });
    }
    if (O.NODE_ENV !== "production" && !Ie(m))
      return V(`router.resolve() was passed an invalid location. This will fail in production.
- Location:`, m), w({});
    let y;
    if (m.path != null)
      O.NODE_ENV !== "production" && "params" in m && !("name" in m) && // @ts-expect-error: the type is never
      Object.keys(m.params).length && V(`Path "${m.path}" was passed with params but they will be ignored. Use a named route alongside params instead.`), y = I({}, m, {
        path: Ge(n, m.path, E.path).path
      });
    else {
      const P = I({}, m.params);
      for (const $ in P)
        P[$] == null && delete P[$];
      y = I({}, m, {
        params: c(P)
      }), E.params = c(E.params);
    }
    const R = t.resolve(y, E), C = m.hash || "";
    O.NODE_ENV !== "production" && C && !C.startsWith("#") && V(`A \`hash\` should always start with the character "#". Replace "${C}" with "#${C}".`), R.params = u(f(R.params));
    const j = so(r, I({}, m, {
      hash: Zr(C),
      path: R.path
    })), k = o.createHref(j);
    return O.NODE_ENV !== "production" && (k.startsWith("//") ? V(`Location "${m}" resolved to "${k}". A resolved location cannot start with multiple slashes.`) : R.matched.length || V(`No match found for location with path "${m.path != null ? m.path : m}"`)), I({
      fullPath: j,
      // keep the hash encoded so fullPath is effectively path + encodedQuery +
      // hash
      hash: C,
      query: (
        // if the user is using a custom query lib like qs, we might have
        // nested objects, so we keep the query as is, meaning it can contain
        // numbers at `$route.query`, but at the point, the user will have to
        // use their own type anyway.
        // https://github.com/vuejs/router/issues/328#issuecomment-649481567
        r === jt ? Wo(m.query) : m.query || {}
      )
    }, R, {
      redirectedFrom: void 0,
      href: k
    });
  }
  function _(m) {
    return typeof m == "string" ? Ge(n, m, l.value.path) : I({}, m);
  }
  function b(m, E) {
    if (d !== m)
      return le(8, {
        from: E,
        to: m
      });
  }
  function S(m) {
    return T(m);
  }
  function D(m) {
    return S(I(_(m), { replace: !0 }));
  }
  function x(m) {
    const E = m.matched[m.matched.length - 1];
    if (E && E.redirect) {
      const { redirect: y } = E;
      let R = typeof y == "function" ? y(m) : y;
      if (typeof R == "string" && (R = R.includes("?") || R.includes("#") ? R = _(R) : (
        // force empty params
        { path: R }
      ), R.params = {}), O.NODE_ENV !== "production" && R.path == null && !("name" in R))
        throw V(`Invalid redirect found:
${JSON.stringify(R, null, 2)}
 when navigating to "${m.fullPath}". A redirect must contain a name or path. This will break in production.`), new Error("Invalid redirect");
      return I({
        query: m.query,
        hash: m.hash,
        // avoid transferring params if the redirect has a path
        params: R.path != null ? {} : m.params
      }, R);
    }
  }
  function T(m, E) {
    const y = d = w(m), R = l.value, C = m.state, j = m.force, k = m.replace === !0, P = x(y);
    if (P)
      return T(
        I(_(P), {
          state: typeof P == "object" ? I({}, C, P.state) : C,
          force: j,
          replace: k
        }),
        // keep original redirectedFrom if it exists
        E || y
      );
    const $ = y;
    $.redirectedFrom = E;
    let re;
    return !j && Ot(r, R, y) && (re = le(16, { to: $, from: R }), yt(
      R,
      R,
      // this is a push, the only way for it to be triggered from a
      // history.listen is with a redirect, which makes it become a push
      !0,
      // This cannot be the first navigation because the initial location
      // cannot be manually navigated to
      !1
    )), (re ? Promise.resolve(re) : pt($, R)).catch((M) => q(M) ? (
      // navigation redirects still mark the router as ready
      q(
        M,
        2
        /* ErrorTypes.NAVIGATION_GUARD_REDIRECT */
      ) ? M : Be(M)
    ) : (
      // reject any unknown error
      We(M, $, R)
    )).then((M) => {
      if (M) {
        if (q(
          M,
          2
          /* ErrorTypes.NAVIGATION_GUARD_REDIRECT */
        ))
          return O.NODE_ENV !== "production" && // we are redirecting to the same location we were already at
          Ot(r, w(M.to), $) && // and we have done it a couple of times
          E && // @ts-expect-error: added only in dev
          (E._count = E._count ? (
            // @ts-expect-error
            E._count + 1
          ) : 1) > 30 ? (V(`Detected a possibly infinite redirection in a navigation guard when going from "${R.fullPath}" to "${$.fullPath}". Aborting to avoid a Stack Overflow.
 Are you always returning a new location within a navigation guard? That would lead to this error. Only return when redirecting or aborting, that should fix this. This might break in production if not fixed.`), Promise.reject(new Error("Infinite redirect in navigation guard"))) : T(
            // keep options
            I({
              // preserve an existing replacement but allow the redirect to override it
              replace: k
            }, _(M.to), {
              state: typeof M.to == "object" ? I({}, C, M.to.state) : C,
              force: j
            }),
            // preserve the original redirectedFrom if any
            E || $
          );
      } else
        M = gt($, R, !0, k, C);
      return mt($, R, M), M;
    });
  }
  function Dn(m, E) {
    const y = b(m, E);
    return y ? Promise.reject(y) : Promise.resolve();
  }
  function Me(m) {
    const E = Oe.values().next().value;
    return E && typeof E.runWithContext == "function" ? E.runWithContext(m) : m();
  }
  function pt(m, E) {
    let y;
    const [R, C, j] = us(m, E);
    y = qe(R.reverse(), "beforeRouteLeave", m, E);
    for (const P of R)
      P.leaveGuards.forEach(($) => {
        y.push(Z($, m, E));
      });
    const k = Dn.bind(null, m, E);
    return y.push(k), ie(y).then(() => {
      y = [];
      for (const P of s.list())
        y.push(Z(P, m, E));
      return y.push(k), ie(y);
    }).then(() => {
      y = qe(C, "beforeRouteUpdate", m, E);
      for (const P of C)
        P.updateGuards.forEach(($) => {
          y.push(Z($, m, E));
        });
      return y.push(k), ie(y);
    }).then(() => {
      y = [];
      for (const P of j)
        if (P.beforeEnter)
          if (U(P.beforeEnter))
            for (const $ of P.beforeEnter)
              y.push(Z($, m, E));
          else
            y.push(Z(P.beforeEnter, m, E));
      return y.push(k), ie(y);
    }).then(() => (m.matched.forEach((P) => P.enterCallbacks = {}), y = qe(j, "beforeRouteEnter", m, E, Me), y.push(k), ie(y))).then(() => {
      y = [];
      for (const P of i.list())
        y.push(Z(P, m, E));
      return y.push(k), ie(y);
    }).catch((P) => q(
      P,
      8
      /* ErrorTypes.NAVIGATION_CANCELLED */
    ) ? P : Promise.reject(P));
  }
  function mt(m, E, y) {
    a.list().forEach((R) => Me(() => R(m, E, y)));
  }
  function gt(m, E, y, R, C) {
    const j = b(m, E);
    if (j)
      return j;
    const k = E === X, P = z ? history.state : {};
    y && (R || k ? o.replace(m.fullPath, I({
      scroll: k && P && P.scroll
    }, C)) : o.push(m.fullPath, C)), l.value = m, yt(m, E, y, k), Be();
  }
  let fe;
  function Mn() {
    fe || (fe = o.listen((m, E, y) => {
      if (!wt.listening)
        return;
      const R = w(m), C = x(R);
      if (C) {
        T(I(C, { replace: !0, force: !0 }), R).catch(ve);
        return;
      }
      d = R;
      const j = l.value;
      z && fo(Vt(j.fullPath, y.delta), xe()), pt(R, j).catch((k) => q(
        k,
        12
        /* ErrorTypes.NAVIGATION_CANCELLED */
      ) ? k : q(
        k,
        2
        /* ErrorTypes.NAVIGATION_GUARD_REDIRECT */
      ) ? (T(
        I(_(k.to), {
          force: !0
        }),
        R
        // avoid an uncaught rejection, let push call triggerError
      ).then((P) => {
        q(
          P,
          20
          /* ErrorTypes.NAVIGATION_DUPLICATED */
        ) && !y.delta && y.type === ue.pop && o.go(-1, !1);
      }).catch(ve), Promise.reject()) : (y.delta && o.go(-y.delta, !1), We(k, R, j))).then((k) => {
        k = k || gt(
          // after navigation, all matched components are resolved
          R,
          j,
          !1
        ), k && (y.delta && // a new navigation has been triggered, so we do not want to revert, that will change the current history
        // entry while a different route is displayed
        !q(
          k,
          8
          /* ErrorTypes.NAVIGATION_CANCELLED */
        ) ? o.go(-y.delta, !1) : y.type === ue.pop && q(
          k,
          20
          /* ErrorTypes.NAVIGATION_DUPLICATED */
        ) && o.go(-1, !1)), mt(R, j, k);
      }).catch(ve);
    }));
  }
  let Fe = pe(), vt = pe(), Re;
  function We(m, E, y) {
    Be(m);
    const R = vt.list();
    return R.length ? R.forEach((C) => C(m, E, y)) : (O.NODE_ENV !== "production" && V("uncaught error during route navigation:"), console.error(m)), Promise.reject(m);
  }
  function Fn() {
    return Re && l.value !== X ? Promise.resolve() : new Promise((m, E) => {
      Fe.add([m, E]);
    });
  }
  function Be(m) {
    return Re || (Re = !m, Mn(), Fe.list().forEach(([E, y]) => m ? y(m) : E()), Fe.reset()), m;
  }
  function yt(m, E, y, R) {
    const { scrollBehavior: C } = e;
    if (!z || !C)
      return Promise.resolve();
    const j = !y && ho(Vt(m.fullPath, 0)) || (R || !y) && history.state && history.state.scroll || null;
    return ke().then(() => C(m, E, j)).then((k) => k && lo(k)).catch((k) => We(k, m, E));
  }
  const Le = (m) => o.go(m);
  let Ue;
  const Oe = /* @__PURE__ */ new Set(), wt = {
    currentRoute: l,
    listening: !0,
    addRoute: h,
    removeRoute: v,
    clearRoutes: t.clearRoutes,
    hasRoute: g,
    getRoutes: p,
    resolve: w,
    options: e,
    push: S,
    replace: D,
    go: Le,
    back: () => Le(-1),
    forward: () => Le(1),
    beforeEach: s.add,
    beforeResolve: i.add,
    afterEach: a.add,
    onError: vt.add,
    isReady: Fn,
    install(m) {
      const E = this;
      m.component("RouterLink", Go), m.component("RouterView", Jo), m.config.globalProperties.$router = E, Object.defineProperty(m.config.globalProperties, "$route", {
        enumerable: !0,
        get: () => B(l)
      }), z && // used for the initial navigation client side to avoid pushing
      // multiple times when the router is used in multiple apps
      !Ue && l.value === X && (Ue = !0, S(o.location).catch((C) => {
        O.NODE_ENV !== "production" && V("Unexpected error when starting the router:", C);
      }));
      const y = {};
      for (const C in X)
        Object.defineProperty(y, C, {
          get: () => l.value[C],
          enumerable: !0
        });
      m.provide(De, E), m.provide(ht, Kn(y)), m.provide(it, l);
      const R = m.unmount;
      Oe.add(m), m.unmount = function() {
        Oe.delete(m), Oe.size < 1 && (d = X, fe && fe(), fe = null, l.value = X, Ue = !1, Re = !1), R();
      }, O.NODE_ENV !== "production" && z && Xo(m, E, t);
    }
  };
  function ie(m) {
    return m.reduce((E, y) => E.then(() => Me(y)), Promise.resolve());
  }
  return wt;
}
function us(e, t) {
  const n = [], r = [], o = [], s = Math.max(t.matched.length, e.matched.length);
  for (let i = 0; i < s; i++) {
    const a = t.matched[i];
    a && (e.matched.find((d) => te(d, a)) ? r.push(a) : n.push(a));
    const l = e.matched[i];
    l && (t.matched.find((d) => te(d, l)) || o.push(l));
  }
  return [n, r, o];
}
function ls() {
  return ee(De);
}
function fs(e) {
  return ee(ht);
}
function ne(e) {
  let t = Xt(), n = Rr(), r = Nr(e), o = tn(), s = ls(), i = fs();
  function a(p) {
    p.scopeSnapshot && (t = p.scopeSnapshot), p.slotSnapshot && (n = p.slotSnapshot), p.vforSnapshot && (r = p.vforSnapshot), p.elementRefSnapshot && (o = p.elementRefSnapshot), p.routerSnapshot && (s = p.routerSnapshot);
  }
  function l(p) {
    if (N.isVar(p))
      return H(d(p));
    if (N.isVForItem(p))
      return Cr(p.fid) ? r.getVForIndex(p.fid) : H(d(p));
    if (N.isVForIndex(p))
      return r.getVForIndex(p.fid);
    if (N.isJs(p)) {
      const { code: g, bind: w } = p, _ = je(w, (b) => u(b));
      return Tr(g, _)();
    }
    if (N.isSlotProp(p))
      return n.getPropsValue(p);
    if (N.isRouterParams(p))
      return H(d(p));
    throw new Error(`Invalid binding: ${p}`);
  }
  function d(p) {
    if (N.isVar(p)) {
      const g = t.getVueRef(p) || mr(p);
      return _t(g, {
        paths: p.path,
        getBindableValueFn: l
      });
    }
    if (N.isVForItem(p))
      return Ir({
        binding: p,
        snapshot: v
      });
    if (N.isVForIndex(p))
      return () => l(p);
    if (N.isRouterParams(p)) {
      const { prop: g = "params" } = p;
      return _t(() => i[g], {
        paths: p.path,
        getBindableValueFn: l
      });
    }
    throw new Error(`Invalid binding: ${p}`);
  }
  function u(p) {
    if (N.isVar(p) || N.isVForItem(p))
      return d(p);
    if (N.isVForIndex(p))
      return l(p);
    if (N.isJs(p))
      return null;
    if (N.isRouterParams(p))
      return d(p);
    throw new Error(`Invalid binding: ${p}`);
  }
  function c(p) {
    if (N.isVar(p))
      return {
        sid: p.sid,
        id: p.id
      };
    if (N.isVForItem(p))
      return {
        type: "vf",
        fid: p.fid
      };
    if (N.isVForIndex(p))
      return {
        type: "vf-i",
        fid: p.fid,
        value: null
      };
    if (N.isJs(p))
      return null;
  }
  function f(p) {
    var g, w;
    (g = p.vars) == null || g.forEach((_) => {
      d({ type: "ref", ..._ }).value = _.val;
    }), (w = p.ele_refs) == null || w.forEach((_) => {
      o.getRef({
        sid: _.sid,
        id: _.id
      }).value[_.method](..._.args);
    });
  }
  function h(p, g) {
    if (bt(g) || bt(p.values))
      return;
    g = g;
    const w = p.values, _ = p.skips || new Array(g.length).fill(0);
    g.forEach((b, S) => {
      if (_[S] === 1)
        return;
      if (N.isVar(b)) {
        const x = d(b);
        x.value = w[S];
        return;
      }
      if (N.isRouterAction(b)) {
        const x = w[S], T = s[x.fn];
        T(...x.args);
        return;
      }
      if (N.isElementRef(b)) {
        const x = o.getRef(b).value, T = w[S];
        x[T.method](...T.args);
        return;
      }
      if (N.isJsOutput(b)) {
        const x = w[S], T = K(x);
        typeof T == "function" && T();
        return;
      }
      const D = d(b);
      D.value = w[S];
    });
  }
  const v = {
    getVForIndex: r.getVForIndex,
    getObjectToValue: l,
    getVueRefObject: d,
    getVueRefObjectOrValue: u,
    getBindingServerInfo: c,
    updateRefFromServer: f,
    updateEventRefFromServer: h,
    replaceSnapshot: a
  };
  return v;
}
class ds {
  async eventSend(t, n) {
    const { fType: r, hKey: o, key: s } = t, i = Je().webServerInfo, a = s !== void 0 ? { key: s } : {}, l = r === "sync" ? i.event_url : i.event_async_url;
    let d = {};
    const u = await fetch(l, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        bind: n,
        hKey: o,
        ...a,
        page: ye(),
        ...d
      })
    });
    if (!u.ok)
      throw new Error(`HTTP error! status: ${u.status}`);
    return await u.json();
  }
  async watchSend(t) {
    const { outputs: n, fType: r, key: o } = t.watchConfig;
    if (!n)
      return null;
    const s = Je().webServerInfo, i = r === "sync" ? s.watch_url : s.watch_async_url, a = t.getServerInputs(), l = {
      key: o,
      input: a,
      page: ye()
    };
    return await (await fetch(i, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(l)
    })).json();
  }
}
class hs {
  async eventSend(t, n) {
    const { fType: r, hKey: o, key: s } = t, i = s !== void 0 ? { key: s } : {};
    let a = {};
    const l = {
      bind: n,
      fType: r,
      hKey: o,
      ...i,
      page: ye(),
      ...a
    };
    return await window.pywebview.api.event_call(l);
  }
  async watchSend(t) {
    const { outputs: n, fType: r, key: o } = t.watchConfig;
    if (!n)
      return null;
    const s = t.getServerInputs(), i = {
      key: o,
      input: s,
      fType: r,
      page: ye()
    };
    return await window.pywebview.api.watch_call(i);
  }
}
let ct;
function ps(e) {
  switch (e.mode) {
    case "web":
      ct = new ds();
      break;
    case "webview":
      ct = new hs();
      break;
  }
}
function An() {
  return ct;
}
function ms(e, t, n) {
  return new gs(e, t, n);
}
class gs {
  constructor(t, n, r) {
    F(this, "taskQueue", []);
    F(this, "id2TaskMap", /* @__PURE__ */ new Map());
    F(this, "input2TaskIdMap", we(() => []));
    this.snapshots = r;
    const o = [], s = (i) => {
      var l;
      const a = new vs(i, r);
      return this.id2TaskMap.set(a.id, a), (l = i.inputs) == null || l.forEach((d) => {
        const u = `${d.sid}-${d.id}`;
        this.input2TaskIdMap.getOrDefault(u).push(a.id);
      }), a;
    };
    t == null || t.forEach((i) => {
      const a = s(i);
      o.push(a);
    }), n == null || n.forEach((i) => {
      const a = {
        type: "ref",
        sid: i.sid,
        id: i.id
      }, l = {
        ...i,
        immediate: !0,
        outputs: [a, ...i.outputs || []]
      }, d = s(l);
      o.push(d);
    }), o.forEach((i) => {
      const {
        deep: a = !0,
        once: l,
        flush: d,
        immediate: u = !0
      } = i.watchConfig, c = {
        immediate: u,
        deep: a,
        once: l,
        flush: d
      }, f = this._getWatchTargets(i);
      G(
        f,
        ([h]) => {
          i.modify = !0, this.taskQueue.push(new ys(i)), this._scheduleNextTick();
        },
        c
      );
    });
  }
  _getWatchTargets(t) {
    if (!t.watchConfig.inputs)
      return [];
    const n = t.slientInputs;
    return t.watchConfig.inputs.filter(
      (o, s) => (N.isVar(o) || N.isVForItem(o) || N.isRouterParams(o)) && !n[s]
    ).map((o) => this.snapshots.getVueRefObjectOrValue(o));
  }
  _scheduleNextTick() {
    ke(() => this._runAllTasks());
  }
  _runAllTasks() {
    const t = this.taskQueue.slice();
    this.taskQueue.length = 0, this._setTaskNodeRelations(t), t.forEach((n) => {
      n.run();
    });
  }
  _setTaskNodeRelations(t) {
    t.forEach((n) => {
      const r = this._findNextNodes(n, t);
      n.appendNextNodes(...r), r.forEach((o) => {
        o.appendPrevNodes(n);
      });
    });
  }
  _findNextNodes(t, n) {
    const r = t.watchTask.watchConfig.outputs;
    if (r && r.length <= 0)
      return [];
    const o = this._getCalculatorTasksByOutput(
      t.watchTask.watchConfig.outputs
    );
    return n.filter(
      (s) => o.has(s.watchTask.id) && s.watchTask.id !== t.watchTask.id
    );
  }
  _getCalculatorTasksByOutput(t) {
    const n = /* @__PURE__ */ new Set();
    return t == null || t.forEach((r) => {
      const o = `${r.sid}-${r.id}`;
      (this.input2TaskIdMap.get(o) || []).forEach((i) => n.add(i));
    }), n;
  }
}
class vs {
  constructor(t, n) {
    F(this, "modify", !0);
    F(this, "_running", !1);
    F(this, "id");
    F(this, "_runningPromise", null);
    F(this, "_runningPromiseResolve", null);
    F(this, "_inputInfos");
    this.watchConfig = t, this.snapshot = n, this.id = Symbol(t.debug), this._inputInfos = this.createInputInfos();
  }
  createInputInfos() {
    const { inputs: t = [] } = this.watchConfig, n = this.watchConfig.data || new Array(t.length).fill(0), r = this.watchConfig.slient || new Array(t.length).fill(0);
    return {
      const_data: n,
      slients: r
    };
  }
  get slientInputs() {
    return this._inputInfos.slients;
  }
  getServerInputs() {
    const { const_data: t } = this._inputInfos;
    return this.watchConfig.inputs ? this.watchConfig.inputs.map((n, r) => t[r] === 0 ? this.snapshot.getObjectToValue(n) : n) : [];
  }
  get running() {
    return this._running;
  }
  get runningPromise() {
    return this._runningPromise;
  }
  /**
   * setRunning
   */
  setRunning() {
    this._running = !0, this._runningPromise = new Promise((t) => {
      this._runningPromiseResolve = t;
    }), this._trySetRunningRef(!0);
  }
  /**
   * taskDone
   */
  taskDone() {
    this._running = !1, this._runningPromiseResolve && (this._runningPromiseResolve(), this._runningPromiseResolve = null), this._trySetRunningRef(!1);
  }
  _trySetRunningRef(t) {
    if (this.watchConfig.running) {
      const n = this.snapshot.getVueRefObject(
        this.watchConfig.running
      );
      n.value = t;
    }
  }
}
class ys {
  /**
   *
   */
  constructor(t) {
    F(this, "prevNodes", []);
    F(this, "nextNodes", []);
    F(this, "_runningPrev", !1);
    this.watchTask = t;
  }
  /**
   * appendPrevNodes
   */
  appendPrevNodes(...t) {
    this.prevNodes.push(...t);
  }
  /**
   *
   */
  appendNextNodes(...t) {
    this.nextNodes.push(...t);
  }
  /**
   * hasNextNodes
   */
  hasNextNodes() {
    return this.nextNodes.length > 0;
  }
  /**
   * run
   */
  async run() {
    if (this.prevNodes.length > 0 && !this._runningPrev)
      try {
        this._runningPrev = !0, await Promise.all(this.prevNodes.map((t) => t.run()));
      } finally {
        this._runningPrev = !1;
      }
    if (this.watchTask.running) {
      await this.watchTask.runningPromise;
      return;
    }
    if (this.watchTask.modify) {
      this.watchTask.modify = !1, this.watchTask.setRunning();
      try {
        await ws(this.watchTask);
      } finally {
        this.watchTask.taskDone();
      }
    }
  }
}
async function ws(e) {
  const { snapshot: t } = e, { outputs: n } = e.watchConfig, r = await An().watchSend(e);
  r && t.updateEventRefFromServer(r, n);
}
class Es {
  constructor(t) {
    F(this, "varMap", /* @__PURE__ */ new Map());
  }
  /**
   * collectVar
   */
  collectVar(t) {
    this.varMap.set(`${t.sid}-${t.id}`, t);
  }
  /**
   * get
   */
  getRef(t) {
    return this.varMap.get(`${t.sid}-${t.id}`);
  }
  /**
   * get
   */
  getWebComputed(t) {
    return this.varMap.get(`${t.sid}-${t.id}`);
  }
  getJsComputed(t) {
    return this.varMap.get(`${t.sid}-${t.id}`);
  }
}
let $n;
function _s(e) {
  $n = new Es(e);
}
function bs() {
  return $n;
}
function Rs(e, t) {
  const { on: n, code: r, immediate: o, deep: s, once: i, flush: a, bind: l = {} } = e, d = je(
    l,
    (f) => t.getVueRefObject(f)
  ), u = K(r, d), c = Array.isArray(n) ? n.map((f) => t.getVueRefObject(f)) : t.getVueRefObject(n);
  return G(c, u, { immediate: o, deep: s, once: i, flush: a });
}
function Os(e, t) {
  const {
    inputs: n = [],
    outputs: r = [],
    slient: o,
    data: s,
    code: i,
    immediate: a = !0,
    deep: l,
    once: d,
    flush: u
  } = e, c = o || new Array(n.length).fill(0), f = s || new Array(n.length).fill(0), h = K(i), v = n.filter((w, _) => c[_] === 0 && f[_] === 0).map((w) => t.getVueRefObject(w)), p = r.length > 1;
  function g() {
    return n.map((w, _) => f[_] === 0 ? Ht(H(t.getVueRefObject(w))) : w);
  }
  G(
    v,
    () => {
      let w = h(...g());
      r.length !== 0 && (p || (w = [w]), r.forEach((_, b) => {
        const S = w[b];
        t.getVueRefObject(_).value = S;
      }));
    },
    { immediate: a, deep: l, once: d, flush: u }
  );
}
function Ss(e, t) {
  return Object.assign(
    {},
    ...Object.entries(e ?? {}).map(([n, r]) => {
      const o = r.map((a) => {
        if (Qe.isWebEventHandler(a)) {
          const l = Vs(a.bind, t);
          return Ps(a, l, t);
        } else
          return ks(a, t);
      }), i = K(
        " (...args)=> Promise.all(promises(...args))",
        {
          promises: (...a) => o.map(async (l) => {
            await l(...a);
          })
        }
      );
      return { [n]: i };
    })
  );
}
function Vs(e, t) {
  return (...n) => (e ?? []).map((r) => {
    if (N.isEventContext(r)) {
      if (r.path.startsWith(":")) {
        const o = r.path.slice(1);
        return K(o)(...n);
      }
      return _e(n[0], r.path.split("."));
    }
    return N.IsBinding(r) ? t.getObjectToValue(r) : r;
  });
}
function Ps(e, t, n) {
  async function r(...o) {
    const s = t(...o), i = await An().eventSend(e, s);
    i && n.updateEventRefFromServer(i, e.set);
  }
  return r;
}
function ks(e, t) {
  const { code: n, inputs: r = [], set: o } = e, s = K(n);
  function i(...a) {
    const l = (r ?? []).map((u) => {
      if (N.isEventContext(u)) {
        if (u.path.startsWith(":")) {
          const c = u.path.slice(1);
          return K(c)(...a);
        }
        return _e(a[0], u.path.split("."));
      }
      if (N.IsBinding(u)) {
        const c = Ht(t.getObjectToValue(u));
        return Ns(c);
      }
      return u;
    }), d = s(...l);
    if (o !== void 0) {
      const c = o.length === 1 ? [d] : d, f = c.map((h) => h === void 0 ? 1 : 0);
      t.updateEventRefFromServer({ values: c, skips: f }, o);
    }
  }
  return i;
}
function Ns(e) {
  return e == null ? e : Array.isArray(e) ? [...e] : typeof e == "object" ? { ...e } : e;
}
function Is(e, t) {
  const n = [];
  (e.bStyle || []).forEach((s) => {
    Array.isArray(s) ? n.push(
      ...s.map((i) => t.getObjectToValue(i))
    ) : n.push(
      je(
        s,
        (i) => t.getObjectToValue(i)
      )
    );
  });
  const r = Hn([e.style || {}, n]);
  return {
    hasStyle: r && Object.keys(r).length > 0,
    styles: r
  };
}
function Cs(e, t) {
  const n = e.classes;
  if (!n)
    return null;
  if (typeof n == "string")
    return ze(n);
  const { str: r, map: o, bind: s } = n, i = [];
  return r && i.push(r), o && i.push(
    je(
      o,
      (a) => t.getObjectToValue(a)
    )
  ), s && i.push(...s.map((a) => t.getObjectToValue(a))), ze(i);
}
function As(e, t) {
  var r;
  const n = {};
  return Et(e.bProps || {}, (o, s) => {
    n[s] = $s(t.getObjectToValue(o), s);
  }), (r = e.proxyProps) == null || r.forEach((o) => {
    const s = t.getObjectToValue(o);
    typeof s == "object" && Et(s, (i, a) => {
      n[a] = i;
    });
  }), { ...e.props || {}, ...n };
}
function $s(e, t) {
  return t === "innerText" ? qt(e) : e;
}
function Ts(e, { slots: t }) {
  const { id: n, use: r } = e.propsInfo, o = Er(n);
  return Ae(() => {
    br(n);
  }), () => {
    const s = e.propsValue;
    return _r(
      n,
      o,
      Object.fromEntries(
        r.map((i) => [i, s[i]])
      )
    ), A($e, null, t.default());
  };
}
const js = W(Ts, {
  props: ["propsInfo", "propsValue"]
});
function xs(e, t) {
  if (!e.slots)
    return null;
  const n = e.slots ?? {};
  return Array.isArray(n) ? t ? ge(n) : () => ge(n) : nn(n, { keyFn: (i) => i === ":" ? "default" : i, valueFn: (i) => {
    const { items: a } = i;
    return (l) => {
      if (i.scope) {
        const d = () => i.props ? Bt(i.props, l, a) : ge(a);
        return A(be, { scope: i.scope }, d);
      }
      return i.props ? Bt(i.props, l, a) : ge(a);
    };
  } });
}
function Bt(e, t, n) {
  return A(
    js,
    { propsInfo: e, propsValue: t },
    () => ge(n)
  );
}
function ge(e) {
  const t = (e ?? []).map((n) => A(Y, {
    component: n
  }));
  return t.length <= 0 ? null : t;
}
function Ds(e, t) {
  const n = {}, r = [];
  return (e || []).forEach((o) => {
    const { sys: s, name: i, arg: a, value: l, mf: d } = o;
    if (i === "vmodel") {
      const u = t.getVueRefObject(l);
      if (n[`onUpdate:${a}`] = (c) => {
        u.value = c;
      }, s === 1) {
        const c = d ? Object.fromEntries(d.map((f) => [f, !0])) : {};
        r.push([qn, u.value, void 0, c]);
      } else
        n[a] = u.value;
    } else if (i === "vshow") {
      const u = t.getVueRefObject(l);
      r.push([zn, u.value]);
    } else
      console.warn(`Directive ${i} is not supported yet`);
  }), {
    newProps: n,
    directiveArray: r
  };
}
function Ms(e, t) {
  const { eRef: n } = e;
  return n === void 0 ? {} : { ref: t.getRef(n) };
}
function Fs(e) {
  const t = ne(), n = tn();
  return () => {
    const { tag: r } = e.component, o = N.IsBinding(r) ? t.getObjectToValue(r) : r, s = lt(o), i = typeof s == "string", a = Cs(e.component, t), { styles: l, hasStyle: d } = Is(e.component, t), u = Ss(e.component.events ?? {}, t), c = xs(e.component, i), f = As(e.component, t), { newProps: h, directiveArray: v } = Ds(
      e.component.dir,
      t
    ), p = Ms(
      e.component,
      n
    ), g = Jn({
      ...f,
      ...u,
      ...h,
      ...p
    }) || {};
    d && (g.style = l), a && (g.class = a);
    const w = A(s, { ...g }, c);
    return v.length > 0 ? Qn(
      // @ts-ignore
      w,
      v
    ) : w;
  };
}
const Y = W(Fs, {
  props: ["component"]
});
function Tn(e, t) {
  var n, r;
  if (e) {
    e.vars && e.vars.forEach((i) => {
      bs().collectVar(i);
    });
    const o = Yt(e, ne(t)), s = ne(t);
    ms(e.py_watch, e.web_computed, s), (n = e.vue_watch) == null || n.forEach((i) => Rs(i, s)), (r = e.js_watch) == null || r.forEach((i) => Os(i, s)), e.eRefs && e.eRefs.forEach((i) => {
      yr(i);
    }), Ae(() => {
      en(e.id, o), wr(e.id);
    });
  }
}
function Ws(e, { slots: t }) {
  const { scope: n } = e;
  return Tn(n), () => A($e, null, t.default());
}
const be = W(Ws, {
  props: ["scope"]
}), Bs = W(
  (e) => {
    const { scope: t, items: n, vforInfo: r } = e;
    return Or(r), Tn(t, r.key), n.length === 1 ? () => A(Y, {
      component: n[0]
    }) : () => n.map(
      (s) => A(Y, {
        component: s
      })
    );
  },
  {
    props: ["scope", "items", "vforInfo"]
  }
);
function Ls(e, t) {
  const { state: n, isReady: r, isLoading: o } = cr(async () => {
    let s = e;
    const i = t;
    if (!s && !i)
      throw new Error("Either config or configUrl must be provided");
    if (!s && i && (s = await (await fetch(i)).json()), !s)
      throw new Error("Failed to load config");
    return s;
  }, {});
  return { config: n, isReady: r, isLoading: o };
}
function Us(e, t) {
  let n;
  return t.component ? n = `Error captured from component:tag: ${t.component.tag} ; id: ${t.component.id} ` : n = "Error captured from app init", console.group(n), console.error("Component:", t.component), console.error("Error:", e), console.groupEnd(), !1;
}
const Ks = { class: "app-box" }, Gs = {
  key: 0,
  style: { position: "absolute", top: "50%", left: "50%", transform: "translate(-50%, -50%)" }
}, Hs = /* @__PURE__ */ W({
  __name: "App",
  props: {
    config: {},
    configUrl: {}
  },
  setup(e) {
    const t = e, { config: n, isLoading: r } = Ls(
      t.config,
      t.configUrl
    );
    let o = null;
    return G(n, (s) => {
      o = s, s.url && (or({
        mode: s.mode,
        version: s.version,
        queryPath: s.url.path,
        pathParams: s.url.params,
        webServerInfo: s.webInfo
      }), ps(s)), _s(s);
    }), Yn(Us), (s, i) => (de(), Se("div", Ks, [
      B(r) ? (de(), Se("div", Gs, i[0] || (i[0] = [
        Xn("p", { style: { margin: "auto" } }, "Loading ...", -1)
      ]))) : (de(), Se("div", {
        key: 1,
        class: ze(["insta-main", B(n).class])
      }, [
        Zn(B(be), {
          scope: B(o).scope
        }, {
          default: er(() => [
            (de(!0), Se($e, null, tr(B(o).items, (a) => (de(), nr(B(Y), { component: a }, null, 8, ["component"]))), 256))
          ]),
          _: 1
        }, 8, ["scope"])
      ], 2))
    ]));
  }
});
function qs(e) {
  const { on: t, scope: n, items: r } = e, o = ne();
  return () => {
    const s = o.getObjectToValue(t);
    return A(be, { scope: n }, () => s ? r.map(
      (a) => A(Y, { component: a })
    ) : void 0);
  };
}
const zs = W(qs, {
  props: ["on", "scope", "items"]
});
function Js(e) {
  const { start: t = 0, end: n, step: r = 1 } = e;
  let o = [];
  if (r > 0)
    for (let s = t; s < n; s += r)
      o.push(s);
  else
    for (let s = t; s > n; s += r)
      o.push(s);
  return o;
}
function Qs(e) {
  const { array: t, bArray: n, items: r, fkey: o, fid: s, scope: i, num: a, tsGroup: l = {} } = e, d = t === void 0, u = a !== void 0, c = d ? n : t, f = ne();
  Vr(s, c, d, u);
  const v = ti(o ?? "index");
  return Ae(() => {
    gr(i.id);
  }), () => {
    const p = Xs(
      u,
      d,
      c,
      f,
      a
    ), g = kr(s), w = p.map((_, b) => {
      const S = v(_, b);
      return g.add(S), Pr(s, S, b), A(Bs, {
        scope: e.scope,
        items: r,
        vforInfo: {
          fid: s,
          key: S
        },
        key: S
      });
    });
    return g.removeUnusedKeys(), l && Object.keys(l).length > 0 ? A(zt, l, {
      default: () => w
    }) : w;
  };
}
const Ys = W(Qs, {
  props: ["array", "items", "fid", "bArray", "scope", "num", "fkey", "tsGroup"]
});
function Xs(e, t, n, r, o) {
  if (e) {
    let i = 0;
    return typeof o == "number" ? i = o : i = r.getObjectToValue(o) ?? 0, Js({
      end: Math.max(0, i)
    });
  }
  const s = t ? r.getObjectToValue(n) || [] : n;
  return typeof s == "object" ? Object.values(s) : s;
}
const Zs = (e) => e, ei = (e, t) => t;
function ti(e) {
  const t = ur(e);
  return typeof t == "function" ? t : e === "item" ? Zs : ei;
}
function ni(e) {
  return e.map((n) => {
    if (n.tag)
      return A(Y, { component: n });
    const r = lt(jn);
    return A(r, {
      scope: n
    });
  });
}
const jn = W(
  (e) => {
    const t = e.scope;
    return () => ni(t.items ?? []);
  },
  {
    props: ["scope"]
  }
);
function ri(e) {
  return e.map((t) => {
    if (t.tag)
      return A(Y, { component: t });
    const n = lt(jn);
    return A(n, {
      scope: t
    });
  });
}
const oi = W(
  (e) => {
    const { scope: t, on: n, items: r } = e, o = Q(r), s = Yt(t), i = ne();
    return Ce.createDynamicWatchRefresh(n, i, async () => {
      const { items: a, on: l } = await Ce.fetchRemote(e, i);
      return o.value = a, l;
    }), Ae(() => {
      en(t.id, s);
    }), () => ri(o.value);
  },
  {
    props: ["sid", "url", "hKey", "on", "bind", "items", "scope"]
  }
);
var Ce;
((e) => {
  function t(r, o, s) {
    let i = null, a = r, l = a.map((u) => o.getVueRefObject(u));
    function d() {
      i && i(), i = G(
        l,
        async () => {
          a = await s(), l = a.map((u) => o.getVueRefObject(u)), d();
        },
        { deep: !0 }
      );
    }
    return d(), () => {
      i && i();
    };
  }
  e.createDynamicWatchRefresh = t;
  async function n(r, o) {
    const s = Object.values(r.bind).map((u) => ({
      sid: u.sid,
      id: u.id,
      value: o.getObjectToValue(u)
    })), i = {
      sid: r.sid,
      bind: s,
      hKey: r.hKey,
      page: ye()
    }, a = {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(i)
    }, l = await fetch(r.url, a);
    if (!l.ok)
      throw new Error("Failed to fetch data");
    return await l.json();
  }
  e.fetchRemote = n;
})(Ce || (Ce = {}));
function si(e) {
  const { scope: t, items: n } = e;
  return () => {
    const r = n.map((o) => A(Y, { component: o }));
    return A(be, { scope: t }, () => r);
  };
}
const Lt = W(si, {
  props: ["scope", "items"]
});
function ii(e) {
  const { on: t, case: n, default: r } = e, o = ne();
  return () => {
    const s = o.getObjectToValue(t), i = n.map((a) => {
      const { value: l, items: d, scope: u } = a.props;
      if (s === l)
        return A(Lt, {
          scope: u,
          items: d,
          key: ["case", l].join("-")
        });
    }).filter((a) => a);
    if (r && !i.length) {
      const { items: a, scope: l } = r.props;
      i.push(A(Lt, { scope: l, items: a, key: "default" }));
    }
    return A($e, i);
  };
}
const ai = W(ii, {
  props: ["case", "on", "default"]
});
function ci(e, { slots: t }) {
  const { name: n = "fade", tag: r } = e;
  return () => A(
    zt,
    { name: n, tag: r },
    {
      default: t.default
    }
  );
}
const ui = W(ci, {
  props: ["name", "tag"]
});
function li(e) {
  const { content: t, r: n = 0 } = e, r = ne(), o = n === 1 ? () => r.getObjectToValue(t) : () => t;
  return () => qt(o());
}
const fi = W(li, {
  props: ["content", "r"]
});
function di(e) {
  if (!e.router)
    throw new Error("Router config is not provided.");
  const { routes: t, kAlive: n = !1 } = e.router;
  return t.map(
    (o) => xn(o, n)
  );
}
function xn(e, t) {
  var l;
  const { server: n = !1, vueItem: r, scope: o } = e, s = () => {
    if (n)
      throw new Error("Server-side rendering is not supported yet.");
    return Promise.resolve(hi(r, o, t));
  }, i = (l = r.children) == null ? void 0 : l.map(
    (d) => xn(d, t)
  ), a = {
    ...r,
    children: i,
    component: s
  };
  return r.component.length === 0 && delete a.component, i === void 0 && delete a.children, a;
}
function hi(e, t, n) {
  const { path: r, component: o } = e, s = A(
    be,
    { scope: t, key: r },
    () => o.map((a) => A(Y, { component: a }))
  );
  return n ? A(rr, null, () => s) : s;
}
function pi(e, t) {
  const { mode: n = "hash" } = t.router, r = n === "hash" ? yo() : n === "memory" ? vo() : _n();
  e.use(
    cs({
      history: r,
      routes: di(t)
    })
  );
}
function vi(e, t) {
  e.component("insta-ui", Hs), e.component("vif", zs), e.component("vfor", Ys), e.component("match", ai), e.component("refresh", oi), e.component("ts-group", ui), e.component("content", fi), t.router && pi(e, t);
}
export {
  vi as default
};
//# sourceMappingURL=insta-ui.js.map
