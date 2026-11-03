from math import cos, pi, sin
from pathlib import Path
import webbrowser


def create_star_image() -> Path:
    """Create an SVG image of a five-pointed star next to this script."""
    width = 500
    height = 500
    center_x = width / 2
    center_y = height / 2
    outer_radius = 210
    inner_radius = 90
    points = []

    for index in range(10):
        radius = outer_radius if index % 2 == 0 else inner_radius
        angle = -pi / 2 + index * pi / 5
        x = center_x + radius * cos(angle)
        y = center_y + radius * sin(angle)
        points.append(f"{x:.2f},{y:.2f}")

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="100%" height="100%" fill="#102a43"/>
  <polygon points="{' '.join(points)}" fill="#ffd166" stroke="#f4a261" stroke-width="8" stroke-linejoin="round"/>
</svg>
"""
    image_path = Path(__file__).with_name("star.svg")
    image_path.write_text(svg, encoding="utf-8")
    return image_path


if __name__ == "__main__":
    image_path = create_star_image()
    print(f"Star image created: {image_path}")
    webbrowser.open(image_path.resolve().as_uri())
