---
name: elisedai-personal-style-ppt
description: Create, restyle, audit, or extend editable PowerPoint decks in EliseDai's personal AI-native editorial style using Tencent Sans when locally available, black, white, and Signal Blue (#276EF1), with text-led storytelling and varied conceptual visuals such as hand-drawn metaphors, geometric stages, full-field sketches, treated photos, and unified screenshots. Use when the user asks for “EliseDai个人PPT风格”, “鲜曜蓝风格”, “个人PPT风格”, “AI native讲PPT”, black-white-blue editorial slides, conceptual illustrations, unified image treatment, or invokes $elisedai-personal-style-ppt.
---

# EliseDai Personal Style PPT

Create a text-led AI-native presentation. Keep the identity consistent through color, typography, composition, and visual metaphor—not by repeating one template or drawing every object in blue.

## Load the required guidance

1. Load and follow the installed presentation-creation skill before authoring a deck.
2. Read [references/style-system.md](references/style-system.md) for every task.
3. Read [references/slide-archetypes.md](references/slide-archetypes.md) when planning a deck or choosing a visual form.
4. Read [references/image-prompts.md](references/image-prompts.md) before generating, editing, or treating visuals.
5. Read [references/screenshot-integrity.md](references/screenshot-integrity.md) whenever the source deck contains screenshots, UI captures, charts, tables, or documentary photos.
6. Read [references/font-compatibility.md](references/font-compatibility.md) for every task. Prefer Tencent Sans when it is installed or supplied by the user; the public Skill does not redistribute proprietary font binaries.

User-supplied templates and explicit directions override this system. Do not mix in an unrelated template.

## Execute the workflow

### 1. Define the communication job

State internally: “By the end, the audience should [outcome] because [central takeaway].” Build a cumulative narrative and give each slide one job.

### 2. Reduce before designing

Write a spoken takeaway title. Remove repeated explanation before changing layout or shrinking type. A normal slide should have one claim, one visual idea, and no more than two visible text levels.

### 3. Choose the canvas field

Select one full-slide field for each slide. The only permitted full-slide backgrounds are pure white `#FFFFFF`, Signal Blue `#276EF1`, and black `#151515`:

- **White field — default:** Pure white canvas; black/gray text; blue appears inside the visual meaning.
- **Signal field — emphasis:** Full Signal Blue canvas; white and light-gray text/visuals; use for covers, transitions, pivotal claims, and closings.
- **Dark field — conceptual depth:** Full black field or a dominant black stage on white; white/gray visuals with one restrained blue signal. Use for unknown space, tension, limits, or a decisive thesis.

Pale blue may exist inside a treated image, light, aperture, or illustration derived from Signal Blue. It is never a fourth slide background.

Do not alternate fields mechanically. Avoid using the same field for more than three consecutive slides unless the narrative requires it.

### 4. Choose one visual form

Use the smallest form that adds meaning:

1. **Typography only:** Use when the sentence itself is the visual.
2. **Hand-drawn metaphor scene:** Use a small person, path, door, cliff, plant, light, or other scene to make an abstract idea felt.
3. **Geometric or spotlight stage:** Use circles, windows, grids, organic masses, and paths to show known/unknown, boundary, search, or transformation.
4. **Full-field sketch:** Use a sparse white/gray drawing on a blue or black field for a chapter break or emotional beat.
5. **Treated evidence:** Use a photo, screenshot, chart, or source artifact only when evidence matters; crop and normalize it with grayscale, pure-white-blue, duotone, or masking.

Do not default to line art. Do not place a detachable icon on the right merely to fill space. Integrate the visual with the page composition.

Before building, consider each slide's best source of meaning:

- Use supplied evidence when the audience must verify a fact, interface, result, person, or event.
- Generate a subject-specific metaphor or geometric scene when the slide explains an abstract principle, boundary, path, tension, or transformation that source evidence cannot show.
- Use editable native shapes when the mechanism is simple enough to express directly.
- Use typography only when another visual would weaken the statement.

Do not set quotas for any visual form. Vary by communication need, not by compliance.

### 5. Generate or treat imagery first

Create the visual for the slide's claim and intended placement before adding decoration. Follow [references/image-prompts.md](references/image-prompts.md).

Keep the main structure black, white, or gray. Use Signal Blue for one semantic role: path, light, active object, change, result, or field. Never render the entire illustration blue unless it is intentionally white linework on a full blue field.

For existing photos and screenshots, preserve the source appearance by default. Use `scripts/treat_photo.py --mode original` for lossless format normalization. Use `screenshot-clean` only when white-background or blue-family normalization is genuinely needed; it must retain non-blue source colors. Use grayscale, white-blue, pale-blue, or duotone only for a stated narrative reason or when the user explicitly requests that treatment.

### 6. Fuse screenshots with the page

Treat a screenshot as evidence, not as decoration:

1. Crop to the evidence-bearing region before styling.
2. Preserve original aspect ratio, UI geometry, color relationships, antialiasing, table rules, and state contrast.
3. Remove irrelevant browser chrome or controls only through cropping; do not repaint the interface merely to match the deck.
4. Preserve original colors by default. Map colors to the Signal Blue system only when color is not evidence and the treatment demonstrably improves readability.
5. Match the screenshot field to the page through whitespace and placement, not by placing it on a decorative colored panel.
6. Place one short audience-facing interpretation beside or below the evidence. Do not surround it with labels.
7. When screenshots or documentary photos are contained evidence, apply one consistent subtle rounded mask, normally 8–12 px, without decorative shadow or colored backing.
8. Treat same-role images as a geometry group: horizontal pairs and vertical stacks must have identical visible width and height, the same radius and crop logic, aligned edges, equal gaps, and aligned caption baselines. Use evidence-aware `cover` cropping rather than stretching; split the slide if equal crops would hide essential information.

For a screenshot with a non-obvious crop, or any deck using three or more evidence images, keep an `evidence-manifest.json` following [references/screenshot-integrity.md](references/screenshot-integrity.md). Record the required evidence region, actual frame, crop, fit, and minimum readable size. Prefer creating a pre-cropped asset at the final aspect ratio; avoid stacking an approximate crop on top of `cover` and trusting the centered result.

Never place an untreated screenshot on a pale-blue rectangle. Crop first, treat second, and lay out third.

For text-dense UI screenshots, prefer original color. `screenshot-clean` is a secondary option; grayscale is never a default for UI, charts, tables, people, or event photos. If the screenshot cannot be read at presentation size, crop tighter or recreate the key statement as editable slide text with a smaller evidence crop.

Before export, compare every used screenshot with its source at 100%. Reject changes that alter the meaning, remove useful color, distort proportions, or make the evidence harder to read.

### 7. Run advisory visual hooks

Use `scripts/visual_quality_hook.py` as a non-blocking design partner. It reports risks and always exits successfully; apply judgment rather than treating suggestions as rules.

- After selecting or treating assets, run `--phase assets --assets-dir <dir>`. For screenshot-heavy decks, also pass `--evidence-manifest <json> --report-dir <qa-dir>` and inspect the generated crop review.
- After writing the deck builder, run `--phase build --builder <file>`.
- Before delivery, run `--phase final` with the builder, assets, and exported `--pptx` paths when available, then inspect the rendered montage and flagged slides at full size.
- For a visually complex deck, optionally keep a small `visual-plan.json` and run `--phase plan --plan <file>`. This is a thinking aid, not a required deliverable.

The hook should surface, not dictate: unreadable screenshot thumbnails, text-heavy screenshots with aggressive recoloring, decorative pale-blue evidence panels, same-role image groups with mismatched visible dimensions or missing rounded masks, monotonous reliance on screenshots, plausible missed opportunities for conceptual imagery, unavailable Tencent Sans fonts, and a PPTX that references but does not embed its fonts.

### 8. Build an editable deck

Use `@oai/artifact-tool` from a plain JavaScript ES module. Keep text, charts, tables, and simple structural rules editable. Embed illustrations and treated images as byte-backed assets. Do not use `python-pptx`.

Prefer these locally installed or user-supplied fonts:

- Titles and key statements: typeface name `TencentSans W7`.
- Body, English, numerals, captions: typeface name `TencentSans W3`.

Confirm font availability before rendering. If Tencent Sans is unavailable, use the approved compatibility fallback from [references/font-compatibility.md](references/font-compatibility.md) and disclose it. In artifact-tool text styles, use `typeface`, not `fontFamily`. Verify the exported PPTX XML contains the intended typeface names, then follow the font reference for desktop PowerPoint, browser-preview, embedding, and packaging checks.

### 9. Verify

Render every slide and inspect it at full size. Fix overflow, wrapping, overlap, weak hierarchy, inconsistent image treatment, detached visuals, and accidental blue decoration.

Run the final hook with the PPTX itself:

```bash
python scripts/visual_quality_hook.py \
  --phase final \
  --assets-dir <assets-dir> \
  --builder <builder.mjs> \
  --evidence-manifest <evidence-manifest.json> \
  --report-dir <qa-dir> \
  --pptx <final.pptx>
```

Do not call a deck portable merely because the font is installed locally. If `ppt/fonts/` is absent inside the PPTX, either use user-supplied licensed font files for the intended delivery or produce an explicitly approved compatibility fallback. Browser and cloud previews are not authoritative for local third-party fonts; use desktop PowerPoint for the final typography check when exact parity matters.

For every slide, ask:

- Can the audience identify the one claim in three seconds?
- Does the visual add a metaphor, mechanism, feeling, or evidence instead of repeating the title?
- Is blue performing one semantic job?
- Are there no more than two visible text levels unless evidence requires a caption?

## Enforce the non-negotiables

- Full-slide backgrounds are only Signal Blue `#276EF1`, pure white `#FFFFFF`, or black `#151515`. Never use beige, cream, yellow, or warm paper.
- Use black, white, gray derived from black, and Signal Blue `#276EF1`; introduce no second accent color.
- Keep ordinary typography black, white, or gray. Do not color keywords blue.
- Prefer Tencent Sans W7 for titles and W3 for body and English; use the documented fallback when the user has not supplied or installed them.
- Use one visual idea per slide and one dominant composition rather than UI panels.
- Use a stable deck grid: consistent outer margins, title baseline, caption position, evidence scale, and footer placement. Vary the visual form inside that grid; do not vary basic alignment arbitrarily.
- Same-role evidence images are one layout object: keep their visible frames, radius, crop behavior, edge alignment, gaps, and caption baselines identical unless a deliberate primary/secondary hierarchy is stated.
- Keep blue below roughly 20% of a white or black slide unless blue is the deliberate full-field background.
- Let visual styles vary across the deck while preserving palette, stroke character, typography, margins, and narrative restraint.
- Unify mixed-source imagery through crop, scale, spacing, and interpretation first. Do not recolor screenshots or photos solely for stylistic consistency.
- Avoid colorful icon sets, gradients, glassmorphism, generic AI circuitry, dashboard cards, decorative blobs, arbitrary blue bars, and repeated right-side icons.
- Never reuse bundled reference images as final slide content. Generate subject-specific visuals.

## Use bundled resources

- `references/font-compatibility.md`: Tencent Sans authoring choices, public-distribution limits, fallbacks, embedding limits, PowerPoint/browser behavior, and delivery rules.
- `assets/style-reference-preview.png`: montage of the current composition references.
- `assets/style-reference.pptx`: editable legacy reference deck; use only when explicitly requested.
- `scripts/treat_photo.py`: deterministic photo and screenshot unification.
- `scripts/visual_quality_hook.py`: advisory checks for image treatment, evidence readability, grouped-image geometry, visual monotony, font assets, PPTX font references, and font embedding risk.
