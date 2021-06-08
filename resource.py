# Imports
# from http import HTTPStatus
# from flask import Blueprint, request, abort
# from flasgger import swag_from

# Exceptions
# from werkzeug.exceptions import BadRequest

# Utils
# from api.utils.file_exists import file_exists

# DB
from models.resource import Resource, ResourceSchema

# resource_api = Blueprint('api', __name__)

# @resource_api.route('/all', methods=['GET'])
# @swag_from({
#     'responses': {
#         HTTPStatus.OK.value: {
#             'description': 'Updates a resource in the database',
#             'schema': ResourceSchema
#         }
#     }
# })
def get_all():
    result = Resource.query.order_by(Resource.name).all()
    return ResourceSchema(many=True).dump(result), 200


# @resource_api.route('/<int:resource_id>', methods=['GET'])
# @swag_from({
#     'responses': {
#         HTTPStatus.OK.value: {
#             'description': 'Updates a resource in the database',
#             'schema': ResourceSchema
#         }
#     }
# })
# def get():
#     """

#     """
#     result = Resource()
#     return ResourceSchema().dump(result), 200


# @resource_api.route('/', methods=['POST'])
# @swag_from({
#     'responses': {
#         HTTPStatus.OK.value: {
#             'description': 'Creates a new resource in the database',
#             'schema': ResourceSchema
#         },
#         HTTPStatus.BadRequest: "Error in validation"
#     }
# })
# def create():
#     """

#     """
#     try:
#         errors = ResourceSchema().validate(request.form)
#         if errors:
#             abort(BadRequest, str(errors))
#         if file_exists():
#             abort(FileExistsError, "Uploaded file already exists")

#         resource = Resource()
#         return ResourceSchema().dump(resource), 200
#     except Exception as error:
#         return error, 404

# @resource_api.route('/<int:resource_id>', methods=['PUT'])
# @swag_from({
#     'responses': {
#         HTTPStatus.OK.value: {
#             'description': 'Updates a resource in the database',
#             'schema': ResourceSchema
#         }
#     }
# })
# def update():
#     """

#     """
#     result = ResourceModel()
#     return ResourceSchema().dump(result), 200
