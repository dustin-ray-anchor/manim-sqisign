"""
Elliptic Curves as Algebraic Objects - Beyond nodes in a graph
Save as: scenes/elliptic_curve_algebra.py
Run with: manim -pql scenes/elliptic_curve_algebra.py EllipticCurveAlgebra
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
POINT_COLOR = YELLOW_C


class EllipticCurveAlgebra(Scene):
    """Visualize elliptic curves as algebraic objects with group structure."""

    def construct(self):
        # Curve parameters used throughout
        a_val, b_val = -1, 1

        def curve_y(x, sign=1):
            """Get y value on curve for given x."""
            val = x**3 + a_val * x + b_val
            if val >= 0:
                return sign * np.sqrt(val)
            return 0

        def find_third_intersection(x1, y1, x2, y2):
            """Find third intersection point of line through (x1,y1) and (x2,y2) with curve."""
            if abs(x2 - x1) < 1e-10:
                # Vertical line - handle separately
                return x1, -y1
            m = (y2 - y1) / (x2 - x1)
            # Sum of roots = m², so x3 = m² - x1 - x2
            x3 = m**2 - x1 - x2
            c = y1 - m * x1
            y3 = m * x3 + c
            return x3, y3

        # === PART 1: FROM NODES TO EQUATIONS ===

        step1 = Text("Beyond Nodes", font_size=24, color=GOLD_A)
        step1.to_corner(UL, buff=0.4)
        self.play(FadeIn(step1))

        # Show the abstract node representation first
        abstract_node = EllipticCurveIcon(
            color=CURVE_COLOR, fill_opacity=0.0, stroke_width=3, shape=1.0
        )
        abstract_node.scale(0.4)

        node_label = MathTex("E", font_size=48, color=CURVE_COLOR)
        node_label.next_to(abstract_node, DOWN, buff=0.3)

        abstract_group = VGroup(abstract_node, node_label)
        abstract_group.move_to(ORIGIN)

        self.play(GrowFromCenter(abstract_node), Write(node_label))
        self.wait(1)

        # Transition text
        question = Text("What's inside?", font_size=28, color=WHITE)
        question.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(question))
        self.wait(1)

        # Move node to the left
        self.play(
            abstract_group.animate.scale(0.6).move_to(LEFT * 4.5),
            FadeOut(question),
        )

        # Show the equation
        equation = MathTex("y^2", "=", "x^3", "+", "a", "x", "+", "b", font_size=48)
        equation.set_color_by_tex("a", TEAL_C)
        equation.set_color_by_tex("b", TEAL_C)
        equation.move_to(RIGHT * 1.5 + UP * 2.5)

        self.play(Write(equation))
        self.wait(1)

        # === PART 2: THE ACTUAL CURVE ===

        step2 = Text("The Curve", font_size=24, color=HIGHLIGHT_COLOR)
        step2.to_corner(UL, buff=0.4)
        self.play(FadeOut(step1), FadeIn(step2))

        # Create axes
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=5,
            y_length=5,
            axis_config={"color": GRAY, "stroke_width": 2},
            tips=False,
        )
        axes.move_to(RIGHT * 1.5 + DOWN * 0.3)

        # Find where curve is valid (x³ - x + 1 ≥ 0)
        # For a=-1, b=1: curve exists for x ≥ -1.3247 approximately
        x_start = -1.3247

        # Plot both branches of the curve
        curve_upper = axes.plot(
            lambda x: curve_y(x, 1),
            x_range=[x_start, 2.5, 0.005],
            color=CURVE_COLOR,
            stroke_width=4,
            use_smoothing=True,
        )
        curve_lower = axes.plot(
            lambda x: curve_y(x, -1),
            x_range=[x_start, 2.5, 0.005],
            color=CURVE_COLOR,
            stroke_width=4,
            use_smoothing=True,
        )

        self.play(Create(axes), run_time=1)
        self.play(Create(curve_upper), Create(curve_lower), run_time=1.5)

        # Show specific equation values
        specific_eq = MathTex("y^2 = x^3 - x + 1", font_size=36, color=WHITE)
        specific_eq.next_to(axes, UP, buff=0.3)
        self.play(Transform(equation, specific_eq))
        self.wait(1)

        # === PART 3: POINTS ON THE CURVE ===

        step3 = Text("Points Form a Group", font_size=24, color=PUBLIC_COLOR)
        step3.to_corner(UL, buff=0.4)
        self.play(FadeOut(step2), FadeIn(step3))

        # Add points P and Q
        x_p = 0.5
        y_p = curve_y(x_p)
        point_P = Dot(axes.c2p(x_p, y_p), color=HIGHLIGHT_COLOR, radius=0.12)
        label_P = MathTex("P", font_size=32, color=HIGHLIGHT_COLOR)
        label_P.next_to(point_P, UL, buff=0.1)

        x_q = 1.5
        y_q = curve_y(x_q)
        point_Q = Dot(axes.c2p(x_q, y_q), color=SECRET_COLOR, radius=0.12)
        label_Q = MathTex("Q", font_size=32, color=SECRET_COLOR)
        label_Q.next_to(point_Q, UL, buff=0.1)

        self.play(FadeIn(point_P, scale=0.5), Write(label_P))
        self.play(FadeIn(point_Q, scale=0.5), Write(label_Q))
        self.wait(1)

        # Point at infinity annotation
        infinity_text = MathTex(
            "O = \\text{point at infinity (identity)}", font_size=28, color=GRAY_B
        )
        infinity_text.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(infinity_text))
        self.wait(1)

        # === PART 4: GEOMETRIC ADDITION ===

        step4 = Text("Geometric Addition", font_size=24, color=GOLD_A)
        step4.to_corner(UL, buff=0.4)
        self.play(FadeOut(step3), FadeIn(step4), FadeOut(infinity_text))

        # Calculate line through P and Q
        slope = (y_q - y_p) / (x_q - x_p)
        intercept = y_p - slope * x_p

        # Find third intersection
        x_r, y_r = find_third_intersection(x_p, y_p, x_q, y_q)

        # Create extended chord line - extend well beyond the points
        x_line_min = min(x_p, x_q, x_r) - 1.5
        x_line_max = max(x_p, x_q, x_r) + 1.0

        # Clamp to axes range
        x_line_min = max(x_line_min, -2.8)
        x_line_max = min(x_line_max, 2.8)

        line_start = axes.c2p(x_line_min, slope * x_line_min + intercept)
        line_end = axes.c2p(x_line_max, slope * x_line_max + intercept)

        chord_line = Line(line_start, line_end, color=GOLD_A, stroke_width=3)
        self.play(Create(chord_line))
        self.wait(0.5)

        # Third intersection point R'
        point_R_prime = Dot(axes.c2p(x_r, y_r), color=GOLD_A, radius=0.1)
        label_R_prime = MathTex("R'", font_size=28, color=GOLD_A)
        label_R_prime.next_to(point_R_prime, UL, buff=0.1)

        self.play(FadeIn(point_R_prime, scale=0.5), Write(label_R_prime))
        self.wait(0.5)

        # Reflection line (vertical)
        reflect_line = DashedLine(
            axes.c2p(x_r, y_r + 0.5),
            axes.c2p(x_r, -y_r - 0.5),
            color=WHITE,
            stroke_width=2,
            stroke_opacity=0.5,
        )
        self.play(Create(reflect_line))

        # Result point P + Q
        point_R = Dot(axes.c2p(x_r, -y_r), color=PURPLE_A, radius=0.12)
        label_R = MathTex("P + Q", font_size=32, color=PURPLE_A)
        label_R.next_to(point_R, UL, buff=0.15)

        self.play(FadeIn(point_R, scale=0.5), Write(label_R))
        self.wait(1)

        # Explanation box
        add_explanation = VGroup(
            Text("1. Draw line through P and Q", font_size=24, color=WHITE),
            Text("2. Find third intersection R'", font_size=24, color=WHITE),
            Text("3. Reflect across x-axis → P + Q", font_size=24, color=WHITE),
        )
        add_explanation.arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        add_explanation.move_to(LEFT * 4.5 + DOWN * 1)

        explain_bg = SurroundingRectangle(
            add_explanation,
            color=GRAY,
            fill_color=BLACK,
            fill_opacity=0.8,
            stroke_width=1,
            buff=0.2,
            corner_radius=0.1,
        )

        self.play(FadeOut(abstract_group))
        self.play(FadeIn(explain_bg), Write(add_explanation), run_time=1.5)
        self.wait(2)

        # === PART 4.5: INTERACTIVE - MOVE P ALONG THE CURVE ===

        step4b = Text("Points Always Land on the Curve", font_size=24, color=TEAL_C)
        step4b.to_corner(UL, buff=0.4)
        self.play(FadeOut(step4), FadeIn(step4b))

        # Remove the explanation box
        self.play(FadeOut(explain_bg), FadeOut(add_explanation))

        # Remove static elements silently - we'll replace with dynamic ones
        self.remove(
            point_P,
            label_P,
            point_R_prime,
            label_R_prime,
            reflect_line,
            point_R,
            label_R,
            chord_line,
        )

        # Create a ValueTracker to control P's x position
        p_x_tracker = ValueTracker(0.5)

        # Q stays fixed
        fixed_x_q = 1.5
        fixed_y_q = curve_y(fixed_x_q)

        # Dynamic P point
        dynamic_P = always_redraw(
            lambda: Dot(
                axes.c2p(p_x_tracker.get_value(), curve_y(p_x_tracker.get_value())),
                color=HIGHLIGHT_COLOR,
                radius=0.12,
            )
        )

        dynamic_P_label = always_redraw(
            lambda: MathTex("P", font_size=32, color=HIGHLIGHT_COLOR).next_to(
                axes.c2p(p_x_tracker.get_value(), curve_y(p_x_tracker.get_value())),
                UL,
                buff=0.1,
            )
        )

        # Dynamic chord line
        def get_chord_line():
            curr_x_p = p_x_tracker.get_value()
            curr_y_p = curve_y(curr_x_p)

            if abs(fixed_x_q - curr_x_p) < 0.05:
                # Points too close, use tangent or skip
                return Line(ORIGIN, ORIGIN, stroke_opacity=0)

            m = (fixed_y_q - curr_y_p) / (fixed_x_q - curr_x_p)
            c = curr_y_p - m * curr_x_p

            # Find third intersection
            x3, y3 = find_third_intersection(curr_x_p, curr_y_p, fixed_x_q, fixed_y_q)

            # Extend line (use same offsets as static version)
            x_min = min(curr_x_p, fixed_x_q, x3) - 1.5
            x_max = max(curr_x_p, fixed_x_q, x3) + 1.0
            x_min = max(x_min, -2.8)
            x_max = min(x_max, 2.8)

            return Line(
                axes.c2p(x_min, m * x_min + c),
                axes.c2p(x_max, m * x_max + c),
                color=GOLD_A,
                stroke_width=3,
            )

        dynamic_chord = always_redraw(get_chord_line)

        # Dynamic R' point
        def get_r_prime():
            curr_x_p = p_x_tracker.get_value()
            curr_y_p = curve_y(curr_x_p)
            if abs(fixed_x_q - curr_x_p) < 0.05:
                return Dot(ORIGIN, radius=0, fill_opacity=0)
            x3, y3 = find_third_intersection(curr_x_p, curr_y_p, fixed_x_q, fixed_y_q)
            return Dot(axes.c2p(x3, y3), color=GOLD_A, radius=0.1)

        dynamic_R_prime = always_redraw(get_r_prime)

        # Dynamic reflection line
        def get_reflect_line():
            curr_x_p = p_x_tracker.get_value()
            curr_y_p = curve_y(curr_x_p)
            if abs(fixed_x_q - curr_x_p) < 0.05:
                return DashedLine(ORIGIN, ORIGIN, stroke_opacity=0)
            x3, y3 = find_third_intersection(curr_x_p, curr_y_p, fixed_x_q, fixed_y_q)
            return DashedLine(
                axes.c2p(x3, y3 + 0.4),
                axes.c2p(x3, -y3 - 0.4),
                color=WHITE,
                stroke_width=2,
                stroke_opacity=0.4,
            )

        dynamic_reflect = always_redraw(get_reflect_line)

        # Dynamic P + Q point
        def get_sum_point():
            curr_x_p = p_x_tracker.get_value()
            curr_y_p = curve_y(curr_x_p)
            if abs(fixed_x_q - curr_x_p) < 0.05:
                return Dot(ORIGIN, radius=0, fill_opacity=0)
            x3, y3 = find_third_intersection(curr_x_p, curr_y_p, fixed_x_q, fixed_y_q)
            return Dot(axes.c2p(x3, -y3), color=PURPLE_A, radius=0.12)

        dynamic_sum = always_redraw(get_sum_point)

        dynamic_sum_label = always_redraw(
            lambda: MathTex("P + Q", font_size=28, color=PURPLE_A).next_to(
                get_sum_point(), UL, buff=0.1
            )
        )

        # Add all dynamic elements
        self.add(
            dynamic_chord,
            dynamic_P,
            dynamic_P_label,
            point_Q,
            label_Q,
            dynamic_R_prime,
            dynamic_reflect,
            dynamic_sum,
            dynamic_sum_label,
        )

        # Explanation text
        move_explanation = Text(
            "As P moves along the curve, P + Q is always on the curve",
            font_size=26,
            color=WHITE,
        )
        move_explanation.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(move_explanation))

        self.wait(0.5)

        # Animate P moving along the curve
        self.play(p_x_tracker.animate.set_value(-0.5), run_time=2, rate_func=smooth)
        self.wait(0.3)
        self.play(p_x_tracker.animate.set_value(1.0), run_time=2, rate_func=smooth)
        self.wait(0.3)
        self.play(p_x_tracker.animate.set_value(-1.0), run_time=2, rate_func=smooth)
        self.wait(0.3)
        self.play(p_x_tracker.animate.set_value(0.5), run_time=1.5, rate_func=smooth)

        self.wait(1)

        # === PART 5: SCALAR MULTIPLICATION ===

        step5 = Text("Scalar Multiplication", font_size=24, color=TEAL_C)
        step5.to_corner(UL, buff=0.4)
        self.play(FadeOut(step4b), FadeIn(step5))

        # Fade out dynamic elements
        self.play(
            FadeOut(dynamic_chord),
            FadeOut(dynamic_P),
            FadeOut(dynamic_P_label),
            FadeOut(dynamic_R_prime),
            FadeOut(dynamic_reflect),
            FadeOut(dynamic_sum),
            FadeOut(dynamic_sum_label),
            FadeOut(point_Q),
            FadeOut(label_Q),
            FadeOut(move_explanation),
        )

        # Recreate static P
        point_P = Dot(axes.c2p(x_p, y_p), color=HIGHLIGHT_COLOR, radius=0.12)
        label_P = MathTex("P", font_size=32, color=HIGHLIGHT_COLOR)
        label_P.next_to(point_P, UL, buff=0.1)
        self.add(point_P, label_P)

        # Show scalar multiplication concept
        scalar_eq = MathTex(
            "[n]P",
            "=",
            "\\underbrace{P + P + \\cdots + P}_{n \\text{ times}}",
            font_size=36,
        )
        scalar_eq[0].set_color(HIGHLIGHT_COLOR)
        scalar_eq.move_to(LEFT * 3.5 + UP * 1)

        self.play(Write(scalar_eq))
        self.wait(1)

        # Show multiples of P
        multi_positions = [
            (0.5, curve_y(0.5), "P"),
            (1.2, curve_y(1.2), "[2]P"),
            (0.1, -curve_y(0.1), "[3]P"),
            (1.8, curve_y(1.8), "[4]P"),
        ]

        colors = [HIGHLIGHT_COLOR, TEAL_C, BLUE_C, PURPLE_C]
        multiples = VGroup()
        multiple_labels = VGroup()

        for i, (x, y, label_text) in enumerate(multi_positions):
            dot = Dot(axes.c2p(x, y), color=colors[i], radius=0.1)
            label = MathTex(label_text, font_size=24, color=colors[i])
            label.next_to(dot, UL, buff=0.15)
            multiples.add(dot)
            multiple_labels.add(label)

        self.play(
            point_P.animate.set_color(colors[0]),
            label_P.animate.set_color(colors[0]),
        )

        for i in range(1, len(multiples)):
            self.play(
                FadeIn(multiples[i], scale=0.5),
                Write(multiple_labels[i]),
                run_time=0.5,
            )

        self.wait(1)

        # Key insight box
        insight_box = VGroup(
            Text("Easy:", font_size=32, color=HIGHLIGHT_COLOR),
            MathTex("P \\to [n]P", font_size=36, color=WHITE),
            Text("Hard:", font_size=32, color=SECRET_COLOR),
            MathTex("[n]P \\to n", font_size=36, color=WHITE),
        )
        insight_box.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        insight_box.move_to(LEFT * 3.5 + DOWN * 1.5)

        insight_bg = SurroundingRectangle(
            insight_box,
            color=GRAY,
            fill_color=BLACK,
            fill_opacity=0.85,
            stroke_width=1,
            buff=0.25,
            corner_radius=0.1,
        )

        self.play(FadeIn(insight_bg), Write(insight_box), run_time=1.5)
        self.wait(1)

        # Final note
        final_note = Text(
            "This is the foundation of elliptic curve cryptography",
            font_size=28,
            color=GOLD_A,
        )
        final_note.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(final_note))

        self.wait(3)
