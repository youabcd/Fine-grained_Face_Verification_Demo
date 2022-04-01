from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/', methods=['POST'])
def ping_pong():
    # data = request.get_data()
    # img1 = request.form.get("img1")
    img1 = request.files.get("img1")
    # img2 = request.form.get("img2")
    print("img1: ", img1)
    # print("img2: ", img2)
    return jsonify({
        'status': 'success'
    })


if __name__ == '__main__':
    app.run(port=8000, debug=True)
