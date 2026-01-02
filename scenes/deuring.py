"""
The Deuring Correspondence - Split Screen Visualization
Shows the parallel worlds of curves/isogenies and quaternion orders/ideals

Save as: scenes/deuring.py
Run with: manim -ql scenes/deuring.py DeuringCorrespondence
"""

from manim import *
import numpy as np

# Color scheme - matched pairs across the correspondence
CURVE_COLOR_1 = BLUE_D
CURVE_COLOR_2 = TEAL_C
CURVE_COLOR_3 = GREEN_C

ORDER_COLOR_1 = BLUE_D  # Same colors - they correspond!
ORDER_COLOR_2 = TEAL_C
ORDER_COLOR_3 = GREEN_C

ISOGENY_COLOR = GOLD_A
IDEAL_COLOR = GOLD_A  # Same - isogenies ↔ ideals

DIVIDER_COLOR = GRAY_B


class DeuringCorrespondence(Scene):
    """Split-screen showing curve world ↔ quaternion world."""

    def construct(self):
        self.setup_split_screen()
        self.show_curve_to_order()
        self.show_isogeny_to_ideal()
        self.show_composition()
        self.show_the_trapdoor()
        self.show_summary()

    def setup_split_screen(self):
        """Create the split screen layout."""
        # Dividing line
        self.divider = Line(UP * 3.5, DOWN * 3.5, color=DIVIDER_COLOR, stroke_width=2)

        # Headers
        self.left_header = Text("Elliptic Curves", font_size=32, color=CURVE_COLOR_1)
        self.left_header.move_to(LEFT * 3.5 + UP * 3)

        self.right_header = Text(
            "Quaternion Algebras", font_size=32, color=ORDER_COLOR_1
        )
        self.right_header.move_to(RIGHT * 3.5 + UP * 3)

        # Correspondence symbol
        self.corresp = Text("↔", font_size=48, color=DIVIDER_COLOR)
        self.corresp.move_to(UP * 3)

        self.play(
            Create(self.divider),
            Write(self.left_header),
            Write(self.right_header),
            Write(self.corresp),
        )
        self.wait(0.5)

    def show_curve_to_order(self):
        """Show: Curve E ↔ Maximal Order O."""
        subtitle = Text("Curves ↔ Maximal Orders", font_size=28)
        subtitle.to_edge(UP).shift(DOWN * 0.8)
        self.play(Write(subtitle))

        # LEFT: Elliptic curve
        curve = Circle(radius=0.8, color=CURVE_COLOR_1, fill_opacity=0.3)
        curve.move_to(LEFT * 3.5 + UP * 0.5)
        curve_label = Text("E", font_size=28).next_to(curve, DOWN)

        curve_note = Text("supersingular curve", font_size=18, color=GRAY)
        curve_note.next_to(curve_label, DOWN, buff=0.1)

        # RIGHT: Maximal order (represented as a 4D lattice box)
        order = self.create_order_visual(RIGHT * 3.5 + UP * 0.5, ORDER_COLOR_1)
        order_label = Text("O = End(E)", font_size=24).next_to(order, DOWN)

        order_note = Text("maximal order in B_{p,∞}", font_size=18, color=GRAY)
        order_note.next_to(order_label, DOWN, buff=0.1)

        # Animate together
        self.play(
            Create(curve),
            Write(curve_label),
            FadeIn(curve_note),
            Create(order),
            Write(order_label),
            FadeIn(order_note),
        )
        self.wait(1)

        # Show the correspondence arrow
        corresp_arrow = DoubleArrow(
            LEFT * 1.5 + UP * 0.5, RIGHT * 1.5 + UP * 0.5, color=WHITE, buff=0.3
        )
        corresp_text = Text("1:1", font_size=24).next_to(corresp_arrow, UP)

        self.play(GrowArrow(corresp_arrow), Write(corresp_text))
        self.wait(1)

        # Add a second curve/order pair
        curve2 = Circle(radius=0.8, color=CURVE_COLOR_2, fill_opacity=0.3)
        curve2.move_to(LEFT * 3.5 + DOWN * 2)
        curve2_label = Text("E'", font_size=28, color=CURVE_COLOR_2).next_to(
            curve2, DOWN
        )

        order2 = self.create_order_visual(RIGHT * 3.5 + DOWN * 2, ORDER_COLOR_2)
        order2_label = Text("O' = End(E')", font_size=24, color=ORDER_COLOR_2)
        order2_label.next_to(order2, DOWN)

        self.play(
            Create(curve2),
            Write(curve2_label),
            Create(order2),
            Write(order2_label),
        )
        self.wait(1)

        # Store for later
        self.curve1 = curve
        self.curve2 = curve2
        self.order1 = order
        self.order2 = order2
        self.curve1_label = curve_label
        self.curve2_label = curve2_label
        self.order1_label = order_label
        self.order2_label = order2_label

        # Clean up some elements
        self.play(
            FadeOut(subtitle),
            FadeOut(corresp_arrow),
            FadeOut(corresp_text),
            FadeOut(curve_note),
            FadeOut(order_note),
        )

    def show_isogeny_to_ideal(self):
        """Show: Isogeny φ ↔ Left O-ideal I."""
        subtitle = Text("Isogenies ↔ Ideals", font_size=28)
        subtitle.to_edge(UP).shift(DOWN * 0.8)
        self.play(Write(subtitle))

        # LEFT: Isogeny arrow
        isogeny = Arrow(
            self.curve1.get_bottom() + DOWN * 0.1,
            self.curve2.get_top() + UP * 0.1,
            color=ISOGENY_COLOR,
            stroke_width=5,
            buff=0.1,
        )
        isogeny_label = Text("φ", font_size=28, color=ISOGENY_COLOR)
        isogeny_label.next_to(isogeny, LEFT, buff=0.1)

        degree_label = Text("deg = d", font_size=18, color=GRAY)
        degree_label.next_to(isogeny_label, DOWN, buff=0.1)

        # RIGHT: Ideal (represented as a connecting band)
        ideal = self.create_ideal_visual(
            self.order1.get_bottom() + DOWN * 0.2,
            self.order2.get_top() + UP * 0.2,
            IDEAL_COLOR,
        )
        ideal_label = Text("I", font_size=28, color=IDEAL_COLOR)
        ideal_label.next_to(ideal, RIGHT, buff=0.1)

        norm_label = Text("Nrd(I) = d", font_size=18, color=GRAY)
        norm_label.next_to(ideal_label, DOWN, buff=0.1)

        # Animate in sync - this is the key visual!
        self.play(GrowArrow(isogeny), Create(ideal), run_time=1.5)
        self.play(
            Write(isogeny_label),
            FadeIn(degree_label),
            Write(ideal_label),
            FadeIn(norm_label),
        )
        self.wait(1)

        # Highlight the degree ↔ norm correspondence
        deg_box = SurroundingRectangle(degree_label, color=YELLOW, buff=0.1)
        norm_box = SurroundingRectangle(norm_label, color=YELLOW, buff=0.1)

        self.play(Create(deg_box), Create(norm_box))

        corresp_note = Text("degree = norm!", font_size=22, color=YELLOW)
        corresp_note.to_edge(DOWN)
        self.play(Write(corresp_note))
        self.wait(1)

        # Store and clean
        self.isogeny = isogeny
        self.ideal = ideal
        self.isogeny_label = isogeny_label
        self.ideal_label = ideal_label

        self.play(
            FadeOut(subtitle),
            FadeOut(deg_box),
            FadeOut(norm_box),
            FadeOut(degree_label),
            FadeOut(norm_label),
            FadeOut(corresp_note),
        )

    def show_composition(self):
        """Show: Composition of isogenies ↔ Product of ideals."""
        subtitle = Text("Composition ↔ Ideal Product", font_size=28)
        subtitle.to_edge(UP).shift(DOWN * 0.8)
        self.play(Write(subtitle))

        # Add a third curve/order
        curve3 = Circle(radius=0.6, color=CURVE_COLOR_3, fill_opacity=0.3)
        curve3.move_to(LEFT * 5 + DOWN * 0.5)
        curve3_label = Text("E''", font_size=24, color=CURVE_COLOR_3)
        curve3_label.next_to(curve3, LEFT)

        order3 = self.create_order_visual(
            RIGHT * 5.5 + DOWN * 0.5, ORDER_COLOR_3, scale=0.6
        )
        order3_label = Text("O''", font_size=24, color=ORDER_COLOR_3)
        order3_label.next_to(order3, RIGHT)

        self.play(
            Create(curve3),
            Write(curve3_label),
            Create(order3),
            Write(order3_label),
        )

        # Second isogeny ψ: E' → E''
        isogeny2 = Arrow(
            self.curve2.get_left() + LEFT * 0.1,
            curve3.get_right() + RIGHT * 0.1,
            color=ORANGE,
            stroke_width=4,
            buff=0.1,
        )
        isogeny2_label = Text("ψ", font_size=24, color=ORANGE)
        isogeny2_label.next_to(isogeny2, UP, buff=0.1)

        # Second ideal J
        ideal2 = self.create_ideal_visual(
            self.order2.get_left() + LEFT * 0.2,
            order3.get_right() + RIGHT * 0.2,
            ORANGE,
            horizontal=True,
        )
        ideal2_label = Text("J", font_size=24, color=ORANGE)
        ideal2_label.next_to(ideal2, UP, buff=0.1)

        self.play(
            GrowArrow(isogeny2),
            Write(isogeny2_label),
            Create(ideal2),
            Write(ideal2_label),
        )
        self.wait(1)

        # Show composition on left side
        comp_text_left = Text("ψ ∘ φ", font_size=28, color=GREEN_C)
        comp_text_left.move_to(LEFT * 3.5 + DOWN * 3.2)

        # Show product on right side
        comp_text_right = Text("I · J", font_size=28, color=GREEN_C)
        comp_text_right.move_to(RIGHT * 3.5 + DOWN * 3.2)

        # Equals sign in middle
        equals = Text("↔", font_size=36).move_to(DOWN * 3.2)

        self.play(Write(comp_text_left), Write(equals), Write(comp_text_right))
        self.wait(1)

        # Flash both to show correspondence
        self.play(
            comp_text_left.animate.scale(1.3),
            comp_text_right.animate.scale(1.3),
            rate_func=there_and_back,
            run_time=0.8,
        )
        self.wait(1)

        # Clean up for next section
        self.play(
            FadeOut(curve3),
            FadeOut(curve3_label),
            FadeOut(order3),
            FadeOut(order3_label),
            FadeOut(isogeny2),
            FadeOut(isogeny2_label),
            FadeOut(ideal2),
            FadeOut(ideal2_label),
            FadeOut(comp_text_left),
            FadeOut(comp_text_right),
            FadeOut(equals),
            FadeOut(subtitle),
        )

    def show_the_trapdoor(self):
        """Show why this is cryptographically useful - the trapdoor!"""
        subtitle = Text("The Cryptographic Trapdoor", font_size=32, color=YELLOW)
        subtitle.to_edge(UP).shift(DOWN * 0.8)
        self.play(Write(subtitle))

        # Highlight the asymmetry
        # LEFT side: just curve E_A, no visible structure
        self.play(
            self.curve1.animate.set_fill(opacity=0.6),
            self.isogeny.animate.set_opacity(0.3),
            self.isogeny_label.animate.set_opacity(0.3),
        )

        left_box = SurroundingRectangle(
            VGroup(self.curve1, self.curve1_label), color=YELLOW, buff=0.2
        )
        left_text = Text("Public: just E_A", font_size=20, color=YELLOW)
        left_text.next_to(left_box, UP)

        self.play(Create(left_box), Write(left_text))

        # RIGHT side: full quaternion structure visible
        right_box = SurroundingRectangle(
            VGroup(self.order1, self.order1_label, self.ideal, self.ideal_label),
            color=GREEN_C,
            buff=0.2,
        )
        right_text = Text("Secret: End(E_A) = O", font_size=20, color=GREEN_C)
        right_text.next_to(right_box, UP)

        self.play(Create(right_box), Write(right_text))
        self.wait(1)

        # Explanation
        explain1 = (
            Text("Anyone can see the curve E_A", font_size=24)
            .to_edge(DOWN)
            .shift(UP * 1.2)
        )

        explain2 = (
            Text("Only the signer knows End(E_A)", font_size=24, color=GREEN_C)
            .to_edge(DOWN)
            .shift(UP * 0.5)
        )

        explain3 = (
            Text(
                "→ Can efficiently compute isogenies via quaternion arithmetic!",
                font_size=22,
                color=YELLOW,
            )
            .to_edge(DOWN)
            .shift(DOWN * 0.2)
        )

        self.play(Write(explain1))
        self.wait(0.5)
        self.play(Write(explain2))
        self.wait(0.5)
        self.play(Write(explain3))
        self.wait(2)

        # Clean up
        self.play(
            FadeOut(left_box),
            FadeOut(left_text),
            FadeOut(right_box),
            FadeOut(right_text),
            FadeOut(explain1),
            FadeOut(explain2),
            FadeOut(explain3),
            FadeOut(subtitle),
            self.isogeny.animate.set_opacity(1),
            self.isogeny_label.animate.set_opacity(1),
            self.curve1.animate.set_fill(opacity=0.3),
        )

    def show_summary(self):
        """Final summary table."""
        # Clear the demo curves
        self.play(
            FadeOut(self.curve1),
            FadeOut(self.curve1_label),
            FadeOut(self.curve2),
            FadeOut(self.curve2_label),
            FadeOut(self.order1),
            FadeOut(self.order1_label),
            FadeOut(self.order2),
            FadeOut(self.order2_label),
            FadeOut(self.isogeny),
            FadeOut(self.isogeny_label),
            FadeOut(self.ideal),
            FadeOut(self.ideal_label),
        )

        title = Text("The Deuring Correspondence", font_size=40)
        title.to_edge(UP).shift(DOWN * 0.3)
        self.play(
            FadeOut(self.left_header),
            FadeOut(self.right_header),
            FadeOut(self.corresp),
            FadeOut(self.divider),
            Write(title),
        )

        # Summary table
        rows = [
            ("Curve E", "↔", "Maximal order O"),
            ("Isogeny φ: E → E'", "↔", "Left O-ideal I"),
            ("Degree deg(φ)", "↔", "Norm Nrd(I)"),
            ("Composition ψ∘φ", "↔", "Product I·J"),
            ("Dual isogeny φ̂", "↔", "Conjugate ideal Ī"),
        ]

        table_entries = VGroup()
        y_start = 1.5
        for i, (left, mid, right) in enumerate(rows):
            y = y_start - i * 0.8
            left_text = Text(left, font_size=24, color=CURVE_COLOR_1)
            left_text.move_to(LEFT * 3 + UP * y)

            mid_text = Text(mid, font_size=28)
            mid_text.move_to(UP * y)

            right_text = Text(right, font_size=24, color=ORDER_COLOR_1)
            right_text.move_to(RIGHT * 3 + UP * y)

            table_entries.add(left_text, mid_text, right_text)

        self.play(LaggedStart(*[Write(e) for e in table_entries], lag_ratio=0.1))
        self.wait(1)

        # Final message
        box = Rectangle(width=11, height=1.2, color=YELLOW, fill_opacity=0.1)
        box.to_edge(DOWN).shift(UP * 0.3)

        message = VGroup(
            Text(
                "With End(E): quaternion arithmetic makes isogeny problems easy",
                font_size=22,
            ),
            Text(
                "Without End(E): isogeny problems remain exponentially hard",
                font_size=22,
                color=GRAY,
            ),
        ).arrange(DOWN, buff=0.15)
        message.move_to(box.get_center())

        self.play(Create(box), Write(message))
        self.wait(3)

    # === Helper methods to create visual elements ===

    def create_order_visual(self, position, color, scale=1.0):
        """Create a visual representation of a maximal order (4D lattice)."""
        # Represent as a stylized 4D lattice structure
        size = 0.7 * scale

        # Main square representing the order
        outer = Square(
            side_length=size * 1.4, color=color, fill_opacity=0.2, stroke_width=2
        )

        # Inner structure suggesting 4D lattice
        inner = Square(
            side_length=size * 0.8, color=color, fill_opacity=0.1, stroke_width=1
        )
        inner.rotate(PI / 4)

        # Dots at lattice points
        dots = VGroup()
        for x in [-0.3, 0, 0.3]:
            for y in [-0.3, 0, 0.3]:
                dot = Dot((x * scale, y * scale, 0), radius=0.03 * scale, color=color)
                dots.add(dot)

        order = VGroup(outer, inner, dots)
        order.move_to(position)
        return order

    def create_ideal_visual(self, start, end, color, horizontal=False):
        """Create a visual representation of an ideal (connecting band)."""
        # Represent as a wavy/banded connection
        if horizontal:
            # Horizontal connection
            path = Line(start, end, color=color, stroke_width=6)
            path.set_opacity(0.7)
        else:
            # Vertical connection with some style
            mid = (start + end) / 2
            path = CubicBezier(
                start,
                start + RIGHT * 0.5,
                end + RIGHT * 0.5,
                end,
                color=color,
                stroke_width=6,
            )
            path.set_opacity(0.7)

        return path


class DeuringInAction(Scene):
    """Show the Deuring correspondence being used in SQIsign signing."""

    def construct(self):
        title = Text("Deuring Correspondence in SQIsign Signing", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))

        # Setup: split screen
        divider = Line(UP * 2.5, DOWN * 2.5, color=GRAY_B, stroke_width=2)
        left_label = Text("What Verifier Sees", font_size=24, color=GRAY)
        left_label.move_to(LEFT * 3.5 + UP * 2.2)
        right_label = Text("What Signer Knows", font_size=24, color=GREEN_C)
        right_label.move_to(RIGHT * 3.5 + UP * 2.2)

        self.play(Create(divider), Write(left_label), Write(right_label))

        # LEFT: The curve E_A (public key)
        ea = Circle(radius=0.6, color=BLUE_D, fill_opacity=0.3)
        ea.move_to(LEFT * 3.5 + UP * 0.5)
        ea_label = Text("E_A", font_size=24).next_to(ea, DOWN)
        pk_note = Text("(public key)", font_size=16, color=GRAY)
        pk_note.next_to(ea_label, DOWN, buff=0.1)

        # LEFT: Target curve E_chl
        echl = Circle(radius=0.6, color=TEAL_C, fill_opacity=0.3)
        echl.move_to(LEFT * 3.5 + DOWN * 2)
        echl_label = Text("E_chl", font_size=24).next_to(echl, DOWN)

        self.play(
            Create(ea),
            Write(ea_label),
            FadeIn(pk_note),
            Create(echl),
            Write(echl_label),
        )

        # LEFT: The required isogeny σ (unknown!)
        sigma_ghost = DashedLine(
            ea.get_bottom() + DOWN * 0.1,
            echl.get_top() + UP * 0.1,
            color=RED_C,
            stroke_width=3,
        )
        sigma_question = Text("σ = ?", font_size=24, color=RED_C)
        sigma_question.next_to(sigma_ghost, LEFT)

        self.play(Create(sigma_ghost), Write(sigma_question))
        self.wait(1)

        # RIGHT: Full quaternion structure
        # Order O_A
        order_a = Square(side_length=0.8, color=BLUE_D, fill_opacity=0.2)
        order_a.move_to(RIGHT * 3.5 + UP * 0.5)
        order_a_label = Text("O_A = End(E_A)", font_size=18)
        order_a_label.next_to(order_a, UP, buff=0.1)

        # Order O_chl
        order_chl = Square(side_length=0.8, color=TEAL_C, fill_opacity=0.2)
        order_chl.move_to(RIGHT * 3.5 + DOWN * 2)
        order_chl_label = Text("O_chl", font_size=18)
        order_chl_label.next_to(order_chl, DOWN, buff=0.1)

        self.play(
            Create(order_a),
            Write(order_a_label),
            Create(order_chl),
            Write(order_chl_label),
        )
        self.wait(0.5)

        # RIGHT: The signer can compute the ideal!
        ideal_arrow = Arrow(
            order_a.get_bottom() + DOWN * 0.1,
            order_chl.get_top() + UP * 0.1,
            color=GOLD_A,
            stroke_width=5,
        )
        ideal_label = Text("I (ideal)", font_size=20, color=GOLD_A)
        ideal_label.next_to(ideal_arrow, RIGHT)

        compute_text = Text(
            "← compute via\n   quaternion\n   arithmetic", font_size=16, color=GREEN_C
        )
        compute_text.next_to(ideal_label, RIGHT, buff=0.2)

        self.play(GrowArrow(ideal_arrow), Write(ideal_label), FadeIn(compute_text))
        self.wait(1)

        # Now show the conversion: ideal → isogeny
        convert_arrow = Arrow(
            RIGHT * 1.5 + DOWN * 0.75, LEFT * 1.5 + DOWN * 0.75, color=YELLOW
        )
        convert_label = Text("IdealToIsogeny", font_size=18, color=YELLOW)
        convert_label.next_to(convert_arrow, UP, buff=0.1)

        self.play(GrowArrow(convert_arrow), Write(convert_label))
        self.wait(0.5)

        # Replace the ghost with the actual isogeny!
        sigma_real = Arrow(
            ea.get_bottom() + DOWN * 0.1,
            echl.get_top() + UP * 0.1,
            color=GREEN_C,
            stroke_width=5,
        )
        sigma_found = Text("σ ✓", font_size=24, color=GREEN_C)
        sigma_found.next_to(sigma_real, LEFT)

        self.play(
            FadeOut(sigma_ghost),
            FadeOut(sigma_question),
            GrowArrow(sigma_real),
            Write(sigma_found),
        )
        self.wait(1)

        # Punchline
        box = Rectangle(width=11, height=1, color=GREEN_C, fill_opacity=0.1)
        box.to_edge(DOWN)
        punchline = Text(
            "Quaternion algebra turns 'find isogeny' into tractable computation",
            font_size=22,
            color=GREEN_C,
        )
        punchline.move_to(box.get_center())

        self.play(Create(box), Write(punchline))
        self.wait(3)
