"""
Dimension-2 Lifting Visualization
The key SQIsign v2.0 innovation that eliminated KLPT

Save as: scenes/dimension2.py
Run with: manim -ql scenes/dimension2.py Dimension2Lifting
"""

from manim import *
import numpy as np

# Color scheme
CURVE_COLOR = BLUE_D
PRODUCT_COLOR = PURPLE_B
STUCK_COLOR = RED_C
SMOOTH_COLOR = GREEN_C
AUXILIARY_COLOR = ORANGE
DIM2_COLOR = TEAL_B


class Dimension2Lifting(Scene):
    """Visualize how dimension-2 techniques compute non-smooth isogenies."""

    def construct(self):
        self.show_the_problem()
        self.show_the_insight()
        self.show_the_lifting()
        self.show_the_chain()
        self.show_the_projection()
        self.show_summary()

    def show_the_problem(self):
        """Show that prime-degree isogenies are stuck."""
        title = Text("The Problem: Non-Smooth Degrees", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))

        # Two curves
        e1 = Circle(radius=0.6, color=CURVE_COLOR, fill_opacity=0.3)
        e1.shift(LEFT * 3)
        e1_label = Text("E₁", font_size=24).next_to(e1, DOWN)

        e2 = Circle(radius=0.6, color=CURVE_COLOR, fill_opacity=0.3)
        e2.shift(RIGHT * 3)
        e2_label = Text("E₂", font_size=24).next_to(e2, DOWN)

        self.play(Create(e1), Create(e2), Write(e1_label), Write(e2_label))

        # The isogeny we need to compute
        arrow = Arrow(e1.get_right(), e2.get_left(), color=STUCK_COLOR, buff=0.2)
        phi_label = Text("φ", font_size=28).next_to(arrow, UP)

        self.play(GrowArrow(arrow), Write(phi_label))

        # Show the degree is prime (non-smooth)
        degree_box = VGroup(
            Text("deg(φ) = 127", font_size=28, color=STUCK_COLOR),
            Text("(prime - no small factors!)", font_size=22, color=GRAY),
        ).arrange(DOWN, buff=0.2)
        degree_box.shift(DOWN * 2)

        self.play(Write(degree_box))
        self.wait(1)

        # Show it's stuck
        stuck_text = Text(
            "Cannot decompose into small steps!", font_size=26, color=STUCK_COLOR
        )
        stuck_text.next_to(degree_box, DOWN, buff=0.3)

        cross = Cross(arrow, stroke_color=STUCK_COLOR, stroke_width=8)

        self.play(Write(stuck_text), Create(cross))
        self.wait(1)

        # Cost label
        cost = Text(
            "Cost: O(127) ≈ direct computation", font_size=22, color=STUCK_COLOR
        )
        cost.to_edge(DOWN)
        self.play(Write(cost))
        self.wait(1)

        # Store for later and clear
        self.e1, self.e2 = e1, e2
        self.e1_label, self.e2_label = e1_label, e2_label
        self.arrow, self.phi_label = arrow, phi_label

        self.play(
            FadeOut(title),
            FadeOut(degree_box),
            FadeOut(stuck_text),
            FadeOut(cross),
            FadeOut(cost),
        )

    def show_the_insight(self):
        """Show the key insight: 127 + 1 = 128 = 2^7."""
        title = Text("The Insight: Degree Shifting", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))

        # Show the arithmetic
        line1 = Text("127 is prime (stuck)", font_size=28, color=STUCK_COLOR)
        line2 = Text("but 127 + 1 = 128", font_size=28)
        line3 = Text("= 2⁷", font_size=36, color=SMOOTH_COLOR)
        line4 = Text("(maximally smooth!)", font_size=24, color=SMOOTH_COLOR)

        arithmetic = VGroup(line1, line2, line3, line4).arrange(DOWN, buff=0.3)
        arithmetic.move_to(ORIGIN)

        self.play(Write(line1))
        self.wait(0.5)
        self.play(Write(line2))
        self.wait(0.5)
        self.play(Write(line3), Write(line4))
        self.wait(1)

        # Key question
        question = Text(
            "Can we compute a degree-128 isogeny instead?", font_size=26, color=TEAL_B
        )
        question.to_edge(DOWN).shift(UP * 0.5)
        self.play(Write(question))
        self.wait(1)

        answer = Text(
            "Yes! Using Kani's Lemma in dimension 2", font_size=26, color=SMOOTH_COLOR
        )
        answer.next_to(question, DOWN, buff=0.3)
        self.play(Write(answer))
        self.wait(1.5)

        self.play(
            FadeOut(title),
            FadeOut(arithmetic),
            FadeOut(question),
            FadeOut(answer),
            FadeOut(self.arrow),
            FadeOut(self.phi_label),
            FadeOut(self.e1),
            FadeOut(self.e2),
            FadeOut(self.e1_label),
            FadeOut(self.e2_label),
        )

    def show_the_lifting(self):
        """Show lifting from E to E × E'."""
        title = Text("Step 1: Lift to Dimension 2", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))

        # Original curve E1
        e1 = Circle(radius=0.5, color=CURVE_COLOR, fill_opacity=0.3)
        e1.shift(LEFT * 4 + UP * 1.5)
        e1_label = Text("E₁", font_size=22).next_to(e1, LEFT)

        self.play(Create(e1), Write(e1_label))

        # Auxiliary curve E'
        e_aux = Circle(radius=0.5, color=AUXILIARY_COLOR, fill_opacity=0.3)
        e_aux.shift(LEFT * 4 + DOWN * 1.5)
        e_aux_label = Text("E'", font_size=22, color=AUXILIARY_COLOR).next_to(
            e_aux, LEFT
        )

        aux_note = Text("(auxiliary curve)", font_size=18, color=GRAY)
        aux_note.next_to(e_aux, DOWN, buff=0.1)

        self.play(Create(e_aux), Write(e_aux_label), FadeIn(aux_note))
        self.wait(0.5)

        # Show the product E1 × E'
        product_box = Rectangle(
            width=1.8, height=2.5, color=PRODUCT_COLOR, fill_opacity=0.2, stroke_width=3
        )
        product_box.shift(RIGHT * 0 + UP * 0)

        # Curves inside the product
        e1_in_prod = Circle(radius=0.35, color=CURVE_COLOR, fill_opacity=0.3)
        e1_in_prod.move_to(product_box.get_center() + UP * 0.6)

        e_aux_in_prod = Circle(radius=0.35, color=AUXILIARY_COLOR, fill_opacity=0.3)
        e_aux_in_prod.move_to(product_box.get_center() + DOWN * 0.6)

        times_symbol = Text("×", font_size=28).move_to(product_box.get_center())

        product_label = Text("E₁ × E'", font_size=24, color=PRODUCT_COLOR)
        product_label.next_to(product_box, DOWN)

        dim_label = Text("(abelian surface)", font_size=18, color=GRAY)
        dim_label.next_to(product_label, DOWN, buff=0.1)

        # Animate the lifting
        self.play(
            TransformFromCopy(e1, e1_in_prod),
            TransformFromCopy(e_aux, e_aux_in_prod),
        )
        self.play(
            Create(product_box),
            Write(times_symbol),
            Write(product_label),
            FadeIn(dim_label),
        )
        self.wait(1)

        # Similarly for E2
        e2 = Circle(radius=0.5, color=CURVE_COLOR, fill_opacity=0.3)
        e2.shift(RIGHT * 4 + UP * 1.5)
        e2_label = Text("E₂", font_size=22).next_to(e2, RIGHT)

        e_aux2 = Circle(radius=0.5, color=AUXILIARY_COLOR, fill_opacity=0.3)
        e_aux2.shift(RIGHT * 4 + DOWN * 1.5)
        e_aux2_label = Text("E''", font_size=22, color=AUXILIARY_COLOR).next_to(
            e_aux2, RIGHT
        )

        self.play(Create(e2), Write(e2_label), Create(e_aux2), Write(e_aux2_label))

        # Second product
        product_box2 = Rectangle(
            width=1.8, height=2.5, color=PRODUCT_COLOR, fill_opacity=0.2, stroke_width=3
        )
        product_box2.shift(RIGHT * 4 + DOWN * 2.5)

        product_label2 = Text("E₂ × E''", font_size=24, color=PRODUCT_COLOR)
        product_label2.next_to(product_box2, DOWN)

        # Store for next section
        self.product_box = product_box
        self.product_box2 = product_box2
        self.title = title

        # Explanation
        explain = Text(
            "Kani's Lemma: degree-d isogeny embeds into degree-(d+1) on products",
            font_size=22,
            color=TEAL_B,
        )
        explain.to_edge(DOWN)
        self.play(Write(explain))
        self.wait(2)

        # Clear for next section
        self.play(
            FadeOut(e1),
            FadeOut(e1_label),
            FadeOut(e_aux),
            FadeOut(e_aux_label),
            FadeOut(aux_note),
            FadeOut(e2),
            FadeOut(e2_label),
            FadeOut(e_aux2),
            FadeOut(e_aux2_label),
            FadeOut(product_box),
            FadeOut(e1_in_prod),
            FadeOut(e_aux_in_prod),
            FadeOut(times_symbol),
            FadeOut(product_label),
            FadeOut(dim_label),
            FadeOut(explain),
            FadeOut(title),
        )

    def show_the_chain(self):
        """Show the (2,2)-isogeny chain computation."""
        title = Text("Step 2: Compute via (2,2)-Isogeny Chain", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))

        # Create chain of products
        num_steps = 7  # 2^7 = 128

        # Products as rectangles
        products = []
        arrows = []

        x_start = -5.5
        x_spacing = 1.5

        for i in range(num_steps + 1):
            x = x_start + i * x_spacing
            rect = Rectangle(
                width=0.8,
                height=1.2,
                color=PRODUCT_COLOR if i > 0 and i < num_steps else CURVE_COLOR,
                fill_opacity=0.3,
                stroke_width=2,
            )
            rect.move_to((x, 0, 0))
            products.append(rect)

        # First and last are special (source and target)
        products[0].set_color(CURVE_COLOR)
        products[-1].set_color(CURVE_COLOR)

        # Labels
        start_label = Text("E₁×E'", font_size=18).next_to(products[0], DOWN)
        end_label = Text("E₂×E''", font_size=18).next_to(products[-1], DOWN)

        # Animate products appearing
        self.play(*[Create(p) for p in products], Write(start_label), Write(end_label))

        # Add arrows with (2,2) labels
        arrow_mobjects = []
        for i in range(num_steps):
            arr = Arrow(
                products[i].get_right(),
                products[i + 1].get_left(),
                color=SMOOTH_COLOR,
                buff=0.1,
                stroke_width=3,
                max_tip_length_to_length_ratio=0.2,
            )
            arrow_mobjects.append(arr)

        # Animate arrows appearing one by one
        for i, arr in enumerate(arrow_mobjects):
            step_label = Text("(2,2)", font_size=14, color=SMOOTH_COLOR)
            step_label.next_to(arr, UP, buff=0.05)
            self.play(GrowArrow(arr), FadeIn(step_label), run_time=0.3)

        self.wait(0.5)

        # Show total degree
        brace = Brace(VGroup(*products), DOWN, buff=0.4)
        brace_label = Text(
            "Total: 7 steps of (2,2) = degree 2⁷ = 128",
            font_size=22,
            color=SMOOTH_COLOR,
        )
        brace_label.next_to(brace, DOWN)

        self.play(Create(brace), Write(brace_label))
        self.wait(1)

        # Cost comparison
        cost_text = VGroup(
            Text("Cost: 7 × O(4) = O(28)", font_size=24, color=SMOOTH_COLOR),
            Text("vs O(127) direct", font_size=20, color=STUCK_COLOR),
        ).arrange(RIGHT, buff=1)
        cost_text.to_edge(DOWN)

        self.play(Write(cost_text))
        self.wait(1.5)

        # Store and clear
        self.play(
            FadeOut(title),
            *[FadeOut(p) for p in products],
            *[FadeOut(a) for a in arrow_mobjects],
            FadeOut(start_label),
            FadeOut(end_label),
            FadeOut(brace),
            FadeOut(brace_label),
            FadeOut(cost_text),
            *(
                [
                    FadeOut(m)
                    for m in self.mobjects
                    if isinstance(m, Text) and "(2,2)" in m.text
                ]
                if hasattr(self, "mobjects")
                else []
            )
        )

    def show_the_projection(self):
        """Show projecting back to get the original isogeny."""
        title = Text("Step 3: Project Back to Dimension 1", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))

        # Product on top
        product_left = Rectangle(
            width=1.2, height=1.8, color=PRODUCT_COLOR, fill_opacity=0.2
        )
        product_left.shift(LEFT * 3 + UP * 1)
        prod_left_label = Text("E₁ × E'", font_size=20, color=PRODUCT_COLOR)
        prod_left_label.next_to(product_left, UP)

        product_right = Rectangle(
            width=1.2, height=1.8, color=PRODUCT_COLOR, fill_opacity=0.2
        )
        product_right.shift(RIGHT * 3 + UP * 1)
        prod_right_label = Text("E₂ × E''", font_size=20, color=PRODUCT_COLOR)
        prod_right_label.next_to(product_right, UP)

        # Arrow between products
        prod_arrow = Arrow(
            product_left.get_right(),
            product_right.get_left(),
            color=SMOOTH_COLOR,
            buff=0.2,
            stroke_width=4,
        )
        prod_arrow_label = Text("(128,128)", font_size=20, color=SMOOTH_COLOR)
        prod_arrow_label.next_to(prod_arrow, UP)

        self.play(
            Create(product_left),
            Write(prod_left_label),
            Create(product_right),
            Write(prod_right_label),
            GrowArrow(prod_arrow),
            Write(prod_arrow_label),
        )
        self.wait(0.5)

        # Projection arrows down
        proj_left = Arrow(
            product_left.get_bottom(),
            product_left.get_bottom() + DOWN * 1.5,
            color=GRAY,
            buff=0.1,
        )
        proj_right = Arrow(
            product_right.get_bottom(),
            product_right.get_bottom() + DOWN * 1.5,
            color=GRAY,
            buff=0.1,
        )

        proj_label = Text("project", font_size=16, color=GRAY)
        proj_label.next_to(proj_left, LEFT, buff=0.1)

        # Original curves at bottom
        e1 = Circle(radius=0.5, color=CURVE_COLOR, fill_opacity=0.3)
        e1.move_to(product_left.get_bottom() + DOWN * 2.2)
        e1_label = Text("E₁", font_size=20).next_to(e1, DOWN)

        e2 = Circle(radius=0.5, color=CURVE_COLOR, fill_opacity=0.3)
        e2.move_to(product_right.get_bottom() + DOWN * 2.2)
        e2_label = Text("E₂", font_size=20).next_to(e2, DOWN)

        self.play(GrowArrow(proj_left), GrowArrow(proj_right), Write(proj_label))
        self.play(Create(e1), Write(e1_label), Create(e2), Write(e2_label))

        # The recovered isogeny!
        recovered_arrow = Arrow(
            e1.get_right(), e2.get_left(), color=SMOOTH_COLOR, buff=0.2, stroke_width=6
        )
        recovered_label = Text("φ (degree 127)", font_size=22, color=SMOOTH_COLOR)
        recovered_label.next_to(recovered_arrow, DOWN)

        self.play(GrowArrow(recovered_arrow), Write(recovered_label))

        # Success message
        success = Text(
            "✓ Computed without factoring 127!", font_size=26, color=SMOOTH_COLOR
        )
        success.to_edge(DOWN)
        self.play(Write(success))
        self.wait(2)

        self.play(*[FadeOut(m) for m in self.mobjects])

    def show_summary(self):
        """Final summary of the technique."""
        title = Text("Dimension-2 Lifting: Summary", font_size=40)
        title.to_edge(UP)
        self.play(Write(title))

        steps = VGroup(
            Text("1. Have degree-d isogeny (d may be non-smooth)", font_size=24),
            Text("2. Note: d + 1 has a factor of 2 (since d is odd)", font_size=24),
            Text("3. Lift to E × E' (abelian surface)", font_size=24),
            Text("4. Compute (2,2)-isogeny chain (all smooth!)", font_size=24),
            Text("5. Project back to get degree-d isogeny", font_size=24),
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        steps.move_to(ORIGIN).shift(UP * 0.5)

        for step in steps:
            self.play(Write(step), run_time=0.8)
            self.wait(0.3)

        self.wait(1)

        # The punchline
        box = Rectangle(width=10, height=1.5, color=SMOOTH_COLOR, fill_opacity=0.1)
        box.to_edge(DOWN).shift(UP * 0.5)

        punchline = VGroup(
            Text(
                "This eliminated KLPT from SQIsign v2.0",
                font_size=26,
                color=SMOOTH_COLOR,
            ),
            Text("Signing: 2000ms → 100ms  (20× faster)", font_size=24),
        ).arrange(DOWN, buff=0.2)
        punchline.move_to(box.get_center())

        self.play(Create(box), Write(punchline))
        self.wait(3)


class KaniLemmaVisualization(Scene):
    """More detailed look at Kani's Lemma."""

    def construct(self):
        title = Text("Kani's Lemma: The Key Insight", font_size=40)
        title.to_edge(UP)
        self.play(Write(title))

        # The "diamond" of curves
        e0 = Circle(radius=0.5, color=CURVE_COLOR, fill_opacity=0.3).shift(UP * 2)
        e1 = Circle(radius=0.5, color=CURVE_COLOR, fill_opacity=0.3).shift(LEFT * 3)
        e2 = Circle(radius=0.5, color=CURVE_COLOR, fill_opacity=0.3).shift(RIGHT * 3)
        e3 = Circle(radius=0.5, color=CURVE_COLOR, fill_opacity=0.3).shift(DOWN * 2)

        e0_label = Text("E₀", font_size=20).next_to(e0, UP)
        e1_label = Text("E₁", font_size=20).next_to(e1, LEFT)
        e2_label = Text("E₂", font_size=20).next_to(e2, RIGHT)
        e3_label = Text("E₃", font_size=20).next_to(e3, DOWN)

        self.play(
            Create(e0),
            Create(e1),
            Create(e2),
            Create(e3),
            Write(e0_label),
            Write(e1_label),
            Write(e2_label),
            Write(e3_label),
        )

        # Isogenies forming the diamond
        phi_a = Arrow(e0.get_center(), e1.get_center(), buff=0.5, color=BLUE_B)
        phi_b = Arrow(e0.get_center(), e2.get_center(), buff=0.5, color=ORANGE)
        phi_c = Arrow(e1.get_center(), e3.get_center(), buff=0.5, color=ORANGE)
        phi_d = Arrow(e2.get_center(), e3.get_center(), buff=0.5, color=BLUE_B)

        deg_a = Text("deg m", font_size=16, color=BLUE_B).next_to(
            phi_a, UP + LEFT, buff=0.1
        )
        deg_b = Text("deg n", font_size=16, color=ORANGE).next_to(
            phi_b, UP + RIGHT, buff=0.1
        )
        deg_c = Text("deg n", font_size=16, color=ORANGE).next_to(
            phi_c, DOWN + LEFT, buff=0.1
        )
        deg_d = Text("deg m", font_size=16, color=BLUE_B).next_to(
            phi_d, DOWN + RIGHT, buff=0.1
        )

        self.play(
            GrowArrow(phi_a),
            GrowArrow(phi_b),
            GrowArrow(phi_c),
            GrowArrow(phi_d),
            Write(deg_a),
            Write(deg_b),
            Write(deg_c),
            Write(deg_d),
        )
        self.wait(1)

        # Explanation
        explain1 = (
            Text("When degrees match (m,n) on opposite sides...", font_size=24)
            .to_edge(DOWN)
            .shift(UP * 1)
        )
        self.play(Write(explain1))
        self.wait(1)

        explain2 = (
            Text(
                "There's an (m+n, m+n)-isogeny on E₀ × E₃ → E₁ × E₂",
                font_size=24,
                color=SMOOTH_COLOR,
            )
            .to_edge(DOWN)
            .shift(UP * 0.3)
        )
        self.play(Write(explain2))
        self.wait(1)

        # Show the product arrow
        product_arrow = CurvedArrow(
            e0.get_center() + DOWN * 0.3 + LEFT * 0.3,
            e3.get_center() + UP * 0.3 + LEFT * 0.3,
            angle=-TAU / 4,
            color=SMOOTH_COLOR,
        )
        product_label = Text("(m+n, m+n)", font_size=18, color=SMOOTH_COLOR)
        product_label.next_to(product_arrow, LEFT)

        self.play(Create(product_arrow), Write(product_label))
        self.wait(2)

        # Key application
        self.play(FadeOut(explain1), FadeOut(explain2))

        application = VGroup(
            Text("For SQIsign: m = 127 (our isogeny), n = 1 (identity)", font_size=22),
            Text(
                "→ Get (128, 128)-isogeny which is 2-smooth!",
                font_size=22,
                color=SMOOTH_COLOR,
            ),
        ).arrange(DOWN, buff=0.3)
        application.to_edge(DOWN)

        self.play(Write(application))
        self.wait(3)
