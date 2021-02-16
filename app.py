import os
from dotenv import load_dotenv
from fill_db import UpdateDb
from create_app import create_app

load_dotenv('.env')

app = create_app('development')


@app.before_first_request
def update_db():
    if os.getenv('FILL_DB') == 'True':
        update = UpdateDb()
        update.recreate_db()


if __name__ == "__main__":
    app.run()
