# Aura AI — "الفجوة" Reel (30s, 1080×1920, 30fps)

Motion graphics only (shapes, type, motion). Built with Remotion inside
[claude-motion](https://github.com/whaleyxbt/claude-motion).

- `aura-gap.mp4`: final render (H.264, no audio)
- `review/`: PNG frames at 00:02, 00:12, 00:20, 00:28
- `src/`: the composition (`AuraGap.tsx`), palette/easing (`theme.ts`), beat timeline (`timeline.json`)
- `claude-motion.patch`: the same change as a git patch (adds `src/aura/`, registers the composition, adds IBM Plex Sans Arabic)

## Re-render

```bash
git clone https://github.com/whaleyxbt/claude-motion && cd claude-motion
git am /path/to/claude-motion.patch
npm install
npx remotion render AuraGap out/aura-gap.mp4 --codec=h264
```

Retime by editing `src/aura/timeline.json`. Easing family: "Aura Expo" (expo-out / expo-in / expo-in-out).
