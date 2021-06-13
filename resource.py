from utils.image import image_resize
from PIL import Image
import connexion, flask, os
from config import db
from datetime import datetime

APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top

print
# DB
from models.resource import Resource, ResourceSchema


def get_all():
    result = Resource.query.order_by(Resource.name).all()
    return ResourceSchema(many=True).dump(result), 200


def get_resource(resource_id):
    result = Resource.query.get_or_404(resource_id)
    return ResourceSchema().dump(result), 200


def create_resource():
    file = connexion.request.files['file']
    print(file)
    return {}, 200

# TODO clean this ugly flow
def update_resource(resource_id):
    resource = Resource.query.get_or_404(resource_id)
    path = os.path.join(APP_ROOT, "storage/" + resource.name)
    if (not os.path.exists(path)):
        return {}, 404
    if (resource.size > 1):
        file = Image.open(path)
        resize = int(int(resource.size) / 2)
        image = image_resize(file, resize) # Resize the image
        image.save(path)
        resource.size = resize
        resource.updated_at = datetime.now()
        db.session.merge(resource)
        db.session.commit()
        return ResourceSchema().dump(resource), 200
    else:
        return {}, 401


def get_file(filename):
    return flask.send_from_directory("storage", filename), 200
