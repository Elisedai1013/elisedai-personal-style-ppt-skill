# Tencent Sans compatibility and delivery

Use this reference for every deck built with this Skill.

## Public distribution boundary

Prefer Tencent Sans for EliseDai's personal style, but do not assume the public Skill contains or may redistribute the proprietary font binaries. Use Tencent Sans only when it is already installed in the authoring environment or the user supplies licensed copies.

The fonts commonly expose two naming models:

- Legacy family names: `TencentSans W3` and `TencentSans W7`.
- Typographic family: `TencentSans`, with styles `W3` and `W7`.

The W7 glyph design is visibly forward-leaning even though some font metadata does not mark it italic. An upright heavy Chinese title can indicate font substitution.

## Authoring choice

When Tencent Sans is available, default to:

- title: `typeface: "TencentSans W7"`;
- body: `typeface: "TencentSans W3"`.

If desktop PowerPoint substitutes either explicit name after the font is installed and the application is restarted, test a compatibility variant using the typographic family name `TencentSans` with regular/bold styling. Render the complete deck because line breaks and text metrics can change.

If Tencent Sans is unavailable, use `Source Han Sans SC` or `Noto Sans CJK SC` consistently for Chinese, English, numerals, and captions. Keep the same W7/W3 hierarchy through bold and regular/light weights. Do not silently mix multiple fallback families.

## Embedding is a separate concern

Having a font installed or supplied beside the deck does not embed it in the PPTX. Never claim fonts are embedded unless the exported package contains font parts under `ppt/fonts/` and the corresponding OOXML relationships.

Treat artifact-tool output as font-referencing by default. Verify the actual PPTX rather than assuming PowerPoint carries the font automatically.

## Rendering and preview behavior

- Install or load user-supplied licensed Tencent Sans files before rendering when exact typography is requested.
- Treat full-size desktop PowerPoint as the typography authority when the deck will be presented from PowerPoint.
- Browser, cloud-drive, Quick Look, LibreOffice, and server-side previews may substitute local third-party fonts.
- After installing fonts, fully quit and reopen PowerPoint. On macOS, confirm both faces are enabled in Font Book and resolve duplicate-font warnings.
- In PowerPoint, use Replace Fonts or the font-warning interface to detect unresolved font references.

## Delivery decision

Before delivery, choose one route and state it accurately:

1. **Editable local-font deck:** use Tencent Sans only when the recipient already has licensed copies or the user explicitly supplies files for that delivery.
2. **Verified embedded-font deck:** use only when inspection confirms embedded font parts and licensing permits the intended distribution.
3. **Compatibility fallback:** use Source Han Sans SC or Noto Sans CJK SC and disclose the substitution.

Never copy proprietary font binaries from the author's machine into a public repository or public download unless the user provides explicit redistribution rights.

## Final font audit

Verify all of the following:

- the builder uses one intended naming model consistently;
- the exported PPTX references the intended names;
- whether `ppt/fonts/` exists is recorded truthfully;
- a full-slide render has no unexpected reflow or substituted titles;
- desktop PowerPoint is checked when exact presentation parity matters;
- the public package does not contain unlicensed font binaries.
