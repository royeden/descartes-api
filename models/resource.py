# from datetime import datetime
from config import db, ma
from marshmallow_sqlalchemy.fields import Nested

from datetime import datetime
class Resource(db.Model):
	__tablename__ = "resource"
	resource_id = db.Column(db.Integer, primary_key=True)

	author = db.Column(db.String(80), nullable=True)
	extension = db.Column(db.String(127), nullable=False)
	filename = db.Column(db.String(255), nullable=False)
	name = db.Column(db.String(127), nullable=False)
	reason = db.relationship(
		"Reason",
		backref="resource",
		cascade="all, delete, delete-orphan",
		single_parent=True,
		order_by="desc(Reason.timestamp)",
	)
	original_size = db.Column(db.Integer, nullable=False)
	size = db.Column(db.Integer, nullable=False)
	uri = db.Column(db.String(255), nullable=False)

	created_at = db.Column(db.DateTime, nullable=False)
	last_modified = db.Column(db.DateTime, nullable=False)
	updated_at = db.Column(db.DateTime, nullable=False)

	x = db.Column(db.Integer, nullable=True)
	y = db.Column(db.Integer, nullable=True)
	z = db.Column(db.Integer, nullable=True)

class Reason(db.Model):
	__tablename__ = 'reason'
	reason_id = db.Column(db.Integer, primary_key=True)
	resource_id = db.Column(db.Integer, db.ForeignKey('resource.resource_id'))
	content = db.Column(db.String, nullable=False)
	timestamp = db.Column(
		db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
	)
class ReasonSchema(ma.SQLAlchemyAutoSchema):
	class Meta:
		model = Reason
		sqla_session = db.session
class ResourceSchema(ma.SQLAlchemyAutoSchema):
	class Meta:
		model = Resource
		sqla_session = db.session
	reason=Nested(ReasonSchema, many=True)

