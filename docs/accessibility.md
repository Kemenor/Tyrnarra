# Accessibility — Conformance Notes

How the site meets WCAG 2.1 AA, what's left as known-borderline, and how to keep new work conformant.

The target is **WCAG 2.1 Level AA**. We are not chasing AAA; some of the visual moodiness (deliberately-dim accent colours, subtle dividers) reads as AA-borderline by design and would lose its character at AAA thresholds.

---

## Colour contrast

### Base palettes pass strongly

Every text-on-background pairing in [`/assets/style-b.css`](../assets/style-b.css) and [`/assets/style-a.css`](../assets/style-a.css) clears WCAG AA (≥4.5:1 for normal text, ≥3:1 for large text and graphic components).

**Style B (grounded — every page under `/talan/` and `/off-continent/`):**

| Foreground | Background | Ratio |
|---|---|---|
| `--text` `#d0c8a8` | `--bg` `#0f0c08` | 11.6 : 1 |
| `--parch` `#c8b890` | `--bg` | 9.95 : 1 |
| `--parch-bright` `#e8d8a8` | `--bg` | 13.8 : 1 |
| `--parch-dim` `#8a7a58` | `--bg` | 4.65 : 1 |
| `--gold` `#c8900a` | `--bg` | 6.92 : 1 |
| `--gold-bright` `#f0b020` | `--bg` | 10.2 : 1 |
| `--gold-dim` `#a07520` | `--bg` | 4.70 : 1 |
| `--text-dim` `#9a9078` | `--bg` | 6.16 : 1 |

**Style A (cosmic — root-level pages: `index.html`, `grand-gods.html`, `non-bound-gods.html`, `gods-law.html`, `magic.html`, `pf2e-registrar.html`):**

| Foreground | Background | Ratio |
|---|---|---|
| `--text` `#c8c4d8` | `--bg` `#06060a` | 11.9 : 1 |
| `--text-bright` `#eeeaf8` | `--bg` | 17.1 : 1 |
| `--text-dim` `#8e8aa6` | `--bg` | 6.10 : 1 |
| `--gold` `#c8a84a` | `--bg` | 8.82 : 1 |
| `--gold-bright` `#f0d080` | `--bg` | 13.5 : 1 |
| `--gold-dim` `#9a8240` | `--bg` | 5.43 : 1 |

### Known borderline (left as-is)

- `--gold-dim` on `--bg2` (`#171209`) is **4.49 : 1**, just under the AA-normal threshold. Only used in breadcrumb hover states. Negligible.

### Per-domain accents must clear 3 : 1

Each Style-B page sets `--domain-accent` in a tiny inline `<style>`. The variable is used in [`/assets/style-b.css`](../assets/style-b.css) for:

- `.subregion-card::before` left stripe (graphic)
- `.gods-city` border, `.gods-city::before/::after` ✦ glyphs (graphic + small text)
- `.accent-card` left border / framed border (graphic)
- `.open-canon` dashed border (graphic)

**`--domain-accent` is never used as a primary text colour in shared CSS.** `.open-canon h3` was historically the exception — it now uses a fixed `var(--gold)` so the heading stays AA-readable even when the page's accent is dim. The dashed border above the heading still carries the domain flavour.

**The 3 : 1 floor applies to every new `--domain-accent`.** WCAG 1.4.11 (Non-text Contrast) requires this for UI components and meaningful graphics — the card stripes are load-bearing for "which section am I in," so they need to be visible.

#### How to check a new accent

```powershell
function To-Linear([double]$c) {
  $c = $c / 255.0
  if ($c -le 0.03928) { return $c / 12.92 }
  return [math]::Pow(($c + 0.055) / 1.055, 2.4)
}
function Luminance([string]$hex) {
  $h = $hex.TrimStart('#')
  $r = [Convert]::ToInt32($h.Substring(0,2),16)
  $g = [Convert]::ToInt32($h.Substring(2,2),16)
  $b = [Convert]::ToInt32($h.Substring(4,2),16)
  return 0.2126*(To-Linear $r) + 0.7152*(To-Linear $g) + 0.0722*(To-Linear $b)
}
function Ratio([string]$fg, [string]$bg) {
  $lf = Luminance $fg; $lb = Luminance $bg
  $l1 = [math]::Max($lf, $lb); $l2 = [math]::Min($lf, $lb)
  return ($l1 + 0.05) / ($l2 + 0.05)
}
Ratio '#yournewhex' '#0f0c08'   # Style B base
Ratio '#yournewhex' '#06060a'   # Style A base
```

Aim for **≥ 3.2** to clear with a small safety margin against subpixel rendering and colour-profile drift. If you want the accent legible as text too, aim for **≥ 4.5**.

If your hue is intentionally moody and dragging up brightness would lose its character, talk to the user before pushing through — there may be a paired-token solution (a graphic accent + a brighter `*-strong` sibling for any text use) rather than a flat brighten.

### Style-A god accents (not yet audited in detail)

The 13 per-god `--<god>` / `--<god>-light` pairs in style-a.css are used as graphic accents on `grand-gods.html`. They have not been individually contrast-checked because they're tied to canon (each god owns a colour and changing it is a worldbuilding decision, not an accessibility decision). If a future audit flags one as failing, surface it as a content question.

---

## Keyboard focus (WCAG 2.4.7)

A universal `:focus-visible` rule lives at the bottom of [`/assets/site-nav.css`](../assets/site-nav.css):

```css
a:focus-visible,
button:focus-visible,
summary:focus-visible,
[tabindex]:focus-visible {
  outline: 2px solid var(--gold-bright, var(--gold, #f0d080));
  outline-offset: 2px;
  border-radius: 2px;
}
```

This loads on every page (site-nav.css is in every page's `<head>`), so it covers both Style A and Style B. The gold-bright outline reads cleanly on the warm Style-B `#0f0c08` and the cool Style-A `#06060a` alike.

**Don't override `outline` on individual interactive elements without putting back a focus indicator** — the rule above is the only thing standing between a keyboard user and a silent site.

---

## Toggle button state (WCAG 4.1.2)

The reveal-toggles for amber `◈ Popular Belief` and red `⚿ GM Secret` boxes are `<button>` elements that swap label and toggle a `.revealed` class on the next sibling. To announce state changes to assistive tech, [`/assets/site-interactions.js`](../assets/site-interactions.js):

1. Calls `btn.setAttribute('aria-expanded', revealed ? 'true' : 'false')` inside `toggleReveal` on every click.
2. Runs an `initAria()` pass on `DOMContentLoaded` that seeds `aria-expanded="false"` on every `.secret-toggle`, `.secret-era-toggle`, and `.legend-era-toggle`.

**The HTML doesn't need to declare `aria-expanded` itself** — the JS seeds it. But if you add a new toggle-button class, add it to the selector list in `initAria()`.

The era-card click target (`.era-card`) is a `<div>` toggled by `toggleEra`. It doesn't currently carry button semantics — if accessibility for keyboard users browsing the history-page eras becomes a priority, this is the next thing to address (give the card `role="button"`, `tabindex="0"`, and a keypress handler).

---

## Color is never the only meaning

The two reveal-types are distinguished by **glyph + label**, not colour:

- Amber boxes lead with `◈` and the word "Popular Belief."
- Red boxes lead with `⚿` and "GM Secret."

A colour-blind reader sees the same glyph and the same words, so the tier is communicated without relying on the amber/red distinction.

---

## What's NOT covered

- **AAA conformance.** Out of scope; some moody design choices would lose character at AAA thresholds.
- **`<img alt>`.** The site has no `<img>` tags at present. If images are added later, every meaningful image needs an `alt` attribute and decorative images need `alt=""`.
- **Forms.** No forms on the site.
- **Video / audio.** No media on the site.
- **WCAG 2.5.5 (Target Size AAA, 44×44px).** The mobile burger sits at roughly 28px tall — clears the WCAG 2.2 AA floor of 24×24 but not the AAA target. Acceptable.
- **Per-ancestry `--card-accent` values in `talan/ancestries.html`.** Thirteen ancestry tiles each set their own accent inline. Not yet audited against the 3:1 floor.

---

## When to re-audit

- Adding a new domain page → check its `--domain-accent` against the snippet above.
- Adding a new shared CSS rule that uses `color: var(--domain-accent)` → it shouldn't; the variable is graphic-only. Use `var(--gold)` or `var(--gold-bright)` for text.
- Adding a new interactive widget → make sure it has a visible focus state (the universal rule covers `<a>`, `<button>`, `<summary>`, `[tabindex]`; anything else needs an explicit `:focus-visible` style).
- Adding a new toggle-button class → add it to `initAria()` in site-interactions.js.
