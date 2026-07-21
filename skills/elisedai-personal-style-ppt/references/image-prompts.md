# Image prompting and treatment

Generate a subject-specific visual for each slide. Use user-provided references only to calibrate composition, contrast, and visual richness.

## General requirements

Every prompt must specify:

- The slide claim and what the visual must add: metaphor, mechanism, feeling, or evidence.
- The intended field: pure white, Signal Blue, or dark; pale blue may appear only inside the image.
- Exact subject, action, scale relationship, and negative-space location.
- Black, white, gray, exact Signal Blue `#276EF1`, and derived pale-blue tints only.
- No text, letters, numbers, logos, watermark, decorative UI, stock icon language, gradients, or generic AI circuitry.

Do not request “a simple icon.” Request an integrated editorial composition or scene.

## Hand-drawn metaphor scene

```text
Use case: illustration-story
Asset type: AI-native editorial presentation illustration
Primary request: express [claim] as one visual metaphor using [small subject] interacting with [path / threshold / cliff / plant / light / environment]
Style/medium: sparse hand-drawn editorial scene with slightly imperfect human linework; conceptual, intelligent, and understated
Composition/framing: wide 16:9-compatible composition; create one dominant spatial relationship and preserve negative space for copy on the [left/right]
Color palette: build the subject and environment mostly with black, white, and gray; use exact Signal Blue #276EF1 only for [path/light/active object/change/result]
Constraints: one scene and one action; blue below 20% of the image; no detached icon, labels, text, logo, watermark, gradient, 3D rendering, UI cards, or decorative objects
```

## Geometric or spotlight stage

```text
Use case: productivity-visual
Asset type: conceptual editorial presentation visual
Primary request: visualize [known/unknown, search, territory, boundary, transformation, or capability] using one large [window/circle/aperture/organic mass/grid] and one small subject or path
Style/medium: restrained editorial geometry combined with sparse hand-drawn marks; cinematic scale contrast without photorealism
Composition/framing: wide composition integrated with slide layout; preserve negative space for copy on the [left/right]; let the visual bleed or form a page boundary
Color palette: black, white, gray, and exact Signal Blue #276EF1; reserve blue for one semantic signal
Constraints: one dominant field, one focal subject, sparse construction marks; no icon collection, labels, text, logo, watermark, gradient, neon glow, dashboard styling, or clutter
```

## Full Signal Blue field sketch

```text
Use case: illustration-story
Asset type: cover or chapter-break presentation visual
Primary request: express [single pivotal claim] with one small [person/object/gesture] performing [action]
Style/medium: sparse hand-drawn editorial sketch with human, slightly imperfect strokes
Composition/framing: full exact Signal Blue #276EF1 field, strong negative space, visual concentrated on the [right/left]
Color palette: white and light-gray linework on Signal Blue; no additional blue shades except subtle derived tints
Constraints: one emotional beat; no black text inside the image, labels, logo, watermark, texture, gradient, glow, shadow, UI styling, or extra decoration
```

## Dark field metaphor

```text
Use case: illustration-story
Asset type: dark conceptual presentation visual
Primary request: express [constraint/unknown/tension/thesis] using one large black environment and one small [person/object/path/light]
Style/medium: high-contrast editorial scene combining organic mass, sparse hand drawing, and restrained geometry
Composition/framing: wide composition; preserve copy space on the [left/right]; use scale contrast and one clear focal point
Color palette: black field, white and gray structure, exact Signal Blue #276EF1 only for [path/light/active point]
Constraints: blue below 10%; no horror styling, photorealism, labels, text, logo, watermark, gradients, neon glow, UI cards, or decorative clutter
```

## Pale-blue evidence or image treatment

```text
Use case: productivity-visual
Asset type: editorial presentation visual
Primary request: depict [subject/scene] supporting [claim]
Style/medium: [quiet editorial photography / editorial collage / sparse illustration]
Composition/framing: clean image region with subject on the [right/left], one dominant visual mass, and usable negative space
Scene/backdrop: pure white #FFFFFF or a pale-blue studio region derived from Signal Blue near #EAF1FF; if the visual must merge into a white slide, outer pixels must be pure white
Color palette: black, white, gray, exact Signal Blue #276EF1, and pale-blue tints only
Constraints: background treatment belongs inside the image; no decorative frame, rounded card, text, logo, watermark, gradient, or unrelated objects
```

## Editing an existing illustration

```text
Use case: precise-object-edit
Input image: Image 1 is the edit target
Primary request: preserve the composition, subject, proportions, crop, and negative space; recolor the main structure to black/gray and only [semantic element] to exact Signal Blue #276EF1
Constraints: blue must remain below 20%; change only specified colors; do not add, remove, move, redraw, or crop any element; no text, logo, or watermark
```

## Photography and screenshot treatment

For deterministic treatment, run:

```bash
python scripts/treat_photo.py input.jpg output.png --mode grayscale
python scripts/treat_photo.py input.jpg output.png --mode original
python scripts/treat_photo.py input.jpg output.png --mode screenshot-clean
python scripts/treat_photo.py input.jpg output.png --mode white-blue
python scripts/treat_photo.py input.jpg output.png --mode pale-blue
python scripts/treat_photo.py input.jpg output.png --mode signal-duotone
```

- Use `original` by default for UI screenshots, charts, tables, people, and documentary photos.
- Use `screenshot-clean` only when a text-dense interface needs near-white and blue-family normalization; it preserves all non-blue source colors, luminance, and antialiasing.
- Use `grayscale` only for a deliberate documentary mood when color carries no identity, state, category, or brand meaning.
- Use `white-blue` for illustrations, photos, and low-text visuals to remove warm casts, make light backgrounds dissolve into a pure-white slide, and retain one blue semantic state.
- Use `pale-blue` for image-led content pages and mixed-source unification.
- Use `signal-duotone` sparingly for covers, transitions, and decisive evidence.
- Crop to the evidence-bearing region before treatment when irrelevant interface chrome dominates. Crop first, treat second, lay out third.
- Never place an untreated screenshot on a pale-blue rectangle. Preserve original color only when color itself is evidence.
- Preserve legibility of source text and charts.
- Compare source and treated screenshots at 100%; reject the treatment if color truthfulness, small text, table lines, or state contrast deteriorates.
- Inspect faces, highlights, shadows, and screenshot contrast after treatment.

## Visual QA

Reject or regenerate when:

- The whole illustration is blue.
- The output looks like a centered icon or corporate infographic.
- The visual merely repeats the title without adding metaphor, mechanism, feeling, or evidence.
- Several unrelated objects compete for attention.
- The generated background creates a visible card when the visual should integrate with the page.
- Blue has no explainable semantic role.
