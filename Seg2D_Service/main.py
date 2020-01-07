from flask import Flask
from waitress import serve
from routes import web_server

# main
if __name__ == "__main__":
    # create flask app
    app = Flask(__name__)
    app.register_blueprint(web_server)
    # create and run server
    serve(app, host = "0.0.0.0", port = 30002)