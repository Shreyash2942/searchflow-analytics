"""Capture and render reproducible Day 7 terminal evidence as PNG files."""

from __future__ import annotations

import csv
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = Path(__file__).resolve().parent


def _font(size: int):
    """Load a readable monospace font available on Windows or fall back safely."""
    candidates = [
        Path("C:/Windows/Fonts/consola.ttf"),
        Path("C:/Windows/Fonts/cour.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def _capture(inputs: str) -> str:
    """Run the real interactive CLI and return combined terminal output."""
    completed = subprocess.run(
        [sys.executable, "main.py", "--interactive"],
        cwd=ROOT,
        input=inputs,
        text=True,
        capture_output=True,
        check=True,
    )
    return completed.stdout + completed.stderr


def _wrapped_lines(text: str, width: int = 112) -> list[str]:
    """Wrap long output lines while retaining blank lines from the terminal."""
    lines: list[str] = []
    for original in text.replace("\r\n", "\n").splitlines():
        if not original:
            lines.append("")
            continue
        while len(original) > width:
            lines.append(original[:width])
            original = original[width:]
        lines.append(original)
    return lines


def _render_terminal(name: str, title: str, output: str) -> Path:
    """Render captured CLI output in a terminal-style evidence image."""
    body_font = _font(23)
    title_font = _font(30)
    small_font = _font(18)
    lines = _wrapped_lines(output)
    line_height = 31
    height = max(430, 132 + line_height * len(lines))
    image = Image.new("RGB", (1600, height), "#0b1220")
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((28, 24, 1572, height - 24), radius=18,
                           fill="#111c2e", outline="#334866", width=2)
    draw.ellipse((58, 49, 74, 65), fill="#ff6b6b")
    draw.ellipse((84, 49, 100, 65), fill="#ffd166")
    draw.ellipse((110, 49, 126, 65), fill="#06d6a0")
    draw.text((155, 43), title, font=title_font, fill="#dbeafe")
    draw.text((155, 82), "Captured from the SearchFlow Analytics interactive CLI",
              font=small_font, fill="#8da7c7")
    y = 128
    for line in lines:
        draw.text((62, y), line, font=body_font, fill="#d7e3f4")
        y += line_height
    path = OUTPUT / name
    image.save(path)
    return path


def _render_benchmark() -> Path:
    """Render all saved benchmark rows as a readable final-results image."""
    body_font = _font(20)
    title_font = _font(30)
    small_font = _font(18)
    rows = list(csv.DictReader((ROOT / "results/performance_results.csv").open(
        newline="", encoding="utf-8")))
    header = "algorithm  size  target  found  index  seconds/search"
    lines = [header, "-" * len(header)]
    for row in rows:
        lines.append(
            f"{row['algorithm']:<9} {int(row['dataset_size']):>5} "
            f"{int(row['target']):>7} {row['found']:<5} {int(row['index']):>6} "
            f"{float(row['execution_time']):.9g}"
        )
    line_height = 29
    height = 150 + line_height * len(lines)
    image = Image.new("RGB", (1600, height), "#0b1220")
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((28, 24, 1572, height - 24), radius=18,
                           fill="#111c2e", outline="#334866", width=2)
    draw.text((62, 48), "SearchFlow Analytics — Final Benchmark Results",
              font=title_font, fill="#dbeafe")
    draw.text((62, 88), "results/performance_results.csv | 24 rows | median batch means",
              font=small_font, fill="#8da7c7")
    y = 126
    for index, line in enumerate(lines):
        color = "#7dd3fc" if index < 2 else "#d7e3f4"
        draw.text((62, y), line, font=body_font, fill=color)
        y += line_height
    path = OUTPUT / "final_benchmark_results.png"
    image.save(path)
    return path


def render() -> list[Path]:
    """Capture the required success, missing, menu, and benchmark evidence."""
    captures = [
        ("linear_100_success.png", "Linear search — 100 elements", "1\n83810\n1\nq\n"),
        ("binary_1000_success.png", "Binary search — 1,000 elements", "2\n96542\n2\nq\n"),
        ("both_10000_success.png", "Both algorithms — 10,000 elements", "3\n27080\n3\nq\n"),
        ("missing_target.png", "Missing target — comparison", "1\n-1\n3\nq\n"),
        ("main_menu.png", "SearchFlow Analytics — main menu", "q\n"),
    ]
    paths = [_render_terminal(name, title, _capture(inputs))
             for name, title, inputs in captures]
    paths.append(_render_benchmark())
    return paths


if __name__ == "__main__":
    for path in render():
        print(path)
