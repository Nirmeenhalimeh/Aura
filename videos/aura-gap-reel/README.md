# Aura AI — "الفجوة" Reel (30s, 1080×1920, 30fps)

Motion graphics only (shapes, type, motion). Built with Remotion inside
[claude-motion](https://github.com/whaleyxbt/claude-motion).

- `aura-gap.mp4`: final render with sound (H.264 + AAC, -14 LUFS, true peak -1.8 dBFS)
- `aura-gap-silent.mp4`: the same picture without audio
- `review/`: PNG frames at 00:02, 00:12, 00:20, 00:28
- `src/`: the composition (`AuraGap.tsx`), palette/easing (`theme.ts`), beat timeline (`timeline.json`), sound cue sheet (`aura_gap.py`)
- `claude-motion.patch`: the same change as a git patch (adds `src/aura/`, registers the composition, adds IBM Plex Sans Arabic)

## Re-render

```bash
git clone https://github.com/whaleyxbt/claude-motion && cd claude-motion
git am /path/to/claude-motion.patch
npm install
npx remotion render AuraGap out/aura-gap-silent.mp4 --codec=h264
python3 -m sfx sfx/cues/aura_gap.py
ffmpeg -y -i out/aura-gap-silent.mp4 -i public/aura-sfx.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -movflags +faststart -shortest out/aura-gap.mp4
```

Retime by editing `src/aura/timeline.json`; picture and sound both read it.
Sound: A minor bed, darkens to Fmaj7 at the gap, resolves to A major on the logo; one impact, on the crack. Easing family: "Aura Expo" (expo-out / expo-in / expo-in-out).
