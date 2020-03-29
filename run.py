from flask import Flask
from app.main.controllers import main
from config import Config

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')

app.config.from_object(Config)
app.register_blueprint(main, url_prefix='/')

if __name__ == '__main__':
    app.run()
