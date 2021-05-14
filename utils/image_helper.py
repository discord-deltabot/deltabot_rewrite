import PIL.Image, PIL.ImageOps
from io import BytesIO


def get_inverted_bytes(imagebytes):
    print("function reached")
    with PIL.Image.open(imagebytes) as img:
        out = PIL.ImageOps.invert(img.convert("RGB"))
    output_buffer = BytesIO()
    out.save(output_buffer, "png")
    output_buffer.seek(0)
    return output_buffer
