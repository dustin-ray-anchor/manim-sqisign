"""
Dimensional Lifting Visualization - SQIsign v2.0
Save as: scenes/dimensional_lifting.py
Run with: manim -pql scenes/dimensional_lifting.py DimensionalLifting
"""

from manim import *
import numpy as np
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from elliptic_curve import EllipticCurve, EllipticCurveWithFill, EllipticCurveIcon, preset_curve


# Color scheme (matching other files)
CURVE_COLOR = BLUE_D
ISOGENY_COLOR = GOLD_A
HIGHLIGHT_COLOR = GREEN_C
SECRET_COLOR = RED_C
PUBLIC_COLOR = BLUE_B


class DimensionalLifting(ThreeDScene):
    """Visualize how dimensional lifting enables efficient isogeny computation."""

    def construct(self):
        # === PART 1: THE 2D BOTTLENECK ===

        # Start with flat 2D view
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, gamma=0)

        # Step indicator in top left
        step_indicator = Text("Step 1: The bottleneck", font_size=24, color=GRAY_B)
        step_indicator.to_corner(UL, buff=0.4)
        self.add_fixed_in_frame_mobjects(step_indicator)
        self.play(FadeIn(step_indicator))

        # Two curves in 2D
        e1 = EllipticCurveIcon(
            color=GREEN_C, fill_opacity=0.0, stroke_width=3, shape=1.0
        )
        e1.scale(0.4).move_to(LEFT * 4)

        e2 = EllipticCurveIcon(
            color=RED_C, fill_opacity=0.0, stroke_width=3, shape=1.0
        )
        e2.scale(0.4).move_to(RIGHT * 4)

        e1_label = MathTex("E_1", font_size=42, color=GREEN_C)
        e1_label.next_to(e1, DOWN, buff=0.2)
        e2_label = MathTex("E_2", font_size=42, color=RED_C)
        e2_label.next_to(e2, DOWN, buff=0.2)

        self.play(
            GrowFromCenter(e1), GrowFromCenter(e2), Write(e1_label), Write(e2_label)
        )
        self.wait(0.5)

        # Show the "bad" isogeny - non-smooth degree
        bad_arrow = Arrow(
            e1.get_right() + RIGHT * 0.1,
            e2.get_left() + LEFT * 0.1,
            color=RED_C,
            stroke_width=4,
            buff=0,
        )
        bad_degree = MathTex(
            "\\deg = p \\text{ (large prime)}", font_size=32, color=RED_C
        )
        bad_degree.next_to(bad_arrow, UP, buff=0.15)

        self.play(GrowArrow(bad_arrow), Write(bad_degree))

        # X mark - can't compute directly
        x_mark = MathTex("\\times", font_size=64, color=RED)
        x_mark.move_to(bad_arrow.get_center())

        impossible = Text("Too slow!", font_size=24, color=RED_C)
        impossible.next_to(bad_arrow, DOWN, buff=0.3)
        self.add_fixed_in_frame_mobjects(impossible)

        self.play(FadeIn(x_mark, scale=2), FadeIn(impossible))
        self.wait(1.5)

        # Show timing
        old_time = MathTex(
            "\\text{KLPT: } \\sim 2000 \\text{ ms}", font_size=36, color=RED_C
        )
        old_time.to_corner(DL, buff=0.5)
        self.add_fixed_in_frame_mobjects(old_time)
        self.play(Write(old_time))
        self.wait(1)

        # Clear the blockage indicators
        self.play(
            FadeOut(x_mark),
            FadeOut(impossible),
            FadeOut(bad_arrow),
            FadeOut(bad_degree),
            FadeOut(old_time),
        )

        # === PART 2: LIFTING TO HIGHER DIMENSIONS ===

        # Update step indicator
        step2 = Text("Step 2: Lift to 2D", font_size=24, color=GOLD_A)
        step2.to_corner(UL, buff=0.4)
        self.add_fixed_in_frame_mobjects(step2)
        self.play(FadeOut(step_indicator), FadeIn(step2))
        step_indicator = step2

        # Create 3D representations - we'll make a "lifted" version
        # First, create companion curves that will form the product
        e1_companion = EllipticCurveIcon(
            color=BLUE_B, fill_opacity=0.0, stroke_width=2, shape=1.0
        )
        e1_companion.scale(0.4).move_to(LEFT * 4)

        e2_companion = EllipticCurveIcon(
            color=BLUE_B, fill_opacity=0.0, stroke_width=2, shape=1.0
        )
        e2_companion.scale(0.4).move_to(RIGHT * 4)

        # Labels for the product
        product_label_1 = MathTex("E_1 \\times E_1'", font_size=40, color=TEAL_C)
        product_label_1.next_to(e1, DOWN, buff=0.5)
        product_label_2 = MathTex("E_2 \\times E_2'", font_size=40, color=TEAL_C)
        product_label_2.next_to(e2, DOWN, buff=0.5)

        # Animate the dimensional lift - rotate camera to reveal 3D
        self.play(FadeOut(e1_label), FadeOut(e2_label))

        # Move companion curves to z-offset position
        e1_companion.shift(OUT * 1.5)
        e2_companion.shift(OUT * 1.5)

        self.play(
            FadeIn(e1_companion, shift=OUT),
            FadeIn(e2_companion, shift=OUT),
        )

        # Dramatic camera rotation to reveal 3D structure
        self.move_camera(
            phi=60 * DEGREES,
            theta=-60 * DEGREES,
            run_time=2,
            added_anims=[Write(product_label_1), Write(product_label_2)],
        )
        self.wait(1)

        # Show "Abelian Surface" label
        surface_note = Text("Abelian Surfaces", font_size=28, color=TEAL_C)
        surface_note.to_edge(DOWN, buff=0.5)
        self.add_fixed_in_frame_mobjects(surface_note)
        self.play(FadeIn(surface_note))

        # Draw vertical connectors to show the product structure
        connector1_lines = VGroup(
            Line(
                e1.get_center(),
                e1_companion.get_center(),
                color=TEAL_C,
                stroke_width=1,
                stroke_opacity=0.5,
            ),
        )
        connector2_lines = VGroup(
            Line(
                e2.get_center(),
                e2_companion.get_center(),
                color=TEAL_C,
                stroke_width=1,
                stroke_opacity=0.5,
            ),
        )

        self.play(Create(connector1_lines), Create(connector2_lines))
        self.wait(1)

        # === PART 3: THE EASY PATH IN HIGHER DIMENSIONS ===

        # Update step indicator
        step3 = Text("Step 3: Chain 2-isogenies", font_size=24, color=GREEN_C)
        step3.to_corner(UL, buff=0.4)
        self.add_fixed_in_frame_mobjects(step3)
        self.play(FadeOut(step_indicator), FadeIn(step3))
        step_indicator = step3

        # Create intermediate "stepping stones" in 3D
        num_steps = 5
        intermediates_bottom = VGroup()
        intermediates_top = VGroup()

        x_positions = np.linspace(-2.5, 2.5, num_steps)

        for i, x in enumerate(x_positions):
            # Bottom curve
            curve_bottom = EllipticCurveIcon(
                color=GOLD_A, fill_opacity=0.0, stroke_width=2, shape=1.0
            )
            curve_bottom.scale(0.25).move_to(np.array([x, 0, 0]))
            intermediates_bottom.add(curve_bottom)

            # Top curve (companion)
            curve_top = EllipticCurveIcon(
                color=GOLD_A, fill_opacity=0.0, stroke_width=1.5, shape=1.0
            )
            curve_top.scale(0.25).move_to(np.array([x, 0, 1.5]))
            intermediates_top.add(curve_top)

        # Animate intermediates appearing
        self.play(
            LaggedStart(
                *[GrowFromCenter(c) for c in intermediates_bottom], lag_ratio=0.1
            ),
            LaggedStart(*[GrowFromCenter(c) for c in intermediates_top], lag_ratio=0.1),
            run_time=1.5,
        )

        # Create the chain of 2-isogenies (arrows between steps)
        arrows_bottom = VGroup()
        arrows_top = VGroup()

        # Arrow from e1 to first intermediate
        arr_start_bottom = Arrow(
            e1.get_right(),
            intermediates_bottom[0].get_left(),
            color=GREEN_C,
            stroke_width=3,
            buff=0.1,
        )
        arr_start_top = Arrow(
            e1_companion.get_right(),
            intermediates_top[0].get_left(),
            color=GREEN_C,
            stroke_width=2,
            buff=0.1,
        )

        self.play(GrowArrow(arr_start_bottom), GrowArrow(arr_start_top))

        # Arrows between intermediates
        for i in range(num_steps - 1):
            arr_b = Arrow(
                intermediates_bottom[i].get_right(),
                intermediates_bottom[i + 1].get_left(),
                color=GREEN_C,
                stroke_width=3,
                buff=0.05,
            )
            arr_t = Arrow(
                intermediates_top[i].get_right(),
                intermediates_top[i + 1].get_left(),
                color=GREEN_C,
                stroke_width=2,
                buff=0.05,
            )
            arrows_bottom.add(arr_b)
            arrows_top.add(arr_t)

        self.play(
            LaggedStart(*[GrowArrow(a) for a in arrows_bottom], lag_ratio=0.1),
            LaggedStart(*[GrowArrow(a) for a in arrows_top], lag_ratio=0.1),
            run_time=1.5,
        )

        # Arrow to e2
        arr_end_bottom = Arrow(
            intermediates_bottom[-1].get_right(),
            e2.get_left(),
            color=GREEN_C,
            stroke_width=3,
            buff=0.1,
        )
        arr_end_top = Arrow(
            intermediates_top[-1].get_right(),
            e2_companion.get_left(),
            color=GREEN_C,
            stroke_width=2,
            buff=0.1,
        )

        self.play(GrowArrow(arr_end_bottom), GrowArrow(arr_end_top))

        self.wait(1.5)

        # === PART 4: PROJECT BACK DOWN ===

        # Update step indicator
        step4 = Text("Step 4: Project to 1D", font_size=24, color=GOLD_A)
        step4.to_corner(UL, buff=0.4)
        self.add_fixed_in_frame_mobjects(step4)
        self.play(FadeOut(step_indicator), FadeIn(step4))
        step_indicator = step4

        # Rotate camera back to 2D view
        self.move_camera(phi=0, theta=-90 * DEGREES, run_time=2)

        # Fade out the 3D elements
        self.play(
            FadeOut(e1_companion),
            FadeOut(e2_companion),
            FadeOut(intermediates_top),
            FadeOut(arrows_top),
            FadeOut(arr_start_top),
            FadeOut(arr_end_top),
            FadeOut(connector1_lines),
            FadeOut(connector2_lines),
            FadeOut(product_label_1),
            FadeOut(product_label_2),
            FadeOut(surface_note),
            run_time=1.5,
        )

        # Update step indicator
        step5 = Text("Step 5: Result", font_size=24, color=GOLD_A)
        step5.to_corner(UL, buff=0.4)
        self.add_fixed_in_frame_mobjects(step5)
        self.play(FadeOut(step_indicator), FadeIn(step5))
        step_indicator = step5

        # Keep the chain visible - add labels to show it represents the isogeny
        phi_label = MathTex("\\varphi", font_size=48, color=GOLD_A)
        phi_label.move_to(UP * 1.5)

        result_text = Text("= chain of 2-isogenies", font_size=28, color=GOLD_A)
        result_text.next_to(phi_label, DOWN, buff=0.3)

        # Checkmark
        check = MathTex("\\checkmark", font_size=72, color=GREEN_C)
        check.move_to(UP * 2.5)

        self.play(Write(phi_label), FadeIn(result_text))
        self.play(FadeIn(check, scale=2))

        # New labels for curves
        new_e1_label = MathTex("E_1", font_size=42, color=GREEN_C)
        new_e1_label.next_to(e1, DOWN, buff=0.2)
        new_e2_label = MathTex("E_2", font_size=42, color=RED_C)
        new_e2_label.next_to(e2, DOWN, buff=0.2)
        self.play(Write(new_e1_label), Write(new_e2_label))

        # Show the dramatic speedup
        self.wait(1)

        speedup_box = VGroup()
        old_timing = MathTex(
            "\\text{v1.0: } \\sim 2000 \\text{ ms}", font_size=36, color=RED_C
        )
        new_timing = MathTex(
            "\\text{v2.0: } \\sim 100 \\text{ ms}", font_size=36, color=GREEN_C
        )
        speedup = MathTex("20\\times \\text{ faster!}", font_size=42, color=GOLD_A)

        speedup_box.add(old_timing, new_timing, speedup)
        speedup_box.arrange(DOWN, buff=0.3)
        speedup_box.to_corner(DR, buff=0.5)

        bg_rect = SurroundingRectangle(
            speedup_box,
            color=GRAY,
            fill_color=BLACK,
            fill_opacity=0.8,
            stroke_width=1,
            buff=0.25,
            corner_radius=0.1,
        )
        self.add_fixed_in_frame_mobjects(bg_rect, speedup_box)

        self.play(FadeIn(bg_rect), FadeIn(speedup_box))

        self.wait(3)
