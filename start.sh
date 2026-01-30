#!/bin/bash
set -e

echo ">>> START.SH EXECUTED <<<"

echo "Removing GUI OpenCV if present..."
pip uninstall -y opencv-python opencv-contrib-python || true

echo "Reinstalling headless OpenCV..."
pip install --no-cache-dir opencv-python-headless==4.8.1.78

echo "Installed OpenCV packages:"
pip list | grep opencv || true

echo "Starting app..."
python app.py
