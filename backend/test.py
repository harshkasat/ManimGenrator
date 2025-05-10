from manim import *
import numpy as np

config.video_dir = "output/video"
config.write_to_movie = True
config.flush_cache = True
config.disable_caching = True

class BinomialExpansion(Scene):
    def construct(self):
        # Introduction
        title = Text("Binomial Theorem", color=BLUE).scale(1.5)
        self.play(Write(title), run_time=2)
        self.wait(1)
        self.play(FadeOut(title), run_time=1)

        # Define the binomial expression
        expression = MathTex(r"(a + b)^n", color=GREEN).scale(1.2)
        self.play(Write(expression), run_time=2)
        self.wait(1)

        # Expand for n=2
        expansion_n2 = MathTex(r"(a + b)^2 = a^2 + 2ab + b^2", color=YELLOW).scale(1.0)
        expansion_n2.next_to(expression, DOWN, buff=0.5)
        self.play(Write(expansion_n2), run_time=3)
        self.wait(1)

        # Expand for n=3
        expansion_n3 = MathTex(r"(a + b)^3 = a^3 + 3a^2b + 3ab^2 + b^3", color=RED).scale(1.0)
        expansion_n3.next_to(expansion_n2, DOWN, buff=0.5)
        self.play(Write(expansion_n3), run_time=4)
        self.wait(1)

        # General formula
        general_formula = MathTex(r"(a + b)^n = \sum_{k=0}^{n} \binom{n}{k} a^{n-k} b^k", color=PURPLE).scale(1.2)
        general_formula.next_to(expansion_n3, DOWN, buff=0.5)
        self.play(Write(general_formula), run_time=5)
        self.wait(2)

        # Explanation of binomial coefficient
        binomial_coeff = MathTex(r"\binom{n}{k} = \frac{n!}{k!(n-k)!}", color=ORANGE).scale(1.0)
        binomial_coeff.next_to(general_formula, DOWN, buff=0.5)
        self.play(Write(binomial_coeff), run_time=4)
        self.wait(2)

        # Example with numbers
        example = MathTex(r"(1 + x)^4 = 1 + 4x + 6x^2 + 4x^3 + x^4", color=TEAL).scale(1.0)
        example.next_to(binomial_coeff, DOWN, buff=0.5)
        self.play(Write(example), run_time=4)
        self.wait(2)

        # Cleanup
        self.play(
            FadeOut(expression),
            FadeOut(expansion_n2),
            FadeOut(expansion_n3),
            FadeOut(general_formula),
            FadeOut(binomial_coeff),
            FadeOut(example),
            run_time=2
        )

        # Conclusion
        conclusion = Text("Binomial Theorem: Expanding Powers!", color=BLUE).scale(1.5)
        self.play(Write(conclusion), run_time=2)
        self.wait(1)
        self.play(FadeOut(conclusion), run_time=1)
        self.wait(1)