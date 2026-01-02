"""
Deuring Correspondence Visualization
Save as: scenes/deuring_correspondence.py
Run with: manim -pql scenes/deuring_correspondence.py DeuringCorrespondence
"""

from manim import *
import numpy as np
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from elliptic_curve import (
    EllipticCurve,
    EllipticCurveWithFill,
    EllipticCurveIcon,
    preset_curve,
)


# Color scheme (matching other files)
CURVE_COLOR = BLUE_D
ISOGENY_COLOR = GOLD_A
HIGHLIGHT_COLOR = GREEN_C
SECRET_COLOR = RED_C
PUBLIC_COLOR = BLUE_B


class DeuringCorrespondence(Scene):
    """Visualize the Deuring correspondence: curves ↔ orders, isogenies ↔ ideals."""

    def construct(self):
        # === SETUP: DIVIDE THE SCREEN ===

        # Vertical divider
        divider = DashedLine(
            UP * 3.5, DOWN * 3.5, color=GRAY, stroke_width=1, dash_length=0.1
        )

        # World labels
        geometric_title = Text("Geometric", font_size=32, color=BLUE_B)
        geometric_title.to_edge(UP, buff=0.4).shift(LEFT * 3.5)

        algebraic_title = Text("Algebraic", font_size=32, color=GOLD_A)
        algebraic_title.to_edge(UP, buff=0.4).shift(RIGHT * 3.5)

        self.play(
            Create(divider), Write(geometric_title), Write(algebraic_title), run_time=1.5
        )
        self.wait(1)

        # === PART 1: CURVES ↔ ORDERS ===

        # Left side: Elliptic curves
        e1 = EllipticCurve(
            a=-1, b=0.5, color=GREEN_C, stroke_width=3
        )
        e1.scale(0.35).move_to(LEFT * 5 + UP * 1)

        e2 = EllipticCurve(
            a=-1, b=0.6, color=TEAL_C, stroke_width=3
        )
        e2.scale(0.35).move_to(LEFT * 2 + UP * 1)

        e1_label = MathTex("E_1", font_size=28, color=GREEN_C)
        e1_label.next_to(e1, DOWN, buff=0.15)
        e2_label = MathTex("E_2", font_size=28, color=TEAL_C)
        e2_label.next_to(e2, DOWN, buff=0.15)

        curve_bracket = BraceBetweenPoints(
            LEFT * 5.8 + DOWN * 1.5, LEFT * 1.2 + DOWN * 1.5, direction=DOWN, color=GRAY
        )
        curve_text = Text("Supersingular curves", font_size=18, color=GRAY)
        curve_text.next_to(curve_bracket, DOWN, buff=0.1)

        # Right side: Maximal orders (represented as lattice-like structures)
        order1 = self.create_order_symbol(GREEN_C).move_to(RIGHT * 2 + UP * 1)
        order2 = self.create_order_symbol(TEAL_C).move_to(RIGHT * 5 + UP * 1)

        o1_label = MathTex("\\mathcal{O}_1", font_size=42, color=GREEN_C)
        o1_label.next_to(order1, DOWN, buff=0.15)
        o2_label = MathTex("\\mathcal{O}_2", font_size=42, color=TEAL_C)
        o2_label.next_to(order2, DOWN, buff=0.15)

        order_bracket = BraceBetweenPoints(
            RIGHT * 1.2 + DOWN * 1.5, RIGHT * 5.8 + DOWN * 1.5, direction=DOWN, color=GRAY
        )
        order_text = Text("Maximal orders", font_size=18, color=GRAY)
        order_text.next_to(order_bracket, DOWN, buff=0.1)

        # Animate curves appearing
        self.play(
            GrowFromCenter(e1),
            GrowFromCenter(e2),
            Write(e1_label),
            Write(e2_label),
            run_time=1.5,
        )
        self.wait(0.8)
        self.play(
            GrowFromCenter(order1),
            GrowFromCenter(order2),
            Write(o1_label),
            Write(o2_label),
            run_time=1.5,
        )
        self.wait(0.8)

        # Show the correspondence with curved arrows
        correspond1 = CurvedArrow(
            e1.get_right() + UP * 0.3,
            order1.get_left() + UP * 0.3,
            color=GREEN_C,
            stroke_width=2,
            angle=-TAU / 6,
        )
        correspond2 = CurvedArrow(
            e2.get_right() + UP * 0.3,
            order2.get_left() + UP * 0.3,
            color=TEAL_C,
            stroke_width=2,
            angle=-TAU / 6,
        )

        self.play(Create(correspond1), Create(correspond2), run_time=1.5)
        self.wait(1)

        # Category labels
        self.play(
            FadeIn(curve_bracket),
            FadeIn(curve_text),
            FadeIn(order_bracket),
            FadeIn(order_text),
            run_time=1.2
        )
        self.wait(2)

        # === PART 2: ISOGENIES ↔ IDEALS ===

        # Left side: Isogeny arrow
        isogeny = Arrow(
            e1.get_center() + DOWN * 0.9,
            e2.get_center() + DOWN * 0.9,
            color=GOLD_A,
            stroke_width=4,
            buff=0.5,
        )
        phi_label = MathTex("\\varphi", font_size=32, color=GOLD_A)
        phi_label.next_to(isogeny, DOWN, buff=0.15)

        # Right side: Ideal (represented as connecting element)
        ideal = self.create_ideal_symbol(GOLD_A).move_to(RIGHT * 3.5 + UP * 1)
        ideal_label = MathTex("I", font_size=48, color=GOLD_A)
        ideal_label.next_to(ideal, DOWN, buff=0.15)

        # Ideal connects the two orders
        ideal_connect1 = Line(
            order1.get_right(),
            ideal.get_left(),
            color=GOLD_A,
            stroke_width=2,
            stroke_opacity=0.6,
        )
        ideal_connect2 = Line(
            ideal.get_right(),
            order2.get_left(),
            color=GOLD_A,
            stroke_width=2,
            stroke_opacity=0.6,
        )

        # Animate isogeny
        self.play(GrowArrow(isogeny), Write(phi_label), run_time=1.2)
        self.wait(0.8)

        # Animate ideal appearing in sync
        self.play(
            Create(ideal_connect1),
            GrowFromCenter(ideal),
            Create(ideal_connect2),
            Write(ideal_label),
            run_time=1.5,
        )
        self.wait(0.8)

        # Show the correspondence
        correspond_iso = CurvedDoubleArrow(
            phi_label.get_right() + RIGHT * 0.2,
            ideal_label.get_left() + LEFT * 0.2,
            color=WHITE,
            stroke_width=2,
            angle=-TAU / 8,
        )

        self.play(Create(correspond_iso), run_time=1.2)
        self.wait(2.5)

        # === PART 3: THE KEY INSIGHT ===

        # Fade the correspondence arrows and brackets
        self.play(
            FadeOut(correspond1),
            FadeOut(correspond2),
            FadeOut(curve_bracket),
            FadeOut(curve_text),
            FadeOut(order_bracket),
            FadeOut(order_text),
            FadeOut(correspond_iso),
            run_time=0.8,
        )

        # Key insight box at bottom
        insight_text = MathTex(
            "\\varphi: E_1 \\to E_2",
            "\\;\\longleftrightarrow\\;",
            "I \\subseteq \\mathcal{O}_1 \\text{ with } \\mathcal{O}_R(I) = \\mathcal{O}_2",
            font_size=28,
        )
        insight_text[0].set_color(BLUE_B)
        insight_text[1].set_color(WHITE)
        insight_text[2].set_color(GOLD_A)
        insight_text.to_edge(DOWN, buff=0.8)

        insight_box = SurroundingRectangle(
            insight_text,
            color=GRAY,
            fill_color=BLACK,
            fill_opacity=0.8,
            stroke_width=1,
            buff=0.2,
            corner_radius=0.1,
        )

        self.play(FadeIn(insight_box), Write(insight_text), run_time=1.5)
        self.wait(3)

        # === PART 4: WHY THIS HELPS ===

        # Clear insight box
        self.play(FadeOut(insight_box), FadeOut(insight_text))

        # Show computation flow
        # Left: "Hard" geometric problem
        hard_label = Text("Hard", font_size=24, color=RED_C)
        hard_label.next_to(isogeny, UP, buff=0.8)

        question = MathTex("?", font_size=48, color=RED_C)
        question.move_to(isogeny.get_center() + UP * 0.5)

        # Right: "Easy" algebraic computation
        easy_label = Text("Easier", font_size=24, color=GREEN_C)
        easy_label.move_to(RIGHT * 3.5 + UP * 2.2)

        # Show algebraic operations
        alg_ops = VGroup(
            MathTex("I \\cdot J", font_size=38, color=GOLD_A),
            MathTex("\\text{norm}(I)", font_size=38, color=GOLD_A),
            MathTex("I + J", font_size=38, color=GOLD_A),
        )
        alg_ops.arrange(DOWN, buff=0.15)
        alg_ops.move_to(RIGHT * 3.5 + DOWN * 1.8)

        self.play(
            FadeIn(hard_label),
            FadeIn(question),
            run_time=1
        )
        self.wait(1.2)

        self.play(
            FadeIn(easy_label),
            LaggedStart(
                *[FadeIn(op, shift=RIGHT * 0.3) for op in alg_ops], lag_ratio=0.2
            ),
            run_time=1.5
        )
        self.wait(1.5)

        # Flow arrow: translate to algebra, compute, translate back
        flow_text = Text(
            "Curves ↔ Quaternion orders: Use algebra!", font_size=24, color=GRAY_B
        )
        flow_text.to_edge(DOWN, buff=0.5)

        self.play(Write(flow_text), run_time=1.2)
        self.wait(3)

        self.play(
            FadeOut(flow_text),
            FadeOut(hard_label),
            FadeOut(question),
            FadeOut(easy_label),
            FadeOut(alg_ops),
        )

        # Highlight both sides pulsing together
        self.play(
            e1.animate.set_color(WHITE),
            order1.animate.set_stroke(WHITE),
            e2.animate.set_color(WHITE),
            order2.animate.set_stroke(WHITE),
            rate_func=there_and_back,
            run_time=1.2,
        )

        self.wait(3)

    def create_order_symbol(self, color):
        """Create a visual representation of a maximal order (lattice-like)."""
        order = VGroup()

        # Main diamond
        diamond = RegularPolygon(n=4, color=color, stroke_width=3)
        diamond.scale(0.4).rotate(PI / 4)

        # Inner structure suggesting ring/lattice
        inner = RegularPolygon(n=4, color=color, stroke_width=1.5, stroke_opacity=0.5)
        inner.scale(0.2).rotate(PI / 4)

        # Cross lines suggesting basis
        h_line = Line(
            LEFT * 0.35, RIGHT * 0.35, color=color, stroke_width=1.5, stroke_opacity=0.5
        )
        v_line = Line(
            UP * 0.35, DOWN * 0.35, color=color, stroke_width=1.5, stroke_opacity=0.5
        )

        order.add(diamond, inner, h_line, v_line)
        return order

    def create_ideal_symbol(self, color):
        """Create a visual representation of an ideal."""
        ideal = VGroup()

        hex_shape = RegularPolygon(n=6, color=color, stroke_width=3, fill_opacity=0.2)
        hex_shape.scale(0.3)
        hex_shape.set_fill(color)

        # Inner dot
        dot = Dot(color=color, radius=0.05)

        ideal.add(hex_shape, dot)
        return ideal
