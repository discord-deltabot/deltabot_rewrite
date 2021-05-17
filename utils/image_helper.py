import PIL.Image, PIL.ImageOps
from io import BytesIO
import requests

def get_image_from_url(url):
    coin = requests.get(url).content
    source = BytesIO(coin)
    return PIL.Image.open(source)

def get_inverted_bytes(imagebytes):
    with PIL.Image.open(imagebytes) as img:
        out = PIL.ImageOps.invert(img.convert("RGB"))
    output_buffer = BytesIO()
    out.save(output_buffer, "png")
    output_buffer.seek(0)
    return output_buffer
