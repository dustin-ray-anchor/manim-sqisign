"""
Torsion Points and Kernels - E[N] as a coordinate grid
Save as: scenes/torsion_points.py
Run with: manim -pql scenes/torsion_points.py TorsionPoints
"""

from manim import *
import numpy as np

# Color scheme
CURVE_COLOR = BLUE_D
ISOGENY_COLOR = GOLD_A
HIGHLIGHT_COLOR = GREEN_C
SECRET_COLOR = RED_C
PUBLIC_COLOR = BLUE_B
P_COLOR = RED_C
Q_COLOR = BLUE_C
KERNEL_COLOR = GOLD_A
TORSION_COLOR = TEAL_B


class TorsionPoints(Scene):
    """Visualize N-torsion as a 2D grid and kernels as subgroups."""

    def construct(self):
        # === PART 1: INTRODUCE N-TORSION ===

        step1 = Text("N-Torsion Subgroup", font_size=24, color=GOLD_A)
        step1.to_corner(UL, buff=0.4)
        self.play(FadeIn(step1))

        # Definition
        definition = MathTex(
            r"E[N] = \{ P \in E : [N]P = \mathcal{O} \}",
            font_size=36,
            color=WHITE,
        )
        definition.move_to(UP * 2)
        self.play(Write(definition))

        explanation = Text(
            "Points that become identity when multiplied by N",
            font_size=24,
            color=GRAY_B,
        )
        explanation.next_to(definition, DOWN, buff=0.3)
        self.play(FadeIn(explanation))

        self.wait(1.5)

        # Key structure
        structure = MathTex(
            r"E[N] \cong (\mathbb{Z}/N\mathbb{Z})^2",
            font_size=42,
            color=HIGHLIGHT_COLOR,
        )
        structure.next_to(explanation, DOWN, buff=0.5)
        self.play(Write(structure))

        size_note = MathTex(
            r"N^2 \text{ elements}",
            font_size=32,
            color=WHITE,
        )
        size_note.next_to(structure, DOWN, buff=0.2)
        self.play(FadeIn(size_note))

        self.wait(2)

        # Clear and transition
        self.play(
            FadeOut(definition),
            FadeOut(explanation),
            FadeOut(structure),
            FadeOut(size_note),
        )

        # === PART 2: VISUALIZE AS GRID ===

        step2 = Text("E[N] as a Coordinate Grid", font_size=24, color=GOLD_A)
        step2.to_corner(UL, buff=0.4)
        self.play(FadeOut(step1), FadeIn(step2))

        # Use N=5 for nice visualization (25 points)
        N = 5
        grid_spacing = 1.1  # Increased for better visibility
        grid_center = DOWN * 0.3

        # Create the grid of torsion points
        torsion_grid = VGroup()
        point_dict = {}  # (a, b) -> dot

        for a in range(N):
            for b in range(N):
                x = (a - N // 2) * grid_spacing
                y = (b - N // 2) * grid_spacing
                pos = grid_center + np.array([x, y, 0])

                dot = Dot(pos, color=TORSION_COLOR, radius=0.08)
                point_dict[(a, b)] = dot
                torsion_grid.add(dot)

        # Grid lines (faint)
        grid_lines = VGroup()
        extent = (N // 2 + 0.5) * grid_spacing

        for i in range(N):
            offset = (i - N // 2) * grid_spacing
            # Vertical lines
            vline = Line(
                grid_center + np.array([offset, -extent, 0]),
                grid_center + np.array([offset, extent, 0]),
                color=GRAY,
                stroke_width=1.5,
                stroke_opacity=0.5,
            )
            # Horizontal lines
            hline = Line(
                grid_center + np.array([-extent, offset, 0]),
                grid_center + np.array([extent, offset, 0]),
                color=GRAY,
                stroke_width=1.5,
                stroke_opacity=0.5,
            )
            grid_lines.add(vline, hline)

        self.play(Create(grid_lines), run_time=0.8)
        self.play(
            LaggedStart(*[FadeIn(d, scale=0.5) for d in torsion_grid], lag_ratio=0.02),
            run_time=1.5,
        )

        # Label showing this is E[5]
        grid_label = MathTex(r"E[5]", font_size=36, color=TORSION_COLOR)
        grid_label.next_to(torsion_grid, UP, buff=0.4)
        size_label = MathTex(r"25 \text{ points}", font_size=28, color=WHITE)
        size_label.next_to(grid_label, RIGHT, buff=0.3)
        self.play(FadeIn(grid_label), FadeIn(size_label))

        self.wait(1)

        # === PART 3: HIGHLIGHT BASIS ===

        step3 = Text("Basis {P, Q}", font_size=24, color=GOLD_A)
        step3.to_corner(UL, buff=0.4)
        self.play(FadeOut(step2), FadeIn(step3))

        # Highlight P (the point at (1, 0) in Z/NZ × Z/NZ)
        P_point = point_dict[(1, 0)]
        P_highlight = P_point.copy().set_color(P_COLOR).scale(1.8)

        P_label = MathTex("P", font_size=36, color=P_COLOR)
        P_label.next_to(P_highlight, DOWN, buff=0.15)

        # Highlight Q (the point at (0, 1) in Z/NZ × Z/NZ)
        Q_point = point_dict[(0, 1)]
        Q_highlight = Q_point.copy().set_color(Q_COLOR).scale(1.8)

        Q_label = MathTex("Q", font_size=36, color=Q_COLOR)
        Q_label.next_to(Q_highlight, LEFT, buff=0.15)

        # Origin/identity point at (0, 0)
        O_point = point_dict[(0, 0)]
        O_highlight = O_point.copy().set_color(WHITE).scale(1.5)
        O_label = MathTex(r"\mathcal{O}", font_size=32, color=WHITE)
        O_label.next_to(O_highlight, DOWN + LEFT, buff=0.1)

        self.play(
            Transform(P_point, P_highlight),
            Transform(Q_point, Q_highlight),
            Transform(O_point, O_highlight),
            FadeIn(P_label),
            FadeIn(Q_label),
            FadeIn(O_label),
            run_time=1,
        )

        # Basis explanation
        basis_text = MathTex(
            r"\text{Any point} = [a]P + [b]Q",
            font_size=32,
            color=WHITE,
        )
        basis_text.to_corner(DR, buff=0.5)

        basis_bg = SurroundingRectangle(
            basis_text,
            color=WHITE,
            fill_color=BLACK,
            fill_opacity=0.9,
            stroke_width=2,
            buff=0.3,
            corner_radius=0.1,
        )

        self.play(FadeIn(basis_bg), FadeIn(basis_text))

        self.wait(1)

        # Show coordinates for a sample point
        sample_a, sample_b = 3, 2  # The point [3]P + [2]Q
        sample_point = point_dict[(sample_a, sample_b)]
        sample_highlight = sample_point.copy().set_color(YELLOW).scale(1.6)

        sample_label = MathTex(
            f"[{sample_a}]P + [{sample_b}]Q",
            font_size=28,
            color=YELLOW,
        )
        sample_label.next_to(sample_highlight, UP + RIGHT, buff=0.1)

        self.play(
            Transform(sample_point, sample_highlight),
            FadeIn(sample_label),
        )

        self.wait(2)

        # Clean up sample
        self.play(FadeOut(sample_label))

        # === PART 4: CYCLIC SUBGROUPS AS LINES ===

        step4 = Text("Cyclic Subgroups", font_size=24, color=GOLD_A)
        step4.to_corner(UL, buff=0.4)
        self.play(FadeOut(step3), FadeIn(step4), FadeOut(basis_bg), FadeOut(basis_text))

        # A cyclic subgroup of order N is generated by some [α]P + [β]Q
        # Show the subgroup generated by P + 2Q (i.e., α=1, β=2)
        alpha, beta = 1, 2

        # Points in the cyclic subgroup: k*(α, β) mod N for k = 0, 1, ..., N-1
        kernel_points = []
        kernel_positions = []
        for k in range(N):
            coord_a = (k * alpha) % N
            coord_b = (k * beta) % N
            if (coord_a, coord_b) in point_dict:
                kernel_points.append(point_dict[(coord_a, coord_b)])
                # Get visual position for path
                x = (coord_a - N // 2) * grid_spacing
                y = (coord_b - N // 2) * grid_spacing
                kernel_positions.append(grid_center + np.array([x, y, 0]))

        # Highlight the kernel subgroup
        kernel_vg = VGroup(*kernel_points)

        # Dim non-kernel points
        non_kernel = VGroup(*[p for p in torsion_grid if p not in kernel_points])

        self.play(
            non_kernel.animate.set_opacity(0.2),
            *[p.animate.set_color(KERNEL_COLOR).scale(1.5) for p in kernel_points],
            run_time=1.5,
        )

        # Connect kernel points with a path to show cyclic structure
        # Order them by k to show the cycle: 0 -> 1 -> 2 -> ... -> 0
        kernel_path_points = kernel_positions + [kernel_positions[0]]  # Close the loop

        kernel_path = VMobject()
        kernel_path.set_points_smoothly(kernel_path_points)
        kernel_path.set_stroke(color=KERNEL_COLOR, width=2, opacity=0.6)

        self.play(Create(kernel_path), run_time=1)

        # Label the generator
        generator_label = MathTex(
            r"\langle [1]P + [2]Q \rangle",
            font_size=32,
            color=KERNEL_COLOR,
        )
        generator_label.to_edge(DOWN, buff=0.8)
        self.play(FadeIn(generator_label))

        self.wait(1)

        # Show this is a kernel
        kernel_text = Text(
            "= Kernel of a degree-5 isogeny",
            font_size=26,
            color=WHITE,
        )
        kernel_text.next_to(generator_label, DOWN, buff=0.2)
        self.play(FadeIn(kernel_text))

        self.wait(2)

        # === PART 5: COMPACT REPRESENTATION ===

        step5 = Text("Compact Encoding", font_size=24, color=GOLD_A)
        step5.to_corner(UL, buff=0.4)
        self.play(FadeOut(step4), FadeIn(step5))

        self.play(FadeOut(generator_label), FadeOut(kernel_text))

        # The key insight box
        insight = VGroup(
            Text("To specify a degree-N isogeny:", font_size=26, color=WHITE),
            MathTex(
                r"\text{Kernel generator } K = [\alpha]P + [\beta]Q",
                font_size=30,
                color=KERNEL_COLOR,
            ),
            Text("Just two integers (α, β) !", font_size=28, color=HIGHLIGHT_COLOR),
        )
        insight.arrange(DOWN, buff=0.25)
        insight.to_edge(DOWN, buff=0.5)

        insight_bg = SurroundingRectangle(
            insight,
            color=GOLD_A,
            fill_color=BLACK,
            fill_opacity=0.9,
            stroke_width=2,
            buff=0.25,
            corner_radius=0.1,
        )

        self.play(FadeIn(insight_bg), FadeIn(insight), run_time=1)

        self.wait(2)

        # Emphasize: (1, 2) encodes this entire isogeny
        # Fade out grid labels before showing coordinates
        self.play(FadeOut(grid_label), FadeOut(size_label))

        coord_box = MathTex(
            r"(\alpha, \beta) = (1, 2)",
            font_size=42,
            color=KERNEL_COLOR,
        )
        coord_box.move_to(UP * 2.8)

        arrow_to_kernel = Arrow(
            coord_box.get_bottom(),
            kernel_vg.get_top() + UP * 0.3,
            color=KERNEL_COLOR,
            buff=0.2,
        )

        self.play(FadeIn(coord_box), GrowArrow(arrow_to_kernel))

        self.wait(2)

        # === PART 6: WHY THIS MATTERS ===

        self.play(
            FadeOut(coord_box),
            FadeOut(arrow_to_kernel),
            FadeOut(insight),
            FadeOut(insight_bg),
        )

        step6 = Text("Why Rational Torsion Matters", font_size=24, color=GOLD_A)
        step6.to_corner(UL, buff=0.4)
        self.play(FadeOut(step5), FadeIn(step6))

        # Restore grid visibility
        self.play(
            non_kernel.animate.set_opacity(1),
            kernel_path.animate.set_opacity(0.3),
            *[p.animate.set_color(TORSION_COLOR).scale(1 / 1.5) for p in kernel_points],
            run_time=1,
        )

        # Prime form explanation
        prime_explanation = VGroup(
            Text("For efficient computation:", font_size=26, color=WHITE),
            MathTex(
                r"E[2^f] \text{ must be } \mathbb{F}_{p^2}\text{-rational}",
                font_size=30,
                color=WHITE,
            ),
            Text("This requires:", font_size=24, color=GRAY_B),
            MathTex(
                r"2^f \mid (p^2 - 1)",
                font_size=34,
                color=HIGHLIGHT_COLOR,
            ),
            Text("So primes have the form:", font_size=24, color=GRAY_B),
            MathTex(
                r"p = 2^f \cdot (\text{small odd}) - 1",
                font_size=32,
                color=GOLD_A,
            ),
        )
        prime_explanation.arrange(DOWN, buff=0.2)
        prime_explanation.move_to(ORIGIN)

        prime_bg = SurroundingRectangle(
            prime_explanation,
            color=GRAY,
            fill_color=BLACK,
            fill_opacity=0.9,
            stroke_width=1,
            buff=0.25,
            corner_radius=0.1,
        )

        self.play(FadeIn(prime_bg), FadeIn(prime_explanation), run_time=1)

        self.wait(7)

        # Final cleanup
        self.play(
            FadeOut(prime_bg),
            FadeOut(prime_explanation),
            FadeOut(grid_label),
            FadeOut(size_label),
            FadeOut(P_label),
            FadeOut(Q_label),
            FadeOut(O_label),
            FadeOut(torsion_grid),
            FadeOut(grid_lines),
            FadeOut(kernel_path),
            FadeOut(step6),
        )

        # === FINAL SUMMARY ===

        summary = VGroup(
            Text("Key Takeaways:", font_size=32, color=GOLD_A),
            MathTex(
                r"E[N] \cong (\mathbb{Z}/N\mathbb{Z})^2", font_size=36, color=WHITE
            ),
            Text("Basis {P, Q} gives coordinates", font_size=28, color=WHITE),
            MathTex(
                r"\text{Kernel } \langle [\alpha]P + [\beta]Q \rangle \to \text{Isogeny}",
                font_size=30,
                color=KERNEL_COLOR,
            ),
            Text(
                "Two integers encode an isogeny!", font_size=28, color=HIGHLIGHT_COLOR
            ),
        )
        summary.arrange(DOWN, buff=0.35)

        self.play(FadeIn(summary), run_time=1.5)

        self.wait(4)
