"""
SQIsign Protocol Overview - Complete Sigma Protocol Visualization
Save as: scenes/sqisign_protocol.py
Run with: manim -pql scenes/sqisign_protocol.py SQIsignProtocolOverview
"""

from manim import *
import numpy as np
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


class SQIsignProtocolOverview(Scene):
    """High-level visualization of the SQIsign sigma protocol."""

    def construct(self):

        # The four curves in the protocol (all single-component, no gaps)
        # Centered vertically for balanced composition
        e0 = EllipticCurve(a=-1, b=0.5, color=PUBLIC_COLOR, stroke_width=3)
        e0.scale(0.28).move_to((-3, 1.5, 0))
        ea = EllipticCurve(a=-1, b=0.8, color=SECRET_COLOR, stroke_width=3)
        ea.scale(0.28).move_to((3, 1.5, 0))
        ecom = EllipticCurve(a=-1, b=0.7, color=CURVE_COLOR, stroke_width=3)
        ecom.scale(0.28).move_to((-3, -1.5, 0))
        echl = EllipticCurve(a=-1, b=0.6, color=CURVE_COLOR, stroke_width=3)
        echl.scale(0.28).move_to((3, -1.5, 0))

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

        secret_note = Text("(public key)", font_size=20, color=PUBLIC_COLOR).next_to(
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
        self.wait(2.5)

        # Secret isogeny τ (the secret key)
        tau = Arrow(e0.get_center(), ea.get_center(), color=SECRET_COLOR, buff=0.3)
        tau_label = MathTex("\\tau", font_size=36, color=SECRET_COLOR).next_to(
            tau, UP, buff=0.1
        )
        secret_text = Text("secret key", font_size=22, color=SECRET_COLOR)
        secret_text.next_to(tau, DOWN, buff=0.2)

        self.play(GrowArrow(tau), Write(tau_label), FadeIn(secret_text))
        self.wait(3.5)

        # === COMMITMENT ===
        step1 = (
            Text("1. COMMIT", font_size=22, color=GOLD_A)
            .to_corner(UL)
            .shift(DOWN * 0.3)
        )
        self.play(Write(step1))

        self.play(GrowFromCenter(ecom), Write(ecom_label))

        psi = Arrow(e0.get_center(), ecom.get_center(), color=GOLD_A, buff=0.3)
        psi_label = MathTex("\\psi", font_size=36, color=GOLD_A).next_to(
            psi, LEFT, buff=0.1
        )

        self.play(GrowArrow(psi), Write(psi_label))

        commit_note = Text("Random secret", font_size=20, color=GOLD_A)
        commit_note.next_to(psi, LEFT, buff=0.5)
        self.play(FadeIn(commit_note))
        self.wait(3.5)

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
            color=TEAL_C,
        )
        hash_note.to_edge(DOWN).shift(UP * 0.5)
        self.play(Write(hash_note))
        self.wait(3.5)

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
            sigma, RIGHT, buff=0.64
        )

        self.play(GrowArrow(sigma), Write(sigma_label))

        # Animate the "finding" of σ
        question = MathTex(
            "\\sigma: E_a \\to E_{\\mathrm{chl}} \\; ?", font_size=40, color=GREEN_C
        ).next_to(sigma, RIGHT, buff=0.64)
        self.play(Write(question), FadeOut(sigma_label))

        self.wait(3)

        self.wait(3.5)

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
            echl.animate.set_opacity(0.15),
            echl_label.animate.set_opacity(0.15),
            # Brighten and highlight signature elements (E_com and σ only)
            ecom.animate.set_color(YELLOW).set_stroke(width=5),
            ecom_label.animate.set_color(YELLOW),
            question.animate.set_color(YELLOW),
        )

        sig_text = MathTex(
            "\\text{Signature} = (E_{\\mathrm{com}}, \\sigma)",
            font_size=40,
            color=YELLOW,
        )
        sig_text.shift(UP * 2)
        self.play(Write(sig_text))
        self.wait(8)
