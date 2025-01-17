from init_app import create_app
from setup_db import setup_database

app = create_app()

if __name__ == "__main__":
    setup_database()
    app.run(host="0.0.0.0", port=5001)
