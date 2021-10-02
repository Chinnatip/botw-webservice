"""
Run a rest API exposing the yolov5s object detection model
"""
import argparse
import io
import torch
import requests
from PIL import Image
from hubconfig import _create
from flask import Flask, request, jsonify
from io import BytesIO

app = Flask(__name__)

DETECTION_URL = "/v1/object-detection/yolov5s"

@app.route(DETECTION_URL, methods=["POST"])
def predict():
    if not request.method == "POST":
        return

    data = request.json

    if data["url"]:
        image_url = data["url"]
        # image_bytes = image_file.read()
        # img = Image.open(io.BytesIO(image_bytes))
        # image_url = 'https://www.carrentpk.com/img/slider-bg1.png'
        response = requests.get(image_url)
        img = Image.open(BytesIO(response.content))

        results = model(img, size=640)
        data = results.pandas().xyxy[0].to_json(orient="records")
        return data


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flask api exposing yolov5 model")
    parser.add_argument("--port", default=5000, type=int, help="port number")
    args = parser.parse_args()
    model = _create(name='yolov5s', pretrained=True, channels=3, classes=1, autoshape=True, verbose=True)  # pretrained
    model.eval()
    app.run(host="0.0.0.0", port=args.port)  # debug=True causes Restarting with stat
