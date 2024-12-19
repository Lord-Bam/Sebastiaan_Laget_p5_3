from app_factory import create_app
from model import Model
import configparser

app = create_app()

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("config.ini")
    model = Model(config)
    # Attach the model to the app instance
    app.model = model
    app.run(debug=True)