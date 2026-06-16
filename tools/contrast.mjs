// contrast.mjs - WCAG contrast-ratio checker for Tyrnarra accent colours.
// Cross-platform (Node); replaces the old PowerShell snippet.
//
// Usage:
//   node tools/contrast.mjs '#6878c0'             # check vs both Style A & B bases
//   node tools/contrast.mjs '#6878c0' '#0f0c08'   # check vs a specific background
//
// Style B base bg = #0f0c08 ; Style A base bg = #06060a.
// The 3:1 floor (WCAG 1.4.11) applies to every --domain-accent. Aim >=3.2 for a
// safety margin against subpixel rendering / colour-profile drift; >=4.5 if the
// accent is also legible as text.

function toLinear(c) {
  c = c / 255;
  return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
}
function luminance(hex) {
  const h = hex.replace(/^#/, "");
  const r = parseInt(h.slice(0, 2), 16);
  const g = parseInt(h.slice(2, 4), 16);
  const b = parseInt(h.slice(4, 6), 16);
  return 0.2126 * toLinear(r) + 0.7152 * toLinear(g) + 0.0722 * toLinear(b);
}
function ratio(fg, bg) {
  const lf = luminance(fg);
  const lb = luminance(bg);
  const l1 = Math.max(lf, lb);
  const l2 = Math.min(lf, lb);
  return (l1 + 0.05) / (l2 + 0.05);
}

function verdict(r) {
  if (r >= 4.5) return "PASS (graphic + text)";
  if (r >= 3.2) return "PASS (graphic, safe margin)";
  if (r >= 3) return "PASS (graphic, tight)";
  return "FAIL (under the 3:1 floor)";
}

const fg = process.argv[2];
if (!fg || !/^#?[0-9a-fA-F]{6}$/.test(fg)) {
  console.error("usage: node tools/contrast.mjs '#rrggbb' ['#bg']");
  process.exit(1);
}

const bgs = process.argv[3]
  ? [[process.argv[3], "custom bg"]]
  : [
      ["#0f0c08", "Style B base"],
      ["#06060a", "Style A base"],
    ];

for (const [bg, label] of bgs) {
  const r = ratio(fg, bg);
  console.log(`${fg} on ${bg} (${label}): ${r.toFixed(2)}:1  ${verdict(r)}`);
}
