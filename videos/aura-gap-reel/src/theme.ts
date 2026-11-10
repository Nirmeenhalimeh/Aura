import {Easing} from 'remotion';
import timeline from './timeline.json';

export const TL = timeline;
export const FPS = TL.fps;
export const W = 1080;
export const H = 1920;
export const SAFE = 90; // side margin for all text
export const TEXT_BOTTOM = H - 300; // Reels UI zone starts below this

export const A = {
  bg: '#0E0F13',
  text: '#F4F1EA',
  textDim: 'rgba(244,241,234,0.62)',
  textFaint: 'rgba(244,241,234,0.10)',
  textLine: 'rgba(244,241,234,0.18)',
  accent: '#C9A46A',
  alert: '#D9534F',
  black: '#000000',
};

export const AF = {
  ar: '"IBM Plex Sans Arabic", system-ui, sans-serif',
  en: '"Inter Variable", Inter, system-ui, sans-serif',
};

/**
 * "Aura Expo": the single easing family for the whole piece.
 * out = arrivals, in = exits, inOut = moves between two states.
 */
export const expoOut = Easing.bezier(0.16, 1, 0.3, 1);
export const expoIn = Easing.bezier(0.7, 0, 0.84, 0);
export const expoInOut = Easing.bezier(0.87, 0, 0.13, 1);

export const clamp01 = (x: number) => Math.min(1, Math.max(0, x));
export const lerp = (a: number, b: number, k: number) => a + (b - a) * k;
export const prog = (t: number, t0: number, t1: number, ease: (x: number) => number = expoInOut) =>
  ease(clamp01((t - t0) / (t1 - t0)));

export type Pt = [number, number];

/** Resample a polyline to n points evenly spaced by arc length (for point-wise path morphs). */
export const resample = (pts: Pt[], n: number): Pt[] => {
  const seg: number[] = [];
  let total = 0;
  for (let i = 1; i < pts.length; i++) {
    const d = Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]);
    seg.push(d);
    total += d;
  }
  const out: Pt[] = [];
  let j = 0;
  let acc = 0;
  for (let k = 0; k < n; k++) {
    const target = (total * k) / (n - 1);
    while (j < seg.length - 1 && acc + seg[j] < target) acc += seg[j++];
    const u = seg[j] ? clamp01((target - acc) / seg[j]) : 0;
    out.push([lerp(pts[j][0], pts[j + 1][0], u), lerp(pts[j][1], pts[j + 1][1], u)]);
  }
  return out;
};

export const toPath = (pts: Pt[]) =>
  pts.map((p, i) => `${i ? 'L' : 'M'}${p[0].toFixed(2)} ${p[1].toFixed(2)}`).join(' ');

/** Color mix of two #rrggbb values. */
export const mix = (a: string, b: string, k: number) => {
  const pa = [1, 3, 5].map((i) => parseInt(a.slice(i, i + 2), 16));
  const pb = [1, 3, 5].map((i) => parseInt(b.slice(i, i + 2), 16));
  return `rgb(${pa.map((v, i) => Math.round(lerp(v, pb[i], clamp01(k)))).join(',')})`;
};
