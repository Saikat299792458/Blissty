from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np

app = Flask(__name__)

def process_image(image_path):
    # Load the image
    img = cv2.imread(image_path)

    # Check if the image has an alpha channel
    if img.shape[2] == 3:
        # Image doesn't have an alpha channel, set transparency to N/A or any desired value
        transparency = 'N/A'
    else:
        # Extract Transparency values
        transparency = np.mean(img[:, :, 3])

    # Extract RGBA values
    rgba_values = {
        '1.Red': np.mean(img[:, :, 2]),
        '2.Green': np.mean(img[:, :, 1]),
        '3.Blue': np.mean(img[:, :, 0]),
        '4.Alpha': transparency,
        '5.Intensity': np.mean(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))
    }

    return rgba_values


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_image', methods=['POST'])
def process_image_route():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'})

    image = request.files['image']
    image_path = 'static/uploads/uploaded_image.png'
    image.save(image_path)

    rgba_values = process_image(image_path)

    return jsonify(rgba_values)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
