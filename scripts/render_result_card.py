from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "pickem_result_card.png"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        Path("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"),
        Path("C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf"),
    ]
    for path in candidates:
        if path.exists():
            return ImageFont.truetype(str(path), size=size)
    return ImageFont.load_default()


def rounded(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], fill: str, outline: str | None = None, width: int = 1) -> None:
    draw.rounded_rectangle(box, radius=14, fill=fill, outline=outline, width=width)


def text(draw: ImageDraw.ImageDraw, xy: tuple[int, int], value: str, size: int, fill: str, bold: bool = False) -> None:
    draw.text(xy, value, font=font(size, bold), fill=fill)


def main() -> None:
    width, height = 1600, 900
    img = Image.new("RGB", (width, height), "#07180f")
    draw = ImageDraw.Draw(img)

    for y in range(height):
        ratio = y / height
        r = int(7 + ratio * 4)
        g = int(24 + ratio * 10)
        b = int(15 + ratio * 5)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    draw.polygon([(0, 0), (1600, 0), (1600, 70), (1250, 120), (980, 70), (720, 130), (470, 80), (0, 150)], fill="#123522")
    draw.polygon([(0, 900), (1600, 900), (1600, 780), (1230, 730), (960, 820), (670, 760), (360, 835), (0, 760)], fill="#0b2a1c")

    text(draw, (96, 82), "CS2 PICK'EM MONTE CARLO", 22, "#64f2a4", True)
    text(draw, (96, 128), "IEM Cologne 2026 Stage 1", 62, "#f4fff7", True)
    text(draw, (98, 204), "Reward-optimized picks: maximize P(at least 5 correct)", 28, "#b9d7c5")

    rounded(draw, (1075, 85, 1435, 255), "#123522", "#2b7f4c", 2)
    text(draw, (1105, 125), "30k simulation check", 24, "#b9d7c5")
    text(draw, (1105, 166), "66.8%", 78, "#ffffff", True)
    text(draw, (1107, 226), "P(hits >= 5)", 22, "#b9d7c5")

    panels = [
        ((96, 295, 526, 715), "#0c4f32", "3-0 picks"),
        ((585, 295, 1105, 715), "#105b3b", "Advance picks"),
        ((1164, 295, 1504, 715), "#713047", "0-3 picks"),
    ]
    for box, header, title in panels:
        rounded(draw, box, "#0b2017", "#2b7f4c", 2)
        x1, y1, x2, _ = box
        draw.rounded_rectangle((x1, y1, x2, y1 + 86), radius=14, fill=header)
        text(draw, (x1 + 30, y1 + 26), title, 30, "#f4fff7", True)

    for y, name in [(450, "SINNERS"), (532, "BIG")]:
        draw.ellipse((136, y - 14, 164, y + 14), fill="#28e38b")
        text(draw, (186, y - 18), name, 32, "#eafff1", True)
    text(draw, (126, 640), "Lottery slots: upside matters,", 22, "#9db8a8")
    text(draw, (126, 672), "but do not burn the safest advances.", 22, "#9db8a8")

    advance = [("GamerLegion", 615, 420), ("B8", 875, 420), ("BetBoom", 615, 492), ("MIBR", 875, 492), ("Lynn Vision", 615, 564), ("HEROIC", 875, 564)]
    for name, x, y in advance:
        text(draw, (x, y), name, 32, "#eafff1", True)
    text(draw, (615, 660), "Stable-score slots: high advancement probability.", 22, "#9db8a8")

    for y, name in [(450, "FlyQuest"), (532, "THUNDER"), (572, "dOWNUNDER")]:
        if y != 572:
            draw.ellipse((1204, y - 14, 1232, y + 14), fill="#ff5277")
        text(draw, (1254, y - 18), name, 32, "#eafff1", True)
    text(draw, (1194, 640), "Chosen for reward threshold,", 22, "#9db8a8")
    text(draw, (1194, 672), "not max average hits.", 22, "#9db8a8")

    rounded(draw, (96, 775, 1504, 833), "#07130e", "#1f5a35", 1)
    text(draw, (124, 792), "github.com/lshhhhhhh/cs2-pickem-monte-carlo", 24, "#c7f7d9", True)
    text(draw, (795, 795), "VRS: 2026-05-22 | Stage 1 only | Model result, not a guarantee", 22, "#9db8a8")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT)
    print(OUT)


if __name__ == "__main__":
    main()
