from flask import Flask, render_template, url_for, request, send_file, jsonify
from model import *
from PIL import Image
import io
import base64

app = Flask(__name__, template_folder='website')

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upscale2x', methods=['POST'])
def upscale_image_2x():
    uploaded_file = request.files['file']
    upscaled_image = upscale2x(uploaded_file)
    image_stream = io.BytesIO()
    upscaled_image.save(image_stream, format='JPEG')
    image_binary = image_stream.getvalue()
    upscaled_image = base64.b64encode(image_binary).decode('utf-8')
    return upscaled_image


@app.route('/upscale3x', methods=['POST'])
def upscale_image_3x():  # Переименовано
    uploaded_file = request.files['file']
    upscaled_image = upscale3x(uploaded_file)
    image_stream = io.BytesIO()
    upscaled_image.save(image_stream, format='JPEG')
    image_binary = image_stream.getvalue()
    upscaled_image = base64.b64encode(image_binary).decode('utf-8')
    return upscaled_image

@app.route('/upscale4x', methods=['POST'])
def upscale_image_4x():  # Переименовано
    uploaded_file = request.files['file']
    upscaled_image = upscale4x(uploaded_file)
    image_stream = io.BytesIO()
    upscaled_image.save(image_stream, format='JPEG')
    image_binary = image_stream.getvalue()
    upscaled_image = base64.b64encode(image_binary).decode('utf-8')
    return upscaled_image

@app.route('/remove_noise', methods=['POST'])
def remove_noise():
    uploaded_file = request.files['file']
    denoised_image = median_filter(uploaded_file)
    image_stream = io.BytesIO()
    denoised_image.save(image_stream, format='JPEG')
    image_binary = image_stream.getvalue()
    upscaled_image = base64.b64encode(image_binary).decode('utf-8')
    return upscaled_image

if __name__ == "__main__":
    app.run(debug=True)