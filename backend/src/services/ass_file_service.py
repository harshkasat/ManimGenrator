import pysrt
import re
import colorsys
from datetime import timedelta


class SRTTOASSConverter:
    def __init__(self, input_file, output_file, wave_speed=2.0):
        self.input_file = input_file
        self.output_file = output_file
        self.wave_speed = wave_speed

    def srt_to_ass_timestamp(self, srt_time):
        """Convert SRT timestamp to ASS timestamp format."""
        total_seconds = srt_time.hours * 3600 + srt_time.minutes * 60 + srt_time.seconds
        centiseconds = srt_time.milliseconds // 10
        return f"{srt_time.hours}:{srt_time.minutes:02d}:{srt_time.seconds:02d}.{centiseconds:02d}"

    def generate_color_wave(self, duration_seconds, speed=1.0, color_count=10):
        """Generate a list of colors for a wave-like gradient effect."""
        colors = []
        for i in range(color_count):
            # Generate HSV color with constant saturation and value, but varying hue
            hue = (i / color_count * 360 + speed * duration_seconds) % 360 / 360
            r, g, b = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
            # Convert to BGRhex format for ASS (ASS uses BGR color format)
            hex_color = f"{int(b * 255):02x}{int(g * 255):02x}{int(r * 255):02x}"
            colors.append(hex_color)
        return colors

    def create_ass_header(
        self,
    ):
        """ASS header with Gibson font for 9:16 vertical videos."""
        header = """[Script Info]
    ScriptType: v4.00+
    PlayResX: 1080
    PlayResY: 1920
    ScaledBorderAndShadow: yes

    [V4+ Styles]
    Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
    Style: Default,Gibson,60,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,2,3,2,50,50,120,1  # Gibson font, bottom-aligned
    Style: TopTitle,Gibson,72,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,3,3,8,50,50,100,1  # Gibson for titles (top)

    [Events]
    Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
    """
        return header

    def create_color_tags(self, text, colors):
        """Create ASS color tags for the text."""
        if not colors:
            return text

        chars = list(text)
        result = []
        color_index = 0

        for char in chars:
            if char.strip():  # Only add color to non-whitespace characters
                color = colors[color_index % len(colors)]
                result.append(f"\\c&H{color}&{char}")
                color_index += 1
            else:
                result.append(char)

        return "".join(result)

    def srt_to_ass_with_colors(self):
        """Convert SRT file to ASS with color-changing effects."""
        # Load the SRT file
        subs = pysrt.open(self.input_file)

        # Create ASS file
        with open(self.output_file, "w", encoding="utf-8") as f:
            f.write(self.create_ass_header())

            for i, sub in enumerate(subs):
                # Calculate duration in seconds
                duration = sub.duration.seconds + sub.duration.milliseconds / 1000

                # Generate colors for this subtitle
                colors = self.generate_color_wave(duration, self.wave_speed)

                # Format text with color tags
                text = sub.text.replace("\n", "\\N")  # ASS newline format
                text = re.sub(r"<[^>]*>", "", text)  # Remove existing HTML tags

                # Important: Add braces for ASS formatting - this was missing and might be part of the issue
                colored_text = self.create_color_tags(text, colors)

                # Format the ASS line
                start_time = self.srt_to_ass_timestamp(sub.start)
                end_time = self.srt_to_ass_timestamp(sub.end)

                # Make sure we have proper opening and closing braces for ASS formatting
                ass_line = f"Dialogue: 0,{start_time},{end_time},Default,,0,0,0,,{{{colored_text}}}, {text}\n"
                f.write(ass_line)

    def generate_ass_file(self):
        self.srt_to_ass_with_colors()


# if __name__ == "__main__":
#     response = SRTTOASSConverter(
#         input_file="output/subtitles/subtitles.srt",
#         output_file="output/subtitles/subtitles.ass",
#     )
#     response.generate_ass_file()
