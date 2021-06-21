from map import fit_image
from utils.image import new_image_crop, image_resize
from PIL import Image
import connexion, flask, os, glob
from datetime import datetime
from math import ceil
from connexion import request

# DB
from config import IMAGE_SIZE, basedir, db, RESIZE_FACTOR
from models.resource import ResourceSchema, Resource, ResourceSchema, Reason

storage_path = os.path.join(basedir, "storage")

def resource_result():
    return (
        Resource.query.order_by(Resource.resource_id)
        .filter(Resource.x != None)
        .filter(Resource.y != None)
        .filter(Resource.z != None)
    )

def get_all():
    result = resource_result().all()
    return ResourceSchema(many=True).dump(result), 200

def get_limited():
    count = len(list(glob.glob(f"{storage_path}/*")))
    limit = round(count / 10)
    result = (
        Resource.query.order_by(Resource.updated_at.asc())
        .filter(Resource.x != None)
        .filter(Resource.y != None)
        .filter(Resource.z != None)
        .filter(Resource.size > 1)
        .limit(limit)
        .all()
    )
    return {
        "resources": ResourceSchema(many=True).dump(result),
        "choose": ceil(count / 200),
        "limit": limit,
        "total": count,
    }, 200


def get_resource(resource_id):
    result = Resource.query.get_or_404(resource_id)
    return ResourceSchema().dump(result), 200


def create_resource(name, reason, lastModified):
    file = connexion.request.files["file"]
    filename = file.filename.split(".")
    extension = filename.pop() # remove extension
    filename = "".join(filename) + ".jpg"

    resource_path = os.path.join(storage_path, file.filename)

    file.save(resource_path)
    image = new_image_crop(Image.open(resource_path))
    save_path = os.path.join(storage_path, filename)
    image.convert("RGB").save(save_path)
    os.unlink(resource_path)
    # jpg = Image.new("RGB", image.size, (255,255,255))
    # jpg.paste(image.convert('RGB'))
    # jpg.save(save_path, quality=95)

    [x, y, z] = fit_image(save_path)
    resource = Resource(
        author=name,
        extension=extension,
        filename=filename,
        name=file.filename,
        reason=[Reason(content=reason, timestamp=datetime.now())],
        original_size=1024,
        size=1024,
        uri="/files/" + filename,
        created_at=datetime.now(),
        last_modified=datetime.now(),
        updated_at=datetime.now(),
        x=x,
        y=y,
        z=z,
    )
    db.session.add(resource)
    db.session.commit()

    return ResourceSchema().dump(resource), 200

def update_resource(resource_id):
    resource = Resource.query.get_or_404(resource_id)
    storage_path = os.path.join(basedir, "storage")
    resource_path = os.path.join(storage_path, resource.filename)
    reason = request.get_json()["reason"]
    
    if not os.path.exists(resource_path):
        return {}, 404
    if not reason:
        return {}, 412
    if resource.size > 1:
        resize = int(resource.size / RESIZE_FACTOR)

        file = Image.open(resource_path)
        # Forces repaint
        if resource.size == IMAGE_SIZE:
            filename = resource.filename.replace(".jpg", f"_{resize}.jpg")
        else:
            filename = resource.filename.replace(f"{resource.size}.jpg", f"_{resize}.jpg")

        save_path = os.path.join(storage_path, filename)

        image = image_resize(file, resize) # Resize the image
        image.save(save_path)
        
        from shutil import copyfile
        copyfile(resource_path, os.path.join(basedir, f"backup/{resource.filename}"))

        resource.reason.append(Reason(content=reason,timestamp=datetime.now()))
        resource.uri = "/files/" + filename
        resource.size = resize
        resource.updated_at = datetime.now()

        db.session.merge(resource)
        db.session.commit()

        os.unlink(resource_path)
        return ResourceSchema().dump(resource), 200
    else:
        return {}, 401


def get_file(filename):
    return flask.send_from_directory("storage", filename), 200

def get_center():
    import numpy as np
    result = resource_result().all()
    resources = []
    for resource in result:
        resources.append([resource.x, resource.y, resource.z])
    points = np.array(resources)
    return { "center": points.mean(axis=0).astype(int).tolist() }, 200
