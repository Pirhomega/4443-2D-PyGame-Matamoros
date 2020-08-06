from PIL import Image

for i in range(1,17):
    image = Image.open(str(i)+'.png').convert("RGBA")
    image = image.crop(box=(5, 0, 64, 64))
    image.save(str(i)+'.png', quality=95)