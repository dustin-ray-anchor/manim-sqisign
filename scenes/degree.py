"""
Degree: The Fundamental Measure of an Isogeny
Save as: scenes/degree.py
Run with: manim -pql scenes/degree.py Degree
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
KERNEL_COLOR = ORANGE
IDENTITY_COLOR = WHITE
DEGREE_COLOR = YELLOW


def get_curve_paths(curve):
    """Extract drawable paths from an EllipticCurve VGroup."""
    paths = [
        sm for sm in curve.submobjects if hasattr(sm, "points") and len(sm.points) > 0
    ]
    if not paths:
        paths = curve.family_members_with_points()
    return paths


class Degree(Scene):
    """Visualize the degree of an isogeny and its multiple characterizations."""

    def construct(self):
        # === PART 1: DEGREE AS KERNEL SIZE ===

        step1 = Text("Degree = Kernel Size", font_size=24, color=GOLD_A)
        step1.to_corner(UL, buff=0.4)
        self.play(FadeIn(step1))

        # Create source curve
        e1 = EllipticCurve(a=-1, b=0.6, color=CURVE_COLOR, stroke_width=4)
        e1.scale(0.4).move_to(LEFT * 4)

        e1_label = MathTex("E_1", font_size=32, color=CURVE_COLOR)
        e1_label.next_to(e1, DOWN, buff=0.25)

        self.play(GrowFromCenter(e1), Write(e1_label))

        # Get curve paths for point placement
        e1_paths = get_curve_paths(e1)
        num_paths = len(e1_paths)

        # Show degree-2, degree-3, degree-4 examples side by side
        degree_examples = [
            (2, GREEN_C, 0.6),
            (3, TEAL_C, 0.75),
            (4, PURPLE_C, 0.8),
        ]

        target_curves = VGroup()
        degree_labels = []
        kernel_dots_groups = []

        for i, (deg, color, b_val) in enumerate(degree_examples):
            # Target curve
            e_target = EllipticCurve(a=-1, b=b_val, color=color, stroke_width=3)
            e_target.scale(0.25).move_to(RIGHT * (0.5 + i * 2.2) + UP * 1.5)
            target_curves.add(e_target)

            # Degree label
            deg_label = MathTex(f"\\deg = {deg}", font_size=28, color=color)
            deg_label.next_to(e_target, DOWN, buff=0.2)
            degree_labels.append(deg_label)

            # Arrow from E1
            arrow = Arrow(
                e1.get_right(),
                e_target.get_left(),
                color=color,
                stroke_width=2,
                buff=0.15,
                max_tip_length_to_length_ratio=0.1,
            )

            self.play(
                GrowFromCenter(e_target),
                GrowArrow(arrow),
                Write(deg_label),
                run_time=0.6,
            )

            # Show kernel points on E1 for this isogeny
            kernel_dots = VGroup()
            # Spread kernel points across the curve
            for j in range(deg):
                prop = 0.1 + (j * 0.8 / deg)
                branch = j % num_paths
                pos = e1_paths[min(branch, num_paths - 1)].point_from_proportion(prop)
                dot = Dot(pos, color=color, radius=0.08)
                kernel_dots.add(dot)

            kernel_dots_groups.append(kernel_dots)

        # Animate showing kernel points for each degree
        kernel_formula = MathTex(
            "\\deg(\\varphi) = |\\ker(\\varphi)|",
            font_size=32,
            color=WHITE,
        )
        kernel_formula.to_edge(DOWN, buff=0.5)
        self.play(Write(kernel_formula))

        # Show kernel points one degree at a time
        for i, (deg, color, _) in enumerate(degree_examples):
            # Highlight this example
            kernel_text = MathTex(
                f"|\\ker| = {deg}",
                font_size=24,
                color=color,
            )
            kernel_text.next_to(target_curves[i], UP, buff=0.15)

            self.play(
                LaggedStart(
                    *[FadeIn(d, scale=0.5) for d in kernel_dots_groups[i]],
                    lag_ratio=0.15,
                ),
                Write(kernel_text),
                run_time=0.8,
            )
            self.wait(0.5)

            # Fade out the kernel dots before next example
            if i < len(degree_examples) - 1:
                self.play(
                    FadeOut(kernel_dots_groups[i]),
                    FadeOut(kernel_text),
                    run_time=0.4,
                )

        self.wait(3)

        # Clean up for next part
        self.play(
            *[FadeOut(m) for m in self.mobjects],
        )

        # === PART 2: DEGREE AS D-TO-1 COVERING ===

        step2 = Text("Degree = Covering Number", font_size=24, color=TEAL_C)
        step2.to_corner(UL, buff=0.4)
        self.play(FadeIn(step2))

        # Two curves
        e1 = EllipticCurve(a=-1, b=0.6, color=CURVE_COLOR, stroke_width=4)
        e1.scale(0.45).move_to(LEFT * 3.5)

        e2 = EllipticCurve(a=-1, b=0.8, color=CURVE_COLOR, stroke_width=4)
        e2.scale(0.45).move_to(RIGHT * 3.5)

        e1_label = MathTex("E_1", font_size=32, color=CURVE_COLOR)
        e1_label.next_to(e1, DOWN, buff=0.25)

        e2_label = MathTex("E_2", font_size=32, color=CURVE_COLOR)
        e2_label.next_to(e2, DOWN, buff=0.25)

        self.play(
            GrowFromCenter(e1),
            GrowFromCenter(e2),
            Write(e1_label),
            Write(e2_label),
        )

        # Isogeny arrow with degree
        isogeny_arrow = Arrow(
            e1.get_right() + RIGHT * 0.1,
            e2.get_left() + LEFT * 0.1,
            color=ISOGENY_COLOR,
            stroke_width=4,
            buff=0.1,
        )
        deg_label = MathTex("\\varphi", font_size=32, color=ISOGENY_COLOR)
        deg_label.next_to(isogeny_arrow, UP, buff=0.1)
        deg_value = MathTex("\\deg = 3", font_size=28, color=DEGREE_COLOR)
        deg_value.next_to(isogeny_arrow, DOWN, buff=0.1)

        self.play(GrowArrow(isogeny_arrow), Write(deg_label), Write(deg_value))
        self.wait(0.5)

        # Get paths for point placement
        e1_paths = get_curve_paths(e1)
        e2_paths = get_curve_paths(e2)

        # Show a point Q on E2
        q_pos = e2_paths[0].point_from_proportion(0.4)
        point_Q = Dot(q_pos, color=HIGHLIGHT_COLOR, radius=0.12)
        label_Q = MathTex("Q", font_size=28, color=HIGHLIGHT_COLOR)
        label_Q.next_to(point_Q, UL, buff=0.1)

        self.play(FadeIn(point_Q, scale=0.5), Write(label_Q))

        # Explanation
        covering_text = Text(
            "Each point Q has exactly 3 preimages",
            font_size=26,
            color=WHITE,
        )
        covering_text.to_edge(DOWN, buff=0.5)
        self.play(Write(covering_text))

        # Show 3 preimages on E1
        preimage_props = [0.2, 0.5, 0.75]
        preimages = VGroup()
        preimage_labels = []
        preimage_arrows = VGroup()

        for i, prop in enumerate(preimage_props):
            branch = i % len(e1_paths)
            pos = e1_paths[min(branch, len(e1_paths) - 1)].point_from_proportion(prop)
            dot = Dot(pos, color=SECRET_COLOR, radius=0.1)
            preimages.add(dot)

            label = MathTex(f"P_{i+1}", font_size=24, color=SECRET_COLOR)
            # Specific positioning for each preimage
            if i == 0:  # P1
                if pos[1] > e1.get_center()[1]:
                    label.next_to(dot, UP, buff=0.08)
                else:
                    label.next_to(dot, DOWN, buff=0.08)
            elif i == 1:  # P2
                label.next_to(dot, LEFT, buff=0.08)
            elif i == 2:  # P3
                label.next_to(dot, UL, buff=0.08)
            preimage_labels.append(label)

            # Arrow from preimage to Q
            arrow = CurvedArrow(
                pos,
                q_pos,
                angle=-0.2 + i * 0.2,
                color=SECRET_COLOR,
                stroke_width=2,
                stroke_opacity=0.6,
                tip_length=0.15,
            )
            preimage_arrows.add(arrow)

        self.play(
            LaggedStart(*[FadeIn(p, scale=0.5) for p in preimages], lag_ratio=0.2),
            LaggedStart(*[Write(l) for l in preimage_labels], lag_ratio=0.2),
            run_time=1,
        )

        self.play(
            LaggedStart(*[Create(a) for a in preimage_arrows], lag_ratio=0.15),
            FadeOut(isogeny_arrow),
            FadeOut(deg_label),
            FadeOut(deg_value),
            run_time=1,
        )

        # Formula
        covering_formula = MathTex(
            "|\\varphi^{-1}(Q)| = \\deg(\\varphi) = 3",
            font_size=28,
            color=WHITE,
        )
        covering_formula.next_to(covering_text, UP, buff=0.3)
        self.play(Write(covering_formula))

        self.wait(4)

        # Clean up
        self.play(*[FadeOut(m) for m in self.mobjects])

        # === PART 3: DEGREE MULTIPLIES UNDER COMPOSITION ===

        step3 = Text("Composition Multiplies Degrees", font_size=24, color=PURPLE_C)
        step3.to_corner(UL, buff=0.4)
        self.play(FadeIn(step3))

        # Three curves in a chain
        curves = []
        curve_labels = []
        b_vals = [0.6, 0.75, 0.8]
        positions = [LEFT * 5, ORIGIN, RIGHT * 5]
        names = ["E_1", "E_2", "E_3"]

        for i, (b, pos, name) in enumerate(zip(b_vals, positions, names)):
            curve = EllipticCurve(a=-1, b=b, color=CURVE_COLOR, stroke_width=3)
            curve.scale(0.35).move_to(pos + UP * 0.5)
            curves.append(curve)

            label = MathTex(name, font_size=28, color=CURVE_COLOR)
            label.next_to(curve, DOWN, buff=0.2)
            curve_labels.append(label)

        self.play(
            *[GrowFromCenter(c) for c in curves],
            *[Write(l) for l in curve_labels],
        )

        # First isogeny: degree 2
        arrow1 = Arrow(
            curves[0].get_right(),
            curves[1].get_left(),
            color=GREEN_C,
            stroke_width=3,
            buff=0.15,
        )
        phi_label = MathTex("\\varphi", font_size=28, color=GREEN_C)
        phi_label.next_to(arrow1, UP, buff=0.1)
        deg1_label = MathTex("\\deg = 2", font_size=24, color=GREEN_C)
        deg1_label.next_to(arrow1, DOWN, buff=0.05)

        self.play(GrowArrow(arrow1), Write(phi_label), Write(deg1_label))

        # Second isogeny: degree 3
        arrow2 = Arrow(
            curves[1].get_right(),
            curves[2].get_left(),
            color=TEAL_C,
            stroke_width=3,
            buff=0.15,
        )
        psi_label = MathTex("\\psi", font_size=28, color=TEAL_C)
        psi_label.next_to(arrow2, UP, buff=0.1)
        deg2_label = MathTex("\\deg = 3", font_size=24, color=TEAL_C)
        deg2_label.next_to(arrow2, DOWN, buff=0.05)

        self.play(GrowArrow(arrow2), Write(psi_label), Write(deg2_label))

        self.wait(1)

        # Show composition arrow
        comp_arrow = CurvedArrow(
            curves[0].get_top() + UP * 0.1,
            curves[2].get_top() + UP * 0.1,
            angle=-0.5,
            color=GOLD_A,
            stroke_width=4,
        )
        comp_label = MathTex("\\psi \\circ \\varphi", font_size=28, color=GOLD_A)
        comp_label.next_to(comp_arrow, UP, buff=0.1)

        self.play(Create(comp_arrow), Write(comp_label))

        # The key formula
        mult_formula = MathTex(
            "\\deg(\\psi \\circ \\varphi) = \\deg(\\psi) \\cdot \\deg(\\varphi) = 3 \\cdot 2 = 6",
            font_size=32,
            color=GOLD_A,
        )
        mult_formula.to_edge(DOWN, buff=0.5)
        self.play(Write(mult_formula))

        self.wait(4)

        # Clean up
        self.play(*[FadeOut(m) for m in self.mobjects])

        # === PART 4: COMPUTATIONAL COST ===

        step4 = Text(
            "Why Degree Matters: Computational Cost", font_size=24, color=SECRET_COLOR
        )
        step4.to_corner(UL, buff=0.4)
        self.play(FadeIn(step4))

        # Key insight text
        cost_insight = Text(
            "Computing an isogeny costs O(degree) operations",
            font_size=28,
            color=WHITE,
        )
        cost_insight.move_to(UP * 2.5)
        self.play(Write(cost_insight))

        self.wait(1)

        # Show the problem with large degrees
        problem_box = VGroup(
            Text("Random degree:", font_size=28, color=WHITE),
            MathTex(
                "d \\approx \\sqrt{p} \\approx 2^{128}",
                font_size=36,
                color=SECRET_COLOR,
            ),
            Text("Cost:", font_size=28, color=WHITE),
            MathTex("2^{128} \\text{ operations}", font_size=36, color=SECRET_COLOR),
            Text("= IMPOSSIBLE", font_size=32, color=SECRET_COLOR, weight=BOLD),
        )
        problem_box.arrange(DOWN, buff=0.2)
        problem_box.move_to(LEFT * 3 + DOWN * 0.5)

        problem_bg = SurroundingRectangle(
            problem_box,
            color=SECRET_COLOR,
            fill_color=BLACK,
            fill_opacity=0.9,
            stroke_width=2,
            buff=0.3,
            corner_radius=0.1,
        )

        self.play(FadeIn(problem_bg), Write(problem_box), run_time=1.5)
        self.wait(1)

        # Show the solution with smooth degrees
        solution_box = VGroup(
            Text("Smooth degree:", font_size=28, color=WHITE),
            MathTex("d = 2^{256}", font_size=36, color=HIGHLIGHT_COLOR),
            Text("Factor into chain:", font_size=28, color=WHITE),
            MathTex(
                "256 \\times O(2) \\approx 512 \\text{ ops}",
                font_size=32,
                color=HIGHLIGHT_COLOR,
            ),
            Text("= EASY!", font_size=32, color=HIGHLIGHT_COLOR, weight=BOLD),
        )
        solution_box.arrange(DOWN, buff=0.2)
        solution_box.move_to(RIGHT * 3 + DOWN * 0.5)

        solution_bg = SurroundingRectangle(
            solution_box,
            color=HIGHLIGHT_COLOR,
            fill_color=BLACK,
            fill_opacity=0.9,
            stroke_width=2,
            buff=0.3,
            corner_radius=0.1,
        )

        self.play(FadeIn(solution_bg), Write(solution_box), run_time=1.5)
        self.wait(4)

        # Clean up
        self.play(*[FadeOut(m) for m in self.mobjects])

        # === PART 5: SMOOTH DEGREE CHAIN VISUALIZATION ===

        step5 = Text(
            "Smooth Degrees: Decompose into Chain", font_size=24, color=HIGHLIGHT_COLOR
        )
        step5.to_corner(UL, buff=0.4)
        self.play(FadeIn(step5))

        # Show degree 8 = 2 × 2 × 2
        explanation = MathTex(
            "\\deg = 8 = 2 \\times 2 \\times 2",
            font_size=32,
            color=WHITE,
        )
        explanation.to_edge(UP, buff=0.8)
        self.play(Write(explanation))

        # Create chain of 4 curves
        chain_curves = []
        chain_labels = []
        chain_b_vals = [0.5, 0.6, 0.75, 0.8]
        chain_positions = [LEFT * 5.5, LEFT * 1.8, RIGHT * 1.8, RIGHT * 5.5]
        chain_names = ["E_0", "E_1", "E_2", "E_3"]

        for b, pos, name in zip(chain_b_vals, chain_positions, chain_names):
            curve = EllipticCurve(a=-1, b=b, color=CURVE_COLOR, stroke_width=3)
            curve.scale(0.28).move_to(pos)
            chain_curves.append(curve)

            label = MathTex(name, font_size=24, color=CURVE_COLOR)
            label.next_to(curve, DOWN, buff=0.15)
            chain_labels.append(label)

        self.play(
            LaggedStart(*[GrowFromCenter(c) for c in chain_curves], lag_ratio=0.15),
            LaggedStart(*[Write(l) for l in chain_labels], lag_ratio=0.15),
            run_time=1.5,
        )

        # Add degree-2 arrows between each pair
        chain_arrows = []
        arrow_labels = []

        for i in range(3):
            arrow = Arrow(
                chain_curves[i].get_right(),
                chain_curves[i + 1].get_left(),
                color=HIGHLIGHT_COLOR,
                stroke_width=3,
                buff=0.1,
            )
            chain_arrows.append(arrow)

            deg_label = MathTex("2", font_size=24, color=HIGHLIGHT_COLOR)
            deg_label.next_to(arrow, UP, buff=0.05)
            arrow_labels.append(deg_label)

        for arrow, label in zip(chain_arrows, arrow_labels):
            self.play(GrowArrow(arrow), Write(label), run_time=0.5)

        self.wait(1)

        # Show total cost calculation
        cost_calc = VGroup(
            Text("Each step: O(2) operations", font_size=26, color=WHITE),
            Text("Total: 3 steps × O(2) = O(6)", font_size=26, color=HIGHLIGHT_COLOR),
            Text("vs. direct O(8) operations", font_size=26, color=GRAY_B),
        )
        cost_calc.arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        cost_calc.to_edge(DOWN, buff=0.5)

        self.play(Write(cost_calc), run_time=1.5)
        self.wait(5)
