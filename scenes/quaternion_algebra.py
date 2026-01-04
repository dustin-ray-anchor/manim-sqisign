"""
Quaternion Algebra B_{p,∞} - From sphere to ellipsoid
Save as: scenes/quaternion_algebra.py
Run with: manim -pql scenes/quaternion_algebra.py QuaternionAlgebra
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
PRIME_COLOR = GOLD_A


class QuaternionAlgebra(ThreeDScene):
    """Visualize the quaternion algebra B_{p,∞} and how it differs from Hamilton's quaternions."""

    def construct(self):
        # === PART 1: SETUP - RECALL THE STANDARD SPHERE ===

        step1 = Text("Hamilton's Quaternions", font_size=24, color=GOLD_A)
        step1.to_corner(UL, buff=0.4)
        self.add_fixed_in_frame_mobjects(step1)
        self.play(FadeIn(step1))

        # Set up 3D view
        self.set_camera_orientation(phi=70 * DEGREES, theta=-45 * DEGREES)

        scale_factor = 2.0

        # Create the unit sphere
        sphere = Surface(
            lambda u, v: scale_factor
            * np.array([np.cos(u) * np.cos(v), np.cos(u) * np.sin(v), np.sin(u)]),
            u_range=[-PI / 2, PI / 2],
            v_range=[0, TAU],
            resolution=(24, 48),
            fill_opacity=0.2,
            stroke_width=0.5,
            stroke_opacity=0.3,
            checkerboard_colors=[BLUE_E, BLUE_D],
        )

        # Create axes
        axis_length = 1.6 * scale_factor

        i_axis = Line3D(
            start=[-axis_length, 0, 0],
            end=[axis_length, 0, 0],
            color=I_COLOR,
            stroke_width=2,
        )
        j_axis = Line3D(
            start=[0, -axis_length, 0],
            end=[0, axis_length, 0],
            color=J_COLOR,
            stroke_width=2,
        )
        k_axis = Line3D(
            start=[0, 0, -axis_length],
            end=[0, 0, axis_length],
            color=K_COLOR,
            stroke_width=2,
        )

        # Axis labels
        label_offset = 0.4
        i_label = MathTex("i", font_size=48, color=I_COLOR)
        i_label.rotate(90 * DEGREES, axis=RIGHT)
        i_label.move_to([axis_length + label_offset, 0, 0])

        j_label = MathTex("j", font_size=48, color=J_COLOR)
        j_label.rotate(90 * DEGREES, axis=RIGHT)
        j_label.move_to([0, axis_length + label_offset, 0])

        k_label = MathTex("k", font_size=48, color=K_COLOR)
        k_label.rotate(90 * DEGREES, axis=RIGHT)
        k_label.move_to([0, 0, axis_length + label_offset])

        axes_group = VGroup(i_axis, j_axis, k_axis)
        labels_group = VGroup(i_label, j_label, k_label)

        # Show the standard relations
        standard_relations = VGroup(
            MathTex("i^2 = -1", font_size=36, color=I_COLOR),
            MathTex("j^2 = -1", font_size=36, color=J_COLOR),
            MathTex("ij = -ji = k", font_size=36, color=K_COLOR),
        )
        standard_relations.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        standard_relations.to_corner(DR, buff=0.5)

        relations_bg = SurroundingRectangle(
            standard_relations,
            color=GRAY,
            fill_color=BLACK,
            fill_opacity=0.9,
            stroke_width=1,
            buff=0.25,
            corner_radius=0.1,
        )

        self.add_fixed_in_frame_mobjects(relations_bg, standard_relations)

        # Build the scene
        self.play(Create(sphere), run_time=1.5)
        self.play(
            GrowFromCenter(i_axis),
            GrowFromCenter(j_axis),
            GrowFromCenter(k_axis),
            run_time=1,
        )
        # self.play(FadeIn(labels_group), run_time=0.6)
        # self.play(FadeIn(relations_bg), FadeIn(standard_relations), run_time=0.8)

        # Norm formula for standard quaternions
        standard_norm = MathTex(
            r"\text{Norm: } a^2 + b^2 + c^2 + d^2",
            font_size=28,
            color=WHITE,
        )
        standard_norm.to_edge(DOWN, buff=0.5)
        self.add_fixed_in_frame_mobjects(standard_norm)
        self.play(FadeIn(standard_norm))

        self.wait(2)

        # === PART 2: INTRODUCE B_{p,∞} ===

        step2 = Text("SQIsign: The Algebra  B", font_size=24, color=GOLD_A)
        step2_sub = MathTex(r"_{p,\infty}", font_size=30, color=GOLD_A)
        step2_sub.next_to(step2, RIGHT, buff=0.05).shift(DOWN * 0.1)
        step2_group = VGroup(step2, step2_sub)
        step2_group.to_corner(UL, buff=0.4)

        self.add_fixed_in_frame_mobjects(step2_group)
        self.play(FadeOut(step1), FadeIn(step2_group))

        # Update relations - highlight the change
        # Note: k² = -p is derived from k = ij, not an axiom
        # Use p = 3 for visible effect (sqrt(3) ≈ 1.73)
        new_relations = VGroup(
            MathTex("p = 3", font_size=36, color=PRIME_COLOR),
            MathTex("i^2 = -1", font_size=36, color=I_COLOR),
            MathTex("j^2 = -p", font_size=36, color=PRIME_COLOR),
            MathTex("ij = -ji = k", font_size=36, color=K_COLOR),
        )
        new_relations.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        new_relations.to_corner(DR, buff=0.5)

        new_relations_bg = SurroundingRectangle(
            new_relations,
            color=GOLD_A,
            fill_color=BLACK,
            fill_opacity=0.9,
            stroke_width=2,
            buff=0.25,
            corner_radius=0.1,
        )

        # Transform to new relations (smooth transition)
        # First fade out old content, then fade in new with expanded box
        self.play(FadeOut(standard_relations), run_time=0.4)
        self.play(
            ReplacementTransform(relations_bg, new_relations_bg),
            run_time=0.6,
        )
        self.add_fixed_in_frame_mobjects(new_relations_bg, new_relations)
        self.play(FadeIn(new_relations), run_time=0.5)

        # Highlight the key difference (only j² = -p, the one change)
        highlight_box = SurroundingRectangle(
            new_relations[2],
            color=PRIME_COLOR,
            stroke_width=3,
            buff=0.1,
        )
        self.add_fixed_in_frame_mobjects(highlight_box)
        self.play(Create(highlight_box), run_time=0.6)

        self.wait(1)

        # === PART 3: MORPH SPHERE TO ELLIPSOID ===

        # Use p = 3 for visible effect (sqrt(3) ≈ 1.73)
        p_value = 3
        compression = 1 / np.sqrt(p_value)

        # Create the ellipsoid (compressed in j and k directions)
        ellipsoid = Surface(
            lambda u, v: scale_factor
            * np.array(
                [
                    np.cos(u) * np.cos(v),  # i direction: unchanged
                    compression * np.cos(u) * np.sin(v),  # j direction: compressed
                    compression * np.sin(u),  # k direction: compressed
                ]
            ),
            u_range=[-PI / 2, PI / 2],
            v_range=[0, TAU],
            resolution=(24, 48),
            fill_opacity=0.2,
            stroke_width=0.5,
            stroke_opacity=0.3,
            checkerboard_colors=[GOLD_E, GOLD_D],
        )

        # Compressed axes
        j_axis_new = Line3D(
            start=[0, -axis_length * compression, 0],
            end=[0, axis_length * compression, 0],
            color=J_COLOR,
            stroke_width=2,
        )
        k_axis_new = Line3D(
            start=[0, 0, -axis_length * compression],
            end=[0, 0, axis_length * compression],
            color=K_COLOR,
            stroke_width=2,
        )

        # New label positions
        j_label_new = MathTex("j", font_size=48, color=J_COLOR)
        j_label_new.rotate(90 * DEGREES, axis=RIGHT)
        j_label_new.move_to([0, axis_length * compression + label_offset, 0])

        k_label_new = MathTex("k", font_size=48, color=K_COLOR)
        k_label_new.rotate(90 * DEGREES, axis=RIGHT)
        k_label_new.move_to([0, 0, axis_length * compression + label_offset])

        # Update norm formula
        new_norm = MathTex(
            r"\text{Nrd}(\alpha) = a^2 + b^2 + ",
            r"p",
            r"c^2 + ",
            r"p",
            r"d^2",
            font_size=28,
        )
        new_norm.set_color(WHITE)
        new_norm[1].set_color(PRIME_COLOR)
        new_norm[3].set_color(PRIME_COLOR)
        new_norm.to_edge(DOWN, buff=0.5)

        self.play(FadeOut(standard_norm))
        self.add_fixed_in_frame_mobjects(new_norm)

        # Animate the transformation!
        self.play(
            Transform(sphere, ellipsoid),
            Transform(j_axis, j_axis_new),
            Transform(k_axis, k_axis_new),
            Transform(j_label, j_label_new),
            Transform(k_label, k_label_new),
            FadeIn(new_norm),
            FadeOut(highlight_box),
            run_time=2.5,
            rate_func=smooth,
        )

        self.wait(1)

        # === PART 4: EXPLAIN THE GEOMETRY ===

        explanation = Text(
            "j and k axes compressed by  1/√p",
            font_size=26,
            color=WHITE,
            t2c={"1/√p": PRIME_COLOR},
        )
        explanation.to_edge(DOWN, buff=1.2)
        self.add_fixed_in_frame_mobjects(explanation)
        self.play(FadeOut(new_norm), FadeIn(explanation))

        # Start gentle camera rotation
        self.begin_ambient_camera_rotation(rate=0.1)

        self.wait(3)

        # === PART 5: KEY PROPERTY - MULTIPLICATIVE NORM ===

        self.play(FadeOut(explanation))

        mult_property = MathTex(
            r"\text{Nrd}(\alpha\beta) = \text{Nrd}(\alpha) \cdot \text{Nrd}(\beta)",
            font_size=28,
            color=WHITE,
        )
        mult_property.to_edge(DOWN, buff=1.2)
        self.add_fixed_in_frame_mobjects(mult_property)
        self.play(FadeIn(mult_property))

        self.wait(2)

        # Final note
        self.play(FadeOut(mult_property))

        final_note = Text(
            "Quaternion Algebra with prime p",
            font_size=26,
            color=WHITE,
        )
        final_note.to_edge(DOWN, buff=1.2)
        self.add_fixed_in_frame_mobjects(final_note)
        self.play(FadeIn(final_note))

        self.wait(4)

        self.stop_ambient_camera_rotation()
        self.wait(2)
