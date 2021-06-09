# DB
from models.resource import Resource, ResourceSchema

def get_all():
    result = Resource.query.order_by(Resource.name).all()
    return ResourceSchema(many=True).dump(result), 200

def get_resource(resource_id):
    result = Resource.query.get_or_404(resource_id)
    return ResourceSchema().dump(result), 200
