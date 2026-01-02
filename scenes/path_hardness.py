"""
Path Finding Hardness Visualization
Save as: scenes/path_hardness.py
Run with: manim -pql scenes/path_hardness.py PathFindingHardness
"""

from manim import *
import numpy as np
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from elliptic_curve import EllipticCurve, EllipticCurveWithFill, EllipticCurveIcon, preset_curve


# Color scheme (matching isogeny_graph.py)
CURVE_COLOR = BLUE_D
ISOGENY_COLOR = GOLD_A
HIGHLIGHT_COLOR = GREEN_C
SECRET_COLOR = RED_C
PUBLIC_COLOR = BLUE_B


class PathFindingHardness(Scene):
    """Visualize the hard problem: finding paths in the isogeny graph."""

    def construct(self):
        # Create a larger, more impressive graph
        num_nodes = 16
        nodes = VGroup()
        positions = []

        # Arrange nodes in an organic circular layout
        np.random.seed(37)
        for i in range(num_nodes):
            angle = i * TAU / num_nodes + np.random.uniform(-0.15, 0.15)
            radius = 2.8 + np.random.uniform(-0.4, 0.4)
            pos = radius * np.array([np.cos(angle), np.sin(angle), 0])
            positions.append(pos)

            # Curves with clean styling (no fill, no back line)
            node = EllipticCurveIcon(
                color=CURVE_COLOR, fill_opacity=0.0, stroke_width=2, shape=1.0
            )
            node.scale(0.18).move_to(pos)
            nodes.add(node)

        # Define graph edges (dense connectivity for expander graph feel)
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

        # Create edges
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
        self.wait(0.5)

        # Designate start and end curves
        start_idx, end_idx = 0, 12
        e1, e2 = nodes[start_idx], nodes[end_idx]

        # Create labels for E1 and E2
        e1_label = MathTex("E_1", font_size=32, color=GREEN_C)
        e1_label.next_to(e1, LEFT, buff=0.15)
        e2_label = MathTex("E_2", font_size=32, color=RED_C)
        e2_label.next_to(e2, RIGHT, buff=0.15)

        # Highlight the two given curves
        self.play(
            e1.animate.set_color(GREEN_C).set_fill(GREEN_C, opacity=0.4).scale(1.4),
            e2.animate.set_color(RED_C).set_fill(RED_C, opacity=0.4).scale(1.4),
            Write(e1_label),
            Write(e2_label),
            run_time=1,
        )

        # Problem statement (minimal, elegant)
        problem = MathTex(
            "\\text{Find } \\varphi: E_1 \\to E_2 \\text{ ?}", font_size=36
        ).to_corner(UL, buff=0.5)
        self.play(Write(problem))
        self.wait(1.5)

        # The secret path we'll reveal
        path_indices = [0, 4, 8, 7, 12]
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
            run_time=0.8
        )

        # Animate path discovery with gradient colors
        path_colors = [GREEN_C, TEAL_C, BLUE_C, PURPLE_C]

        for i, edge in enumerate(path_edges):
            color = path_colors[i]
            next_node = nodes[path_indices[i + 1]]

            # Create glowing effect on edge
            glow_edge = edge.copy().set_stroke(color, width=8, opacity=0.4)

            if i < len(path_edges) - 1:
                self.play(
                    edge.animate.set_color(color).set_stroke(width=4).set_opacity(1),
                    FadeIn(glow_edge),
                    next_node.animate.set_color(color).set_opacity(1),
                    run_time=0.6,
                )
            else:
                # Last edge - don't recolor E2
                self.play(
                    edge.animate.set_color(color).set_stroke(width=4).set_opacity(1),
                    FadeIn(glow_edge),
                    next_node.animate.set_opacity(1),
                    run_time=0.6,
                )

        self.wait(1)

        # Show the path as φ
        phi_on_path = MathTex("\\varphi", font_size=28, color=GOLD_A)
        path_center = (positions[path_indices[2]] + positions[path_indices[1]]) / 2
        phi_on_path.move_to(path_center + UP * 0.5)
        self.play(FadeIn(phi_on_path, scale=1.5))
        self.wait(1)

        # Complexity annotation - elegant positioning
        classical = MathTex(
            "\\text{Classical: } O(\\sqrt{p})", font_size=42, color=WHITE
        )
        quantum = MathTex(
            "\\text{Quantum: } O(\\sqrt[4]{p})", font_size=42, color=BLUE_B
        )
        exponential = MathTex(
            "\\text{Exponential in } \\log p", font_size=36, color=WHITE
        )

        complexity_box = VGroup(classical, quantum, exponential)
        complexity_box.arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        complexity_box.to_corner(DR, buff=0.5)

        # Subtle background for readability
        bg_rect = SurroundingRectangle(
            complexity_box,
            color=GRAY,
            fill_color=BLACK,
            fill_opacity=0.7,
            stroke_width=1,
            buff=0.2,
            corner_radius=0.1,
        )

        self.play(FadeIn(bg_rect), Write(classical), run_time=0.8)
        self.play(Write(quantum), run_time=0.8)
        self.play(FadeIn(exponential), run_time=0.6)

        self.wait(2)

        # Final emphasis
        hard_statement = MathTex(
            "\\text{Computationally Hard}", font_size=36, color=GOLD_A
        ).to_corner(UL, buff=0.5)

        self.play(Transform(problem, hard_statement), run_time=1)

        self.wait(3)
