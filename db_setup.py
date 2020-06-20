from app import app, db
from app.models import User
import json
db.create_all()
"""
with open('config.json', 'r') as config_file:
    db_config = json.load(config_file)

engine = create_engine(db_config['SQLITE_DATABASE']['FILE_NAME'])
Base.metadata.screate_all(engine)
"""