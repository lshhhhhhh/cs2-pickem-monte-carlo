from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "vrs_winrate_explainer.png"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        Path("C:/Windows/Fonts/msyhbd.ttc" if bold else "C:/Windows/Fonts/msyh.ttc"),
        Path("C:/Windows/Fonts/simhei.ttf"),
        Path("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"),
    ]
    for path in candidates:
        if path.exists():
            return ImageFont.truetype(str(path), size=size)
    return ImageFont.load_default()


def logistic(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))


def bo3_from_map_prob(p_map: float) -> float:
    return p_map * p_map * (3.0 - 2.0 * p_map)


def text(draw: ImageDraw.ImageDraw, xy: tuple[int, int], value: str, size: int, fill: str, bold: bool = False) -> None:
    draw.text(xy, value, font=font(size, bold), fill=fill)


def rounded(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], fill: str, outline: str, width: int = 2, radius: int = 22) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def main() -> None:
    width, height = 1920, 1080
    img = Image.new("RGB", (width, height), "#07170f")
    draw = ImageDraw.Draw(img)

    for y in range(height):
        ratio = y / height
        draw.line([(0, y), (width, y)], fill=(6, int(22 + ratio * 24), int(15 + ratio * 8)))

    draw.polygon([(0, 0), (1920, 0), (1920, 120), (1540, 190), (1180, 125), (820, 205), (420, 128), (0, 220)], fill="#10351f")
    draw.polygon([(0, 1080), (1920, 1080), (1920, 930), (1520, 850), (1190, 950), (760, 880), (370, 990), (0, 890)], fill="#0b281b")

    text(draw, (90, 72), "VRS 分差怎么反推胜率？", 64, "#f4fff7", True)
    text(draw, (94, 154), "把两队 VRS 分数差，映射成单图胜率；BO3 再由单图胜率推出来。", 32, "#b8d8c5")

    formula_box = (90, 250, 860, 505)
    rounded(draw, formula_box, "#0b2118", "#2d8050", 2)
    text(draw, (132, 292), "模型核心", 34, "#70f0aa", True)
    text(draw, (132, 360), "单图胜率 = logistic((A分 - B分) / 400)", 32, "#f4fff7", True)
    text(draw, (132, 425), "BO3胜率 = p² × (3 - 2p)", 32, "#f4fff7", True)

    chart_box = (940, 250, 1810, 810)
    rounded(draw, chart_box, "#0b2118", "#2d8050", 2)
    text(draw, (980, 292), "示例：VRS 领先越多，BO3 优势越明显", 34, "#70f0aa", True)

    diffs = [0, 50, 100, 200, 300, 400]
    scale = 400.0
    rows = []
    for diff in diffs:
        p_map = logistic(diff / scale)
        p_bo3 = bo3_from_map_prob(p_map)
        rows.append((diff, p_map, p_bo3))

    y0 = 375
    text(draw, (995, y0), "VRS分差", 28, "#b8d8c5", True)
    text(draw, (1215, y0), "单图胜率", 28, "#b8d8c5", True)
    text(draw, (1455, y0), "BO3胜率", 28, "#b8d8c5", True)
    draw.line((990, y0 + 48, 1768, y0 + 48), fill="#245d3d", width=2)

    for idx, (diff, p_map, p_bo3) in enumerate(rows):
        y = y0 + 82 + idx * 62
        fill = "#f4fff7" if idx % 2 == 0 else "#d7f2e0"
        text(draw, (1015, y), f"+{diff}", 30, fill, True)
        text(draw, (1235, y), f"{p_map * 100:.1f}%", 30, fill, True)
        text(draw, (1475, y), f"{p_bo3 * 100:.1f}%", 30, "#79f2ad", True)
        bar_x = 1595
        bar_w = int(165 * p_bo3)
        draw.rounded_rectangle((bar_x, y + 8, bar_x + 165, y + 29), radius=10, fill="#123321")
        draw.rounded_rectangle((bar_x, y + 8, bar_x + bar_w, y + 29), radius=10, fill="#29e38b")

    explain_box = (90, 575, 860, 810)
    rounded(draw, explain_box, "#0b2118", "#2d8050", 2)
    text(draw, (132, 618), "为什么看起来反直觉？", 34, "#70f0aa", True)
    text(draw, (132, 685), "Pick'Em 优化的不是“谁最强”，", 34, "#f4fff7", True)
    text(draw, (132, 742), "而是“哪套选择最容易拿到 5 分”。", 34, "#f4fff7", True)

    footer = (90, 885, 1810, 970)
    rounded(draw, footer, "#07130e", "#1f5a35", 1, 18)
    text(draw, (126, 912), "CS2 Pick'Em Monte Carlo | VRS logistic scale = 400 | Stage 1 only", 30, "#c7f7d9", True)
    text(draw, (126, 950), "示意图：实际结果还取决于首轮对阵、瑞士轮路径、BO1/BO3 赛制和奖励阈值。", 22, "#9db8a8")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT)
    print(OUT)


if __name__ == "__main__":
    main()
