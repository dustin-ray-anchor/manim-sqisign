from manim import *

class TestScene(Scene):
    def construct(self):
        # Create a circle and square
        circle = Circle(color=BLUE, fill_opacity=0.5)
        square = Square(color=RED, fill_opacity=0.5)
        
        # Animate
        self.play(Create(circle))
        self.play(Transform(circle, square))
        self.play(circle.animate.shift(RIGHT * 2))
        self.wait()