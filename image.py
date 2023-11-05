from PIL import Image, ImageDraw

# 打开PNG图像
image = Image.open("img/alpha-wolf.png")

if image.mode != 'RGBA':
    image = image.convert('RGBA')

width, height = image.size
new_image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
draw = ImageDraw.Draw(new_image)
border_width = 1  # 可以根据需要调整边框宽度

# 遍历是否为不透明
for x in range(width):
    for y in range(height):
        r, g, b, a = image.getpixel((x, y))
        if a == 255:
            # 这个像素是非透明的，绘制边框
            draw.rectangle([x - border_width, y - border_width, x + border_width, y + border_width], outline=(255, 255, 255, 255))

# 合并原图像和带有边框的新图像
# result_image = Image.alpha_composite(image, new_image)
result_image = new_image.paste(image, (0,0), image)

new_image.save("img/alpha-wolf_selected.png")

image.close()
new_image.close()
