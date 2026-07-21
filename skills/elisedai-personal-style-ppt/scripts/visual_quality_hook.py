#!/usr/bin/env python3
"""Advisory visual-quality hook for Signal Blue editorial PPT work.

The hook never blocks delivery. It inspects available builder code and raster assets,
then prints concise suggestions that the author can accept or ignore with judgment.
"""

from __future__ import annotations

import argparse
import json
import re
import zipfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageOps, ImageStat


IMAGE_CALL_RE = re.compile(
    r"image\([^\n]*?[\"']([^\"']+\.(?:png|jpe?g|webp))[\"'][^\n]*?,\s*"
    r"([0-9.]+)\s*,\s*([0-9.]+)\s*,\s*([0-9.]+)\s*,\s*([0-9.]+)",
    re.IGNORECASE,
)
GENERATED_CALL_RE = re.compile(
    r"generatedImage\([^\n]*?[\"']([^\"']+\.(?:png|jpe?g|webp))[\"']",
    re.IGNORECASE,
)
SLIDE_BLOCK_RE = re.compile(r"(?m)^//\s*(\d{1,2})(?:\s|$)")


def resolve_manifest_path(value: str, manifest_path: Path) -> Path:
    candidate = Path(value).expanduser()
    if not candidate.is_absolute():
        candidate = manifest_path.parent / candidate
    return candidate.resolve()


def dimension_pair(value: object) -> tuple[float, float]:
    """Accept documented objects and the convenient [width, height] shorthand."""
    if isinstance(value, dict):
        return float(value.get("width", 0)), float(value.get("height", 0))
    if isinstance(value, (list, tuple)) and len(value) >= 2:
        return float(value[0]), float(value[1])
    return 0.0, 0.0


def normalized_box_to_pixels(box: object, width: int, height: int) -> tuple[float, float, float, float]:
    """Accept {x,y,width,height,unit} or normalized [x,y,width,height]."""
    if isinstance(box, dict):
        x = float(box.get("x", 0))
        y = float(box.get("y", 0))
        w = float(box.get("width", 1))
        h = float(box.get("height", 1))
        unit = str(box.get("unit", "normalized"))
    elif isinstance(box, (list, tuple)) and len(box) >= 4:
        x, y, w, h = (float(box[index]) for index in range(4))
        unit = "normalized"
    else:
        x, y, w, h, unit = 0.0, 0.0, 1.0, 1.0, "normalized"
    if unit == "pixels":
        return x, y, x + w, y + h
    return x * width, y * height, (x + w) * width, (y + h) * height


def effective_visible_rect(
    source_width: int,
    source_height: int,
    frame_width: float,
    frame_height: float,
    crop: object,
    fit: str,
) -> tuple[tuple[float, float, float, float], float]:
    """Return the centered source rectangle that remains visible and extra cover-loss ratio."""
    if isinstance(crop, dict):
        crop_left = float(crop.get("left", 0))
        crop_top = float(crop.get("top", 0))
        crop_right = float(crop.get("right", 0))
        crop_bottom = float(crop.get("bottom", 0))
    elif isinstance(crop, (list, tuple)) and len(crop) >= 4:
        crop_left, crop_top, crop_right, crop_bottom = (float(crop[index]) for index in range(4))
    else:
        crop_left = crop_top = crop_right = crop_bottom = 0.0
    left = max(0.0, min(1.0, crop_left)) * source_width
    top = max(0.0, min(1.0, crop_top)) * source_height
    right = (1 - max(0.0, min(1.0, crop_right))) * source_width
    bottom = (1 - max(0.0, min(1.0, crop_bottom))) * source_height
    if right <= left or bottom <= top:
        return (left, top, right, bottom), 1.0

    cropped_width = right - left
    cropped_height = bottom - top
    explicit_area = cropped_width * cropped_height
    if fit != "cover" or frame_width <= 0 or frame_height <= 0:
        return (left, top, right, bottom), 0.0

    source_ratio = cropped_width / cropped_height
    frame_ratio = frame_width / frame_height
    if source_ratio > frame_ratio:
        visible_width = cropped_height * frame_ratio
        inset = (cropped_width - visible_width) / 2
        left += inset
        right -= inset
    elif source_ratio < frame_ratio:
        visible_height = cropped_width / frame_ratio
        inset = (cropped_height - visible_height) / 2
        top += inset
        bottom -= inset
    visible_area = max(0.0, right - left) * max(0.0, bottom - top)
    return (left, top, right, bottom), max(0.0, 1 - visible_area / explicit_area)


def rect_intersection_area(first: tuple[float, float, float, float], second: tuple[float, float, float, float]) -> float:
    left = max(first[0], second[0])
    top = max(first[1], second[1])
    right = min(first[2], second[2])
    bottom = min(first[3], second[3])
    return max(0.0, right - left) * max(0.0, bottom - top)


def rect_area(rect: tuple[float, float, float, float]) -> float:
    return max(0.0, rect[2] - rect[0]) * max(0.0, rect[3] - rect[1])


def build_crop_review(entries: list[dict], manifest_path: Path, report_dir: Path) -> Path | None:
    panels: list[Image.Image] = []
    for entry in entries:
        source_value = entry.get("source")
        if not source_value:
            continue
        source_path = resolve_manifest_path(str(source_value), manifest_path)
        if not source_path.is_file():
            continue
        try:
            source = Image.open(source_path).convert("RGB")
        except OSError:
            continue
        frame_width, frame_height = dimension_pair(entry.get("frame", {}))
        visible, _ = effective_visible_rect(
            source.width,
            source.height,
            frame_width,
            frame_height,
            entry.get("crop", {}),
            str(entry.get("fit", "cover")),
        )
        draw = ImageDraw.Draw(source)
        draw.rectangle(visible, outline=(220, 38, 38), width=max(3, source.width // 450))
        required = entry.get("required_region")
        if isinstance(required, (dict, list, tuple)):
            required_rect = normalized_box_to_pixels(required, source.width, source.height)
            draw.rectangle(required_rect, outline=(39, 110, 241), width=max(3, source.width // 450))
        source.thumbnail((560, 300))
        panel = Image.new("RGB", (580, 340), "white")
        panel.paste(source, ((580 - source.width) // 2, 28))
        label = f"slide {entry.get('slide', '?')} | {source_path.name.encode('ascii', 'replace').decode('ascii')[:58]}"
        ImageDraw.Draw(panel).text((10, 8), label, fill=(21, 21, 21))
        panels.append(panel)
    if not panels:
        return None
    columns = 2
    rows = (len(panels) + columns - 1) // columns
    sheet = Image.new("RGB", (columns * 580, rows * 340 + 28), (238, 238, 238))
    ImageDraw.Draw(sheet).text((12, 8), "RED = final visible crop | BLUE = required evidence", fill=(21, 21, 21))
    for index, panel in enumerate(panels):
        x = (index % columns) * 580
        y = 28 + (index // columns) * 340
        sheet.paste(ImageOps.expand(panel, border=1, fill=(190, 190, 190)), (x, y))
    report_dir.mkdir(parents=True, exist_ok=True)
    output = report_dir / "evidence-crop-review.png"
    sheet.save(output)
    return output


def inspect_evidence_manifest(path: Path, report_dir: Path | None = None) -> list[str]:
    if not path.is_file():
        return [f"未找到证据裁切清单：{path}"]
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return [f"无法读取证据裁切清单：{path}"]
    entries = payload.get("evidence", payload) if isinstance(payload, dict) else payload
    if not isinstance(entries, list):
        return ["证据裁切清单应为数组，或包含 evidence 数组。"]

    suggestions: list[str] = []
    group_items: dict[str, list[dict]] = {}
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        slide = entry.get("slide", "?")
        source_value = entry.get("source")
        if not source_value:
            suggestions.append(f"第 {slide} 页证据项缺少 source。")
            continue
        source_path = resolve_manifest_path(str(source_value), path)
        if not source_path.is_file():
            suggestions.append(f"第 {slide} 页未找到源图：{source_path}")
            continue
        try:
            with Image.open(source_path) as source:
                source_width, source_height = source.size
        except OSError:
            suggestions.append(f"第 {slide} 页无法读取源图：{source_path.name}")
            continue

        frame_width, frame_height = dimension_pair(entry.get("frame", {}))
        fit = str(entry.get("fit", "cover"))
        visible, cover_loss = effective_visible_rect(
            source_width,
            source_height,
            frame_width,
            frame_height,
            entry.get("crop", {}),
            fit,
        )
        if cover_loss > 0.08:
            suggestions.append(
                f"第 {slide} 页 {source_path.name} 在显式 crop 后又被 cover 居中裁掉 {cover_loss:.0%}；"
                "请预裁成最终比例、改用 contain，或把必保留区域写入 required_region。"
            )

        required = entry.get("required_region")
        if isinstance(required, (dict, list, tuple)):
            required_rect = normalized_box_to_pixels(required, source_width, source_height)
            required_area = rect_area(required_rect)
            coverage = rect_intersection_area(visible, required_rect) / required_area if required_area else 0
            if coverage < 0.98:
                suggestions.append(
                    f"第 {slide} 页最终可见区域只保留了必需证据的 {coverage:.0%}：{entry.get('evidence', source_path.name)}。"
                    "这会造成界面、句子或人物被截残。"
                )
            occupancy = rect_intersection_area(visible, required_rect) / max(1.0, rect_area(visible))
            if occupancy < float(entry.get("min_evidence_occupancy", 0.32)):
                suggestions.append(
                    f"第 {slide} 页必需证据仅占最终截图约 {occupancy:.0%}；舞台、浏览器或空白可能过多，"
                    "请裁紧或把关键状态改为可编辑文字。"
                )

        min_width, min_height = dimension_pair(entry.get("min_frame", {}))
        if frame_width < min_width or frame_height < min_height:
            suggestions.append(
                f"第 {slide} 页证据框为 {frame_width:g}×{frame_height:g}，低于清单要求的 "
                f"{min_width:g}×{min_height:g}；截图文字可能不可读。"
            )
        group = entry.get("group")
        if group:
            group_items.setdefault(str(group), []).append(entry)

    for group, items in group_items.items():
        if len(items) < 2:
            continue
        first = items[0]
        baseline = (
            *dimension_pair(first.get("frame", {})),
            first.get("radius", 10), first.get("caption_y"), first.get("fit", "cover"),
        )
        mismatched = []
        for item in items[1:]:
            current = (
                *dimension_pair(item.get("frame", {})),
                item.get("radius", 10), item.get("caption_y"), item.get("fit", "cover"),
            )
            if current != baseline:
                mismatched.append(str(item.get("slide", "?")))
        if mismatched:
            suggestions.append(
                f"证据组 {group} 的可视框、圆角、fit 或说明基线不一致，涉及第 "
                + "、".join(mismatched)
                + " 页。"
            )

    if report_dir:
        report = build_crop_review(entries, path, report_dir)
        if report:
            suggestions.append(f"已生成裁切审阅图：{report}（红框是最终可见区域，蓝框是必保留证据）。")
    return suggestions


def image_groups(text: str) -> list[tuple[str, list[tuple[str, float, float, float, float]]]]:
    """Return numeric slide blocks with parsed evidence-image geometry."""
    matches = list(SLIDE_BLOCK_RE.finditer(text))
    groups: list[tuple[str, list[tuple[str, float, float, float, float]]]] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        calls = [
            (filename, float(x), float(y), float(w), float(h))
            for filename, x, y, w, h in IMAGE_CALL_RE.findall(text[match.end():end])
        ]
        if len(calls) >= 2:
            groups.append((match.group(1), calls))
    return groups


def mismatched_same_role_groups(text: str) -> list[str]:
    """Flag likely horizontal pairs or vertical stacks whose visible frames differ."""
    findings: list[str] = []
    for slide_number, calls in image_groups(text):
        mismatches: set[str] = set()
        for index, first in enumerate(calls):
            for second in calls[index + 1:]:
                f_name, f_x, f_y, f_w, f_h = first
                s_name, s_x, s_y, s_w, s_h = second
                horizontal_pair = abs(f_y - s_y) <= 20 and abs(f_x - s_x) >= 80
                vertical_pair = abs(f_x - s_x) <= 20 and abs(f_y - s_y) >= 60
                if not (horizontal_pair or vertical_pair):
                    continue
                width_delta = abs(f_w - s_w) / max(f_w, s_w)
                height_delta = abs(f_h - s_h) / max(f_h, s_h)
                if width_delta > 0.05 or height_delta > 0.05:
                    mismatches.add(f"{f_name} ↔ {s_name}")
        if mismatches:
            findings.append(f"第 {int(slide_number)} 页：" + "、".join(sorted(mismatches)))
    return findings


def inspect_builder(path: Path, has_evidence_manifest: bool = False) -> list[str]:
    if not path.is_file():
        return [f"未找到构建文件：{path}"]
    text = path.read_text(encoding="utf-8", errors="ignore")
    calls = IMAGE_CALL_RE.findall(text)
    suggestions: list[str] = []
    generated = GENERATED_CALL_RE.findall(text) + [
        item[0] for item in calls if "generated" in item[0].lower()
    ]
    generic_source = [item for item in calls if re.fullmatch(r"image\d+\.(?:png|jpe?g|webp)", item[0], re.I)]
    small = [item for item in calls if float(item[3]) < 360 or float(item[4]) < 110]
    group_mismatches = mismatched_same_role_groups(text)

    if calls and not generated and len(generic_source) / len(calls) >= 0.8:
        suggestions.append(
            "整套构建几乎只引用 imageNN 形式的原始素材，未发现明确的 generated 配图；请回看抽象观点页，判断隐喻或几何画面是否比截图更有解释力。"
        )
    if len(generic_source) >= 8 and not generated:
        suggestions.append(
            "证据图片使用频率较高且视觉来源单一；建议挑选关键证据，其余页面考虑纯文字、原生结构或概念配图。"
        )
    if small:
        names = "、".join(item[0] for item in small[:6])
        suggestions.append(
            f"发现可能过小的证据图：{names}。若截图文字承担证据，请进一步裁剪；全页查看时不可读就不应保留整图。"
        )
    if group_mismatches:
        suggestions.append(
            "发现可能属于同组、但可视框尺寸不一致的图片："
            + "；".join(group_mismatches[:6])
            + "。请统一宽高、圆角、间距与基线；长宽比不同则裁切证据区，不要拉伸。"
        )
    if len(calls) >= 2 and not ("roundRect" in text and "borderRadius" in text):
        suggestions.append(
            "构建中存在多张证据图，但未检测到统一的圆角图片遮罩。包含式截图或纪实照片建议使用一致的 8–12 px 圆角；全出血图可保留直角。"
        )
    pale_is_used = bool(
        re.search(r"(?:rect|box)\([^\n]*(?:\bPALE\b|C\.pale|#EAF1FF)", text, re.IGNORECASE)
    )
    if pale_is_used:
        suggestions.append(
            "构建中使用了浅蓝色字段；请确认它只属于图片内部，而不是截图背后的装饰矩形。"
        )
    if calls and len(calls) / max(1, text.count("deck.slides.add") + text.count("base(")) > 0.8:
        suggestions.append(
            "图片几乎覆盖每个内容节拍；请确认强观点页没有因为“必须放图”而加入弱证据。"
        )
    if not has_evidence_manifest and re.search(r"\bcrop\s*[:=]", text) and re.search(r"cover", text, re.I):
        suggestions.append(
            "构建器同时使用 crop 与 cover，但未提供 evidence-manifest.json；Hook 无法判断居中二次裁切是否截掉关键证据。"
        )
    return suggestions


def image_metrics(path: Path) -> tuple[float, float, float]:
    with Image.open(path) as image:
        rgb = image.convert("RGB")
        sample = rgb.copy()
        sample.thumbnail((640, 640))
        hsv = sample.convert("HSV")
        saturation = ImageStat.Stat(hsv.getchannel("S")).mean[0] / 255
        edges = sample.convert("L").filter(ImageFilter.FIND_EDGES)
        histogram = edges.histogram()
        total = sum(histogram) or 1
        edge_density = sum(histogram[48:]) / total
        width, height = rgb.size
        megapixels = width * height / 1_000_000
    return saturation, edge_density, megapixels


def inspect_assets(directory: Path) -> list[str]:
    if not directory.is_dir():
        return [f"未找到素材目录：{directory}"]
    suggestions: list[str] = []
    risky: set[str] = set()
    tiny: set[str] = set()
    for path in sorted(directory.rglob("*")):
        if not path.is_file():
            continue
        if path.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp"}:
            continue
        try:
            saturation, edge_density, megapixels = image_metrics(path)
        except OSError:
            continue
        if "treated" in path.parts and edge_density > 0.16 and saturation > 0.10 and any(
            token in path.stem.lower() for token in ("white", "blue", "duotone", "treated", "image")
        ):
            risky.add(path.name)
        if megapixels < 0.12:
            tiny.add(path.name)
    if risky:
        suggestions.append(
            "这些素材可能是文字密集 UI 且经过较强改色："
            + "、".join(sorted(risky)[:8])
            + "。优先用 screenshot-clean 或原色降饱和，避免破坏文字抗锯齿。"
        )
    if tiny:
        suggestions.append(
            "这些素材原始分辨率偏低：" + "、".join(sorted(tiny)[:8]) + "。不要再缩成难以辨认的截图缩略图。"
        )

    source_dir = directory / "source"
    treated_dir = directory / "treated"
    color_loss: list[str] = []
    if source_dir.is_dir() and treated_dir.is_dir():
        source_by_stem = {
            path.stem: path
            for path in source_dir.rglob("*")
            if path.is_file() and path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}
        }
        for treated in treated_dir.rglob("*"):
            if not treated.is_file() or treated.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp"}:
                continue
            source = source_by_stem.get(treated.stem)
            if source is None:
                continue
            try:
                source_saturation, _, _ = image_metrics(source)
                treated_saturation, _, _ = image_metrics(treated)
            except OSError:
                continue
            if source_saturation >= 0.08 and treated_saturation < max(0.025, source_saturation * 0.4):
                color_loss.append(treated.name)
    if color_loss:
        suggestions.append(
            "这些处理图相对源图出现明显色彩流失："
            + "、".join(color_loss[:8])
            + "。截图、人物和纪实照片默认应保留原色；确认灰度化具有明确叙事理由。"
        )
    return suggestions


def inspect_plan(path: Path) -> list[str]:
    if not path.is_file():
        return [
            "没有找到可选的 visual-plan.json；如果素材复杂，可先记录每页的 visual_role、asset_action 和一句理由，方便回看选择是否单一。"
        ]
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return [f"无法读取视觉计划：{path}"]
    slides = payload.get("slides", payload) if isinstance(payload, dict) else payload
    if not isinstance(slides, list):
        return ["视觉计划应为数组，或包含 slides 数组。"]
    roles = [str(item.get("visual_role", "")) for item in slides if isinstance(item, dict)]
    if roles and len(set(roles)) == 1:
        return [f"视觉计划全部选择了 {roles[0]}；请确认这是叙事需要，而不是默认动作。"]
    return []


def inspect_pptx_fonts(path: Path) -> list[str]:
    if not path.is_file():
        return [f"未找到最终 PPTX：{path}"]

    suggestions: list[str] = []
    skill_root = Path(__file__).resolve().parent.parent
    optional_fonts = [
        skill_root / "assets" / "fonts" / "TencentSans-W3.ttf",
        skill_root / "assets" / "fonts" / "TencentSans-W7.ttf",
    ]
    missing_assets = [font.name for font in optional_fonts if not font.is_file() or font.stat().st_size == 0]
    if missing_assets:
        suggestions.append(
            "公开版 Skill 未内置腾讯字体：" + "、".join(missing_assets) + "。确认本机已有授权字体，或使用文档中的 Source Han Sans / Noto Sans CJK 兼容方案。"
        )

    try:
        with zipfile.ZipFile(path) as package:
            members = package.namelist()
            xml_members = [
                member
                for member in members
                if member.endswith(".xml") and (member.startswith("ppt/slides/") or member.startswith("ppt/theme/"))
            ]
            referenced: set[str] = set()
            for member in xml_members:
                payload = package.read(member).decode("utf-8", errors="ignore")
                referenced.update(re.findall(r'typeface="([^"]+)"', payload))
            embedded = [member for member in members if member.startswith("ppt/fonts/") and not member.endswith("/")]
    except (OSError, zipfile.BadZipFile):
        return [f"无法读取 PPTX 字体信息：{path}"]

    tencent_references = sorted(name for name in referenced if "tencentsans" in name.lower() or "腾讯体" in name)
    if not tencent_references:
        suggestions.append(
            "最终 PPTX 未检测到 Tencent Sans 字体引用；请确认构建器没有回退到 Calibri、苹方或微软雅黑。"
        )
    elif not embedded:
        suggestions.append(
            "最终 PPTX 引用了 "
            + "、".join(tencent_references)
            + "，但未检测到 ppt/fonts/ 嵌入字体部件。确认接收方已有授权字体，或交付兼容字体版本；不要把网页预览当作字体一致性证明。"
        )
    else:
        suggestions.append(
            f"最终 PPTX 检测到 {len(embedded)} 个嵌入字体部件；仍需在目标 PowerPoint 环境确认授权、字形与换行。"
        )
    return suggestions


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase", choices=("plan", "assets", "build", "final"), required=True)
    parser.add_argument("--plan", type=Path)
    parser.add_argument("--assets-dir", type=Path)
    parser.add_argument("--builder", type=Path)
    parser.add_argument("--pptx", type=Path)
    parser.add_argument("--evidence-manifest", type=Path)
    parser.add_argument("--report-dir", type=Path)
    args = parser.parse_args()

    suggestions: list[str] = []
    if args.phase == "plan" and args.plan:
        suggestions.extend(inspect_plan(args.plan))
    if args.phase in {"assets", "final"} and args.assets_dir:
        suggestions.extend(inspect_assets(args.assets_dir))
    if args.phase in {"assets", "final"} and args.evidence_manifest:
        suggestions.extend(inspect_evidence_manifest(args.evidence_manifest, args.report_dir))
    if args.phase in {"build", "final"} and args.builder:
        suggestions.extend(inspect_builder(args.builder, bool(args.evidence_manifest)))
    if args.phase == "final" and args.pptx:
        suggestions.extend(inspect_pptx_fonts(args.pptx))

    if not suggestions:
        print(f"[elisedai-ppt-hook:{args.phase}] 未发现明显风险；继续使用视觉判断并进行全尺寸检查。")
        return
    print(f"[elisedai-ppt-hook:{args.phase}] 建议复看：")
    for suggestion in suggestions:
        print(f"- {suggestion}")


if __name__ == "__main__":
    main()
