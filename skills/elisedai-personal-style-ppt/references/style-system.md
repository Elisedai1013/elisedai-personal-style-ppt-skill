# Style system

## Core idea

Build a text-led AI-native editorial page, not a software interface. Preserve one identity while varying the visual form. The system is black, white, and Signal Blue; gray is a neutral derived from black, not another accent.

## Palette

| Role | Color |
| --- | --- |
| Signal Blue | `#276EF1` |
| Primary ink | `#151515` |
| Pure white | `#FFFFFF` |
| Pale-blue image tint | `#EAF1FF` |
| Body gray | `#666666` |
| Quiet gray | `#969696` |
| Hairline gray | `#D8D8D8` |

The only permitted full-slide backgrounds are `#276EF1`, `#FFFFFF`, and `#151515`. Do not use beige, cream, yellow, warm white, or another chromatic accent. Pale blue is an image tint, not a slide field.

## Color behavior

Black, white, and blue are a system, not a requirement to show all three on every page.

- On white: use black titles, gray support, and blue only inside the visual meaning.
- On blue: use white titles and light-gray support. Avoid blue-on-blue decoration.
- On black: use white titles, gray construction lines, and at most one blue signal.
- In illustrations: build 70–85% of the subject with black/white/gray and reserve blue for the path, light, active object, change, result, or field.
- In charts: use black/gray for context and blue for the claim-bearing series or interval.

Never color a keyword blue merely to create emphasis.

## Canvas fields

### White field

Use for most explanation, method, comparison, and evidence slides.

- Pure white `#FFFFFF` canvas.
- Black/gray typography.
- Visual may bleed, form a stage, or occupy 45–65% of the page.
- Avoid placing every visual inside the same pale rectangle.

### Signal field

Use for covers, section breaks, pivotal claims, and closings.

- Full Signal Blue canvas.
- White title and white/light-gray visual.
- Sparse composition with large quiet areas.
- Use for no more than one emotional beat at a time.

### Dark field

Use for unknown space, constraints, tension, search, or a decisive thesis.

- Full black field or one dominant organic black mass on white.
- White/gray visual structure.
- One blue path, point, or light may carry the meaning.
- Do not use for ordinary explanation pages.

### Pale-blue image treatment

Use inside a photo, screenshot, source slide, or large illustration. It is not a slide background.

- Keep the page white.
- Treat the image itself with pale blue, grayscale, or duotone.
- Use a clean crop or organic mask, never a rounded UI card.
- Do not place an untreated image on top of a blue rectangle and call it unified.

## Typography

- Title and key statement: `TencentSans W7` when locally installed or supplied by the user.
- Body, English, numerals, labels, and captions: `TencentSans W3` when locally installed or supplied by the user.
- If Tencent Sans is unavailable, use the approved fallback in `font-compatibility.md` consistently across Chinese, English, and numerals.
- Deck title: 52–68 px.
- Slide title: 42–58 px.
- Subheading or one support line: 24–30 px.
- Body: 18–24 px.
- Caption and page marker: 11–15 px.
- Use at most two visible text sizes on an ordinary slide. A caption is the only routine third level.
- Mixed Chinese and English should remain in the Tencent family; do not let English fall back to a different typeface.

## Layout

- Default to 16:9 at 1280 × 720.
- Use 64–80 px outer margins.
- Favor asymmetric 38/62, 42/58, or overlapping editorial compositions.
- Let a visual shape the page. It may bleed to an edge, create a window, form an organic boundary, or sit behind the title.
- Keep one dominant visual mass and one quiet region.
- Use flat compositions. Avoid card grids, pills, badges, navigation chrome, and repeated rounded rectangles.
- Vary silhouettes across the deck while preserving margins, type rhythm, palette, and stroke character.

## Visual language

### Typography-only statement

Use when the claim is strong enough to carry the page. Do not add a decorative icon.

### Hand-drawn metaphor scene

- Use a small person, path, door, cliff, plant, light, threshold, or similarly legible metaphor.
- Show one action or tension.
- Use slightly imperfect human lines rather than polished corporate icons.
- Let black/gray build the scene and blue mark the semantic change.

### Geometric or spotlight stage

- Use circles, windows, grids, organic black masses, dotted paths, and sparse symbols.
- Use scale contrast: one large field or aperture plus one small subject.
- Use for known/unknown, territory, model behavior, search, and boundaries.
- Keep the geometry expressive rather than diagrammatically exhaustive.

### Full-field sketch

- Use blue or black as the full canvas.
- Draw one sparse white/gray scene or gesture.
- Use for chapter changes and emotional pauses, not dense explanation.

### Treated evidence

- Use source screenshots, photos, charts, or original slides only when they provide evidence.
- Convert mixed-source visuals to grayscale, pale-blue, or signal duotone.
- Crop to the evidence-bearing region and remove irrelevant UI chrome when possible.
- Add one short audience-facing interpretation outside the image; do not surround it with multiple labels.
- If interface text is the evidence, crop until it remains readable at full-slide viewing size. A complete but unreadable screen is not evidence.

## Photography and screenshots

- Prefer quiet editorial scenes with strong negative space and controlled backgrounds.
- Preserve natural skin tones and documentary color by default. Use grayscale only for an intentional narrative reason.
- For screenshots, preserve original colors, readable evidence, aspect ratio, antialiasing, and UI-state contrast by default.
- Use blue light, backdrop, mask, or duotone as part of the image treatment; do not add a decorative blue border.
- Use `screenshot-clean` only when normalization is needed. It preserves non-blue colors, luminance, and antialiasing while gently normalizing white and blue UI pixels.
- Reserve `white-blue` for illustrations, photos, or low-text visuals that need a stronger palette reset.
- When the screenshot contains the key sentence, number, or state, reproduce that item as editable slide text and keep the crop as proof rather than shrinking the whole interface.

### Screenshot fusion decision

1. **Identify the evidence.** Decide whether the audience needs a sentence, a control, a diagram, a result, or the whole interface relationship.
2. **Crop first.** Remove unused browser chrome, empty margins, navigation, and unrelated controls before any color treatment.
3. **Choose the receiving field.** A light screenshot should end in pure white so its edge dissolves into a white slide. A dark screenshot should end in black so it dissolves into a dark stage.
4. **Preserve color first.** Keep source colors unless a specific, reversible treatment improves readability without changing meaning.
5. **Normalize only with cause.** Map an existing blue family toward Signal Blue only when it does not erase a category, state, brand, or human/documentary cue.
6. **Interpret once.** Add one short audience-facing explanation beside or below the evidence, outside the crop.

After treatment, compare the source and result at 100%. Reject any version that makes source text, table rules, or UI states harder to read.

Never use a pale-blue rectangle as a decorative container for an untreated screenshot. Crop first, treat second, lay out third.

## Rhythm

Vary visual forms, not brand language. A common 10-slide rhythm is:

1. Signal field — cover
2. White field — typographic question
3. Dark field — pivotal thesis
4. White field — metaphor scene
5. White field — treated evidence
6. White field — geometric mechanism
7. Signal field — chapter transition
8. White field — comparison or result
9. Dark or white field — synthesis
10. Signal field — closing

## Anti-patterns

- Drawing the entire illustration in blue.
- Repeating a pale-blue rectangle with a centered icon on every content slide.
- Using a generated visual that merely repeats the title.
- Treating line art as the only permitted visual form.
- Blue dots, bars, underlines, bullets, keywords, or page numbers used only as decoration.
- Several explanation blocks, labels, source notes, and conclusions competing on one page.
- Gradient blue backgrounds, neon glow, glassmorphism, or generic AI circuitry.
- Dense card grids, dashboard layouts, and colorful icon sets.
- Randomly mixed visual styles without consistent palette, line character, or composition.
