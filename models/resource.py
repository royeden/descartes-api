# TODO move to API
# from datetime import datetime
from config import db, ma

class Resource(db.Model):
	__tablename__ = 'resource'
	resource_id = db.Column(db.Integer, primary_key=True)
	author = db.Column(db.String(80), nullable=True)
	name = db.Column(db.String(127), nullable=False)
	reason = db.Column(db.String(512), nullable=False)
	size = db.Column(db.Integer, nullable=False)
	uri = db.Column(db.String(256), nullable=False)
	last_modified = db.Column(db.DateTime, nullable=False)
	created_at = db.Column(db.DateTime, nullable=False)
	updated_at = db.Column(db.DateTime, nullable=False)
	
	x = db.Column(db.Integer, nullable=True)
	y = db.Column(db.Integer, nullable=True)
	z = db.Column(db.Integer, nullable=True)

class ResourceSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Resource
        sqla_session = db.session    