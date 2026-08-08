from manim import *

class Minimal(Scene):
    def construct(self):
        ellipse = Ellipse(width=4, height=2)
        ellipse.set_opacity(0.99)
        self.play(Create(ellipse))