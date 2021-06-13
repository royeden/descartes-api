import os
from datetime import datetime
from config import DB_PATH, db
from models.resource import Resource 

# Delete database file if it exists currently
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

# Create the database
db.create_all()

from glob import glob
# Iterate over the PEOPLE structure and populate the database
for i, filepath in enumerate(glob('storage/*')):
    resource = Resource(
        author="Anonimx",
        name=filepath.split("/")[1],
        reason="test",
        size=512,
        uri="/files/" + filepath.split("/")[1],
        last_modified=datetime.now(),
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    db.session.add(resource)

db.session.commit()