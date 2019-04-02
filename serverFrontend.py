from flask import Flask
from flask import request
from flask import jsonify
from flask import send_from_directory


app = Flask(__name__)


@app.route('/', defaults=dict(filename=None))
@app.route('/<path:filename>', methods=['GET', 'POST'])
def index(filename):
    filename = filename or 'index.html'
    if request.method == 'GET':
        return send_from_directory('.', filename)

    return jsonify(request.data)


if __name__ == '__main__': 
    app.run(port=8080, debug=True)
    # app.run(debug=True, host='0.0.0.0')