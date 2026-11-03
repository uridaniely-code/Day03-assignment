from math import cos, pi, sin
from pathlib import Path
import webbrowser


def create_solar_system_image() -> Path:
    """Create a labeled SVG illustration of the solar system."""
    width = 1100
    height = 900
    center_x = width / 2
    center_y = height / 2 + 20
    planets = [
        ("Mercury", 58, 3, "#b8a99a", -90, 0, -13),
        ("Venus", 92, 6, "#e6b566", -48, 0, -17),
        ("Earth", 130, 7, "#48a9e6", 5, 0, 22),
        ("Mars", 170, 5, "#e76f51", 65, 12, 4),
        ("Jupiter", 230, 15, "#d4a373", 155, -8, 29),
        ("Saturn", 295, 12, "#e9c46a", -15, 5, -23),
        ("Uranus", 350, 9, "#80cbc4", 120, -5, 24),
        ("Neptune", 405, 9, "#5e81d1", -165, -12, -16),
    ]
    stars = [
        (72, 92, 2), (175, 210, 1.5), (280, 75, 1), (405, 165, 1.5),
        (525, 80, 1), (680, 145, 2), (820, 76, 1.5), (1000, 190, 1),
        (1020, 320, 1.5), (75, 390, 1), (120, 690, 2), (275, 815, 1.5),
        (475, 790, 1), (690, 830, 1.5), (895, 760, 1), (1030, 640, 2),
        (970, 500, 1), (830, 310, 1), (355, 310, 1), (225, 570, 1.5),
    ]

    star_marks = "\n".join(
        f'  <circle cx="{x}" cy="{y}" r="{radius}" fill="#dbeafe" opacity="0.7"/>'
        for x, y, radius in stars
    )
    orbit_marks = "\n".join(
        f'  <circle cx="{center_x}" cy="{center_y}" r="{orbit}" fill="none" stroke="#486581" stroke-width="1" opacity="0.65"/>'
        for _, orbit, *_ in planets
    )
    planet_marks = []
    for name, orbit, radius, color, degrees, label_dx, label_dy in planets:
        angle = degrees * pi / 180
        x = center_x + orbit * cos(angle)
        y = center_y + orbit * sin(angle)
        if name == "Saturn":
            planet_marks.append(
                f'  <ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{radius + 8}" ry="4" '
                f'transform="rotate(-20 {x:.1f} {y:.1f})" fill="none" stroke="#f4d28c" stroke-width="3"/>'
            )
        planet_marks.append(
            f'  <circle cx="{x:.1f}" cy="{y:.1f}" r="{radius}" fill="{color}" '
            f'stroke="#f0f4f8" stroke-opacity="0.45" stroke-width="1.5"/>'
        )
        planet_marks.append(
            f'  <text x="{x + label_dx:.1f}" y="{y + label_dy:.1f}" class="planet-label">{name}</text>'
        )

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="100%" height="100%" fill="#102a43"/>
  <style>
    text {{ font-family: Arial, sans-serif; fill: #f0f4f8; }}
    .title {{ font-size: 30px; font-weight: bold; fill: #ffd166; }}
    .subtitle {{ font-size: 15px; fill: #bcccdc; }}
    .planet-label {{ font-size: 13px; }}
  </style>
{star_marks}
  <text x="{width / 2}" y="48" text-anchor="middle" class="title">Our Solar System</text>
  <text x="{width / 2}" y="74" text-anchor="middle" class="subtitle">A stylized guide to the Sun and its eight planets</text>
{orbit_marks}
  <circle cx="{center_x}" cy="{center_y}" r="27" fill="#ffd166" stroke="#f4a261" stroke-width="5"/>
  <text x="{center_x}" y="{center_y + 49}" text-anchor="middle" class="planet-label">Sun</text>
{chr(10).join(planet_marks)}
  <text x="{width / 2}" y="{height - 24}" text-anchor="middle" class="subtitle">Planet sizes and distances are not to scale</text>
</svg>
"""
    image_path = Path(__file__).with_name("solar_system.svg")
    image_path.write_text(svg, encoding="utf-8")
    return image_path


if __name__ == "__main__":
    image_path = create_solar_system_image()
    print(f"Solar system image created: {image_path}")
    webbrowser.open(image_path.resolve().as_uri())
