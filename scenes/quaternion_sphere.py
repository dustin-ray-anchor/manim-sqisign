"""
Quaternion Sphere - Visualizing i, j, k as rotation axes
Save as: scenes/quaternion_sphere.py
Run with: manim -pql scenes/quaternion_sphere.py QuaternionSphere
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
REAL_COLOR = WHITE
POINT_COLOR = YELLOW


class QuaternionSphere(ThreeDScene):
    """Visualize quaternions as points on a sphere."""

    def construct(self):
        # === SETUP ===

        title = Text("Quaternion Unit Sphere", font_size=24, color=GOLD_A)
        title.to_corner(UL, buff=0.4)
        self.add_fixed_in_frame_mobjects(title)
        self.play(FadeIn(title))

        # Set up 3D view
        self.set_camera_orientation(phi=70 * DEGREES, theta=-45 * DEGREES)

        # Create the unit sphere (scaled up for better visibility)
        scale_factor = 2.5
        sphere = Surface(
            lambda u, v: scale_factor
            * np.array([np.cos(u) * np.cos(v), np.cos(u) * np.sin(v), np.sin(u)]),
            u_range=[-PI / 2, PI / 2],
            v_range=[0, TAU],
            resolution=(24, 48),
            fill_opacity=0.15,
            stroke_width=0.5,
            stroke_opacity=0.3,
            checkerboard_colors=[BLUE_E, BLUE_D],
        )

        # Create axes through the sphere as simple lines
        axis_length = 1.8 * scale_factor
        k_axis_length = 1.4 * scale_factor  # Shorter k-axis for better label visibility

        # i-axis (x-axis) - red
        i_axis = Line3D(
            start=[-axis_length, 0, 0],
            end=[axis_length, 0, 0],
            color=I_COLOR,
            stroke_width=2,
        )

        # j-axis (y-axis) - green
        j_axis = Line3D(
            start=[0, -axis_length, 0],
            end=[0, axis_length, 0],
            color=J_COLOR,
            stroke_width=2,
        )

        # k-axis (z-axis) - blue (shorter for label visibility)
        k_axis = Line3D(
            start=[0, 0, -k_axis_length],
            end=[0, 0, k_axis_length],
            color=K_COLOR,
            stroke_width=2,
        )

        # Small dots at axis endpoints for cleaner look
        axis_dots = VGroup(
            Dot3D([axis_length, 0, 0], color=I_COLOR, radius=0.08),
            Dot3D([-axis_length, 0, 0], color=I_COLOR, radius=0.08),
            Dot3D([0, axis_length, 0], color=J_COLOR, radius=0.08),
            Dot3D([0, -axis_length, 0], color=J_COLOR, radius=0.08),
            Dot3D([0, 0, k_axis_length], color=K_COLOR, radius=0.08),
            Dot3D([0, 0, -k_axis_length], color=K_COLOR, radius=0.08),
        )

        # Axis labels (positioned at axis endpoints in 3D space)
        label_offset = 0.5  # Distance beyond axis endpoint

        i_label = MathTex("i", font_size=54, color=I_COLOR)
        i_label.rotate(90 * DEGREES, axis=RIGHT)
        i_label.move_to([axis_length + label_offset, 0, 0])

        i_neg_label = MathTex("-i", font_size=48, color=I_COLOR)
        i_neg_label.rotate(90 * DEGREES, axis=RIGHT)
        i_neg_label.move_to([-axis_length - label_offset, 0, 0])

        j_label = MathTex("j", font_size=54, color=J_COLOR)
        j_label.rotate(90 * DEGREES, axis=RIGHT)
        j_label.move_to([0, axis_length + label_offset, 0])

        j_neg_label = MathTex("-j", font_size=48, color=J_COLOR)
        j_neg_label.rotate(90 * DEGREES, axis=RIGHT)
        j_neg_label.move_to([0, -axis_length - label_offset, 0])

        k_label = MathTex("k", font_size=54, color=K_COLOR)
        k_label.rotate(90 * DEGREES, axis=RIGHT)
        k_label.move_to([0, 0, k_axis_length + label_offset])

        k_neg_label = MathTex("-k", font_size=48, color=K_COLOR)
        k_neg_label.rotate(90 * DEGREES, axis=RIGHT)
        k_neg_label.move_to([0, 0, -k_axis_length - label_offset])

        # Build the scene
        self.play(Create(sphere), run_time=1.5)

        # Grow axes outward from origin simultaneously
        self.play(
            GrowFromCenter(i_axis),
            GrowFromCenter(j_axis),
            GrowFromCenter(k_axis),
            run_time=1.5,
        )

        # Fade in endpoint dots
        self.play(
            LaggedStart(*[FadeIn(d, scale=0.5) for d in axis_dots], lag_ratio=0.08),
            run_time=0.8,
        )

        # Add labels (in 3D space, will rotate with camera)
        self.play(
            FadeIn(i_label),
            FadeIn(i_neg_label),
            FadeIn(j_label),
            FadeIn(j_neg_label),
            FadeIn(k_label),
            FadeIn(k_neg_label),
            run_time=0.8,
        )

        # === VALUE TRACKER AND DISPLAY ===

        def generate_valid_spherical_coords():
            """Generate random theta, phi where all i,j,k are in [0.1, 0.9]"""
            max_attempts = 100
            for _ in range(max_attempts):
                # Generate random spherical coordinates
                theta = np.random.uniform(0, 2 * PI)
                phi = np.random.uniform(0.3, PI - 0.3)  # Avoid poles

                # Calculate resulting i, j, k
                i = np.sin(phi) * np.cos(theta)
                j = np.sin(phi) * np.sin(theta)
                k = np.cos(phi)

                # Check if all are in valid range
                if all(0.1 <= abs(val) <= 0.9 for val in [i, j, k]):
                    return theta, phi

            # Fallback to safe default
            return PI/4, PI/3

        # Start with a valid random position
        initial_theta, initial_phi = generate_valid_spherical_coords()
        theta_tracker = ValueTracker(initial_theta)
        phi_tracker = ValueTracker(initial_phi)

        def get_point_coords():
            theta = theta_tracker.get_value()
            phi = phi_tracker.get_value()
            x = np.sin(phi) * np.cos(theta)
            y = np.sin(phi) * np.sin(theta)
            z = np.cos(phi)
            return scale_factor * np.array([x, y, z])

        # Create the moving point on the sphere
        point_on_sphere = always_redraw(
            lambda: Dot3D(
                get_point_coords(),
                color=POINT_COLOR,
                radius=0.15,
            )
        )

        # Line from origin to point
        radius_line = always_redraw(
            lambda: Line3D(
                [0, 0, 0],
                get_point_coords(),
                color=POINT_COLOR,
                stroke_width=2,
            )
        )

        # Value display in top right corner
        def create_value_display():
            coords = get_point_coords() / scale_factor
            i_val = coords[0]
            j_val = coords[1]
            k_val = coords[2]

            display = VGroup(
                MathTex(f"i = {i_val:+.2f}", font_size=42, color=I_COLOR),
                MathTex(f"j = {j_val:+.2f}", font_size=42, color=J_COLOR),
                MathTex(f"k = {k_val:+.2f}", font_size=42, color=K_COLOR),
            )
            display.arrange(DOWN, aligned_edge=LEFT, buff=0.15)
            display.to_corner(UR, buff=0.5)
            return display

        value_display = always_redraw(create_value_display)

        display_bg = always_redraw(
            lambda: SurroundingRectangle(
                create_value_display(),
                color=WHITE,
                fill_color=BLACK,
                fill_opacity=0.9,
                stroke_width=1,
                buff=0.2,
                corner_radius=0.1,
            )
        )

        self.add_fixed_in_frame_mobjects(display_bg, value_display)

        # Add point and radius line
        self.play(
            FadeIn(display_bg),
            FadeIn(value_display),
            FadeIn(point_on_sphere, scale=0.5),
            Create(radius_line),
            run_time=1,
        )

        self.wait(1)

        # === ANIMATE POINT MOVING AROUND SPHERE ===

        # Start slow ambient camera rotation
        self.begin_ambient_camera_rotation(rate=0.08)

        # Generate random valid positions and animate between them
        num_positions = 6
        for i in range(num_positions):
            target_theta, target_phi = generate_valid_spherical_coords()
            self.play(
                theta_tracker.animate.set_value(target_theta),
                phi_tracker.animate.set_value(target_phi),
                run_time=2.5,
                rate_func=smooth,
            )
            self.wait(0.3)

        self.wait(1)

        # === FINAL MESSAGE ===

        explanation = Text(
            "Point on unit sphere = unit quaternion",
            font_size=28,
            color=WHITE,
        )
        explanation.to_edge(DOWN, buff=0.5)

        explanation_bg = SurroundingRectangle(
            explanation,
            color=WHITE,
            fill_color=BLACK,
            fill_opacity=0.9,
            stroke_width=2,
            buff=0.3,
            corner_radius=0.1,
        )

        self.add_fixed_in_frame_mobjects(explanation_bg, explanation)
        self.play(FadeIn(explanation_bg), FadeIn(explanation))

        # Continue rotation
        self.wait(4)
        self.stop_ambient_camera_rotation()

        self.wait(2)
