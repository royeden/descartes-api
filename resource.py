# DB
from models.resource import Resource, ResourceSchema


def get_all():
    result = Resource.query.order_by(Resource.name).all()
    return ResourceSchema(many=True).dump(result), 200


def get_resource(resource_id):
    result = Resource.query.get_or_404(resource_id)
    return ResourceSchema().dump(result), 200


def create_resource(file):
    print(file)
    return {}, 200


def get_file(filename):
    import flask
    return flask.send_from_directory("storage", filename), 200


def resize_file(filename):
    import flask
    file = flask.send_from_directory("storage", filename)
    return {}, 200