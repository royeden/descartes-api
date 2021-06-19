import os
from datetime import datetime, time
from config import DB_PATH, db
from models.resource import Resource, Reason 

# Delete database file if it exists currently
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

# Create the database
db.create_all()

from glob import glob
# Iterate over the PEOPLE structure and populate the database
for i, filepath in enumerate(glob('storage/*')):
    file = filepath.split("/").pop()
    file_split = file.split(".")
    extension = file_split.pop()
    name = "".join(file_split)
    filename = f"{name}_512.{extension}"
    os.rename(filepath, filepath.replace(file, filename))
    resource = Resource(
        author="Anonimx",
        extension=extension,
        filename=filename,
        name=name,
        reason=[Reason(content="Test", timestamp=datetime.now())],
        original_size=512,
        size=512,
        uri="/files/" + filename,
        created_at=datetime.now(),
        last_modified=datetime.now(),
        updated_at=datetime.now(),
    )
    db.session.add(resource)

db.session.commit()