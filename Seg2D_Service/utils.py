from PIL import Image, ImageOps
from io import BytesIO
import base64

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
        image_se  = base64_to_image(data["images"][image_name]["se"])
        image_bse = base64_to_image(data["images"][image_name]["bse"])
        # append images
        images_name.append(image_name)
        images_se.append(image_se)
        images_bse.append(image_bse)
    # return results
    return images_name, images_se, images_bse

# pack_image_data
def pack_image_data(images_name: [], images: []) -> dict:
    data = { "images": {} }
    # pack data
    for image_name, image in zip(images_name, images):
        data["images"][image_name] = { "seg": image_to_base64(image) }
    # return results
    return data

# calculate_segmentation
def calculate_segmentation(images_se: [], images_bse: []) -> []:
    images_seg = []
    # calculations
    for image_se in images_se:
        images_seg.append(ImageOps.invert(image_se))
    # return results
    return images_seg