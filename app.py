"""
Simple app to upload an image via a web form 
and view the inference results on the image in the browser.
"""
import argparse
import io
import os
import requests
from PIL import Image

import torch
from flask import Flask, render_template, request, redirect, jsonify
from io import BytesIO
from hubconfig import _create

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def webapp():
    if request.method == "POST":
        if "file" not in request.files:
            return redirect(request.url)
        file = request.files["file"]
        if not file:
            return

        img_bytes = file.read()
        img = Image.open(io.BytesIO(img_bytes))
        results = model(img, size=640)

        # for debugging
        # data = results.pandas().xyxy[0].to_json(orient="records")
        # return data

        results.render()  # updates results.imgs with boxes and labels
        for img in results.imgs:
            img_base64 = Image.fromarray(img)
            img_base64.save("static/image0.jpg", format="JPEG")
        return redirect("static/image0.jpg")

    return render_template("index.html")


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
    port = int(os.environ.get("PORT", 5000))
    parser = argparse.ArgumentParser(description="Flask app exposing yolov5 models")
    parser.add_argument("--port", default=port, type=int, help="port number")
    args = parser.parse_args()
    model = _create(name='yolov5s', pretrained=True, channels=3, classes=1, autoshape=True, verbose=True)  # pretrained
    model.eval()
    app.run(host="0.0.0.0", port=args.port)  # debug=True causes Restarting with stat