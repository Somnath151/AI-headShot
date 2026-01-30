import os
import cv2
import numpy as np
from flask import Flask, request, render_template, redirect, url_for
from insightface.app import FaceAnalysis
from insightface.model_zoo import get_model

UPLOAD_FOLDER = "static/uploads"
RESULT_FOLDER = "static/results"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

app = Flask(__name__)

# Face detection
face_app = FaceAnalysis(name="buffalo_l")
face_app.prepare(ctx_id=-1)  # CPU

# Face swap model
swapper = get_model("inswapper_128.onnx", download=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        src_file = request.files["source"]
        tgt_file = request.files["target"]

        src_path = os.path.join(UPLOAD_FOLDER, src_file.filename)
        tgt_path = os.path.join(UPLOAD_FOLDER, tgt_file.filename)

        src_file.save(src_path)
        tgt_file.save(tgt_path)

        src_img = cv2.imread(src_path)
        tgt_img = cv2.imread(tgt_path)

        src_faces = face_app.get(src_img)
        tgt_faces = face_app.get(tgt_img)

        if not src_faces or not tgt_faces:
            return "Face not detected", 400

        result = swapper.get(
            tgt_img,
            tgt_faces[0],
            src_faces[0],
            paste_back=True
        )

        out_path = os.path.join(RESULT_FOLDER, "result.png")
        cv2.imwrite(out_path,result,[cv2.IMWRITE_JPEG_QUALITY, 98] )


        #return redirect(url_for("result"))

    return render_template("index.html", result="result.png")


@app.route("/result")
def result():
    return '<img src="/static/results/result.png" width="400">'

if __name__ == "__main__":
   app.run(host="0.0.0.0", port=8080)

