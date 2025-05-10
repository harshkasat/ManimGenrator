from manim import *
import numpy as np

# Set custom config
config.video_dir = "output/video"

class GoldenRatio(Scene):
    def construct(self):
        # Define colors
        GOLDEN_YELLOW = "#FFC857"
        PHI_COLOR = "#6495ED"
        RECT_COLOR = "#A0522D"

        # Introduction
        title = Tex("The Golden Ratio: \\(\\varphi\\)", color=GOLDEN_YELLOW).scale(1.5)
        self.play(Write(title), run_time=2)
        self.wait(1)
        self.play(FadeOut(title), run_time=1)

        # Define Golden Ratio value
        phi = (1 + np.sqrt(5)) / 2
        phi_tex = MathTex(
            "\\varphi = \\frac{1 + \\sqrt{5}}{2} \\approx 1.618", color=PHI_COLOR
        )
        self.play(Write(phi_tex), run_time=2)
        self.wait(1)

        # Create a square
        square = Square(side_length=2, color=RECT_COLOR)
        self.play(Create(square), run_time=1)
        self.wait(0.5)

        # Create a rectangle
        rectangle = Rectangle(height=2, width=2 * phi, color=RECT_COLOR)
        rectangle.move_to(square.get_center())  # Ensure it's centered.

        # Transform to golden rectangle
        self.play(Transform(square, rectangle), Write(MathTex("1")), run_time=2)
        self.wait(1)

        # Adding square to golden rectangle
        square2 = Square(side_length=2, color=GOLDEN_YELLOW).move_to(
            rectangle.get_center() + np.array([phi, 0, 0])
        )
        self.play(Create(square2))

        # Illustrating subdivision
        line = Line(start=np.array([phi, -1, 0]), end=np.array([phi, 1, 0])).move_to(
            rectangle.get_center() + np.array([phi, 0, 0])
        )
        self.play(Create(line))

        text1 = MathTex("1").move_to(np.array([1, -2, 0]))
        text2 = MathTex("\\varphi - 1").move_to(np.array([3.1, -2, 0]))
        self.play(Write(text1))
        self.play(Write(text2))
        self.wait(2)

        # Fibonacci sequence visualization
        self.play(
            FadeOut(phi_tex, text1, text2, line), square2.animate.fade(0.2), run_time=1
        )
        square_list = []
        square_list.append(
            Square(side_length=2, color=GOLDEN_YELLOW).move_to(np.array([0, 0, 0]))
        )
        square_list.append(
            Square(side_length=2, color=GOLDEN_YELLOW).next_to(
                square_list[0], LEFT, buff=0
            )
        )
        square_list.append(
            Square(side_length=4, color=GOLDEN_YELLOW).next_to(
                square_list[0], UP, buff=0
            )
        )
        square_list.append(
            Square(side_length=6, color=GOLDEN_YELLOW).next_to(
                square_list[1], UP, buff=0
            )
        )
        square_list.append(
            Square(side_length=10, color=GOLDEN_YELLOW).next_to(
                square_list[3], LEFT, buff=0
            )
        )
        square_list.append(
            Square(side_length=16, color=GOLDEN_YELLOW).next_to(
                square_list[4], DOWN, buff=0
            )
        )

        self.play(Create(square_list[1]), Create(square_list[2]), run_time=1)
        self.play(Create(square_list[3]), Create(square_list[4]), run_time=1)
        self.play(Create(square_list[5]), run_time=1)

        # Final fade out
        self.wait(1)
        self.play(*[FadeOut(obj) for obj in self.mobjects], run_time=2)
        self.wait(1)
