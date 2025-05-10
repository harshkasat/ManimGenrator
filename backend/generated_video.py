from manim import *
import numpy as np

# Set custom config
config.video_dir = "output/video"
config.write_to_movie = True
config.flush_cache = True
config.disable_caching = True

class BinomialIntro(Scene):
    def construct(self):
        # Title
        title = Tex("Unveiling the Binomial").scale(1.5)
        self.play(Write(title), run_time=2)
        self.wait(1)
        self.play(FadeOut(title), run_time=1)

        # Definition
        definition = MathTex(r"(a + b)^n = \sum_{k=0}^{n} \binom{n}{k} a^{n-k} b^k").scale(1.2)
        self.play(Write(definition), run_time=3)
        self.wait(2)

        # Highlight components
        a_plus_b = MathTex("(a + b)").set_color(BLUE).scale(1.2)
        n_exponent = MathTex("n").set_color(YELLOW).scale(1.2)
        binom_coeff = MathTex(r"\binom{n}{k}").set_color(GREEN).scale(1.2)
        a_term = MathTex("a^{n-k}").set_color(RED).scale(1.2)
        b_term = MathTex("b^k").set_color(PURPLE).scale(1.2)

        a_plus_b.move_to(definition[0][0:5])
        n_exponent.move_to(definition[0][6])
        binom_coeff.move_to(definition[0][8:14])
        a_term.move_to(definition[0][15:21])
        b_term.move_to(definition[0][22:25])

        self.play(
            Circumscribe(a_plus_b),
            Circumscribe(n_exponent),
            run_time=1.5
        )
        self.wait(0.5)
        self.play(
            Circumscribe(binom_coeff),
            Circumscribe(a_term),
            Circumscribe(b_term),
            run_time=1.5
        )
        self.wait(1)
        self.play(FadeOut(definition, a_plus_b, n_exponent, binom_coeff, a_term, b_term), run_time=1)

        # Example
        example_title = Tex("Let's look at an example:").scale(1)
        self.play(Write(example_title), run_time=2)
        self.wait(1)
        self.play(FadeOut(example_title), run_time=1)

        example = MathTex(r"(x + y)^3 = x^3 + 3x^2y + 3xy^2 + y^3").scale(1)
        self.play(Write(example), run_time=3)
        self.wait(2)
        self.play(Indicate(example), run_time=2)

        # Matrix Transformation example
        matrix_text = MathTex(r"\begin{bmatrix} 1 & 0 \\ 0 & -1 \end{bmatrix}").scale(0.8).to_corner(UL)
        vector = np.array([1, 1, 0])
        dot = Dot(point=vector[:2], color=YELLOW)
        vector_mob = Arrow(start=ORIGIN, end=vector[:2], color=YELLOW)

        self.play(Create(matrix_text), Create(dot), Create(vector_mob))
        self.wait(1)

        matrix = np.array([[1, 0], [0, -1]])
        result = np.dot(matrix, vector[:2])
        transformed_vector = np.append(result, 0)
        transformed_dot = Dot(point=transformed_vector[:2], color=GREEN)
        transformed_vector_mob = Arrow(start=ORIGIN, end=transformed_vector[:2], color=GREEN)

        self.play(Transform(dot, transformed_dot), Transform(vector_mob, transformed_vector_mob), run_time=2)
        self.wait(1)
        self.play(FadeOut(example, matrix_text, dot, vector_mob, transformed_dot, transformed_vector_mob), run_time=1)

        # End Screen
        end_text = Text("That's Binomial!").scale(1.5)
        self.play(Write(end_text), run_time=2)
        self.wait(1)
        self.play(FadeOut(end_text), run_time=1)
        self.wait(1)


### MANIM CODE:

from manim import *
import numpy as np

# Set custom config
config.video_dir = "output/video"
config.write_to_movie = True
config.flush_cache = True
config.disable_caching = True

class BinomialIntro(Scene):
    def construct(self):
        # Title
        title = Tex("Unveiling the Binomial").scale(1.5)
        self.play(Write(title), run_time=2)
        self.wait(1)
        self.play(FadeOut(title), run_time=1)

        # Definition
        definition = MathTex(r"(a + b)^n = \sum_{k=0}^{n} \binom{n}{k} a^{n-k} b^k").scale(1.2)
        self.play(Write(definition), run_time=3)
        self.wait(2)

        # Highlight components
        a_plus_b = MathTex("(a + b)").set_color(BLUE).scale(1.2)
        n_exponent = MathTex("n").set_color(YELLOW).scale(1.2)
        binom_coeff = MathTex(r"\binom{n}{k}").set_color(GREEN).scale(1.2)
        a_term = MathTex("a^{n-k}").set_color(RED).scale(1.2)
        b_term = MathTex("b^k").set_color(PURPLE).scale(1.2)

        a_plus_b.move_to(definition[0][0:5])
        n_exponent.move_to(definition[0][6])
        binom_coeff.move_to(definition[0][8:14])
        a_term.move_to(definition[0][15:21])
        b_term.move_to(definition[0][22:25])

        self.play(
            Circumscribe(a_plus_b),
            Circumscribe(n_exponent),
            run_time=1.5
        )
        self.wait(0.5)
        self.play(
            Circumscribe(binom_coeff),
            Circumscribe(a_term),
            Circumscribe(b_term),
            run_time=1.5
        )
        self.wait(1)
        self.play(FadeOut(definition, a_plus_b, n_exponent, binom_coeff, a_term, b_term), run_time=1)

        # Example
        example_title = Tex("Let's look at an example:").scale(1)
        self.play(Write(example_title), run_time=2)
        self.wait(1)
        self.play(FadeOut(example_title), run_time=1)

        example = MathTex(r"(x + y)^3 = x^3 + 3x^2y + 3xy^2 + y^3").scale(1)
        self.play(Write(example), run_time=3)
        self.wait(2)
        self.play(Indicate(example), run_time=2)

        # Matrix Transformation example
        matrix_text = MathTex(r"\begin{bmatrix} 1 & 0 \\ 0 & -1 \end{bmatrix}").scale(0.8).to_corner(UL)
        vector = np.array([1, 1, 0])
        dot = Dot(point=vector[:2], color=YELLOW)
        vector_mob = Arrow(start=ORIGIN, end=vector[:2], color=YELLOW)

        self.play(Create(matrix_text), Create(dot), Create(vector_mob))
        self.wait(1)

        matrix = np.array([[1, 0], [0, -1]])
        result = np.dot(matrix, vector[:2])
        transformed_vector = np.append(result, 0)
        transformed_dot = Dot(point=transformed_vector[:2], color=GREEN)
        transformed_vector_mob = Arrow(start=ORIGIN, end=transformed_vector[:2], color=GREEN)

        self.play(Transform(dot, transformed_dot), Transform(vector_mob, transformed_vector_mob), run_time=2)
        self.wait(1)
        self.play(FadeOut(example, matrix_text, dot, vector_mob, transformed_dot, transformed_vector_mob), run_time=1)

        # End Screen
        end_text = Text("That's Binomial!").scale(1.5)
        self.play(Write(end_text), run_time=2)
        self.wait(1)
        self.play(FadeOut(end_text), run_time=1)
        self.wait(1)