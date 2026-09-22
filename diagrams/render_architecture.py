"""Render the Day 1 architecture PNG; requires the optional Pillow package."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def render() -> Path:
    """Draw the planned pipeline and save it beside this source file."""
    image = Image.new("RGB", (1500, 1700), "#f5f7fb")
    draw = ImageDraw.Draw(image)
    title_font = ImageFont.load_default(size=42)
    heading_font = ImageFont.load_default(size=27)
    body_font = ImageFont.load_default(size=21)
    ink = "#172b4d"

    def centered(text: str, x: int, y: int, font=body_font, fill=ink) -> None:
        draw.text((x, y), text, font=font, fill=fill, anchor="mm")

    def box(x: int, y: int, width: int, heading: str, detail: str, color: str) -> None:
        draw.rounded_rectangle((x - width // 2, y, x + width // 2, y + 92),
                               radius=16, fill=color, outline="#b9c7d9", width=2)
        centered(heading, x, y + 31, heading_font)
        centered(detail, x, y + 66)

    def arrow(points: list[tuple[int, int]]) -> None:
        draw.line(points, fill="#526783", width=4, joint="curve")
        x, y = points[-1]
        draw.polygon([(x, y), (x - 9, y - 14), (x + 9, y - 14)], fill="#526783")

    centered("SearchFlow Analytics", 750, 55, title_font)
    centered("Planned Version 1 pipeline | Day 1 architecture", 750, 104)
    box(750, 145, 800, "CLI orchestration", "Select dataset size, integer target, and algorithm(s)", "#e3ebff")
    arrow([(750, 237), (750, 275)])
    box(750, 275, 700, "Generate integers / use existing CSV", "Required sizes: 100, 1,000, and 10,000", "#e4f4f1")
    arrow([(750, 367), (750, 405)])
    box(750, 405, 700, "Load CSV", "Convert stored values into integer data", "#e4f4f1")
    arrow([(750, 497), (750, 535)])
    box(750, 535, 700, "Validate and prepare", "Numeric values, nonempty data, expected count", "#e4f4f1")
    arrow([(750, 627), (750, 657), (410, 657), (410, 695)])
    arrow([(750, 627), (750, 657), (1090, 657), (1090, 695)])
    box(410, 695, 580, "Original-order data", "Preserve the unsorted list", "#fff0d6")
    box(1090, 695, 580, "Sorted copy", "Prepare binary-search input", "#e3ebff")

    draw.rounded_rectangle((75, 855, 1425, 1050), radius=18,
                           fill="#edf0f6", outline="#8294ad", width=2)
    centered("Time each search call using a high-resolution clock", 750, 882)
    arrow([(410, 787), (410, 915)])
    arrow([(1090, 787), (1090, 915)])
    box(410, 915, 580, "Linear search", "Matching index or -1 | O(n) worst case", "#fff0d6")
    box(1090, 915, 580, "Binary search", "Matching index or -1 | O(log n) worst case", "#e3ebff")
    arrow([(410, 1007), (410, 1080), (750, 1080), (750, 1120)])
    arrow([(1090, 1007), (1090, 1080), (750, 1080), (750, 1120)])
    box(750, 1120, 780, "Collect measured results", "Algorithm, size, target, found, index, execution time", "#e4f4f1")
    arrow([(750, 1212), (750, 1250)])
    box(750, 1250, 780, "Save benchmark CSV", "results/performance_results.csv", "#e4f4f1")
    arrow([(750, 1342), (750, 1372), (410, 1372), (410, 1410)])
    arrow([(750, 1342), (750, 1372), (1090, 1372), (1090, 1410)])
    box(410, 1410, 580, "CLI display", "Found status, input-list index, measured time", "#e3ebff")
    box(1090, 1410, 580, "Written analysis", "Big O, measured trends, recommendations", "#e3ebff")
    centered("Search timing excludes loading, sorting, CSV writes, and terminal output.", 750, 1570)
    centered("Discuss sorting cost separately when comparing one-time and repeated searches.", 750, 1610)
    output = Path(__file__).resolve().with_name("pipeline_architecture.png")
    image.save(output)
    return output


if __name__ == "__main__":
    print(render())
