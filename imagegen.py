"""Lightweight fallback image generator for the matryoshka prompt app.

This module provides a minimal `make_image` function so the Streamlit UI can
produce a tangible file even when no external model is available. It renders the
prompt text onto a simple textured background; callers can swap this file for a
real generator without changing the app code.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from random import randint
from textwrap import wrap

from PIL import Image, ImageDraw, ImageFilter, ImageFont


def _draw_background(draw: ImageDraw.ImageDraw, width: int, height: int) -> None:
    """Paint a soft paper-like backdrop with a few pastel dots."""

    colors = ["#f7f0e8", "#f0e8dd", "#e9e0d5"]
    for x in range(0, width, 40):
        for y in range(0, height, 40):
            shade = colors[(x + y) % len(colors)]
            draw.rectangle((x, y, x + 40, y + 40), fill=shade)

    # Sprinkle gentle dots to hint at the wallpaper motif.
    accent_colors = ["#d5c3b8", "#c0b0a6", "#e0d0c4", "#b8c6d8", "#d9bcd0"]
    for _ in range(180):
        radius = randint(2, 5)
        cx = randint(0, width)
        cy = randint(0, height)
        color = accent_colors[randint(0, len(accent_colors) - 1)]
        draw.ellipse((cx - radius, cy - radius, cx + radius, cy + radius), fill=color)


def _wrap_text(text: str, chars_per_line: int = 60) -> list[str]:
    lines: list[str] = []
    for block in text.split("\n"):
        lines.extend(wrap(block.strip(), width=chars_per_line) or [""])
    return lines


def make_image(prompt: str, *, width: int = 900, height: int = 1200, output_dir: str = "generated") -> str:
    """Render a simple wallpaper preview with the prompt text overlay.

    Returns the path to the saved PNG file.
    """

    Path(output_dir).mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = Path(output_dir) / f"matryoshka_prompt_{timestamp}.png"

    canvas = Image.new("RGB", (width, height), "#f6eee2")
    draw = ImageDraw.Draw(canvas)

    _draw_background(draw, width, height)

    try:
        title_font = ImageFont.truetype("DejaVuSans-Bold.ttf", 30)
        body_font = ImageFont.truetype("DejaVuSans.ttf", 20)
    except OSError:
        title_font = ImageFont.load_default()
        body_font = ImageFont.load_default()

    title = "Matryoshka Prompt"
    title_w, title_h = draw.textsize(title, font=title_font)
    draw.text(((width - title_w) / 2, 30), title, fill="#4a3a2c", font=title_font)

    body_lines = _wrap_text(prompt, chars_per_line=60)
    y = 100
    for line in body_lines:
        draw.text((40, y), line, fill="#3b2f26", font=body_font)
        y += body_font.getsize(line)[1] + 6

    canvas = canvas.filter(ImageFilter.GaussianBlur(radius=0.25))
    canvas.save(output_path)

    return str(output_path)


__all__ = ["make_image"]
