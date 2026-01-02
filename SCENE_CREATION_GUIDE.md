# SQIsign Manim Scene Creation Guide

## Project Overview
This project creates educational visualizations for SQIsign (a post-quantum signature scheme based on supersingular isogenies) using Manim. All scenes follow consistent styling and conventions.

---

## File Structure

### 1. File Header
Every scene file must start with:

```python
"""
[Scene Description] - [Brief Explanation]
Save as: scenes/[filename].py
Run with: manim -pql scenes/[filename].py [SceneClassName]
"""

from manim import *
import numpy as np
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from elliptic_curve import EllipticCurve, EllipticCurveWithFill, EllipticCurveIcon, preset_curve
```

### 2. Color Scheme (REQUIRED)
Always include this exact color scheme after imports:

```python
# Color scheme
CURVE_COLOR = BLUE_D
ISOGENY_COLOR = GOLD_A
HIGHLIGHT_COLOR = GREEN_C
SECRET_COLOR = RED_C
PUBLIC_COLOR = BLUE_B
```

**Usage:**
- `CURVE_COLOR`: Regular elliptic curves in diagrams
- `ISOGENY_COLOR`: Arrows/edges representing isogenies
- `HIGHLIGHT_COLOR`: Success states, correct paths
- `SECRET_COLOR`: Secret keys, problems, wrong paths
- `PUBLIC_COLOR`: Public keys, starting points

---

## Elliptic Curve Visualization

### CRITICAL: Choosing the Right Class

**Use `EllipticCurve` (NO FILL) for all standard visualizations:**
```python
curve = EllipticCurve(a=-1, b=0.6, color=CURVE_COLOR, stroke_width=3)
```

**Use `EllipticCurveIcon` for stylized diagram nodes:**
```python
node = EllipticCurveIcon(color=CURVE_COLOR, fill_opacity=0.0, stroke_width=2, shape=1.0)
```

**NEVER use `EllipticCurveWithFill` unless specifically needed for a special effect.**

### Safe Parameters
To avoid gaps in curves, always use:
- `a = -1` (fixed)
- `b` in range `0.5` to `0.8` (vary for visual diversity)
- Examples: `b=0.5`, `b=0.6`, `b=0.7`, `b=0.8`

### Scaling Guidelines
- Large featured curves: `scale(0.6)` to `scale(0.8)`
- Medium curves: `scale(0.28)` to `scale(0.4)`
- Small diagram nodes: `scale(0.12)` to `scale(0.25)`
- Tiny graph nodes: `scale(0.18)`

### Example
```python
# Good: Mathematical accuracy, no fill
e1 = EllipticCurve(a=-1, b=0.6, color=GREEN_C, stroke_width=3)
e1.scale(0.35).move_to(LEFT * 3)

# Good: Multiple nodes with variety
for i in range(num_nodes):
    b_val = 0.5 + (i % 4) * 0.1  # Cycles through 0.5, 0.6, 0.7, 0.8
    node = EllipticCurve(a=-1, b=b_val, color=CURVE_COLOR, stroke_width=2)
    node.scale(0.18)
```

---

## Layout Conventions

### NO TITLES
**NEVER create title text at the top of the screen.** Instead, use the upper-left corner for step indicators.

### Step Indicators (Upper Left)
Use for multi-step scenes:

```python
step1 = Text("Step 1: Description", font_size=24, color=GOLD_A)
step1.to_corner(UL, buff=0.4)
self.play(FadeIn(step1))

# Later, transition to next step
step2 = Text("Step 2: Next action", font_size=24, color=GREEN_C)
step2.to_corner(UL, buff=0.4)
self.play(FadeOut(step1), FadeIn(step2))
```

### Positioning
- **UL (Upper Left)**: Step indicators
- **DL (Down Left)**: Supplementary notes
- **DR (Down Right)**: Legend boxes, complexity annotations
- **DOWN**: Explanatory text that spans the bottom
- **UP**: Occasional emphasis text

### Text Placement
```python
# Bottom explanatory text
explanation = Text("Your explanation here", font_size=28, color=WHITE)
explanation.to_edge(DOWN, buff=0.5)

# Corner boxes with background
info_box = VGroup(...)
info_box.to_corner(DR, buff=0.5)

bg_rect = SurroundingRectangle(
    info_box,
    color=GRAY,
    fill_color=BLACK,
    fill_opacity=0.8,
    stroke_width=1,
    buff=0.25,
    corner_radius=0.1,
)
```

---

## Typography Standards

### Font Sizes (MINIMUM)
**All text must be clearly legible:**

- **Step indicators**: `font_size=24` (minimum)
- **Main explanatory text**: `font_size=28` to `font_size=32`
- **Math labels on curves**: `font_size=36` to `font_size=42`
- **Legend/info boxes**: `font_size=42` to `font_size=54` for main content
- **Small annotations**: `font_size=20` (minimum, use sparingly)
- **Dramatic comparisons**: `font_size=72` or larger

### Text Colors (CRITICAL)
**ALWAYS use WHITE or bright colors for text. NEVER use GRAY for main text.**

```python
# CORRECT
explanation = Text("...", font_size=28, color=WHITE)
step1 = Text("Step 1: ...", font_size=24, color=GOLD_A)

# WRONG - text will be hard to read
explanation = Text("...", font_size=28, color=GRAY)  # ❌ Don't do this
```

### Text-Arrow Color Matching
**Labels for arrows must match the arrow color:**

```python
tau = Arrow(e0.get_center(), ea.get_center(), color=SECRET_COLOR, buff=0.3)
tau_label = MathTex("\\tau", font_size=36, color=SECRET_COLOR)  # Same color!
secret_text = Text("secret key", font_size=22, color=SECRET_COLOR)  # Same color!
```

**Rule:** If an arrow is `GOLD_A`, all its associated labels should be `GOLD_A`. If it's `TEAL_C`, labels are `TEAL_C`.

---

## Animation Patterns

### Creating Objects

**Curves:**
```python
self.play(GrowFromCenter(curve))
```

**Multiple curves (staggered):**
```python
self.play(
    LaggedStart(*[GrowFromCenter(n) for n in nodes], lag_ratio=0.05),
    run_time=1.5
)
```

**Arrows:**
```python
self.play(GrowArrow(arrow))
```

**Edges/Lines:**
```python
self.play(Create(edge))
```

**Text:**
```python
self.play(Write(text))  # For dramatic effect
self.play(FadeIn(text))  # For quick appearance
```

### Transitions
```python
# Standard fade transition
self.play(FadeOut(old_element), FadeIn(new_element))

# Transform text
self.play(Transform(old_text, new_text))

# Focus attention by dimming background
self.play(
    *[n.animate.set_opacity(0.15) for n in background_nodes],
    *[e.animate.set_opacity(1) for e in foreground_elements],
    run_time=0.8
)
```

### Timing
- Quick transitions: `run_time=0.6` to `run_time=0.8`
- Standard animations: `run_time=1` to `run_time=1.5`
- Dramatic reveals: `run_time=2` to `run_time=2.5`
- Always include `self.wait()` between major sections (1-3 seconds)

---

## Scene Structure

### Part Markers
Use clear comments to separate sections:

```python
def construct(self):
    # === PART 1: SETUP ===

    # Create elements
    ...
    self.wait(1)

    # === PART 2: THE PROBLEM ===

    # Show the challenge
    ...
    self.wait(2)

    # === PART 3: THE SOLUTION ===

    # Demonstrate the approach
    ...
    self.wait(3)
```

### Progressive Revelation
Build scenes incrementally:
1. Show base elements
2. Add connections/relationships
3. Highlight key features
4. Dim background, focus on important parts
5. Final summary or dramatic reveal

---

## Common Patterns

### Graph Visualization
```python
# Create nodes
nodes = VGroup()
for i in range(num_nodes):
    b_val = 0.5 + (i % 4) * 0.1
    node = EllipticCurve(a=-1, b=b_val, color=CURVE_COLOR, stroke_width=2)
    node.scale(0.18).move_to(position[i])
    nodes.add(node)

# Create edges
edges = VGroup()
for (i, j) in edge_pairs:
    edge = Line(
        nodes[i].get_center(),
        nodes[j].get_center(),
        color=GRAY,
        stroke_width=2,
        stroke_opacity=0.3,
    )
    edges.add(edge)

# Animate appearance
self.play(LaggedStart(*[GrowFromCenter(n) for n in nodes], lag_ratio=0.05))
self.play(LaggedStart(*[Create(e) for e in edges], lag_ratio=0.02))
```

### Path Highlighting
```python
# Dim non-path elements
self.play(
    *[n.animate.set_opacity(0.15) for n in non_path_nodes],
    *[e.animate.set_opacity(0.08) for e in non_path_edges],
)

# Highlight path with glow
for edge in path_edges:
    glow = edge.copy().set_stroke(color, width=8, opacity=0.4)
    self.play(
        edge.animate.set_color(color).set_stroke(width=4).set_opacity(1),
        FadeIn(glow),
    )
```

### Info Boxes
```python
info_text = VGroup(
    Text("Line 1", font_size=42, color=WHITE),
    Text("Line 2", font_size=42, color=GREEN_C),
    Text("Line 3", font_size=36, color=WHITE),
)
info_text.arrange(DOWN, aligned_edge=LEFT, buff=0.25)
info_text.to_corner(DR, buff=0.5)

bg_rect = SurroundingRectangle(
    info_text,
    color=GRAY,
    fill_color=BLACK,
    fill_opacity=0.8,
    stroke_width=1,
    buff=0.25,
    corner_radius=0.1,
)

self.play(FadeIn(bg_rect), Write(info_text))
```

---

## Best Practices

### Visual Hierarchy
1. **Bright colors** for important elements (WHITE, GOLD_A, GREEN_C, RED_C)
2. **Opacity** to create focus (dim background to 0.15, highlight to 1.0)
3. **Scale** to emphasize (scale(1.5) for highlighted nodes)
4. **Stroke width** for importance (2-3 normal, 4-6 emphasized)

### Pacing
- Don't rush: include adequate `self.wait()` calls
- Use `run_time` to control speed
- Build complexity gradually
- Give viewers time to absorb information

### Accessibility
- **Always use bright text** (WHITE or vibrant colors)
- **Large font sizes** (minimum 24, prefer 28+)
- **High contrast** (bright on dark, never gray on gray)
- **Clear labels** that match their associated elements

### Code Quality
- Use descriptive variable names (`start_node`, not `n1`)
- Comment sections clearly
- Group related animations
- Keep `construct()` readable with clear sections

---

## Example Scene Template

```python
"""
[Scene Name] - [Description]
Save as: scenes/example.py
Run with: manim -pql scenes/example.py ExampleScene
"""

from manim import *
import numpy as np
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from elliptic_curve import EllipticCurve, EllipticCurveIcon

# Color scheme
CURVE_COLOR = BLUE_D
ISOGENY_COLOR = GOLD_A
HIGHLIGHT_COLOR = GREEN_C
SECRET_COLOR = RED_C
PUBLIC_COLOR = BLUE_B


class ExampleScene(Scene):
    """Description of what this scene visualizes."""

    def construct(self):
        # === PART 1: SETUP ===

        step1 = Text("Step 1: Setup", font_size=24, color=GOLD_A)
        step1.to_corner(UL, buff=0.4)
        self.play(FadeIn(step1))

        # Create curves (no fill!)
        e1 = EllipticCurve(a=-1, b=0.6, color=CURVE_COLOR, stroke_width=3)
        e1.scale(0.35).move_to(LEFT * 3)

        e2 = EllipticCurve(a=-1, b=0.7, color=CURVE_COLOR, stroke_width=3)
        e2.scale(0.35).move_to(RIGHT * 3)

        # Labels (bright colors, large fonts)
        e1_label = MathTex("E_1", font_size=36, color=GREEN_C)
        e1_label.next_to(e1, DOWN, buff=0.3)

        e2_label = MathTex("E_2", font_size=36, color=RED_C)
        e2_label.next_to(e2, DOWN, buff=0.3)

        self.play(
            GrowFromCenter(e1),
            GrowFromCenter(e2),
            Write(e1_label),
            Write(e2_label),
        )

        # Explanatory text (white, legible)
        explanation = Text(
            "Clear explanation of what's happening",
            font_size=28,
            color=WHITE
        )
        explanation.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(explanation))

        self.wait(2)

        # === PART 2: ACTION ===

        step2 = Text("Step 2: Main concept", font_size=24, color=GREEN_C)
        step2.to_corner(UL, buff=0.4)
        self.play(FadeOut(step1), FadeIn(step2))

        # Arrow with matching color label
        arrow = Arrow(e1.get_right(), e2.get_left(), color=GOLD_A, buff=0.3)
        arrow_label = MathTex("\\varphi", font_size=36, color=GOLD_A)
        arrow_label.next_to(arrow, UP, buff=0.2)

        self.play(GrowArrow(arrow), Write(arrow_label))
        self.wait(2)

        # === PART 3: CONCLUSION ===

        # Final emphasis
        self.play(FadeOut(explanation))

        final_message = Text("Key takeaway", font_size=32, color=WHITE)
        final_message.to_edge(DOWN, buff=0.5)
        self.play(Write(final_message))

        self.wait(3)
```

---

## Checklist for New Scenes

Before submitting a new scene, verify:

- [ ] File header with description and run command
- [ ] Standard color scheme defined
- [ ] `sys.path.insert` for elliptic_curve import
- [ ] Using `EllipticCurve` (not WithFill) for standard curves
- [ ] Curve parameters: `a=-1`, `b` in range 0.5-0.8
- [ ] NO title at top (use step indicators in UL instead)
- [ ] All text is WHITE or bright colors (NEVER gray)
- [ ] Font sizes are 24+ (preferably 28+ for main text)
- [ ] Text colors match associated arrow/element colors
- [ ] Clear section markers (`# === PART N: ... ===`)
- [ ] Adequate `self.wait()` calls between sections
- [ ] Info boxes have large, legible fonts (42+)
- [ ] Opacity used effectively to guide focus
- [ ] Progressive revelation of concepts
- [ ] Final wait of 3+ seconds at end

---

## Reference Scenes

Study these existing scenes for examples:

- **`maze_metaphor.py`**: Graph layout, path visualization, step indicators
- **`sqisign_protocol.py`**: Protocol steps, color matching, clear progression
- **`path_hardness.py`**: Info boxes, complexity notation, focus techniques
- **`dimensional_lifting.py`**: 3D transitions, intermediate steps, dramatic reveals
- **`deuring_correspondence.py`**: Two-column layout, correspondence visualization

---

## Common Mistakes to Avoid

1. ❌ Using `EllipticCurveWithFill` by default
2. ❌ Creating titles at the top of the screen
3. ❌ Using gray text for important information
4. ❌ Font sizes smaller than 24
5. ❌ Mismatched colors (gray label on gold arrow)
6. ❌ Rushing animations (no wait times)
7. ❌ Using curve parameters that create gaps (b < 0.5 or b > 0.8)
8. ❌ Cluttered scenes without clear focus
9. ❌ Missing explanatory text
10. ❌ Forgetting `sys.path.insert` for imports

---

## Getting Help

- Check existing scenes in `/scenes/` for patterns
- Use `elliptic_curve.py` for curve class documentation
- Test renders frequently: `manim -pql scenes/your_scene.py YourScene`
- Ensure text is legible at typical viewing distances
