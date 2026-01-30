#!/bin/bash

echo "Removing GUI OpenCV if present..."
pip uninstall -y opencv-python opencv-contrib-python || true

echo "Installed OpenCV packages:"
pip list | grep opencv || true

echo "Starting app..."
python app.py
