"""
Maximal Orders - Lattices in Quaternion Algebras
Save as: scenes/maximal_order.py
Run with: manim -pql scenes/maximal_order.py MaximalOrder
"""

from manim import *
import numpy as np

# Color scheme
CURVE_COLOR = BLUE_D
ISOGENY_COLOR = GOLD_A
HIGHLIGHT_COLOR = GREEN_C
SECRET_COLOR = RED_C
PUBLIC_COLOR = BLUE_B
I_COLOR = RED_C
J_COLOR = GREEN_C
K_COLOR = BLUE_C
LATTICE_COLOR = TEAL_B
ORDER_COLOR = PURPLE_B
IDEAL_COLOR = GOLD_A


class MaximalOrder(ThreeDScene):
    """Visualize maximal orders as lattices in quaternion algebras."""

    def construct(self):
        # === PART 1: RECALL THE QUATERNION SPACE ===

        step1 = Text("Quaternion Algebra  B", font_size=24, color=GOLD_A)
        step1_sub = MathTex(r"_{p,\infty}", font_size=18, color=GOLD_A)
        step1_sub.next_to(step1, RIGHT, buff=0.05).shift(DOWN * 0.08)
        step1_group = VGroup(step1, step1_sub)
        step1_group.to_corner(UL, buff=0.4)
        self.add_fixed_in_frame_mobjects(step1_group)
        self.play(FadeIn(step1_group))

        self.set_camera_orientation(phi=70 * DEGREES, theta=-45 * DEGREES)

        scale_factor = 4.5  # Increased for better visibility
        p_value = 3
        compression = 1 / np.sqrt(p_value)

        # Create faint ellipsoid as background context
        ellipsoid = Surface(
            lambda u, v: scale_factor
            * np.array(
                [
                    np.cos(u) * np.cos(v),
                    compression * np.cos(u) * np.sin(v),
                    compression * np.sin(u),
                ]
            ),
            u_range=[-PI / 2, PI / 2],
            v_range=[0, TAU],
            resolution=(20, 40),
            fill_opacity=0.08,
            stroke_width=0.3,
            stroke_opacity=0.15,
            checkerboard_colors=[BLUE_E, BLUE_D],
        )

        # Axes (faint)
        axis_length = 1.4 * scale_factor
        axes = VGroup(
            Line3D(
                [-axis_length, 0, 0],
                [axis_length, 0, 0],
                color=I_COLOR,
                stroke_width=1.5,
            ),
            Line3D(
                [0, -axis_length * compression, 0],
                [0, axis_length * compression, 0],
                color=J_COLOR,
                stroke_width=1.5,
            ),
            Line3D(
                [0, 0, -axis_length * compression],
                [0, 0, axis_length * compression],
                color=K_COLOR,
                stroke_width=1.5,
            ),
        )
        axes.set_opacity(0.4)

        self.play(FadeIn(ellipsoid), FadeIn(axes), run_time=1)

        # Explanation
        continuous_text = Text(
            "Continuous space of all quaternions",
            font_size=26,
            color=WHITE,
        )
        continuous_text.to_edge(DOWN, buff=0.5)
        self.add_fixed_in_frame_mobjects(continuous_text)
        self.play(FadeIn(continuous_text))

        self.wait(1.5)

        # === PART 2: INTRODUCE MAXIMAL ORDER ===

        step2 = Text("Maximal Order  O", font_size=24, color=ORDER_COLOR)
        step2.to_corner(UL, buff=0.4)
        self.add_fixed_in_frame_mobjects(step2)
        self.play(
            FadeOut(step1_group),
            FadeIn(step2),
            FadeOut(continuous_text),
        )

        # New explanation
        order_text = Text(
            "A maximal order: discrete 'integer-like' quaternions",
            font_size=26,
            color=WHITE,
        )
        order_text.to_edge(DOWN, buff=0.5)
        self.add_fixed_in_frame_mobjects(order_text)
        self.play(FadeIn(order_text))

        # Generate lattice points for a maximal order
        # Using basis {1, i, j, (1+i+j+k)/2} style structure
        # Simplified: just show a 3D lattice in the i,j,k subspace
        lattice_points = VGroup()
        lattice_range = 2

        for a in range(-lattice_range, lattice_range + 1):
            for b in range(-lattice_range, lattice_range + 1):
                for c in range(-lattice_range, lattice_range + 1):
                    # Scale and compress appropriately
                    x = a * 0.6 * scale_factor / 2
                    y = b * 0.6 * compression * scale_factor / 2
                    z = c * 0.6 * compression * scale_factor / 2

                    # Check if point is inside the ellipsoid
                    # Ellipsoid equation: (x/a)² + (y/b)² + (z/c)² ≤ 1
                    ellipsoid_check = (
                        (x / scale_factor) ** 2
                        + (y / (scale_factor * compression)) ** 2
                        + (z / (scale_factor * compression)) ** 2
                    )

                    # Only show points within ellipsoid and reasonable bounds
                    if (
                        ellipsoid_check <= 1.0
                        and abs(x) <= axis_length
                        and abs(y) <= axis_length * compression
                        and abs(z) <= axis_length * compression
                    ):
                        # Size based on distance from origin (closer = bigger)
                        dist = np.sqrt(x**2 + y**2 + z**2)
                        radius = 0.08 if dist < 1.5 else 0.05

                        point = Dot3D(
                            [x, y, z],
                            color=LATTICE_COLOR,
                            radius=radius,
                        )
                        lattice_points.add(point)

        # Animate lattice appearing
        self.play(
            LaggedStart(
                *[FadeIn(p, scale=0.5) for p in lattice_points],
                lag_ratio=0.02,
            ),
            run_time=2,
        )

        self.wait(1)

        # Start gentle rotation
        self.begin_ambient_camera_rotation(rate=0.08)

        # === PART 3: HIGHLIGHT STRUCTURE ===

        self.play(FadeOut(order_text))

        structure_text = Text(
            "Forms a 4-dimensional lattice (shown: i, j, k subspace)",
            font_size=24,
            color=WHITE,
        )
        structure_text.to_edge(DOWN, buff=0.5)
        self.add_fixed_in_frame_mobjects(structure_text)
        self.play(FadeIn(structure_text))

        self.wait(2)

        # === PART 4: ANALOGY BOX ===

        self.play(FadeOut(structure_text))

        analogy = VGroup(
            Text("Analogy:", font_size=32, color=GOLD_A),
            MathTex(r"\mathbb{Z}[i] \subset \mathbb{C}", font_size=36, color=WHITE),
            Text("Gaussian integers in complex plane", font_size=24, color=GRAY_B),
            MathTex(r"\mathcal{O} \subset B_{p,\infty}", font_size=36, color=WHITE),
            Text("Maximal order in quaternion algebra", font_size=24, color=GRAY_B),
        )
        analogy.arrange(DOWN, buff=0.2)
        analogy.to_corner(DR, buff=0.4)

        analogy_bg = SurroundingRectangle(
            analogy,
            color=GRAY,
            fill_color=BLACK,
            fill_opacity=0.9,
            stroke_width=1,
            buff=0.25,
            corner_radius=0.1,
        )

        self.add_fixed_in_frame_mobjects(analogy_bg, analogy)
        self.play(FadeIn(analogy_bg), FadeIn(analogy), run_time=1)

        self.wait(3)

        # === PART 5: TEASE IDEALS ===

        step3 = Text("Next: Ideals", font_size=24, color=IDEAL_COLOR)
        step3.to_corner(UL, buff=0.4)
        self.add_fixed_in_frame_mobjects(step3)
        self.play(FadeOut(step2), FadeIn(step3))

        self.play(FadeOut(analogy), FadeOut(analogy_bg))

        # Highlight a subset of points as an "ideal"
        ideal_points = VGroup()
        for point in lattice_points:
            pos = point.get_center()
            # Select points where coordinates are "even" - represents a sub-lattice
            x, y, z = pos[0], pos[1], pos[2]
            grid_x = round(x / (0.6 * scale_factor / 2))
            grid_y = round(y / (0.6 * compression * scale_factor / 2))
            grid_z = round(z / (0.6 * compression * scale_factor / 2))

            if grid_x % 2 == 0 and grid_y % 2 == 0 and grid_z % 2 == 0:
                ideal_points.add(point)

        # Dim non-ideal points, highlight ideal points
        non_ideal = VGroup(*[p for p in lattice_points if p not in ideal_points])

        self.play(
            non_ideal.animate.set_opacity(0.15),
            *[p.animate.set_color(IDEAL_COLOR).scale(1.5) for p in ideal_points],
            run_time=1.5,
        )

        ideal_text = Text(
            "An ideal: a sub-lattice with special properties",
            font_size=26,
            color=WHITE,
        )
        ideal_text.to_edge(DOWN, buff=0.5)
        self.add_fixed_in_frame_mobjects(ideal_text)
        self.play(FadeIn(ideal_text))

        self.wait(2)

        # Key connection
        self.play(FadeOut(ideal_text))

        connection = VGroup(
            Text("The Deuring Correspondence:", font_size=28, color=GOLD_A),
            Text("Ideals  ↔  Isogenies", font_size=32, color=WHITE),
            Text("Ideal norm  =  Isogeny degree", font_size=28, color=HIGHLIGHT_COLOR),
        )
        connection.arrange(DOWN, buff=0.25)
        connection.to_edge(DOWN, buff=0.4)

        connection_bg = SurroundingRectangle(
            connection,
            color=GOLD_A,
            fill_color=BLACK,
            fill_opacity=0.9,
            stroke_width=2,
            buff=0.25,
            corner_radius=0.1,
        )

        self.add_fixed_in_frame_mobjects(connection_bg, connection)
        self.play(FadeIn(connection_bg), FadeIn(connection), run_time=1)

        self.wait(4)

        self.stop_ambient_camera_rotation()
        self.wait(2)
