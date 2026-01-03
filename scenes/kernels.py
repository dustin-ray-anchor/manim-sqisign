"""
Kernels: What Determines an Isogeny
Save as: scenes/kernels.py
Run with: manim -pql scenes/kernels.py Kernels
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


def get_curve_paths(curve):
    """Extract drawable paths from an EllipticCurve VGroup."""
    paths = [
        sm for sm in curve.submobjects if hasattr(sm, "points") and len(sm.points) > 0
    ]
    if not paths:
        paths = curve.family_members_with_points()
    return paths


class Kernels(Scene):
    """Visualize how kernels determine isogenies."""

    def construct(self):
        # === PART 1: SETUP - ISOGENY BETWEEN CURVES ===

        step1 = Text("Isogenies Have Kernels", font_size=24, color=GOLD_A)
        step1.to_corner(UL, buff=0.4)
        self.play(FadeIn(step1))

        # Create two curves side by side
        e1 = EllipticCurve(a=-1, b=0.6, color=CURVE_COLOR, stroke_width=4)
        e1.scale(0.45).move_to(LEFT * 3.5)

        e2 = EllipticCurve(a=-1, b=0.7, color=CURVE_COLOR, stroke_width=4)
        e2.scale(0.45).move_to(RIGHT * 3.5)

        e1_label = MathTex("E_1", font_size=36, color=CURVE_COLOR)
        e1_label.next_to(e1, DOWN, buff=0.3)

        e2_label = MathTex("E_2", font_size=36, color=CURVE_COLOR)
        e2_label.next_to(e2, DOWN, buff=0.3)

        self.play(
            GrowFromCenter(e1),
            GrowFromCenter(e2),
            Write(e1_label),
            Write(e2_label),
        )

        # Isogeny arrow
        isogeny_arrow = Arrow(
            e1.get_right() + RIGHT * 0.2,
            e2.get_left() + LEFT * 0.2,
            color=ISOGENY_COLOR,
            stroke_width=4,
            buff=0.1,
        )
        phi_label = MathTex("\\varphi", font_size=36, color=ISOGENY_COLOR)
        phi_label.next_to(isogeny_arrow, UP, buff=0.15)

        self.play(GrowArrow(isogeny_arrow), Write(phi_label))
        self.wait(1)

        # === PART 2: SHOW POINTS ON E1 ===

        step2 = Text("Points on the Source Curve", font_size=24, color=PUBLIC_COLOR)
        step2.to_corner(UL, buff=0.4)
        self.play(FadeOut(step1), FadeIn(step2))

        point_names = ["P_1", "P_2", "P_3", "P_4", "P_5", "O"]
        point_colors = [HIGHLIGHT_COLOR, TEAL_C, BLUE_C, PURPLE_C, PINK, IDENTITY_COLOR]

        # Get the actual curve paths from submobjects
        e1_paths = get_curve_paths(e1)
        num_e1_paths = len(e1_paths)

        # Sample points from the curve paths
        # (branch_index, proportion along that branch)
        point_samples = [
            (0, 0.15),  # P1
            (0, 0.40),  # P2
            (0, 0.65),  # P3
            (1 % num_e1_paths, 0.25),  # P4
            (1 % num_e1_paths, 0.55),  # P5
            (0, 0.90),  # O
        ]

        points_e1 = VGroup()
        point_labels_e1 = []

        for i, (name, color) in enumerate(zip(point_names, point_colors)):
            branch_idx, prop = point_samples[i]
            branch_idx = min(branch_idx, num_e1_paths - 1)

            # Get position on the actual curve path
            pos = e1_paths[branch_idx].point_from_proportion(prop)

            dot = Dot(pos, color=color, radius=0.1)
            points_e1.add(dot)

            label = MathTex(name, font_size=24, color=color)
            # Position label based on vertical position relative to curve center
            if pos[1] > e1.get_center()[1]:
                label.next_to(dot, UP, buff=0.08)
            else:
                label.next_to(dot, DOWN, buff=0.08)
            point_labels_e1.append(label)

        # Animate points appearing
        self.play(
            LaggedStart(*[FadeIn(p, scale=0.5) for p in points_e1], lag_ratio=0.1),
            LaggedStart(*[Write(l) for l in point_labels_e1], lag_ratio=0.1),
            run_time=1.5,
        )
        self.wait(1)

        # === PART 3: DEFINE THE KERNEL ===

        step3 = Text(
            "The Kernel: Points That Map to O", font_size=24, color=KERNEL_COLOR
        )
        step3.to_corner(UL, buff=0.4)
        self.play(FadeOut(step2), FadeIn(step3))

        # Kernel definition
        kernel_def = MathTex(
            "\\ker(\\varphi) = \\{ P \\in E_1 : \\varphi(P) = O \\}",
            font_size=32,
            color=WHITE,
        )
        kernel_def.to_edge(DOWN, buff=0.5)
        self.play(Write(kernel_def))
        self.wait(1)

        # Highlight kernel points (P1, P3, P5, and O form the kernel)
        kernel_indices = [0, 2, 4, 5]  # P1, P3, P5, O
        non_kernel_indices = [1, 3]  # P2, P4

        # Create glow rings around kernel points
        kernel_glows = VGroup()
        for i in kernel_indices:
            glow = Circle(radius=0.18, color=KERNEL_COLOR, stroke_width=3)
            glow.move_to(points_e1[i].get_center())
            kernel_glows.add(glow)

        self.play(
            *[Create(g) for g in kernel_glows],
            *[
                points_e1[i].animate.set_color(KERNEL_COLOR)
                for i in kernel_indices[:-1]
            ],  # Don't recolor O
            run_time=1,
        )

        # Dim non-kernel points
        self.play(
            *[points_e1[i].animate.set_opacity(0.3) for i in non_kernel_indices],
            *[point_labels_e1[i].animate.set_opacity(0.3) for i in non_kernel_indices],
            run_time=0.6,
        )

        kernel_text = MathTex(
            "\\ker(\\varphi) = \\{O, P_1, P_3, P_5\\}",
            font_size=28,
            color=KERNEL_COLOR,
        )
        kernel_text.next_to(e1, UP, buff=0.4)
        self.play(Write(kernel_text))
        self.wait(2)

        # === PART 4: KERNEL MAPS TO IDENTITY ===

        step4 = Text("Kernel Points Collapse to O", font_size=24, color=IDENTITY_COLOR)
        step4.to_corner(UL, buff=0.4)
        self.play(FadeOut(step3), FadeIn(step4))

        # Get E2 paths for point sampling
        e2_paths = get_curve_paths(e2)
        num_e2_paths = len(e2_paths)

        # Show identity point on E2 (sample from curve)
        identity_pos = e2_paths[0].point_from_proportion(0.90)
        identity_e2 = Dot(identity_pos, color=IDENTITY_COLOR, radius=0.15)
        identity_label = MathTex("O", font_size=32, color=IDENTITY_COLOR)
        identity_label.next_to(identity_e2, UR, buff=0.1)

        self.play(FadeIn(identity_e2, scale=0.5), Write(identity_label))
        self.wait(0.5)

        # Create copies of kernel points that will animate to O
        kernel_copies = VGroup()
        for i in kernel_indices:
            copy = points_e1[i].copy()
            copy.set_color(KERNEL_COLOR if i != 5 else IDENTITY_COLOR)
            kernel_copies.add(copy)

        self.add(kernel_copies)

        # Animate kernel points "flying" to identity on E2
        self.play(
            *[
                kc.animate.move_to(identity_e2.get_center()).scale(0.5).set_opacity(0.7)
                for kc in kernel_copies
            ],
            run_time=1.5,
            rate_func=smooth,
        )

        # Flash at identity to show they've merged
        flash = Circle(radius=0.3, color=KERNEL_COLOR, stroke_width=4)
        flash.move_to(identity_e2.get_center())
        self.play(
            Create(flash),
            flash.animate.scale(0.1).set_opacity(0),
            FadeOut(kernel_copies),
            run_time=0.8,
        )
        self.remove(flash)

        collapse_text = Text(
            "All kernel points map to the identity",
            font_size=26,
            color=WHITE,
        )
        collapse_text.to_edge(DOWN, buff=0.5)
        self.play(FadeOut(kernel_def), FadeIn(collapse_text))
        self.wait(2)

        # === PART 5: NON-KERNEL POINTS MAP NORMALLY ===

        step5 = Text("Other Points Map Normally", font_size=24, color=TEAL_C)
        step5.to_corner(UL, buff=0.4)
        self.play(FadeOut(step4), FadeIn(step5))

        # Restore non-kernel points
        self.play(
            *[points_e1[i].animate.set_opacity(1) for i in non_kernel_indices],
            *[point_labels_e1[i].animate.set_opacity(1) for i in non_kernel_indices],
        )

        # Show where non-kernel points map on E2
        # (branch_index, proportion)
        mapped_samples = [
            (0, 0.35),  # Where P2 maps
            (1 % num_e2_paths, 0.45),  # Where P4 maps
        ]

        mapped_points = VGroup()
        mapped_labels = []

        for i, (idx, (branch_idx, prop)) in enumerate(
            zip(non_kernel_indices, mapped_samples)
        ):
            color = point_colors[idx]
            branch_idx = min(branch_idx, num_e2_paths - 1)
            pos = e2_paths[branch_idx].point_from_proportion(prop)

            dot = Dot(pos, color=color, radius=0.1)
            mapped_points.add(dot)

            label = MathTex(f"\\varphi({point_names[idx]})", font_size=20, color=color)
            if pos[1] > e2.get_center()[1]:
                label.next_to(dot, UP, buff=0.1)
            else:
                label.next_to(dot, DOWN, buff=0.1)
            mapped_labels.append(label)

        # Create trajectory arrows
        trajectories = VGroup()
        for i, (idx, (branch_idx, prop)) in enumerate(
            zip(non_kernel_indices, mapped_samples)
        ):
            start = points_e1[idx].get_center()
            branch_idx = min(branch_idx, num_e2_paths - 1)
            end = e2_paths[branch_idx].point_from_proportion(prop)
            traj = CurvedArrow(
                start, end, angle=-0.3, color=point_colors[idx], stroke_width=2
            )
            trajectories.add(traj)

        self.play(
            *[Create(t) for t in trajectories],
            run_time=1,
        )
        self.play(
            *[FadeIn(p, scale=0.5) for p in mapped_points],
            *[Write(l) for l in mapped_labels],
            run_time=1,
        )

        self.wait(2)

        # === PART 6: KEY INSIGHT ===

        step6 = Text("Key Insight", font_size=24, color=GOLD_A)
        step6.to_corner(UL, buff=0.4)
        self.play(FadeOut(step5), FadeIn(step6))

        # Clean up some elements
        self.play(
            FadeOut(trajectories),
            FadeOut(mapped_points),
            *[FadeOut(l) for l in mapped_labels],
            FadeOut(collapse_text),
            FadeOut(kernel_text),
            FadeOut(kernel_glows),
        )

        # The key insight box
        insight_box = VGroup(
            Text("The kernel completely", font_size=32, color=WHITE),
            Text("determines the isogeny", font_size=32, color=WHITE),
            MathTex(
                "\\ker(\\varphi) \\;\\Longrightarrow\\; \\varphi",
                font_size=36,
                color=GOLD_A,
            ),
        )
        insight_box.arrange(DOWN, buff=0.2)
        insight_box.move_to(DOWN * 2)

        insight_bg = SurroundingRectangle(
            insight_box,
            color=GOLD_A,
            fill_color=BLACK,
            fill_opacity=0.9,
            stroke_width=2,
            buff=0.3,
            corner_radius=0.1,
        )

        self.play(FadeIn(insight_bg), Write(insight_box), run_time=1.5)
        self.wait(2)

        # === PART 7: DIFFERENT KERNELS → DIFFERENT CURVES ===

        step7 = Text(
            "Different Kernels, Different Targets", font_size=24, color=HIGHLIGHT_COLOR
        )
        step7.to_corner(UL, buff=0.4)
        self.play(FadeOut(step6), FadeIn(step7))

        # Move existing elements up and shrink
        self.play(
            FadeOut(insight_bg),
            FadeOut(insight_box),
            FadeOut(e2),
            FadeOut(e2_label),
            FadeOut(isogeny_arrow),
            FadeOut(phi_label),
            FadeOut(identity_e2),
            FadeOut(identity_label),
            e1.animate.scale(0.7).move_to(LEFT * 5 + UP * 1),
            e1_label.animate.scale(0.8).next_to(LEFT * 5 + UP * 1, DOWN, buff=0.2),
            *[p.animate.scale(0.7).shift(LEFT * 1.5 + UP * 1) for p in points_e1],
            *[l.animate.scale(0.7).shift(LEFT * 1.5 + UP * 1) for l in point_labels_e1],
        )

        # Show multiple target curves with different kernels
        target_curves = VGroup()
        target_labels = []
        kernel_specs = [
            ("\\{O, P_1\\}", "E_2", GREEN_C, 0.6),
            ("\\{O, P_2\\}", "E_3", TEAL_C, 0.65),
            ("\\{O, P_3\\}", "E_4", PURPLE_C, 0.7),
        ]

        for i, (ker_text, curve_name, color, b) in enumerate(kernel_specs):
            curve = EllipticCurve(a=-1, b=b, color=color, stroke_width=3)
            curve.scale(0.3).move_to(RIGHT * 2 + UP * (1.5 - i * 1.5))
            target_curves.add(curve)

            label = MathTex(curve_name, font_size=28, color=color)
            label.next_to(curve, RIGHT, buff=0.2)
            target_labels.append(label)

            # Arrow from E1
            arrow = Arrow(
                e1.get_right(),
                curve.get_left(),
                color=color,
                stroke_width=2,
                buff=0.1,
            )

            # Kernel annotation
            ker_label = MathTex(ker_text, font_size=20, color=color)
            ker_label.next_to(arrow, UP, buff=0.05)

            self.play(
                GrowFromCenter(curve),
                GrowArrow(arrow),
                Write(label),
                Write(ker_label),
                run_time=0.8,
            )

        self.wait(1)

        # Final message
        final_text = Text(
            "To specify an isogeny, just specify which points go to zero",
            font_size=26,
            color=GOLD_A,
        )
        final_text.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(final_text))

        self.wait(3)
