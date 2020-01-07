from PIL import Image
from io import BytesIO
import requests
import base64
import json
import os

# test image files SE
image_files_se = [
    "./images/se/2_OUTCROP-1P00_S01.tif",
    "./images/se/2_OUTCROP-1P00_S02.tif"
]
# test image files BSE
image_files_bse = [
    "./images/bse/2_OUTCROP-1P00_B01.tif",
    "./images/bse/2_OUTCROP-1P00_B02.tif"
]

# request url
REQUEST_URL = "http://localhost:30002/seg2d"
# request header
REQUEST_HEADER = { "Content-Type": "application/json" }

# image_to_base64
def image_to_base64(image: Image) -> str:
    buff = BytesIO()
    image.save(buff, format="png")
    return base64.b64encode(buff.getvalue()).decode('utf-8')

# base64_to_image
def base64_to_image(data: str) -> Image:
    return Image.open(BytesIO(base64.b64decode(data)))

# main
if __name__ == "__main__":
    # load images to lists
    images_se  = [Image.open(file_name).convert("L") for file_name in image_files_se]
    images_bse = [Image.open(file_name).convert("L") for file_name in image_files_bse]
    # convert images to base64
    base64s_se  = [image_to_base64(image) for image in images_se]
    base64s_bse = [image_to_base64(image) for image in images_bse]
    # create request data
    request_data = { "images": {} }
    for file_path, base64_se, base64_bse in zip(image_files_se, base64s_se, base64s_bse):
        file_name, file_ext = os.path.splitext(os.path.basename(file_path))
        request_data["images"][file_name] = { "se": base64_se, "bse": base64_bse }
    # send request and get response
    response = requests.post(
        url = REQUEST_URL,
        data = json.dumps(request_data),
        headers = REQUEST_HEADER
    )
    # get response
    response_data = response.json()
    # get images segmentation
    images_seg = []
    images_seg_name = []
    for image_name in response_data["images"]:
        image_seg = base64_to_image(response_data["images"][image_name]["seg"])
        images_seg.append(image_seg)
        images_seg_name.append(image_name)
    # save images
    for image_name, image_seg in zip(images_seg_name, images_seg):
        image_seg.save("./images/seg/{}_seg.tif".format(image_name))