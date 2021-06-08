import os
from datetime import datetime
from config import DB_PATH, db
from models.resource import Resource 

# Delete database file if it exists currently
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

# Create the database
db.create_all()

# Iterate over the PEOPLE structure and populate the database
resource = Resource(
    author="Anonimx",
    name="test.png",
    reason="test",
    size=1024,
    uri="storage/test.png",
    last_modified=datetime.now(),
    created_at=datetime.now(),
    updated_at=datetime.now(),
)
db.session.add(resource)

db.session.commit()