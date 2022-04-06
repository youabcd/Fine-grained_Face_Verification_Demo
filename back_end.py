from flask import Flask, request, jsonify
import numpy as np
import base64
import cv2
from inference import inference

app = Flask(__name__)
save_image = "./images/"


@app.route('/original_image', methods=['POST'])
def original_image():
    img = request.files.get("img")
    print("img: ", img)
    # img.save(save_image + img.filename)
    return jsonify({
        'status': 'success'
    })


@app.route('/cropped_image', methods=['POST'])
def cropped_image():
    img1 = request.form.get("img1")
    img1 = img1.split(',')[1]
    image1 = base64.b64decode(img1)
    image1 = np.frombuffer(image1, np.uint8)
    image1 = cv2.imdecode(image1, cv2.IMREAD_GRAYSCALE)
    image1 = cv2.resize(image1, (64, 64))
    print("image1 shape", image1.shape)
    img2 = request.form.get("img2")
    img2 = img2.split(',')[1]
    image2 = base64.b64decode(img2)
    image2 = np.frombuffer(image2, np.uint8)
    image2 = cv2.imdecode(image2, cv2.IMREAD_GRAYSCALE)
    image2 = cv2.resize(image2, (64, 64))
    print("image2 shape", image2.shape)
    res, cs = inference(image1, image2, 'config/parameter_200_100.npz', 'config/feature.npz')
    return jsonify({
        'status': 'success',
        'result': res,
        'cs': cs,
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
