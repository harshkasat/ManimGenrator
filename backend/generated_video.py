from manim import *
import numpy as np

class GaussianBlurAveraging(Scene):
    def construct(self):
        # Setup Configuration - Ensure this is at the beginning of your construct method!
        config.video_dir = "output/video"
        config.write_to_movie = True
        config.flush_cache = True
        config.disable_caching = True
        config.pixel_width = 1080
        config.pixel_height = 1920
        config.frame_width = 9
        config.frame_height = 16

        # Title
        title = Text("Gaussian Blur as Averaging", font_size=48)
        self.play(Write(title), run_time=2)
        self.wait(1)
        self.play(FadeOut(title), run_time=1)

        # Initial Pixel Grid
        grid_size = 5
        pixels = VGroup(*[
            Rectangle(width=0.5, height=0.5).move_to([x - grid_size/2*0.5, y - grid_size/2*0.5, 0])
            for x in range(grid_size) for y in range(grid_size)
        ])
        pixels.set_stroke(WHITE, width=1)
        self.play(Create(pixels), run_time=2)

        # Simulate Image Data (Example: some random dark pixels)
        dark_pixels = [(0, 0), (2, 2), (4, 4), (1, 3), (3, 1)]
        for x, y in dark_pixels:
            index = x * grid_size + y
            pixels[index].set_fill(BLACK, opacity=1)
        self.wait(1)

        # Explanation of Averaging
        averaging_text = Text("Blurring = Averaging Pixel Values", font_size=36)
        averaging_text.to_edge(UP)
        self.play(Write(averaging_text), run_time=2)

        # Focus on a single pixel
        focus_pixel_index = 12  # Example pixel at center
        focus_pixel = pixels[focus_pixel_index]
        surround_rect = SurroundingRectangle(focus_pixel, color=YELLOW, buff=0.1)
        self.play(Create(surround_rect), run_time=1)
        self.wait(1)

        # Highlight Neighbors
        neighbors_indices = [6, 7, 8, 11, 13, 16, 17, 18]  # Indices of neighbors for grid_size = 5 and focus_pixel_index = 12
        neighbors = VGroup(*[pixels[i] for i in neighbors_indices])
        self.play(Indicate(neighbors, color=GREEN), run_time=2)

        # Averaging Calculation (Simplified)
        calculation_text = MathTex(r"\text{New Value} = \frac{\text{Pixel Value} + \text{Sum of Neighbors}}{\text{Number of Pixels}}", font_size=30)
        calculation_text.to_edge(DOWN)
        self.play(Write(calculation_text), run_time=3)
        self.wait(2)

        # Perform Averaging (visual change)
        original_color = focus_pixel.get_fill_color()
        original_opacity = focus_pixel.get_fill_opacity()

        neighbor_colors = [pixels[i].get_fill_color() for i in neighbors_indices]
        neighbor_opacities = [pixels[i].get_fill_opacity() for i in neighbors_indices]

        #Calculate the new average opacity
        new_opacity = (original_opacity + sum(neighbor_opacities)) / (len(neighbors_indices) + 1)

        self.play(
            focus_pixel.animate.set_fill(color=original_color, opacity=new_opacity), run_time=2
        )
        self.wait(1)

        # Apply Averaging to All Pixels (Simulated Blur)
        self.play(FadeOut(surround_rect, calculation_text, averaging_text), run_time=1)

        for i in range(grid_size * grid_size):
            neighbors_indices_all = []
            x = i // grid_size
            y = i % grid_size
            
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < grid_size and 0 <= ny < grid_size and (dx != 0 or dy != 0):
                        neighbors_indices_all.append(nx * grid_size + ny)
            
            neighbor_colors_all = [pixels[j].get_fill_color() for j in neighbors_indices_all]
            neighbor_opacities_all = [pixels[j].get_fill_opacity() for j in neighbors_indices_all]
            
            new_opacity_all = (pixels[i].get_fill_opacity() + sum(neighbor_opacities_all)) / (len(neighbors_indices_all) + 1)

            self.play(
                pixels[i].animate.set_fill(color=pixels[i].get_fill_color(), opacity=min(new_opacity_all, 1)), run_time=0.1
            )

        self.wait(2)

        # Smoothing Effect
        smoothing_text = Text("Repeated Averaging = Smoothing", font_size=36)
        smoothing_text.to_edge(UP)
        self.play(Write(smoothing_text), run_time=2)
        self.wait(1)

        # Further Blurring (Repeat Averaging)
        for i in range(grid_size * grid_size):
            neighbors_indices_all = []
            x = i // grid_size
            y = i % grid_size
            
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < grid_size and 0 <= ny < grid_size and (dx != 0 or dy != 0):
                        neighbors_indices_all.append(nx * grid_size + ny)
            
            neighbor_colors_all = [pixels[j].get_fill_color() for j in neighbors_indices_all]
            neighbor_opacities_all = [pixels[j].get_fill_opacity() for j in neighbors_indices_all]
            
            new_opacity_all = (pixels[i].get_fill_opacity() + sum(neighbor_opacities_all)) / (len(neighbors_indices_all) + 1)

            self.play(
                pixels[i].animate.set_fill(color=pixels[i].get_fill_color(), opacity=min(new_opacity_all, 1)), run_time=0.1
            )
        self.wait(2)

        # Final Fade Out
        self.play(FadeOut(pixels, smoothing_text), run_time=2)
        self.wait(1)