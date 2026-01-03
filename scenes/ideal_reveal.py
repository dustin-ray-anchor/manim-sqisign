"""
Path Finding with Secret Ideal Reveal - Shows how the secret ideal makes path-finding tractable
Save as: scenes/ideal_reveal.py
Run with: manim -pql scenes/ideal_reveal.py IdealReveal
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
IDEAL_COLOR = PURPLE_A


class IdealReveal(ThreeDScene):
    """Visualize how the secret ideal makes path-finding tractable."""

    def construct(self):
        # === PART 1: SETUP 2D GRAPH (same as PathFindingHardness) ===

        num_nodes = 16
        nodes = VGroup()
        positions = []

        np.random.seed(37)
        for i in range(num_nodes):
            angle = i * TAU / num_nodes + np.random.uniform(-0.15, 0.15)
            radius = 2.8 + np.random.uniform(-0.4, 0.4)
            pos = radius * np.array([np.cos(angle), np.sin(angle), 0])
            positions.append(pos)

            node = EllipticCurveIcon(
                color=CURVE_COLOR, fill_opacity=0.0, stroke_width=2, shape=1.0
            )
            node.scale(0.18).move_to(pos)
            nodes.add(node)

        # Define graph edges
        edge_pairs = [
            (0, 1),
            (0, 4),
            (0, 15),
            (1, 2),
            (1, 5),
            (2, 3),
            (2, 6),
            (3, 4),
            (3, 7),
            (4, 8),
            (5, 6),
            (5, 9),
            (5, 10),
            (6, 7),
            (6, 11),
            (7, 8),
            (7, 12),
            (8, 9),
            (8, 13),
            (9, 10),
            (9, 14),
            (10, 11),
            (10, 15),
            (11, 12),
            (12, 13),
            (13, 14),
            (14, 15),
        ]

        edges = VGroup()
        edge_dict = {}
        for i, j in edge_pairs:
            edge = Line(
                positions[i],
                positions[j],
                color=GRAY,
                stroke_width=1.5,
                stroke_opacity=0.3,
            )
            edges.add(edge)
            edge_dict[(min(i, j), max(i, j))] = edge

        # Animate graph appearing
        self.play(
            LaggedStart(*[GrowFromCenter(n) for n in nodes], lag_ratio=0.05),
            run_time=1.5,
        )
        self.play(LaggedStart(*[Create(e) for e in edges], lag_ratio=0.02), run_time=1)

        # Highlight start and end
        start_idx, end_idx = 0, 12
        path_indices = [0, 4, 8, 7, 12]

        e1, e2 = nodes[start_idx], nodes[end_idx]

        e1_label = MathTex("E_1", font_size=32, color=GREEN_C)
        e1_label.next_to(e1, LEFT, buff=0.15)
        e2_label = MathTex("E_2", font_size=32, color=RED_C)
        e2_label.next_to(e2, RIGHT, buff=0.15)

        self.play(
            e1.animate.set_color(GREEN_C).set_fill(GREEN_C, opacity=0.4).scale(1.4),
            e2.animate.set_color(RED_C).set_fill(RED_C, opacity=0.4).scale(1.4),
            Write(e1_label),
            Write(e2_label),
            run_time=1,
        )

        # Problem statement
        step1 = Text("The Hard Problem", font_size=24, color=SECRET_COLOR)
        step1.to_corner(UL, buff=0.4)
        self.add_fixed_in_frame_mobjects(step1)

        self.play(FadeIn(step1))
        self.wait(1.5)

        # Show exponential paths - the maze
        question_marks = VGroup()
        for i in range(8):
            angle = i * TAU / 8 + 0.2
            qm = MathTex("?", font_size=28, color=WHITE)
            qm.move_to(1.5 * np.array([np.cos(angle), np.sin(angle), 0]))
            question_marks.add(qm)

        self.play(
            LaggedStart(*[FadeIn(q, scale=0.5) for q in question_marks], lag_ratio=0.1),
            run_time=1,
        )
        self.wait(1)

        # === PART 2: TRANSITION TO 3D ===

        step2 = Text("Secret Structure", font_size=24, color=IDEAL_COLOR)
        step2.to_corner(UL, buff=0.4)
        self.add_fixed_in_frame_mobjects(step2)

        self.play(
            FadeOut(step1),
            FadeIn(step2),
            FadeOut(question_marks),
            run_time=1,
        )

        # Rotate camera to reveal 3D
        self.move_camera(phi=60 * DEGREES, theta=-45 * DEGREES, run_time=2)
        self.wait(0.5)

        # === PART 3: REVEAL THE IDEAL ===

        # Create the secret ideal as a glowing plane/surface behind the graph
        ideal_depth = -1.5

        ideal_plane = Surface(
            lambda u, v: np.array([u, v, ideal_depth]),
            u_range=[-4, 4],
            v_range=[-4, 4],
            resolution=(20, 20),
            fill_opacity=0.15,
            stroke_width=0,
            checkerboard_colors=[IDEAL_COLOR, PURPLE_E],
        )

        # Ideal label
        ideal_label = MathTex("\\mathfrak{I}", font_size=72, color=IDEAL_COLOR)
        ideal_label.move_to([0, 0, ideal_depth])
        ideal_label.rotate(90 * DEGREES, axis=RIGHT)

        # Fade in the ideal plane from below
        self.play(
            FadeIn(ideal_plane, shift=OUT * 0.5), Write(ideal_label), run_time=1.5
        )
        self.wait(1)
        self.play(FadeOut(step2))

        # === PART 4: IDEAL PROJECTS THE PATH VIA VERTICAL PLANES ===

        path_positions_3d = [positions[i] for i in path_indices]

        # Now highlight the actual path edges
        path_edges = []
        for i in range(len(path_indices) - 1):
            a, b = path_indices[i], path_indices[i + 1]
            key = (min(a, b), max(a, b))
            path_edges.append(edge_dict[key])

        # Dim non-path elements
        non_path_nodes = [n for idx, n in enumerate(nodes) if idx not in path_indices]
        non_path_edges = [e for e in edges if e not in path_edges]

        self.play(
            *[n.animate.set_opacity(0.15) for n in non_path_nodes],
            *[e.animate.set_opacity(0.08) for e in non_path_edges],
            run_time=0.8,
        )

        # Animate path illumination with vertical curtain planes
        path_colors = [GREEN_C, TEAL_C, BLUE_C, PURPLE_C]

        step4 = Text(
            "Pathfinding is easy with secret Ideal", font_size=24, color=HIGHLIGHT_COLOR
        )
        step4.to_corner(UL, buff=0.4)
        self.add_fixed_in_frame_mobjects(step4)

        self.play(FadeIn(step4))

        curtain_planes = VGroup()

        for i, edge in enumerate(path_edges):
            color = path_colors[i]
            next_node = nodes[path_indices[i + 1]]

            # Get the two endpoint positions for this edge
            pos1 = path_positions_3d[i]
            pos2 = path_positions_3d[i + 1]

            # Create vertical curtain plane connecting path edge to ideal plane
            # Four corners: top-left, top-right, bottom-right, bottom-left
            curtain_vertices = [
                [pos1[0], pos1[1], 0],  # top-left (path node i)
                [pos2[0], pos2[1], 0],  # top-right (path node i+1)
                [pos2[0], pos2[1], ideal_depth],  # bottom-right (on ideal)
                [pos1[0], pos1[1], ideal_depth],  # bottom-left (on ideal)
            ]

            curtain = Polygon(
                *curtain_vertices,
                color=color,
                fill_color=color,
                fill_opacity=0.25,
                stroke_width=2,
                stroke_opacity=0.6,
            )

            # Edge on the ideal plane (bottom of the curtain)
            ideal_edge = Line(
                [pos1[0], pos1[1], ideal_depth],
                [pos2[0], pos2[1], ideal_depth],
                color=color,
                stroke_width=4,
                stroke_opacity=0.8,
            )

            # Glow effect on the path edge
            glow_edge = edge.copy().set_stroke(color, width=8, opacity=0.4)

            curtain_planes.add(curtain)

            if i < len(path_edges) - 1:
                self.play(
                    edge.animate.set_color(color).set_stroke(width=4).set_opacity(1),
                    FadeIn(glow_edge),
                    next_node.animate.set_color(color).set_opacity(1),
                    FadeIn(curtain),
                    Create(ideal_edge),
                    run_time=0.7,
                )
            else:
                # Last edge - don't recolor E2
                self.play(
                    edge.animate.set_color(color).set_stroke(width=4).set_opacity(1),
                    FadeIn(glow_edge),
                    next_node.animate.set_opacity(1),
                    FadeIn(curtain),
                    Create(ideal_edge),
                    run_time=0.7,
                )

        self.wait(1)

        # === PART 5: THE CONTRAST ===

        # Rotate to a better viewing angle to see the curtains
        self.move_camera(phi=45 * DEGREES, theta=-60 * DEGREES, run_time=1.5)

        # Show complexity comparison
        complexity_box = VGroup(
            Text("Without secret:", font_size=36, color=WHITE),
            MathTex("O(\\sqrt{p})", font_size=42, color=SECRET_COLOR),
            Text("With ideal:", font_size=36, color=WHITE),
            MathTex("O(\\text{poly}(\\log p))", font_size=42, color=HIGHLIGHT_COLOR),
        )
        complexity_box.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        complexity_box.to_corner(DR, buff=0.5)

        bg_rect = SurroundingRectangle(
            complexity_box,
            color=GRAY,
            fill_color=BLACK,
            fill_opacity=0.85,
            stroke_width=1,
            buff=0.25,
            corner_radius=0.1,
        )

        self.add_fixed_in_frame_mobjects(bg_rect)
        self.add_fixed_in_frame_mobjects(complexity_box)

        self.play(FadeIn(bg_rect))
        self.wait(3)
