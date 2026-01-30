import os
from PIL import Image
import numpy as np
from flask import Flask, request, render_template, redirect, url_for
from insightface.app import FaceAnalysis
from insightface.model_zoo import get_model

UPLOAD_FOLDER = "static/uploads"
RESULT_FOLDER = "static/results"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

app = Flask(__name__)


def load_image_bgr(path):
    img = Image.open(path).convert("RGB")
    arr = np.array(img)
    return arr[:, :, ::-1]  # RGB → BGR

def save_image_bgr(arr, path):
    rgb = arr[:, :, ::-1]  # BGR → RGB
    Image.fromarray(rgb).save(path)

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

        src_img = load_image_bgr(src_path)
        tgt_img = load_image_bgr(tgt_path)


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
        save_image_bgr(result, out_path)


        #return redirect(url_for("result"))

    return render_template("index.html", result="result.png")


@app.route("/result")
def result():
    return '<img src="/static/results/result.png" width="400">'

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

