# Manim Code Examples (Community v0.19.0)

## Example 1: Basic Shapes and Text

**Description:** Shows a circle and text, then fades them out.

```python
# ### MANIM CODE:
from manim import *
import numpy as np

class BasicShapes(Scene):
    def construct(self):
        circle = Circle(color=BLUE, fill_opacity=0.5)
        text = Text("Hello Manim!").next_to(circle, DOWN)
        self.play(Create(circle), Write(text), run_time=5) # Longer duration for narration
        self.wait(5) # Pause for narration
        self.play(FadeOut(circle), FadeOut(text), run_time=5)
        self.wait(15) # Fill remaining time
```

```text
# ### NARRATION:
Here we create a blue circle and display the text "Hello Manim!" below it. After a brief pause, both elements fade away.
```

## Example 2: Vector Transformation with Labels

**Description:** Creates a vector, displays a transformation matrix, applies the transformation, and labels the steps.

```python
# ### MANIM CODE:
from manim import *
import numpy as np

class VectorTransform(Scene):
    def construct(self):
        # Setup
        axes = Axes(x_range=[-5, 5, 1], y_range=[-5, 5, 1], x_length=6, y_length=6)
        vec_start = np.array([1, 1, 0])
        matrix = np.array([[0, -1], [1, 0]]) # 90 deg rotation

        # Initial vector
        vector = Arrow(ORIGIN, vec_start, buff=0, color=YELLOW)
        vec_label = MathTex("v", color=YELLOW).next_to(vector.get_end(), UR, buff=0.1)
        self.play(Create(axes), Create(vector), Write(vec_label), run_time=6) # Show initial state

        # Matrix
        matrix_tex = MathTex(r"M = \begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix}", color=RED).to_corner(UL)
        self.play(Write(matrix_tex), run_time=4) # Introduce matrix

        # Transformation
        vec_end = np.append(np.dot(matrix, vec_start[:2]), 0)
        new_vector = Arrow(ORIGIN, vec_end, buff=0, color=GREEN)
        new_vec_label = MathTex("Mv", color=GREEN).next_to(new_vector.get_end(), UR, buff=0.1)
        transform_label = Text("Applying 90° Rotation", font_size=24).next_to(matrix_tex, DOWN, aligned_edge=LEFT)

        self.play(Write(transform_label), run_time=3) # Explain transform
        self.play(Transform(vector, new_vector), Transform(vec_label, new_vec_label), run_time=7) # Show transform

        self.wait(10) # Hold final state
```

```text
# ### NARRATION:
We start with vector v in yellow on the coordinate plane. This is the rotation matrix M we'll use. Now, we apply the matrix M to rotate vector v by 90 degrees, resulting in the green vector Mv.
```
## Example 3: BraceAnnotation

**Description:** Shows how to create braces and attach text/latex to them.

```python
# ### MANIM CODE:
from manim import *
import numpy as np

class BraceAnnotation(Scene):
    def construct(self):
        dot = Dot([-2, -1, 0])
        dot2 = Dot([2, 1, 0])
        line = Line(dot.get_center(), dot2.get_center()).set_color(ORANGE)
        b1 = Brace(line)
        b1text = b1.get_text("Horizontal distance")
        b2 = Brace(line, direction=line.copy().rotate(PI / 2).get_unit_vector())
        b2text = b2.get_tex("x-x_1")
        
        self.play(Create(line), Create(dot), Create(dot2), run_time=3)
        self.play(Create(b1), Write(b1text), run_time=3)
        self.play(Create(b2), Write(b2text), run_time=3)
        self.wait(21) # Fill remaining time
```

```text
# ### NARRATION:
Here we demonstrate how to add annotations with braces. First, we create a line between two dots. Then we add a horizontal brace with text below it showing "Horizontal distance." Finally, we add a vertical brace with mathematical notation showing the difference between x coordinates.
```

## Example 4: SinAndCosFunctionPlot

**Description:** Plots sine and cosine functions on an axis with labels.

```python
# ### MANIM CODE:
from manim import *
import numpy as np

class SinAndCosFunctionPlot(Scene):
    def construct(self):
        axes = Axes(
            x_range=[-10, 10.3, 1],
            y_range=[-1.5, 1.5, 1],
            x_length=10,
            axis_config={"color": GREEN},
            x_axis_config={
                "numbers_to_include": np.arange(-10, 10.01, 2),
                "numbers_with_elongated_ticks": np.arange(-10, 10.01, 2),
            },
            tips=False,
        )
        axes_labels = axes.get_axis_labels()
        sin_graph = axes.plot(lambda x: np.sin(x), color=BLUE)
        cos_graph = axes.plot(lambda x: np.cos(x), color=RED)

        sin_label = axes.get_graph_label(
            sin_graph, "\\sin(x)", x_val=-10, direction=UP / 2
        )
        cos_label = axes.get_graph_label(cos_graph, label="\\cos(x)")

        vert_line = axes.get_vertical_line(
            axes.i2gp(TAU, cos_graph), color=YELLOW, line_func=Line
        )
        line_label = axes.get_graph_label(
            cos_graph, r"x=2\pi", x_val=TAU, direction=UR, color=WHITE
        )

        # Animation sequence
        self.play(Create(axes), Write(axes_labels), run_time=3)
        self.play(Create(sin_graph), Create(cos_graph), run_time=5)
        self.play(Write(sin_label), Write(cos_label), run_time=3)
        self.play(Create(vert_line), Write(line_label), run_time=3)
        self.wait(16) # Fill remaining time
```

```text
# ### NARRATION:
In this animation, we plot the sine and cosine functions on a coordinate plane. The sine function is shown in blue, while the cosine function is shown in red. We add labels to each curve and mark a vertical line at x equals 2π to highlight this important value. Notice how the curves oscillate between -1 and 1 as they extend across the x-axis.
```

## Example 5: PointMovingOnShapes

**Description:** Demonstrates how to animate a dot moving along paths and rotating.

```python
# ### MANIM CODE:
from manim import *
import numpy as np

class PointMovingOnShapes(Scene):
    def construct(self):
        circle = Circle(radius=1, color=BLUE)
        dot = Dot()
        dot2 = dot.copy().shift(RIGHT)
        self.add(dot)

        line = Line([3, 0, 0], [5, 0, 0])
        self.play(Create(line), run_time=2)
        self.play(GrowFromCenter(circle), run_time=2)
        self.play(Transform(dot, dot2), run_time=2)
        self.play(MoveAlongPath(dot, circle), run_time=7, rate_func=linear)
        self.play(Rotating(dot, about_point=[2, 0, 0]), run_time=7)
        self.wait(10) # Fill remaining time
```

```text
# ### NARRATION:
Here we demonstrate moving and transforming objects. We begin with a dot and create a line and circle. Then, we transform the dot by shifting it to the right. Watch as the dot moves along the circular path at a constant speed. Finally, the dot rotates around a fixed point, showing how we can create complex animations by combining different movements.
```

## Example 6: ThreeDSurfacePlot

**Description:** Creates a 3D Gaussian surface plot with colored checkerboard pattern.

```python
# ### MANIM CODE:
from manim import *
import numpy as np

class ThreeDSurfacePlot(ThreeDScene):
    def construct(self):
        resolution_fa = 24
        self.set_camera_orientation(phi=75 * DEGREES, theta=-30 * DEGREES)

        def param_gauss(u, v):
            x = u
            y = v
            sigma, mu = 0.4, [0.0, 0.0]
            d = np.linalg.norm(np.array([x - mu[0], y - mu[1]]))
            z = np.exp(-(d ** 2 / (2.0 * sigma ** 2)))
            return np.array([x, y, z])

        gauss_plane = Surface(
            param_gauss,
            resolution=(resolution_fa, resolution_fa),
            v_range=[-2, +2],
            u_range=[-2, +2]
        )

        gauss_plane.scale(2, about_point=ORIGIN)
        gauss_plane.set_style(fill_opacity=1, stroke_color=GREEN)
        gauss_plane.set_fill_by_checkerboard(ORANGE, BLUE, opacity=0.5)
        axes = ThreeDAxes()
        
        self.play(Create(axes), run_time=2)
        self.play(Create(gauss_plane), run_time=3)
        self.begin_ambient_camera_rotation(rate=0.1)
        self.wait(25) # Fill remaining time
```

```text
# ### NARRATION:
In this animation, we're creating a three-dimensional Gaussian surface plot. We first set up the camera angle to view our 3D scene properly. The surface is defined by a Gaussian function that creates a bell curve shape in three dimensions. We apply a checkerboard pattern with orange and blue colors to highlight the surface features. Notice how the ambient camera rotation helps us visualize the 3D nature of the surface from multiple angles.
```

## Example 7: MovingAngle

**Description:** Shows an animated angle that changes based on a ValueTracker.

```python
# ### MANIM CODE:
from manim import *
import numpy as np

class MovingAngle(Scene):
    def construct(self):
        rotation_center = LEFT

        theta_tracker = ValueTracker(110)
        line1 = Line(LEFT, RIGHT)
        line_moving = Line(LEFT, RIGHT)
        line_ref = line_moving.copy()
        line_moving.rotate(
            theta_tracker.get_value() * DEGREES, about_point=rotation_center
        )
        a = Angle(line1, line_moving, radius=0.5, other_angle=False)
        tex = MathTex(r"\theta").move_to(
            Angle(
                line1, line_moving, radius=0.5 + 3 * SMALL_BUFF, other_angle=False
            ).point_from_proportion(0.5)
        )

        self.play(Create(line1), Create(line_moving), run_time=2)
        self.play(Create(a), Write(tex), run_time=2)
        self.wait(2)

        line_moving.add_updater(
            lambda x: x.become(line_ref.copy()).rotate(
                theta_tracker.get_value() * DEGREES, about_point=rotation_center
            )
        )

        a.add_updater(
            lambda x: x.become(Angle(line1, line_moving, radius=0.5, other_angle=False))
        )
        tex.add_updater(
            lambda x: x.move_to(
                Angle(
                    line1, line_moving, radius=0.5 + 3 * SMALL_BUFF, other_angle=False
                ).point_from_proportion(0.5)
            )
        )

        self.play(theta_tracker.animate.set_value(40), run_time=3)
        self.play(theta_tracker.animate.increment_value(140), run_time=3)
        self.play(tex.animate.set_color(RED), run_time=1)
        self.play(theta_tracker.animate.set_value(350), run_time=7)
        self.wait(10) # Fill remaining time
```

```text
# ### NARRATION:
This animation demonstrates how to create a dynamic angle that updates as values change. We start with two lines forming an angle of 110 degrees. Using updaters and a ValueTracker, we can animate the angle changing smoothly. Watch as we decrease the angle to 40 degrees, then increase it by 140 degrees. As the angle continues to change, we also highlight the theta symbol in red before completing a full rotation to 350 degrees.
```

## Example 8: GraphAreaPlot

**Description:** Demonstrates how to show areas between curves and Riemann rectangles.

```python
# ### MANIM CODE:
from manim import *
import numpy as np

class GraphAreaPlot(Scene):
    def construct(self):
        ax = Axes(
            x_range=[0, 5],
            y_range=[0, 6],
            x_axis_config={"numbers_to_include": [2, 3]},
            tips=False,
        )

        labels = ax.get_axis_labels()

        curve_1 = ax.plot(lambda x: 4 * x - x ** 2, x_range=[0, 4], color=BLUE_C)
        curve_2 = ax.plot(
            lambda x: 0.8 * x ** 2 - 3 * x + 4,
            x_range=[0, 4],
            color=GREEN_B,
        )

        line_1 = ax.get_vertical_line(ax.input_to_graph_point(2, curve_1), color=YELLOW)
        line_2 = ax.get_vertical_line(ax.i2gp(3, curve_1), color=YELLOW)

        riemann_area = ax.get_riemann_rectangles(
            curve_1, x_range=[0.3, 0.6], dx=0.03, color=BLUE, fill_opacity=0.5
        )
        area = ax.get_area(
            curve_2, [2, 3], bounded_graph=curve_1, color=GREY, opacity=0.5
        )

        self.play(Create(ax), Write(labels), run_time=3)
        self.play(Create(curve_1), Create(curve_2), run_time=4)
        self.play(Create(line_1), Create(line_2), run_time=3)
        self.play(FadeIn(riemann_area), run_time=3) 
        self.play(FadeIn(area), run_time=3)
        self.wait(14) # Fill remaining time
```

```text
# ### NARRATION:
In this animation, we visualize areas between curves using Manim's plotting capabilities. We create two functions, shown in blue and green, and mark two vertical lines at x equals 2 and x equals 3. The small blue rectangles demonstrate Riemann sums, which approximate the area under a curve. The gray shaded region shows the area between both curves from x equals 2 to x equals 3. These visualizations are powerful tools for understanding calculus concepts like integration and area between curves.
```

Example 9: Camera Movement
Description: Demonstrates how to move and zoom the camera to focus on specific objects.

# ### MANIM CODE:
from manim import *

class CameraMovement(Scene):
    def construct(self):
        square = Square().shift(LEFT)
        circle = Circle().shift(RIGHT)
        self.add(square, circle)
        self.play(self.camera.frame.animate.move_to(square), run_time=2)
        self.wait(1)
        self.play(self.camera.frame.animate.move_to(circle), run_time=2)
        self.wait(1)
        self.play(self.camera.frame.animate.scale(0.5), run_time=2)
        self.wait(1)
        self.play(self.camera.frame.animate.scale(2), run_time=2)
        self.wait(1)

# ### NARRATION:
Here, we have a square and a circle. We move the camera to focus on the square, then shift to the circle. Next, we zoom in to get a closer look, and finally zoom out to see the entire scene again.


Example 10: BackgroundRectangle Usage
Description: Shows how to add a background rectangle to text for better visibility.

# ### MANIM CODE:
from manim import *

class BackgroundRectangleExample(Scene):
    def construct(self):
        text = Text("Important Note", font_size=48)
        bg_rect = BackgroundRectangle(text, fill_opacity=0.5, buff=0.1)
        self.add(bg_rect, text)
        self.wait(2)

# ### NARRATION:
In this example, we add a semi-transparent background rectangle behind the text "Important Note" to make it stand out against the background.

Example 11: ValueTracker and always_redraw
Description: Demonstrates dynamic updates using ValueTracker and always_redraw.
# ### MANIM CODE:
from manim import *

class ValueTrackerExample(Scene):
    def construct(self):
        tracker = ValueTracker(0)
        number = always_redraw(lambda: DecimalNumber(tracker.get_value()).to_edge(UP))
        self.add(number)
        self.play(tracker.animate.set_value(100), run_time=5)
        self.wait(1)

# ### NARRATION:
We use a ValueTracker to animate a number from 0 to 100. The DecimalNumber updates in real-time as the tracker changes.

Example 12: Custom Mobject
Description: Creates a custom mobject by subclassing Mobject.

# ### MANIM CODE:
from manim import *

class CustomShape(VGroup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        circle = Circle()
        square = Square().shift(RIGHT)
        self.add(circle, square)

class CustomMobjectExample(Scene):
    def construct(self):
        shape = CustomShape()
        self.add(shape)
        self.play(shape.animate.shift(UP))
        self.wait(1)

# ### NARRATION:
We define a custom shape by combining a circle and a square. Then, we animate the entire shape moving upward.


Example 13: Using Updaters
Description: Shows how to use updaters for dynamic behavior.

# ### MANIM CODE:
from manim import *

class UpdaterExample(Scene):
    def construct(self):
        dot = Dot()
        self.add(dot)
        def updater(mob, dt):
            mob.shift(RIGHT * dt)
        dot.add_updater(updater)
        self.wait(2)
        dot.remove_updater(updater)
        self.wait(1)

# ### NARRATION:
Here, we add an updater to a dot, causing it to move to the right over time. After 2 seconds, we remove the updater to stop the movement.


Example 14: Text and MathTex Animation Sync
Description: Animates Text and MathTex objects together.
# ### MANIM CODE:
from manim import *

class TextMathTexExample(Scene):
    def construct(self):
        text = Text("Euler's Identity:")
        formula = MathTex("e^{i\\pi} + 1 = 0")
        group = VGroup(text, formula).arrange(DOWN)
        self.play(Write(group))
        self.wait(2)

# ### NARRATION:
We display Euler's Identity by combining a text label with the corresponding mathematical formula, animating them together.

Example 15: Lagged Start Animations
Description: Demonstrates staggered animations using LaggedStart.

# ### MANIM CODE:
from manim import *

class LaggedStartExample(Scene):
    def construct(self):
        squares = VGroup(*[Square() for _ in range(5)]).arrange(RIGHT)
        self.play(LaggedStart(*[FadeIn(sq) for sq in squares], lag_ratio=0.5))
        self.wait(1)

# ### NARRATION:
We create five squares and fade them in one after another with a delay, creating a cascading effect.

Example 16: SVG and Image Support
Description: Imports and displays an SVG image.

# ### MANIM CODE:
from manim import *

class SVGImageExample(Scene):
    def construct(self):
        svg = SVGMobject("example.svg").scale(2)
        self.play(FadeIn(svg))
        self.wait(2)

# ### NARRATION:
We load an SVG file named "example.svg" and display it in the scene, scaling it up for better visibility.


Example 17: Animated Arrows
Description: Shows how to animate an arrow between two moving dots.

# ### MANIM CODE:
from manim import *

class ArrowAnimation(Scene):
    def construct(self):
        dot1 = Dot(LEFT * 2)
        dot2 = Dot(RIGHT * 2)
        arrow = always_redraw(lambda: Arrow(dot1.get_center(), dot2.get_center()))
        self.add(dot1, dot2, arrow)
        self.play(dot1.animate.shift(RIGHT * 2), dot2.animate.shift(LEFT * 2))
        self.wait(1)

# ### NARRATION:
We have two dots and an arrow pointing from the first to the second. As the dots move, the arrow updates in real-time to stay between them.

Example 18: Graph Plotting
Description: Plots a mathematical function on axes.

# ### MANIM CODE:
from manim import *

class GraphExample(Scene):
    def construct(self):
        ax = Axes(x_range=[-3, 3], y_range=[-1, 9])
        graph = ax.plot(lambda x: x**2, color=BLUE)
        self.play(Create(ax), Create(graph))
        self.wait(1)

# ### NARRATION:
This graph plots the function y = x squared using Axes and plot. The graph is colored blue.

Example 19: Parametric Functions
Description: Draws a circle using a parametric function.

# ### MANIM CODE:
from manim import *

class ParametricCircle(Scene):
    def construct(self):
        ax = Axes()
        circle = ax.plot_parametric_curve(
            lambda t: [np.cos(t), np.sin(t), 0],
            t_range=[0, TAU],
            color=YELLOW
        )
        self.play(Create(ax), Create(circle))
        self.wait(1)

# ### NARRATION:
We use a parametric function to draw a circle. X is cosine of t and Y is sine of t. This forms a smooth circular path.

Example 20: Brace and Label
Description: Adds a brace and label to highlight part of an object.

# ### MANIM CODE:
from manim import *

class BraceExample(Scene):
    def construct(self):
        rect = Rectangle(width=4, height=2)
        brace = Brace(rect, direction=DOWN)
        label = brace.get_text("Width")
        self.add(rect, brace, label)
        self.wait(1)

# ### NARRATION:
A rectangle is shown, and we use a brace below it with a label that says "Width" to show dimension visually.

Example 21: Coordinates and Points
Description: Marks a coordinate point on a grid with a label.

# ### MANIM CODE:
from manim import *

class CoordinateLabel(Scene):
    def construct(self):
        ax = Axes()
        dot = Dot(ax.coords_to_point(2, 3), color=RED)
        label = MathTex("(2,3)").next_to(dot, UR)
        self.play(Create(ax), FadeIn(dot), Write(label))
        self.wait(1)

# ### NARRATION:
We place a red dot at coordinate (2, 3) on a graph and label it with the matching text.


Example 22: Dashed Lines
Description: Adds a dashed line from a point to the axes.

# ### MANIM CODE:
from manim import *

class DashedLineExample(Scene):
    def construct(self):
        ax = Axes()
        point = ax.coords_to_point(2, 3)
        dashed = DashedLine(point, ax.c2p(2, 0))
        self.add(ax, Dot(point), dashed)
        self.wait(1)


# ### NARRATION:
We drop a dashed line from the point (2, 3) straight down to the x-axis, like showing projections in math.


Example 23: Multiple Scenes in a File
Description: Demonstrates how to create multiple scenes in the same script.

# ### MANIM CODE:
from manim import *

class FirstScene(Scene):
    def construct(self):
        self.play(Write(Text("Scene One")))
        self.wait(1)

class SecondScene(Scene):
    def construct(self):
        self.play(Write(Text("Scene Two")))
        self.wait(1)

# ### NARRATION:
This file has two different scenes. Manim will render each separately when called, allowing you to keep related animations together.


Example 24: Transform Between Shapes
Description: Morphs one shape into another.

# ### MANIM CODE:
from manim import *

class ShapeTransform(Scene):
    def construct(self):
        circle = Circle()
        square = Square()
        self.play(Create(circle))
        self.wait(1)
        self.play(Transform(circle, square))
        self.wait(1)

# ### NARRATION:
We create a circle, then morph it into a square using the Transform animation. This makes transitions smooth.
