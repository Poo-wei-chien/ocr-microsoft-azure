from flask import Flask, request, jsonify, render_template
from flask_swagger_ui import get_swaggerui_blueprint
from analyze import read_image

app = Flask(__name__, template_folder='templates')

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.yaml'  # Changed to point to static folder
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Image Analysis API"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/static/swagger.yaml")  # Changed route to match API_URL
def swagger_yaml():
    return app.send_static_file('swagger.yaml')

@app.route("/api/v1/analysis/", methods=['POST'])
def analysis():
    try:
        get_json = request.get_json()
        image_uri = get_json['uri']
    except:
        return jsonify({'error': 'Missing URI in JSON'}), 400

    try:
        res = read_image(image_uri)
        response_data = {
            "text": res
        }
        return jsonify(response_data), 200
    except:
        return jsonify({'error': 'Error in processing'}), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)