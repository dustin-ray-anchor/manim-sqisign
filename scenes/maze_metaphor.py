"""
SQIsign Maze Metaphor - The 30-Second Version
Save as: scenes/maze_metaphor.py
Run with: manim -pql scenes/maze_metaphor.py MazeMetaphor
"""

from manim import *
import numpy as np
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from elliptic_curve import EllipticCurve, EllipticCurveWithFill


# Color scheme
CURVE_COLOR = BLUE_D
ISOGENY_COLOR = GOLD_A
HIGHLIGHT_COLOR = GREEN_C
SECRET_COLOR = RED_C
PUBLIC_COLOR = BLUE_B
PATH_COLOR = GOLD_A
WRONG_COLOR = RED_C
RIGHT_COLOR = GREEN_C


class MazeMetaphor(Scene):
    """SQIsign explained as navigating a maze."""

    def construct(self):
        # === BUILD THE MAZE ===

        # Create a grid-based maze with nodes and edges
        # 5x4 grid of nodes
        rows, cols = 4, 6
        spacing = 1.4

        nodes = {}
        node_objects = VGroup()

        # Create nodes (small elliptic curves)
        for r in range(rows):
            for c in range(cols):
                x = (c - (cols - 1) / 2) * spacing
                y = (r - (rows - 1) / 2) * spacing

                b_val = 0.5 + ((r + c) % 4) * 0.1
                node = EllipticCurve(a=-1, b=b_val, color=CURVE_COLOR, stroke_width=2)
                node.scale(0.12).move_to(np.array([x, y, 0]))
                nodes[(r, c)] = node
                node_objects.add(node)

        # Define maze edges (not all connections - creates maze-like structure)
        edge_list = [
            # Row 0
            ((0, 0), (0, 1)),
            ((0, 1), (0, 2)),
            ((0, 3), (0, 4)),
            ((0, 4), (0, 5)),
            # Row 1
            ((1, 0), (1, 1)),
            ((1, 2), (1, 3)),
            ((1, 3), (1, 4)),
            ((1, 4), (1, 5)),
            # Row 2
            ((2, 0), (2, 1)),
            ((2, 1), (2, 2)),
            ((2, 2), (2, 3)),
            ((2, 4), (2, 5)),
            # Row 3
            ((3, 0), (3, 1)),
            ((3, 1), (3, 2)),
            ((3, 2), (3, 3)),
            ((3, 3), (3, 4)),
            ((3, 4), (3, 5)),
            # Vertical connections
            ((0, 0), (1, 0)),
            ((1, 0), (2, 0)),
            ((2, 0), (3, 0)),
            ((0, 1), (1, 1)),
            ((2, 1), (3, 1)),
            ((0, 2), (1, 2)),
            ((1, 2), (2, 2)),
            ((1, 3), (2, 3)),
            ((2, 3), (3, 3)),
            ((0, 4), (1, 4)),
            ((2, 4), (3, 4)),
            ((0, 5), (1, 5)),
            ((1, 5), (2, 5)),
            ((2, 5), (3, 5)),
            # Some diagonal shortcuts (the "secret" paths)
            ((1, 1), (2, 2)),
            ((2, 2), (3, 3)),
        ]

        edges = {}
        edge_objects = VGroup()

        for (r1, c1), (r2, c2) in edge_list:
            if (r1, c1) in nodes and (r2, c2) in nodes:
                edge = Line(
                    nodes[(r1, c1)].get_center(),
                    nodes[(r2, c2)].get_center(),
                    color=GRAY,
                    stroke_width=2,
                    stroke_opacity=0.4,
                )
                edges[((r1, c1), (r2, c2))] = edge
                edges[((r2, c2), (r1, c1))] = edge  # Bidirectional lookup
                edge_objects.add(edge)

        # Shift maze slightly up
        maze_group = VGroup(node_objects, edge_objects)
        maze_group.shift(UP * 0.3)

        # No title - will add step indicators later
        self.play(
            LaggedStart(*[GrowFromCenter(n) for n in node_objects], lag_ratio=0.02),
            run_time=2,
        )
        self.play(
            LaggedStart(*[Create(e) for e in edge_objects], lag_ratio=0.02), run_time=1.5
        )
        self.wait(1)

        # Label: nodes are curves
        curve_note = Text("Nodes = Elliptic curves", font_size=20, color=GRAY_B)
        curve_note.to_corner(DL, buff=0.4)
        edge_note = Text("Edges = Isogenies", font_size=20, color=GRAY_B)
        edge_note.next_to(curve_note, UP, aligned_edge=LEFT, buff=0.15)

        self.play(FadeIn(curve_note), FadeIn(edge_note))
        self.wait(1.5)

        # === MARK START AND END ===

        start_pos = (0, 0)
        end_pos = (3, 5)

        start_node = nodes[start_pos]
        end_node = nodes[end_pos]

        # Highlight start (secret key origin)
        start_label = Text("Start", font_size=22, color=GREEN_C)
        start_label.next_to(start_node, LEFT, buff=0.15)

        # Highlight end (public key)
        end_label = Text("Public Key", font_size=22, color=PUBLIC_COLOR)
        end_label.next_to(end_node, RIGHT, buff=0.15)

        self.play(
            start_node.animate.set_color(GREEN_C).scale(1.5),
            end_node.animate.set_color(PUBLIC_COLOR).scale(1.5),
            Write(start_label),
            Write(end_label),
        )
        self.wait(1.5)

        # === PART 1: THE HARD WAY (no secret) ===

        step1 = Text("Step 1: Without secret", font_size=24, color=RED_C)
        step1.to_corner(UL, buff=0.4)
        self.play(FadeIn(step1))

        # Animate a wandering search with wrong turns
        # Path that takes wrong turns before eventually finding the way
        hard_path = [
            (0, 0),
            (0, 1),
            (0, 2),
            (1, 2),  # Start exploring
            (2, 2),  # Go down
            (2, 1),  # Wrong turn - go left
            (3, 1),  # Dead end area
            (3, 0),  # More wrong
            (2, 0),  # Backtrack
            (1, 0),  # More backtrack
            (1, 1),  # Try different route
            (2, 2),  # Back to center
            (2, 3),
            (3, 3),  # Down and right
            (3, 4),
            (3, 5),  # Finally reach end
        ]

        # Create a dot to show the "searcher"
        searcher = Dot(color=RED_C, radius=0.1)
        searcher.move_to(nodes[hard_path[0]].get_center())
        self.play(FadeIn(searcher, scale=2))

        # Track visited edges for coloring
        visited_edges = []
        wrong_turn_indices = [5, 6, 7, 8, 9]  # Indices where we're going wrong

        for i in range(len(hard_path) - 1):
            curr = hard_path[i]
            next_pos = hard_path[i + 1]

            # Find the edge
            edge_key = (curr, next_pos)
            if edge_key not in edges:
                edge_key = (next_pos, curr)

            if edge_key in edges:
                edge = edges[edge_key]

                # All path edges are red
                self.play(
                    searcher.animate.move_to(nodes[next_pos].get_center()),
                    edge.animate.set_color(RED_C).set_stroke(width=3, opacity=0.8),
                    run_time=0.3,
                )

        # Show time taken
        hard_time = Text("⏱ Exponential time", font_size=24, color=RED_C)
        hard_time.to_corner(DR, buff=0.4)
        self.play(FadeIn(hard_time))
        self.wait(2)

        # === RESET FOR EASY PATH ===

        # Fade out the hard path coloring
        self.play(
            FadeOut(searcher),
            FadeOut(step1),
            FadeOut(hard_time),
            *[
                edge.animate.set_color(GRAY).set_stroke(width=2, opacity=0.4)
                for edge in edge_objects
            ],
            run_time=0.8
        )

        # === PART 2: THE EASY WAY (with secret) ===

        step2 = Text("Step 2: With secret", font_size=24, color=GREEN_C)
        step2.to_corner(UL, buff=0.4)
        self.play(FadeIn(step2))

        # The secret shortcut path (using the diagonal edges)
        secret_path = [(0, 0), (1, 0), (1, 1), (2, 2), (3, 3), (3, 4), (3, 5)]

        # Show "secret key" knowledge
        secret_label = Text("Secret Key = Shortcut", font_size=22, color=SECRET_COLOR)
        secret_label.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(secret_label))

        # Create a new searcher
        fast_searcher = Dot(color=GREEN_C, radius=0.12)
        fast_searcher.move_to(nodes[secret_path[0]].get_center())

        # Add a trail effect
        trail = VGroup()

        self.play(FadeIn(fast_searcher, scale=2))

        # Animate the fast path with glowing effect
        for i in range(len(secret_path) - 1):
            curr = secret_path[i]
            next_pos = secret_path[i + 1]

            edge_key = (curr, next_pos)
            if edge_key not in edges:
                edge_key = (next_pos, curr)

            if edge_key in edges:
                edge = edges[edge_key]

                # Create glow effect
                glow = edge.copy().set_stroke(GREEN_C, width=8, opacity=0.3)

                self.play(
                    fast_searcher.animate.move_to(nodes[next_pos].get_center()),
                    edge.animate.set_color(GREEN_C).set_stroke(width=4, opacity=1),
                    FadeIn(glow),
                    run_time=0.4,
                )
                trail.add(glow)

        # Show time taken
        easy_time = Text("⏱ Polynomial time", font_size=24, color=GREEN_C)
        easy_time.to_corner(DR, buff=0.4)
        self.play(FadeIn(easy_time))
        self.wait(2)

        # === FINAL SUMMARY ===

        self.play(
            FadeOut(step2),
            FadeOut(secret_label),
            FadeOut(easy_time),
            FadeOut(fast_searcher),
            FadeOut(trail),
            FadeOut(start_label),
            FadeOut(end_label),
            FadeOut(curve_note),
            FadeOut(edge_note),
            *[
                edge.animate.set_color(GRAY).set_stroke(width=2, opacity=0.3)
                for edge in edge_objects
            ],
            *[
                node.animate.set_color(CURVE_COLOR).scale(
                    1 / 1.5 if node in [start_node, end_node] else 1
                )
                for node in node_objects
            ],
            run_time=1
        )

        # Summary box
        summary = VGroup(
            Text("The Isogeny Maze:", font_size=28, color=WHITE),
            Text(
                "• Without secret: Exponentially hard",
                font_size=22,
                color=RED_C,
            ),
            Text("• Secret key = shortcut", font_size=22, color=SECRET_COLOR),
            Text("• With secret: Polynomially easy", font_size=22, color=GREEN_C),
        )
        summary.arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        summary.move_to(ORIGIN)

        bg_rect = SurroundingRectangle(
            summary,
            color=GRAY,
            fill_color=BLACK,
            fill_opacity=0.9,
            stroke_width=1,
            buff=0.3,
            corner_radius=0.15,
        )

        self.play(
            FadeIn(bg_rect),
            Write(summary[0]),
        )
        self.play(
            LaggedStart(
                *[FadeIn(line, shift=RIGHT * 0.3) for line in summary[1:]],
                lag_ratio=0.3
            ),
            run_time=2,
        )

        self.wait(4)
