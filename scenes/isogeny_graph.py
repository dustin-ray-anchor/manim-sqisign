"""
Isogeny Graph Visualization - Test Scene (LaTeX-free version)
Save as: scenes/isogeny_graph.py
Run with: manim -pql scenes/isogeny_graph.py IsogenyGraphIntro
"""

from manim import *
import numpy as np
from typing import cast
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from elliptic_curve import EllipticCurve, EllipticCurveWithFill, preset_curve


# Color scheme for SQIsign visualizations
CURVE_COLOR = BLUE_D
ISOGENY_COLOR = GOLD_A
HIGHLIGHT_COLOR = GREEN_C
SECRET_COLOR = RED_C
PUBLIC_COLOR = BLUE_B


class IsogenyGraphIntro(Scene):
    """Basic introduction to the isogeny graph concept."""

    def construct(self):
        # Title
        title = Text("The Supersingular Isogeny Graph", font_size=42)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Create nodes (elliptic curves)
        num_nodes = 12
        nodes = VGroup()
        labels = VGroup()

        # Arrange in a roughly circular pattern with some randomness
        np.random.seed(42)  # Reproducible layout
        for i in range(num_nodes):
            angle = i * TAU / num_nodes + np.random.uniform(-0.2, 0.2)
            radius = 2.5 + np.random.uniform(-0.3, 0.3)
            pos = radius * np.array([np.cos(angle), np.sin(angle), 0])

            # Use different curve parameters for variety
            a_val = -1 - (i % 4)
            b_val = 1 + (i % 3)
            node = EllipticCurveWithFill(
                a=a_val, b=b_val, color=CURVE_COLOR, fill_opacity=0.3, stroke_width=2
            )
            node.scale(0.2).move_to(pos)
            label = Text(f"E{i}", font_size=20)
            label.next_to(node, normalize(pos) * 0.4, buff=0.1)

            nodes.add(node)
            labels.add(label)

        # Shift everything down a bit to make room for title
        graph_group = VGroup(nodes, labels)
        graph_group.shift(DOWN * 0.5)

        # Animate nodes appearing
        self.play(
            LaggedStart(*[GrowFromCenter(n) for n in nodes], lag_ratio=0.1), run_time=2
        )
        self.play(LaggedStart(*[FadeIn(l) for l in labels], lag_ratio=0.05), run_time=1)

        # Explanation
        explanation = Text(
            "Each node is a supersingular elliptic curve", font_size=28, color=GRAY_B
        )
        explanation.to_edge(DOWN)
        self.play(FadeIn(explanation))
        self.wait(1)

        # Add edges (isogenies) - each node connects to ~3 others
        edges = VGroup()
        edge_pairs = [
            (0, 1),
            (0, 5),
            (0, 11),
            (1, 2),
            (1, 6),
            (2, 3),
            (2, 7),
            (3, 4),
            (3, 8),
            (4, 5),
            (4, 9),
            (5, 10),
            (6, 7),
            (6, 11),
            (7, 8),
            (8, 9),
            (9, 10),
            (10, 11),
        ]

        for i, j in edge_pairs:
            edge = Line(
                nodes[i].get_center(),
                nodes[j].get_center(),
                color=ISOGENY_COLOR,
                stroke_width=2,
            )
            edges.add(edge)

        # Update explanation
        new_explanation = Text(
            "Edges are isogenies (structure-preserving maps)",
            font_size=28,
            color=GRAY_B,
        )
        new_explanation.to_edge(DOWN)

        self.play(
            LaggedStart(*[Create(e) for e in edges], lag_ratio=0.05),
            Transform(explanation, new_explanation),
            run_time=2,
        )
        self.wait(1)

        # Highlight the hard problem: finding a path
        start_node = nodes[0]
        end_node = nodes[8]

        self.play(
            start_node.animate.set_color(GREEN_C).scale(1.5),
            end_node.animate.set_color(RED_C).scale(1.5),
        )

        problem_text = Text(
            "Hard problem: Given two curves, find a path between them",
            font_size=28,
            color=GRAY_B,
        )
        problem_text.to_edge(DOWN)
        self.play(Transform(explanation, problem_text))

        # Show a path being searched (random walk effect)
        current = 0
        path_edges = []
        visited = {0}

        # Simulate searching (not actually finding shortest path)
        search_path = [0, 1, 6, 7, 8]  # Predetermined for demo

        for i in range(len(search_path) - 1):
            curr_idx = search_path[i]
            next_idx = search_path[i + 1]

            # Find the edge
            for e, (a, b) in zip(edges, edge_pairs):
                if (a == curr_idx and b == next_idx) or (
                    b == curr_idx and a == next_idx
                ):
                    self.play(
                        e.animate.set_color(HIGHLIGHT_COLOR).set_stroke(width=4),
                        nodes[next_idx].animate.set_color(HIGHLIGHT_COLOR),
                        run_time=0.5,
                    )
                    break

        self.wait(1)

        # Final message
        final_text = Text(
            "Best known: exponential time (even with quantum computers)",
            font_size=28,
            color=GRAY_B,
        )
        final_text.to_edge(DOWN)
        self.play(Transform(explanation, final_text))
        self.wait(2)


class DegreeVisualization(Scene):
    """Visualize why smooth degrees are computationally cheaper."""

    def construct(self):
        title = Text("Isogeny Degree: Why Smoothness Matters", font_size=38)
        title.to_edge(UP)
        self.play(Write(title))

        # Setup: Two curves with an isogeny between them
        e1 = EllipticCurveWithFill(
            a=-1, b=1, color=CURVE_COLOR, fill_opacity=0.3, stroke_width=3
        )
        e1.scale(0.7).shift(LEFT * 4)
        e2 = EllipticCurveWithFill(
            a=-3, b=3, color=CURVE_COLOR, fill_opacity=0.3, stroke_width=3
        )
        e2.scale(0.7).shift(RIGHT * 4)

        e1_label = MathTex("E_1", font_size=28).next_to(e1, DOWN)
        e2_label = MathTex("E_2", font_size=28).next_to(e2, DOWN)

        arrow = Arrow(e1.get_right(), e2.get_left(), color=ISOGENY_COLOR, buff=0.2)
        phi_label = MathTex("\\varphi", font_size=32).next_to(arrow, UP)

        self.play(Create(e1), Create(e2), Write(e1_label), Write(e2_label))
        self.play(GrowArrow(arrow), Write(phi_label))
        self.wait(0.5)

        # Show degree concept
        degree_text = MathTex("\\deg(\\varphi) = d", font_size=28)
        degree_text.shift(UP * 1.5)
        self.play(Write(degree_text))

        # Cost explanation
        cost_text = MathTex(
            "\\text{Computational cost} \\approx O(d) \\text{ using Vélu's formulas}",
            font_size=26,
        )
        cost_text.shift(DOWN * 2)
        self.play(FadeIn(cost_text))
        self.wait(1)

        # Clear and show comparison
        self.play(
            FadeOut(e1),
            FadeOut(e2),
            FadeOut(e1_label),
            FadeOut(e2_label),
            FadeOut(arrow),
            FadeOut(phi_label),
            FadeOut(degree_text),
            FadeOut(cost_text),
        )

        # === NON-SMOOTH CASE ===
        non_smooth_title = Text("Non-smooth degree (prime)", font_size=30, color=RED_C)
        non_smooth_title.shift(UP * 2.5)
        self.play(Write(non_smooth_title))

        # Single massive arrow
        big_e1 = EllipticCurveWithFill(
            a=-1, b=1, color=CURVE_COLOR, fill_opacity=0.3, stroke_width=2
        )
        big_e1.scale(0.3).move_to(LEFT * 4)
        big_e2 = EllipticCurveWithFill(
            a=-2, b=2, color=CURVE_COLOR, fill_opacity=0.3, stroke_width=2
        )
        big_e2.scale(0.3).move_to(RIGHT * 4)
        big_arrow = Arrow(LEFT * 3.5, RIGHT * 3.5, color=RED_C, stroke_width=8)

        prime_deg = MathTex(
            "d = 2^{256} - 189 \\text{ (prime)}", font_size=24, color=RED_C
        )
        prime_deg.next_to(big_arrow, UP)

        self.play(
            GrowFromCenter(big_e1),
            GrowFromCenter(big_e2),
            GrowArrow(big_arrow),
            Write(prime_deg),
        )

        prime_cost = MathTex(
            "\\text{Cost: } O(2^{256}) \\text{ operations}", font_size=24, color=RED_C
        )
        prime_cost.shift(DOWN * 1)
        impossible = Text("← Impossible!", font_size=24, color=RED_C)
        impossible.next_to(prime_cost, RIGHT)

        self.play(Write(prime_cost), FadeIn(impossible))
        self.wait(1.5)

        # Clear non-smooth
        self.play(
            FadeOut(non_smooth_title),
            FadeOut(big_e1),
            FadeOut(big_e2),
            FadeOut(big_arrow),
            FadeOut(prime_deg),
            FadeOut(prime_cost),
            FadeOut(impossible),
        )

        # === SMOOTH CASE ===
        smooth_title = Text(
            "Smooth degree (factors into small primes)", font_size=30, color=GREEN_C
        )
        smooth_title.shift(UP * 2.5)
        self.play(Write(smooth_title))

        # Chain of small isogenies
        num_steps = 8
        dots = VGroup()
        arrows_list = []

        x_positions = np.linspace(-5, 5, num_steps + 1)

        for i, x in enumerate(x_positions):
            # Use different curve parameters for visual variety
            a_val = -1 if i % 2 == 0 else -2
            b_val = 1 if i % 2 == 0 else 2
            curve = EllipticCurveWithFill(
                a=a_val, b=b_val, color=CURVE_COLOR, fill_opacity=0.3, stroke_width=2
            )
            curve.scale(0.18).move_to(np.array([x, 0, 0]))
            dots.add(curve)

        for i in range(num_steps):
            arr = Arrow(
                np.array([x_positions[i] + 0.2, 0, 0]),
                np.array([x_positions[i + 1] - 0.2, 0, 0]),
                color=GREEN_C,
                stroke_width=3,
                buff=0,
            )
            arrows_list.append(arr)

        arrows = VGroup(*arrows_list)

        self.play(LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.1))
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows_list], lag_ratio=0.1))

        smooth_deg = MathTex(
            "d = 2^{256} = 2 \\cdot 2 \\cdot 2 \\cdot \\ldots \\cdot 2 \\text{ (256 times)}",
            font_size=24,
            color=GREEN_C,
        )
        smooth_deg.shift(UP * 1)
        self.play(Write(smooth_deg))

        smooth_cost = MathTex(
            "\\text{Cost: } 256 \\times O(2) = O(512)", font_size=24, color=GREEN_C
        )
        smooth_cost.shift(DOWN * 1.5)
        easy = Text("← Easy!", font_size=24, color=GREEN_C)
        easy.next_to(smooth_cost, RIGHT)

        self.play(Write(smooth_cost), FadeIn(easy))
        self.wait(2)

        # Dramatic comparison
        self.play(
            FadeOut(smooth_title),
            FadeOut(dots),
            FadeOut(arrows),
            FadeOut(smooth_deg),
            FadeOut(smooth_cost),
            FadeOut(easy),
        )

        comparison_red = MathTex("2^{256}", font_size=48, color=RED_C)
        comparison_vs = Text("  vs  ", font_size=48)
        comparison_green = MathTex("512", font_size=48, color=GREEN_C)

        comparison = VGroup(comparison_red, comparison_vs, comparison_green)
        comparison.arrange(RIGHT)

        self.play(Write(comparison))

        factor = MathTex("\\approx 10^{74} \\times \\text{ faster!}", font_size=36)
        factor.next_to(comparison, DOWN, buff=0.5)
        self.play(Write(factor))

        self.wait(2)


class SQIsignProtocolOverview(Scene):
    """High-level visualization of the SQIsign sigma protocol."""

    def construct(self):

        # The four curves in the protocol (smaller scale, tighter parameters for less gap)
        # Shifted up to center the scene (no title)
        e0 = EllipticCurve(a=-0.5, b=0.5, color=PUBLIC_COLOR, stroke_width=3)
        e0.scale(0.28).move_to((-3, 2, 0))
        ea = EllipticCurve(a=-1, b=0.8, color=SECRET_COLOR, stroke_width=3)
        ea.scale(0.28).move_to((3, 2, 0))
        ecom = EllipticCurve(a=-1.5, b=1.2, color=CURVE_COLOR, stroke_width=3)
        ecom.scale(0.28).move_to((-3, -1, 0))
        echl = EllipticCurve(a=-0.8, b=0.6, color=CURVE_COLOR, stroke_width=3)
        echl.scale(0.28).move_to((3, -1, 0))

        e0_label = MathTex("E_0", font_size=36).next_to(e0, UP, buff=0.3)
        ea_label = MathTex("E_a", font_size=36, color=SECRET_COLOR).next_to(
            ea, UP, buff=0.3
        )
        ecom_label = MathTex("E_{\\mathrm{com}}", font_size=36).next_to(
            ecom, DOWN, buff=0.3
        )
        echl_label = MathTex("E_{\\mathrm{chl}}", font_size=36).next_to(
            echl, DOWN, buff=0.3
        )

        secret_note = Text("(public key)", font_size=20, color=GRAY).next_to(
            ea_label, RIGHT, buff=0.1
        )

        # Show E_0 and E_A first
        self.play(
            GrowFromCenter(e0),
            Write(e0_label),
            GrowFromCenter(ea),
            Write(ea_label),
            FadeIn(secret_note),
        )
        self.wait(1.5)

        # Secret isogeny τ (the secret key)
        tau = Arrow(e0.get_center(), ea.get_center(), color=SECRET_COLOR, buff=0.3)
        tau_label = MathTex("\\tau", font_size=36, color=SECRET_COLOR).next_to(
            tau, UP, buff=0.1
        )
        secret_text = Text("secret key", font_size=22, color=SECRET_COLOR)
        secret_text.next_to(tau, DOWN, buff=0.2)

        self.play(GrowArrow(tau), Write(tau_label), FadeIn(secret_text))
        self.wait(2.5)

        # === COMMITMENT ===
        step1 = (
            Text("1. COMMIT", font_size=22, color=GOLD_A).to_edge(LEFT).shift(DOWN * 0)
        )
        self.play(Write(step1))

        self.play(GrowFromCenter(ecom), Write(ecom_label))

        psi = Arrow(e0.get_center(), ecom.get_center(), color=GOLD_A, buff=0.3)
        psi_label = MathTex("\\psi", font_size=36, color=GOLD_A).next_to(
            psi, LEFT, buff=0.1
        )

        self.play(GrowArrow(psi), Write(psi_label))

        commit_note = Text("Random secret isogeny", font_size=20, color=GRAY)
        commit_note.next_to(psi, RIGHT, buff=0.3)
        self.play(FadeIn(commit_note))
        self.wait(2.5)

        # === CHALLENGE ===
        step2 = Text("2. CHALLENGE", font_size=22, color=TEAL_C).next_to(
            step1, DOWN, buff=0.5, aligned_edge=LEFT
        )
        self.play(Write(step2), FadeOut(commit_note))

        self.play(GrowFromCenter(echl), Write(echl_label))

        phi = Arrow(ecom.get_center(), echl.get_center(), color=TEAL_C, buff=0.3)
        phi_label = MathTex("\\varphi", font_size=36, color=TEAL_C).next_to(
            phi, DOWN, buff=0.1
        )

        self.play(GrowArrow(phi), Write(phi_label))

        hash_note = MathTex(
            "\\varphi = \\text{Hash}(E_a, E_{\\mathrm{com}}, \\text{message})",
            font_size=26,
            color=GRAY,
        )
        hash_note.to_edge(DOWN).shift(UP * 0.5)
        self.play(Write(hash_note))
        self.wait(2.5)

        # === RESPONSE ===
        step3 = Text("3. RESPONSE", font_size=22, color=GREEN_C).next_to(
            step2, DOWN, buff=0.5, aligned_edge=LEFT
        )
        self.play(Write(step3), FadeOut(hash_note))

        # The response isogeny σ
        sigma = Arrow(
            ea.get_center(), echl.get_center(), color=GREEN_C, buff=0.3, stroke_width=6
        )
        sigma_label = MathTex("\\sigma", font_size=40, color=GREEN_C).next_to(
            sigma, RIGHT, buff=0.1
        )

        # Animate the "finding" of σ
        question = MathTex("\\sigma: E_a \\to E_{\\mathrm{chl}} \\; ?", font_size=30)
        question.next_to(sigma, RIGHT, buff=0.5)
        self.play(Write(question))
        self.wait(1.5)

        self.play(GrowArrow(sigma), Write(sigma_label))

        self.wait(2.5)

        # Highlight the signature - fade background elements and emphasize signature
        self.play(
            # Fade text elements
            step1.animate.set_opacity(0.2),
            step2.animate.set_opacity(0.2),
            step3.animate.set_opacity(0.2),
            # Dim background elements
            e0.animate.set_opacity(0.15),
            e0_label.animate.set_opacity(0.15),
            ea.animate.set_opacity(0.15),
            ea_label.animate.set_opacity(0.15),
            secret_note.animate.set_opacity(0.15),
            tau.animate.set_opacity(0.15),
            tau_label.animate.set_opacity(0.15),
            secret_text.animate.set_opacity(0.15),
            psi.animate.set_opacity(0.15),
            psi_label.animate.set_opacity(0.15),
            phi.animate.set_opacity(0.15),
            phi_label.animate.set_opacity(0.15),
            # Brighten and highlight signature elements
            ecom.animate.set_color(YELLOW).set_stroke(width=5),
            ecom_label.animate.set_color(YELLOW),
            sigma.animate.set_color(YELLOW).set_stroke(width=8),
            sigma_label.animate.set_color(YELLOW),
            echl.animate.set_color(YELLOW).set_stroke(width=5),
            echl_label.animate.set_color(YELLOW),
        )

        sig_text = MathTex(
            "\\text{Signature} = (E_{\\mathrm{com}}, \\sigma)",
            font_size=40,
            color=YELLOW,
        )
        sig_text.shift(UP * 2)
        self.play(Write(sig_text))
        self.wait(3)
