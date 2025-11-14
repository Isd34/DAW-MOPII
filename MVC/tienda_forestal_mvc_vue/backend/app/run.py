from flask import Flask
from flask_cors import CORS
from controllers.producto_controller import producto_blueprint

app = Flask(__name__)
CORS(app)  # Habilita CORS para comunicación con Vue.js

app.register_blueprint(producto_blueprint, url_prefix='/api')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

