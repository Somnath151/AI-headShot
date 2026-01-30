#!/bin/bash
set -e

echo ">>> START.SH EXECUTED <<<"

echo "Python being used:"
which python
python --version

echo "Pip being used:"
python -m pip --version

echo "Removing GUI OpenCV if present..."
python -m pip uninstall -y opencv-python opencv-contrib-python || true

echo "Installing headless OpenCV..."
python -m pip install --no-cache-dir opencv-python-headless==4.8.1.78

echo "Installed OpenCV packages:"
python -m pip list | grep opencv || true

echo "Testing cv2 import:"
python - <<EOF
import cv2
print("cv2 version:", cv2.__version__)
EOF

echo "Starting app..."
python app.py
