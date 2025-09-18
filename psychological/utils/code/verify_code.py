import random
import string
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
from io import BytesIO


class VerifyCodeGenerator:
    def __init__(self, width=120, height=40, char_count=4, font_size=28, spacing=8):
        self.width = width
        self.height = height
        self.char_count = char_count
        self.font_size = font_size
        self.spacing = spacing
        try:
            if os.name == 'nt':
                self.font = ImageFont.truetype('arial.ttf', self.font_size)
            else:
                self.font = ImageFont.truetype(
                    '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', self.font_size)
        except (OSError, IOError):
            self.font = ImageFont.load_default()

    def random_code(self):
        return ''.join(random.choices(string.digits + string.ascii_uppercase, k=self.char_count))

    def create_image(self, code: str):
        image = Image.new('RGB', (self.width, self.height),
                          self._get_random_background_color())
        draw = ImageDraw.Draw(image)

        self._draw_background_pattern(draw)
        self._draw_disturbance_elements(draw)
        self._draw_disturbance_lines(draw)
        self._draw_code_characters(draw, code)

        image = self._apply_image_effects(image)
        return image

    def _get_random_background_color(self):
        return (random.randint(240, 250), random.randint(240, 250), random.randint(240, 250))

    def _draw_background_pattern(self, draw):
        for _ in range(100):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            draw.point((x, y), fill=self._get_random_light_color())

    def _draw_disturbance_elements(self, draw):
        for _ in range(30):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            size = random.randint(1, 2)
            draw.ellipse([x - size, y - size, x + size, y + size],
                         fill=self._get_random_light_color())

    def _draw_disturbance_lines(self, draw):
        for _ in range(4):
            start_x = random.randint(0, self.width // 4)
            start_y = random.randint(0, self.height)
            end_x = start_x + random.randint(self.width // 2, self.width)
            end_y = random.randint(0, self.height)
            draw.line([(start_x, start_y), (end_x, end_y)],
                      fill=self._get_random_light_color(), width=1)

        for _ in range(3):
            control_points = [
                (random.randint(0, self.width // 3),
                 random.randint(0, self.height)),
                (random.randint(self.width // 3, 2 * self.width // 3),
                 random.randint(0, self.height)),
                (random.randint(2 * self.width // 3, self.width),
                 random.randint(0, self.height))
            ]
            for i in range(len(control_points) - 1):
                draw.line([control_points[i], control_points[i + 1]],
                          fill=self._get_random_light_color(), width=1)

    def _draw_code_characters(self, draw, code):
        total_chars_width = sum(
            draw.textbbox((0, 0), char, font=self.font)[
                2] - draw.textbbox((0, 0), char, font=self.font)[0]
            for char in code
        ) + self.spacing * (len(code) - 1)
        start_x = max(0, (self.width - total_chars_width) // 2)

        for i, char in enumerate(code):
            char_bbox = draw.textbbox((0, 0), char, font=self.font)
            char_width = char_bbox[2] - char_bbox[0]
            x = start_x + sum(
                draw.textbbox((0, 0), c, font=self.font)[
                    2] - draw.textbbox((0, 0), c, font=self.font)[0] + self.spacing
                for c in code[:i]
            )
            y = (self.height - self.font_size) // 2 + random.randint(-5, 5)

            char_color = self._get_random_dark_color()
            shadow_color = tuple(max(0, c - 30) for c in char_color)

            draw.text((x + 1, y + 1), char, font=self.font, fill=shadow_color)
            draw.text((x, y), char, font=self.font, fill=char_color)

    def _get_random_light_color(self):
        return (
            random.randint(180, 220),
            random.randint(180, 220),
            random.randint(180, 220)
        )

    def _get_random_dark_color(self):
        return (
            random.randint(30, 120),
            random.randint(30, 120),
            random.randint(30, 120)
        )

    def _apply_image_effects(self, image):
        if random.random() > 0.5:
            image = image.filter(ImageFilter.GaussianBlur(radius=0.5))
        if random.random() > 0.7:
            image = image.filter(ImageFilter.SMOOTH)
        return image

    def generate(self):
        code = self.random_code()
        image = self.create_image(code)
        buf = BytesIO()
        image.save(buf, 'PNG')
        buf.seek(0)
        return code, buf
