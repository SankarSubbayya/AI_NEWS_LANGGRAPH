"""Enhanced Fallback Cover Image Generator.

Creates visually appealing gradient covers with design elements when AI generation is unavailable.
"""

import base64
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import os
from datetime import datetime

def create_enhanced_cover(
    main_topic: str = "AI in Cancer Care",
    width: int = 1792,
    height: int = 1024,
    style: str = "professional"
) -> str:
    """Create an enhanced gradient cover with design elements.
    
    Args:
        main_topic: Newsletter topic
        width: Image width
        height: Image height
        style: Visual style (professional, modern, abstract, scientific)
        
    Returns:
        Base64 encoded image string with data URI prefix
    """
    
    # Style-specific color schemes
    color_schemes = {
        "professional": {
            "gradient_start": (102, 126, 234),  # Purple-blue
            "gradient_end": (118, 75, 162),      # Deep purple
            "accent": (255, 255, 255),           # White
            "pattern": (118, 75, 162, 30)        # Semi-transparent purple
        },
        "modern": {
            "gradient_start": (79, 172, 254),    # Bright blue
            "gradient_end": (0, 242, 254),       # Cyan
            "accent": (255, 255, 255),
            "pattern": (0, 242, 254, 40)
        },
        "abstract": {
            "gradient_start": (236, 72, 153),    # Pink
            "gradient_end": (147, 51, 234),      # Purple
            "accent": (255, 255, 255),
            "pattern": (236, 72, 153, 50)
        },
        "scientific": {
            "gradient_start": (5, 150, 105),     # Teal
            "gradient_end": (6, 95, 70),         # Dark teal
            "accent": (255, 255, 255),
            "pattern": (6, 95, 70, 40)
        }
    }
    
    colors = color_schemes.get(style, color_schemes["professional"])
    
    # Create base image
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Draw smooth gradient background
    for y in range(height):
        ratio = y / height
        r = int(colors["gradient_start"][0] * (1 - ratio) + colors["gradient_end"][0] * ratio)
        g = int(colors["gradient_start"][1] * (1 - ratio) + colors["gradient_end"][1] * ratio)
        b = int(colors["gradient_start"][2] * (1 - ratio) + colors["gradient_end"][2] * ratio)
        draw.rectangle([(0, y), (width, y + 1)], fill=(r, g, b))
    
    # Add geometric pattern overlay
    _add_geometric_pattern(draw, width, height, colors["pattern"], style)
    
    # Add decorative elements
    _add_decorative_circles(draw, width, height, colors["accent"], style)
    
    # Add subtle grid
    if style in ["modern", "scientific"]:
        _add_grid_lines(draw, width, height, colors["pattern"])
    
    # Save to base64
    buffered = BytesIO()
    img.save(buffered, format="PNG", optimize=True)
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    return f"data:image/png;base64,{img_str}"


def _add_geometric_pattern(draw, width, height, color, style):
    """Add geometric pattern overlay."""
    if style == "professional":
        # Hexagonal pattern
        size = 100
        for y in range(-100, height + 100, int(size * 0.866)):
            for x in range(-100, width + 100, size):
                x_offset = size // 2 if (y // int(size * 0.866)) % 2 else 0
                _draw_hexagon(draw, x + x_offset, y, size // 3, color)
    
    elif style == "modern":
        # Diagonal lines
        for i in range(0, width + height, 80):
            draw.line([(i, 0), (i - height, height)], fill=color, width=2)
    
    elif style == "abstract":
        # Organic blobs
        import random
        random.seed(42)
        for _ in range(15):
            x = random.randint(0, width)
            y = random.randint(0, height)
            r = random.randint(100, 300)
            draw.ellipse([x - r, y - r, x + r, y + r], fill=color)
    
    elif style == "scientific":
        # Network nodes
        import random
        random.seed(42)
        points = [(random.randint(0, width), random.randint(0, height)) for _ in range(30)]
        for i, p1 in enumerate(points):
            for p2 in points[i+1:]:
                dist = ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5
                if dist < 200:
                    draw.line([p1, p2], fill=color, width=1)


def _draw_hexagon(draw, x, y, size, color):
    """Draw a hexagon."""
    import math
    points = []
    for i in range(6):
        angle = math.pi / 3 * i
        px = x + size * math.cos(angle)
        py = y + size * math.sin(angle)
        points.append((px, py))
    draw.polygon(points, outline=color)


def _add_decorative_circles(draw, width, height, color, style):
    """Add decorative circular elements."""
    # Large accent circle
    circle_x = width * 0.85
    circle_y = height * 0.5
    circle_r = height * 0.4
    
    # Draw multiple concentric circles for depth
    for i in range(3):
        alpha = 20 - i * 5
        draw.ellipse(
            [circle_x - circle_r - i*30, circle_y - circle_r - i*30,
             circle_x + circle_r + i*30, circle_y + circle_r + i*30],
            outline=color + (alpha,),
            width=3
        )
    
    # Small accent circles
    small_circles = [
        (width * 0.1, height * 0.2, height * 0.08),
        (width * 0.15, height * 0.8, height * 0.06),
        (width * 0.9, height * 0.15, height * 0.05),
    ]
    
    for cx, cy, cr in small_circles:
        draw.ellipse(
            [cx - cr, cy - cr, cx + cr, cy + cr],
            fill=color + (30,)
        )


def _add_grid_lines(draw, width, height, color):
    """Add subtle grid lines."""
    spacing = 100
    alpha = 15
    
    # Vertical lines
    for x in range(0, width, spacing):
        draw.line([(x, 0), (x, height)], fill=color[:3] + (alpha,), width=1)
    
    # Horizontal lines
    for y in range(0, height, spacing):
        draw.line([(0, y), (width, y)], fill=color[:3] + (alpha,), width=1)


# Convenience function
def generate_enhanced_cover_base64(
    main_topic: str = "AI in Cancer Care",
    style: str = "professional"
) -> str:
    """Generate enhanced cover and return as base64 data URI.
    
    Args:
        main_topic: Newsletter topic
        style: Visual style
        
    Returns:
        Base64 data URI string
    """
    return create_enhanced_cover(main_topic=main_topic, style=style)


if __name__ == "__main__":
    # Test generation
    print("Generating enhanced cover...")
    cover = generate_enhanced_cover_base64(style="professional")
    print(f"✅ Generated cover ({len(cover)} characters)")
    print("To test, paste the base64 string into an HTML <img src='...'> tag")

