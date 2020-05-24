import os

from flask_migrate import Migrate

from app import create_app, db

app = create_app(os.getenv('FLASK_ENV', default='default'))
migrate = Migrate(app, db)

if __name__ == "__main__":
    app.run()
