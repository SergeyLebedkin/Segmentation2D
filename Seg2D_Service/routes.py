from flask import Blueprint, request, jsonify
from utils import *

# create web server
web_server = Blueprint("web_server", __name__)

# sermentation 2d server
@web_server.route("/seg2d", methods=["POST"])
def seg2d():
    # get request data
    request_data = request.get_json()
    # extract image data
    images_name, images_se, images_bse = extract_image_data(request_data)
    # create image segmentations
    images_seg = calculate_segmentation(images_se, images_bse)
    # create response_data
    response_data = pack_image_data(images_name, images_seg)
    # send results
    return jsonify(response_data)