"""
Isogenies as Structure-Preserving Maps - Shows how isogenies respect the group law
Save as: scenes/isogeny_morphism.py
Run with: manim -pql scenes/isogeny_morphism.py IsogenyMorphism
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


class IsogenyMorphism(MovingCameraScene):
    """Visualize how isogenies preserve the group structure."""

    def construct(self):
        # Curve parameters
        a1, b1 = -1, 1  # E₁: y² = x³ - x + 1
        a2, b2 = -1, 0.8  # E₂: y² = x³ - x + 0.8 (different curve)

        def curve_y(x, a, b, sign=1):
            val = x**3 + a * x + b
            if val >= 0:
                return sign * np.sqrt(val)
            return 0

        def find_third_intersection(x1, y1, x2, y2, a, b):
            if abs(x2 - x1) < 1e-10:
                return x1, -y1
            m = (y2 - y1) / (x2 - x1)
            x3 = m**2 - x1 - x2
            c = y1 - m * x1
            y3 = m * x3 + c
            return x3, y3

        # === PART 1: TWO CURVES ===

        step1 = Text("Morphisms Between Curves", font_size=24, color=GOLD_A)
        step1.to_corner(UL, buff=0.4)
        self.play(FadeIn(step1))

        # Create two sets of axes side by side
        axes1 = Axes(
            x_range=[-2.5, 2.5, 1],
            y_range=[-2.5, 2.5, 1],
            x_length=4,
            y_length=4,
            axis_config={"color": GRAY, "stroke_width": 1.5},
            tips=False,
        )
        axes1.move_to(LEFT * 3.5)

        axes2 = Axes(
            x_range=[-2.5, 2.5, 1],
            y_range=[-2.5, 2.5, 1],
            x_length=4,
            y_length=4,
            axis_config={"color": GRAY, "stroke_width": 1.5},
            tips=False,
        )
        axes2.move_to(RIGHT * 3.5)

        # Curve labels
        e1_label = MathTex("E_1", font_size=36, color=HIGHLIGHT_COLOR)
        e1_label.next_to(axes1, UP, buff=0.2)

        e2_label = MathTex("E_2", font_size=36, color=PUBLIC_COLOR)
        e2_label.next_to(axes2, UP, buff=0.2)

        # Plot curves
        x_start1 = -1.3247
        curve1_upper = axes1.plot(
            lambda x: curve_y(x, a1, b1, 1),
            x_range=[x_start1, 2.2, 0.005],
            color=HIGHLIGHT_COLOR,
            stroke_width=3,
            use_smoothing=True,
        )
        curve1_lower = axes1.plot(
            lambda x: curve_y(x, a1, b1, -1),
            x_range=[x_start1, 2.2, 0.005],
            color=HIGHLIGHT_COLOR,
            stroke_width=3,
            use_smoothing=True,
        )

        x_start2 = -1.28  # For a=-1, b=0.8
        curve2_upper = axes2.plot(
            lambda x: curve_y(x, a2, b2, 1),
            x_range=[x_start2, 2.2, 0.005],
            color=PUBLIC_COLOR,
            stroke_width=3,
            use_smoothing=True,
        )
        curve2_lower = axes2.plot(
            lambda x: curve_y(x, a2, b2, -1),
            x_range=[x_start2, 2.2, 0.005],
            color=PUBLIC_COLOR,
            stroke_width=3,
            use_smoothing=True,
        )

        # Animate curves appearing
        self.play(
            Create(axes1), Create(axes2), Write(e1_label), Write(e2_label), run_time=1
        )
        self.play(
            Create(curve1_upper),
            Create(curve1_lower),
            Create(curve2_upper),
            Create(curve2_lower),
            run_time=1.5,
        )

        # The isogeny arrow
        phi_arrow = Arrow(
            axes1.get_right() + LEFT * 0.3,
            axes2.get_left() + RIGHT * 0.3,
            color=ISOGENY_COLOR,
            stroke_width=4,
            buff=0.1,
            max_tip_length_to_length_ratio=0.05,
        )
        phi_label = MathTex("\\varphi", font_size=42, color=ISOGENY_COLOR)
        phi_label.next_to(phi_arrow, UP, buff=0.15)

        self.play(GrowArrow(phi_arrow), Write(phi_label))
        self.wait(1)

        # Explanation
        explanation = Text(
            "An isogeny maps points from one curve to another",
            font_size=26,
            color=WHITE,
        )
        explanation.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(explanation))
        self.wait(1.5)

        # === PART 2: POINTS AND THEIR IMAGES ===

        step2 = Text("Mapping Points", font_size=24, color=TEAL_C)
        step2.to_corner(UL, buff=0.4)
        self.play(FadeOut(step1), FadeIn(step2), FadeOut(explanation))

        # Points on E₁ - spread out across the curve
        x_p, x_q = -0.5, 1.8
        y_p = curve_y(x_p, a1, b1)
        y_q = curve_y(x_q, a1, b1)

        point_P = Dot(axes1.c2p(x_p, y_p), color=YELLOW_C, radius=0.1)
        label_P = MathTex("P", font_size=36, color=YELLOW_C)
        label_P.next_to(point_P, UL, buff=0.15)

        point_Q = Dot(axes1.c2p(x_q, y_q), color=TEAL_C, radius=0.1)
        label_Q = MathTex("Q", font_size=36, color=TEAL_C)
        label_Q.next_to(point_Q, UL, buff=0.15)

        self.play(
            FadeIn(point_P, scale=0.5),
            Write(label_P),
            FadeIn(point_Q, scale=0.5),
            Write(label_Q),
        )
        self.wait(0.5)

        # Compute P + Q on E₁
        x_r, y_r = find_third_intersection(x_p, y_p, x_q, y_q, a1, b1)
        # P + Q is the reflection
        x_sum, y_sum = x_r, -y_r

        point_PQ = Dot(axes1.c2p(x_sum, y_sum), color=RESULT_COLOR, radius=0.1)
        label_PQ = MathTex("P + Q", font_size=32, color=RESULT_COLOR)
        label_PQ.next_to(point_PQ, DL, buff=0.15)

        # Show the sum point
        self.play(FadeIn(point_PQ, scale=0.5), Write(label_PQ))
        self.wait(0.5)

        # === PART 3: THE KEY PROPERTY ===

        step3 = Text("Structure Preservation", font_size=24, color=GOLD_A)
        step3.to_corner(UL, buff=0.4)
        self.play(FadeOut(step2), FadeIn(step3))

        # Map points to E₂ - spread out across the curve
        # In reality φ is a specific map, but we'll show the concept
        x_phi_p, x_phi_q = -0.3, 1.9
        y_phi_p = curve_y(x_phi_p, a2, b2)
        y_phi_q = curve_y(x_phi_q, a2, b2)

        point_phi_P = Dot(axes2.c2p(x_phi_p, y_phi_p), color=YELLOW_C, radius=0.1)
        label_phi_P = MathTex("\\varphi(P)", font_size=32, color=YELLOW_C)
        label_phi_P.next_to(point_phi_P, UL, buff=0.15)

        point_phi_Q = Dot(axes2.c2p(x_phi_q, y_phi_q), color=TEAL_C, radius=0.1)
        label_phi_Q = MathTex("\\varphi(Q)", font_size=32, color=TEAL_C)
        label_phi_Q.next_to(point_phi_Q, UL, buff=0.15)

        # Animate points "traveling" through the isogeny
        # Create temporary copies that will move
        traveling_P = point_P.copy()
        traveling_Q = point_Q.copy()

        self.play(
            traveling_P.animate.move_to(point_phi_P.get_center()),
            run_time=1,
            rate_func=smooth,
        )
        self.play(FadeOut(traveling_P), FadeIn(point_phi_P), Write(label_phi_P))

        self.play(
            traveling_Q.animate.move_to(point_phi_Q.get_center()),
            run_time=1,
            rate_func=smooth,
        )
        self.play(FadeOut(traveling_Q), FadeIn(point_phi_Q), Write(label_phi_Q))

        self.wait(0.5)

        # Now the key: compute φ(P) + φ(Q) on E₂
        x_r2, y_r2 = find_third_intersection(x_phi_p, y_phi_p, x_phi_q, y_phi_q, a2, b2)
        x_sum2, y_sum2 = x_r2, -y_r2

        # Also map P+Q through φ
        point_phi_PQ = Dot(axes2.c2p(x_sum2, y_sum2), color=RESULT_COLOR, radius=0.1)

        # Show the sum point (no label yet)
        self.play(FadeIn(point_phi_PQ, scale=0.5))
        self.wait(1)

        # Now show that φ(P+Q) lands in the SAME place
        traveling_PQ = point_PQ.copy()
        self.play(
            traveling_PQ.animate.move_to(point_phi_PQ.get_center()),
            run_time=1.2,
            rate_func=smooth,
        )

        # Flash to show they're the same point!
        self.play(
            Flash(point_phi_PQ, color=GOLD_A, line_length=0.3, flash_radius=0.4),
            FadeOut(traveling_PQ),
        )
        self.wait(0.5)

        # Zoom in to examine this key point more closely
        zoom_center = point_phi_PQ.get_center()
        self.play(
            self.camera.frame.animate.move_to(zoom_center).scale(0.4),
            run_time=1.5,
        )
        self.wait(1)

        # After zoom, show the first label
        label_phi_PQ_v1 = MathTex(
            "\\varphi(P) + \\varphi(Q)", font_size=32, color=RESULT_COLOR
        )
        label_phi_PQ_v1.next_to(point_phi_PQ, DOWN, buff=0.8).shift(LEFT * 0.3)

        bg_v1 = SurroundingRectangle(
            label_phi_PQ_v1,
            color=WHITE,
            fill_color=BLACK,
            fill_opacity=0.9,
            stroke_width=2,
            buff=0.15,
        )

        self.play(FadeIn(bg_v1), Write(label_phi_PQ_v1))
        self.wait(0.5)

        # Transform to show equality
        label_phi_PQ_v2 = MathTex(
            "\\varphi(P+Q)",
            "=",
            "\\varphi(P) + \\varphi(Q)",
            font_size=36,
            color=RESULT_COLOR,
        )
        label_phi_PQ_v2.next_to(point_phi_PQ, DOWN, buff=0.8).shift(RIGHT * 0.1)

        bg_v2 = SurroundingRectangle(
            label_phi_PQ_v2,
            color=WHITE,
            fill_color=BLACK,
            fill_opacity=0.9,
            stroke_width=2,
            buff=0.15,
        )

        self.play(Transform(label_phi_PQ_v1, label_phi_PQ_v2), Transform(bg_v1, bg_v2))
        self.wait(5)
