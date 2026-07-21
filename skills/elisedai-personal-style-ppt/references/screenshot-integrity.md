# Screenshot and evidence integrity

Use this reference whenever a deck contains screenshots, UI captures, charts, tables, documentary photos, or source artifacts.

## Default decision

Preserve the source image. Style the page around the evidence before styling the evidence itself.

Use this order:

1. Keep original color and aspect ratio.
2. Crop to the evidence-bearing region.
3. Enlarge until the evidence is readable at presentation size.
4. Reproduce the key sentence, number, or state as editable slide text when the crop still cannot carry it.
5. Apply color treatment only when the reason is explicit and the treated image remains at least as legible as the source.

## Evidence inventory

Before building, record for every used screenshot:

- source file and source slide;
- the exact evidence the audience must see;
- intended crop;
- whether original color carries meaning;
- treatment mode: `original`, `screenshot-clean`, or an explicitly justified special treatment;
- minimum presentation size.

Do not place multiple small screenshots merely because they appeared together in the source deck. Select the strongest evidence or split the content across slides.

### Machine-readable crop manifest

For any non-obvious crop, and for decks with three or more evidence images, store the inventory as `evidence-manifest.json` in scratch space. This lets the advisory Hook compute the *actual* source rectangle left after both explicit crop and centered `cover` cropping.

```json
{
  "evidence": [
    {
      "slide": 18,
      "source": "/absolute/path/source-slide.png",
      "evidence": "完整的 Command 入口、当前应用和被带入的上下文",
      "frame": {"width": 596, "height": 492},
      "crop": {"left": 0.12, "top": 0.06, "right": 0.22, "bottom": 0.09},
      "fit": "cover",
      "required_region": {"x": 0.25, "y": 0.18, "width": 0.50, "height": 0.62},
      "min_frame": {"width": 560, "height": 420},
      "min_evidence_occupancy": 0.35,
      "radius": 10,
      "group": "codex-iteration",
      "caption_y": 610
    }
  ]
}
```

- `required_region` is the smallest source-image rectangle that must survive; values are normalized by default. Use `"unit": "pixels"` for pixel coordinates.
- `frame` is the final visible slide frame, not the source image size.
- `min_frame` records the smallest acceptable presentation size for readable evidence.
- For compact generated manifests, `frame` and `min_frame` may also use `[width, height]`, while normalized `required_region` may use `[x, y, width, height]`.
- `group`, `radius`, and `caption_y` let the Hook compare same-role screenshots.
- Run `visual_quality_hook.py --phase assets --evidence-manifest <json> --report-dir <qa-dir>`. In the review image, red is the final visible crop and blue is the required evidence region.

If the red rectangle does not contain the blue rectangle, fix the asset before layout. Prefer a deterministic pre-crop at the final aspect ratio, then place it without an additional explicit crop. Do not keep adjusting normalized crop values by eye inside the deck builder.

## Color rules

- Default UI, chart, table, person, and event-photo mode: `original`.
- `screenshot-clean`: preserve non-blue colors, normalize near-white backgrounds, and gently map an existing blue family toward Signal Blue.
- Grayscale: use only when documentary mood is intentional and color does not identify people, brands, states, categories, or evidence.
- `white-blue`, pale-blue, and duotone: use for low-text illustrations or deliberately stylized imagery, not text-dense screenshots.
- Never recolor a screenshot solely because the surrounding slide is black-white-blue.

## Layout rules

- Preserve aspect ratio; never stretch a screenshot.
- Avoid hidden double-cropping. An explicit crop followed by `fit: cover` may remove more content around the center. Pre-crop to the final frame ratio or verify the computed final visible rectangle with the Hook.
- Prefer one dominant evidence crop per slide.
- Keep a consistent evidence edge and caption baseline across related slides.
- Use whitespace, crop, and scale to integrate evidence. Do not add arbitrary frames, pale-blue backing cards, or decorative borders.
- Use a subtle rounded mask for screenshots and documentary photos when they sit as contained evidence on a slide. Default to an 8–12 px radius, keep the radius consistent within a deck, and do not add a decorative shadow or colored backing panel. Keep square corners for full-bleed imagery or when rounding would crop meaningful edge content.
- Treat same-role screenshots as a geometry group. Horizontal pairs must use identical visible width and height, aligned top edges, equal gaps, the same radius, the same crop logic, and aligned caption baselines. Vertical pairs must use identical visible width and height, equal gaps, aligned left/right edges, and the same radius.
- When source aspect ratios differ, use deliberate `cover` cropping to equalize the visible frames while preserving the evidence-bearing region. Never stretch. If equal crops would remove essential evidence, split the screenshots across slides or explicitly establish a primary/secondary hierarchy instead of leaving accidental size differences.
- Equal outer frames are not enough when `contain` makes the screenshots appear visibly different. Judge the actual visible image area at full-slide scale.
- If two screenshots are required for comparison, give them equal visual weight unless one is explicitly the recommended state; the hierarchy must be deliberate and audience-readable.

## Final comparison

Inspect source and slide at 100% and verify:

- color relationships remain truthful;
- text and table lines remain readable;
- no UI state or brand marker was accidentally suppressed;
- the crop still provides enough context;
- no stretching, accidental clipping, or inconsistent screenshot scale appears;
- same-role image groups have matching visible dimensions, radius, edge alignment, gap rhythm, and caption baseline;
- the slide caption explains why the evidence matters.

Reject the slide if the treatment makes the evidence less trustworthy or less readable.
