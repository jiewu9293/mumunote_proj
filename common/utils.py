import random
import string
from PIL import Image, ImageFont, ImageDraw
from io import BytesIO

class ImageCode():

    def get_text(self):
        #list = random.sample("123456789asdfghjk",4)
        list = random.sample(string.ascii_letters + string.digits, 4)
        return "".join(list)

    def rand_color(self):
        # rgb的颜色
        red = random.randint(0, 255)
        green = random.randint(0, 255)
        blue = random.randint(0, 255)
        return red, green, blue

    def draw_lines(self, draw, num, width, height):
        for i in range(num):
            x1 = random.randint(0, width)
            y1 = random.randint(0, height)
            x2 = random.randint(0, width)
            y2 = random.randint(height, height)
            draw.line(((x1, y1), (x2, y2)), fill="black", width=2)

    def draw_verify_code(self):
        code = self.get_text()

        width, height = 80, 38
        im = Image.new("RGB", (width, height), "white")
        font = ImageFont.truetype(font="/System/Library/Fonts/Supplemental/Arial.ttf", size=20)
        draw = ImageDraw.Draw(im)

        # 绘制干扰线
        self.draw_lines(draw, 2, width, height)
        for i in range(4):
            draw.text((random.randint(3, 10) + 15 * i, random.randint(3, 10)),
                      text=code[i], fill=self.rand_color(), font=font)

        self.draw_lines(draw,2,width,height)

        return im,code

    def get_code(self):
        image, code = self.draw_verify_code()
        buf = BytesIO()
        image.save(buf, "jpeg")
        image_b_string = buf.getvalue()
        return code, image_b_string



image_code = ImageCode()
image_code.draw_verify_code()