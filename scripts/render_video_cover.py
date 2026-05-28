from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "video_cover_iem_cologne_2026.png"


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


def text(draw: ImageDraw.ImageDraw, xy: tuple[int, int], value: str, size: int, fill: str, bold: bool = False) -> None:
    draw.text(xy, value, font=font(size, bold), fill=fill)


def centered(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], value: str, size: int, fill: str, bold: bool = False) -> None:
    fnt = font(size, bold)
    bounds = draw.textbbox((0, 0), value, font=fnt)
    x = box[0] + (box[2] - box[0] - (bounds[2] - bounds[0])) // 2
    y = box[1] + (box[3] - box[1] - (bounds[3] - bounds[1])) // 2 - 4
    draw.text((x, y), value, font=fnt, fill=fill)


def rounded(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], fill: str, outline: str | None = None, width: int = 2, radius: int = 18) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def main() -> None:
    width, height = 1920, 1080
    img = Image.new("RGB", (width, height), "#10100d")
    draw = ImageDraw.Draw(img)

    for y in range(height):
        ratio = y / height
        draw.line([(0, y), (width, y)], fill=(int(18 + ratio * 15), int(18 + ratio * 11), int(14 + ratio * 8)))

    # Angular tactical blocks inspired by CS broadcast graphics.
    draw.polygon([(0, 0), (1920, 0), (1920, 210), (1560, 150), (1190, 260), (770, 150), (390, 245), (0, 180)], fill="#2a2619")
    draw.polygon([(0, 1080), (1920, 1080), (1920, 850), (1505, 940), (1170, 820), (735, 960), (365, 845), (0, 930)], fill="#1a1914")
    draw.polygon([(1220, 0), (1920, 0), (1920, 1080), (1510, 1080), (1320, 650), (1500, 265)], fill="#070807")
    draw.polygon([(1450, 0), (1920, 0), (1920, 1080), (1690, 1080), (1540, 610), (1650, 260)], fill="#d58a1d")
    draw.polygon([(1525, 0), (1920, 0), (1920, 1080), (1800, 1080), (1640, 585), (1735, 260)], fill="#f0b42c")

    # Subtle diagonal stripe texture.
    for x in range(-300, width, 92):
        draw.line([(x, 1080), (x + 520, 0)], fill="#29251a", width=3)

    # Main thumbnail text: few words, huge anchor.
    text(draw, (82, 90), "别听玄学预测！", 118, "#f5f2e8", True)
    text(draw, (88, 265), "IEM 科隆", 142, "#ffffff", True)
    text(draw, (88, 430), "最无敌作业", 152, "#ffffff", True)
    text(draw, (92, 612), "来了", 152, "#ffffff", True)

    text(draw, (980, 210), "30000", 250, "#f0b42c", True)
    text(draw, (1338, 460), "次", 112, "#f5f2e8", True)
    text(draw, (1042, 602), "模拟", 124, "#ffffff", True)

    rounded(draw, (92, 845, 650, 940), "#1a1914", "#f0b42c", 5, 16)
    centered(draw, (92, 845, 650, 940), "VRS 模型", 54, "#f5f2e8", True)

    rounded(draw, (690, 845, 1060, 940), "#1a1914", "#d65a1f", 5, 16)
    centered(draw, (690, 845, 1060, 940), "Stage 1", 50, "#f5f2e8", True)

    text(draw, (96, 992), "不是凭感觉，是把赛制跑完 30000 遍。", 46, "#d6cdb7", True)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT)
    print(OUT)


if __name__ == "__main__":
    main()
