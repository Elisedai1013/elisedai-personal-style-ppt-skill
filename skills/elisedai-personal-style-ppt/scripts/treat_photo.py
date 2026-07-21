#!/usr/bin/env python3
"""Apply deterministic Signal Blue editorial treatments to raster images."""

from __future__ import annotations

import argparse
import colorsys
from pathlib import Path

from PIL import Image, ImageEnhance, ImageOps


SIGNAL_BLUE = (0x27, 0x6E, 0xF1)
PALE_BLUE = (0xEA, 0xF0, 0xFF)
INK = (0x0A, 0x0A, 0x0A)
SIGNAL_HUE = colorsys.rgb_to_hls(*(component / 255 for component in SIGNAL_BLUE))[0]


def lerp(a: tuple[int, int, int], b: tuple[int, int, int], t: float) -> tuple[int, int, int]:
    return tuple(round(x + (y - x) * t) for x, y in zip(a, b))


def make_duotone(gray: Image.Image) -> Image.Image:
    channels = [[], [], []]
    for value in range(256):
        if value <= 132:
            color = lerp(INK, SIGNAL_BLUE, value / 132)
        else:
            color = lerp(SIGNAL_BLUE, PALE_BLUE, (value - 132) / 123)
        for channel, component in zip(channels, color):
            channel.append(component)
    return Image.merge("RGB", tuple(gray.point(channel) for channel in channels))


def is_blue_hue(hue: float, saturation: float) -> bool:
    return 0.50 <= hue <= 0.74 and saturation >= 0.10


def signal_blue_with_luminance(lightness: float, saturation: float, *, gentle: bool) -> tuple[int, int, int]:
    target_saturation = max(0.22 if gentle else 0.36, min(0.82, saturation * 0.9))
    if lightness > 0.82:
        target_saturation = min(target_saturation, 0.34 if gentle else 0.46)
    red, green, blue = colorsys.hls_to_rgb(SIGNAL_HUE, lightness, target_saturation)
    return tuple(round(component * 255) for component in (red, green, blue))


def make_screenshot_clean(image: Image.Image) -> Image.Image:
    """Preserve screenshot color and text while normalizing white and blue UI pixels."""
    rgb = image.convert("RGB")
    source_pixels = rgb.load()
    result = rgb.copy()
    result_pixels = result.load()
    for y in range(rgb.height):
        for x in range(rgb.width):
            red, green, blue = source_pixels[x, y]
            hue, lightness, saturation = colorsys.rgb_to_hls(red / 255, green / 255, blue / 255)
            if lightness >= 0.97 and saturation <= 0.08:
                result_pixels[x, y] = (255, 255, 255)
            elif is_blue_hue(hue, saturation):
                result_pixels[x, y] = signal_blue_with_luminance(
                    lightness, saturation, gentle=True
                )
    return result


def make_white_blue(image: Image.Image, gray: Image.Image) -> Image.Image:
    """Strong palette reset for low-text visuals; non-blue structure becomes neutral."""
    white_threshold = 242
    normalized_gray = gray.point(
        lambda value: 255 if value >= white_threshold else round(value * 255 / white_threshold)
    )
    neutral = Image.merge("RGB", (normalized_gray, normalized_gray, normalized_gray))
    rgb = image.convert("RGB")
    source_pixels = rgb.load()
    result = neutral.copy()
    result_pixels = result.load()
    for y in range(rgb.height):
        for x in range(rgb.width):
            red, green, blue = source_pixels[x, y]
            hue, lightness, saturation = colorsys.rgb_to_hls(red / 255, green / 255, blue / 255)
            if is_blue_hue(hue, saturation):
                result_pixels[x, y] = signal_blue_with_luminance(
                    lightness, saturation, gentle=False
                )
    return result


def treat(image: Image.Image, mode: str, contrast: float) -> Image.Image:
    alpha = image.getchannel("A") if image.mode == "RGBA" else None
    gray = ImageOps.grayscale(image.convert("RGB"))
    gray = ImageEnhance.Contrast(gray).enhance(contrast)

    if mode == "original":
        result = image.convert("RGBA" if alpha is not None else "RGB")
    elif mode == "grayscale":
        result = Image.merge("RGB", (gray, gray, gray))
    elif mode == "white-blue":
        result = make_white_blue(image, gray)
    elif mode == "screenshot-clean":
        result = make_screenshot_clean(image)
    elif mode == "pale-blue":
        result = ImageOps.colorize(gray, black=(0x16, 0x18, 0x1D), white=PALE_BLUE)
    elif mode == "signal-duotone":
        result = make_duotone(gray)
    else:
        raise ValueError(f"Unsupported mode: {mode}")

    if alpha is not None:
        result.putalpha(alpha)
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument(
        "--mode",
        choices=("original", "grayscale", "screenshot-clean", "white-blue", "pale-blue", "signal-duotone"),
        default="original",
    )
    parser.add_argument("--contrast", type=float, default=1.08)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.contrast <= 0:
        raise SystemExit("--contrast must be positive")
    if not args.input.is_file():
        raise SystemExit(f"Input image not found: {args.input}")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(args.input) as image:
        result = treat(image, args.mode, args.contrast)
        result.save(args.output)
    print(f"Saved {args.mode} treatment to {args.output}")


if __name__ == "__main__":
    main()
