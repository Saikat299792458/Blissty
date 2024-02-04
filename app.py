# Cetrion 2023

from flask import Flask, render_template, request, jsonify
from datetime import datetime
from functions import functions

app = Flask(__name__)
inst = functions()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_image', methods=['POST'])
def process_image_route():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'})

    if 'modelName' not in request.form:
        return jsonify({'error': 'No model name provided'})
    
    if 'opticalCondition' not in request.form:
        return jsonify({'error': 'No optical condition provided'})

    image = request.files['image']
    model_name = request.form['modelName']
    optical_condition = request.form['opticalCondition']

    # Generate timestamps
    time = datetime.now()
    filename = time.strftime('%Y%m%d%H%M%S') + '.png'
    timestamp = time.strftime('%Y/%m/%d %I:%M:%S %p')

    # Save the uploaded image
    image.save(inst.path + filename)

    rgba_values = inst.process_image(filename)

    # Log the processed data with the provided model name
    inst.update_excel_file(timestamp, model_name, optical_condition, filename)

    return jsonify(rgba_values)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
