"""
Endomorphisms - Self-maps of Elliptic Curves
Save as: scenes/endomorphisms.py
Run with: manim -pql scenes/endomorphisms.py Endomorphisms
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
RESULT_COLOR = PURPLE_A
ENDO_COLOR = TEAL_C


class Endomorphisms(ThreeDScene):
    """Visualize endomorphisms as self-maps of elliptic curves."""

    def construct(self):
        # === PART 1: WHAT IS AN ENDOMORPHISM? ===

        step1 = Text("Endomorphisms: Self-Maps", font_size=24, color=GOLD_A)
        step1.to_corner(UL, buff=0.4)
        self.add_fixed_in_frame_mobjects(step1)
        self.play(FadeIn(step1))

        # Show a single curve with looping arrow
        curve_icon = EllipticCurve(a=-1, b=0.6, color=CURVE_COLOR, stroke_width=4)
        curve_icon.scale(0.5).move_to(ORIGIN)

        self.play(GrowFromCenter(curve_icon))
        self.wait(1)

        # Create a looping arrow to show self-map
        loop_arrow = CurvedArrow(
            curve_icon.get_right() + UP * 0.3,
            curve_icon.get_right() + DOWN * 0.3,
            angle=-TAU * 0.7,
            color=ENDO_COLOR,
            stroke_width=4,
        )
        loop_arrow.shift(RIGHT * 0.8)

        phi_label = MathTex("\\varphi: E \\to E", font_size=36, color=ENDO_COLOR)
        phi_label.next_to(loop_arrow, RIGHT, buff=0.2)

        self.play(Create(loop_arrow), Write(phi_label))
        self.wait(1)

        explanation = Text(
            "An endomorphism maps a curve to itself",
            font_size=28,
            color=WHITE,
        )
        explanation.to_edge(DOWN, buff=0.5)
        self.add_fixed_in_frame_mobjects(explanation)
        self.play(FadeIn(explanation))
        self.wait(2)

        # === PART 2: TRIVIAL ENDOMORPHISMS [n] ===

        step2 = Text("Trivial Endomorphisms: [n]", font_size=24, color=HIGHLIGHT_COLOR)
        step2.to_corner(UL, buff=0.4)
        self.add_fixed_in_frame_mobjects(step2)
        self.play(
            FadeOut(step1),
            FadeIn(step2),
            FadeOut(loop_arrow),
            FadeOut(phi_label),
            FadeOut(explanation),
        )

        self.play(FadeOut(curve_icon))

        # Create axes with the curve
        a_val, b_val = -1, 1

        def curve_y(x, sign=1):
            val = x**3 + a_val * x + b_val
            if val >= 0:
                return sign * np.sqrt(val)
            return 0

        axes = Axes(
            x_range=[-2.5, 2.5, 1],
            y_range=[-2.5, 2.5, 1],
            x_length=6,
            y_length=6,
            axis_config={"color": GRAY, "stroke_width": 2},
            tips=False,
        )

        x_start = -1.3247
        curve_upper = axes.plot(
            lambda x: curve_y(x, 1),
            x_range=[x_start, 2.2, 0.005],
            color=CURVE_COLOR,
            stroke_width=4,
            use_smoothing=True,
        )
        curve_lower = axes.plot(
            lambda x: curve_y(x, -1),
            x_range=[x_start, 2.2, 0.005],
            color=CURVE_COLOR,
            stroke_width=4,
            use_smoothing=True,
        )

        self.play(Create(axes), Create(curve_upper), Create(curve_lower), run_time=1.5)

        # Show a point P
        x_p = 0.5
        y_p = curve_y(x_p)
        point_P = Dot(axes.c2p(x_p, y_p), color=HIGHLIGHT_COLOR, radius=0.12)
        label_P = MathTex("P", font_size=36, color=HIGHLIGHT_COLOR)
        label_P.next_to(point_P, UP, buff=0.15)

        self.play(FadeIn(point_P, scale=0.5), Write(label_P))
        self.wait(0.5)

        n_explanation = MathTex(
            "[n]P = \\underbrace{P + P + \\cdots + P}_{n \\text{ times}}",
            font_size=32,
            color=WHITE,
        )
        n_explanation.to_edge(DOWN, buff=0.5)
        self.add_fixed_in_frame_mobjects(n_explanation)
        self.play(FadeIn(n_explanation))
        self.wait(1)

        # Show multiples
        multiples_data = [
            (0.5, curve_y(0.5), "P", HIGHLIGHT_COLOR),
            (1.3, curve_y(1.3), "[2]P", TEAL_C),
            (-0.2, -curve_y(-0.2), "[3]P", BLUE_C),
            (1.7, curve_y(1.7), "[4]P", PURPLE_C),
        ]

        multiple_dots = VGroup()
        multiple_labels = VGroup()

        for i, (x, y, text, color) in enumerate(multiples_data):
            if i == 0:
                continue
            dot = Dot(axes.c2p(x, y), color=color, radius=0.1)
            label = MathTex(text, font_size=28, color=color)
            label.next_to(dot, UL if y > 0 else DL, buff=0.1)
            multiple_dots.add(dot)
            multiple_labels.add(label)

        for dot, label in zip(multiple_dots, multiple_labels):
            self.play(FadeIn(dot, scale=0.5), Write(label), run_time=0.6)

        self.wait(1)

        every_curve_text = Text(
            "Every curve has [n] endomorphisms for all integers n",
            font_size=26,
            color=WHITE,
        )
        every_curve_text.to_edge(DOWN, buff=0.5)

        every_curve_bg = SurroundingRectangle(
            every_curve_text,
            color=WHITE,
            fill_color=BLACK,
            fill_opacity=0.9,
            stroke_width=2,
            buff=0.2,
        )

        self.add_fixed_in_frame_mobjects(every_curve_bg, every_curve_text)
        self.play(FadeOut(n_explanation), FadeIn(every_curve_bg), FadeIn(every_curve_text))
        self.wait(2)

        # === PART 3: THE ENDOMORPHISM RING ===

        step3 = Text("The Endomorphism Ring End(E)", font_size=24, color=GOLD_A)
        step3.to_corner(UL, buff=0.4)
        self.add_fixed_in_frame_mobjects(step3)
        self.play(FadeOut(step2), FadeIn(step3), FadeOut(every_curve_bg), FadeOut(every_curve_text))

        self.play(
            FadeOut(multiple_dots),
            FadeOut(multiple_labels),
            FadeOut(point_P),
            FadeOut(label_P),
        )

        ring_title = MathTex("\\text{End}(E)", font_size=42, color=GOLD_A)
        ring_elements = MathTex(
            "\\{\\ldots, [-2], [-1], [0], [1], [2], [3], \\ldots\\}",
            font_size=32,
            color=WHITE,
        )
        ring_operations = VGroup(
            MathTex("[2] + [3] = [5]", font_size=28, color=TEAL_C),
            MathTex("[2] \\circ [3] = [6]", font_size=28, color=TEAL_C),
        )
        ring_operations.arrange(DOWN, aligned_edge=LEFT, buff=0.15)

        ring_box = VGroup(ring_title, ring_elements, ring_operations)
        ring_box.arrange(DOWN, buff=0.3)
        ring_box.move_to(RIGHT * 3.5)

        ring_bg = SurroundingRectangle(
            ring_box,
            color=GRAY,
            fill_color=BLACK,
            fill_opacity=0.85,
            stroke_width=1,
            buff=0.3,
            corner_radius=0.1,
        )

        self.add_fixed_in_frame_mobjects(ring_bg, ring_box)
        self.play(FadeIn(ring_bg), Write(ring_box), run_time=1.5)

        ring_explanation = Text(
            "Endomorphisms form a ring: you can add and compose them",
            font_size=26,
            color=WHITE,
        )
        ring_explanation.to_edge(DOWN, buff=0.5)
        self.add_fixed_in_frame_mobjects(ring_explanation)
        self.play(FadeIn(ring_explanation))
        self.wait(5)

