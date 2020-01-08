from PIL import Image, ImageOps
from io import BytesIO
import base64
import json
import numpy

# image_to_base64
def image_to_base64(image: Image) -> str:
    buff = BytesIO()
    image.save(buff, format="png")
    return base64.b64encode(buff.getvalue()).decode('utf-8')

# base64_to_image
def base64_to_image(data: str) -> Image:
    return Image.open(BytesIO(base64.b64decode(data)))
 
# extract_image_data
def extract_image_data(data: dict) -> ([], [], []):
    images_name = []
    images_se = []
    images_bse = []
    # extract images
    for image_name in data["images"]:
        # decode image
        image_se  = base64_to_image(data["images"][image_name]["se"]).convert("L")
        image_bse = base64_to_image(data["images"][image_name]["bse"]).convert("L")
        # append images
        images_name.append(image_name)
        images_se.append(image_se)
        images_bse.append(image_bse)
    # return results
    return images_name, images_se, images_bse

# pack_image_data
def pack_image_data(images_name: [], images: []) -> dict:
    data = { "success": True }
    data["segmentations"] = json.dumps([image_to_base64(image) for image in images])
    data["dimensions"] = json.dumps([[image.height, image.width] for image in images])
    return data

# calculate_segmentation
def calculate_segmentation(images_se: [], images_bse: []) -> []:
    images_seg = []
    # calculations
    for image_se in images_se:
        image_array = numpy.array(image_se)
        image_array_res = numpy.fix(image_array / 64)
        images_seg.append(Image.fromarray(image_array_res).convert('L'))
    # return results
    return images_seg