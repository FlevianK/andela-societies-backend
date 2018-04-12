"""Validation schemas."""
from datetime import date
from marshmallow import (Schema, fields, post_load, validates,
                         validate, ValidationError)
from api.models import User, Activity, ActivityType


class BaseSchema(Schema):
    """Creates a base validation schema."""

    uuid = fields.String(dump_only=True, validate=[
        validate.Length(max=36)])
    name = fields.String(
        required=True,
        error_messages={
            'required': {'message': 'A name is required.'}
        })
    photo = fields.String()
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)
    description = fields.String()


class ActivityTypesSchema(BaseSchema):
    """Creates a validation schema for activity types."""

    description = fields.String(
        required=True,
        error_messages={
            'required': 'A description is required.'
        }
    )
    value = fields.Integer(
        required=True,
        error_messages={
            'required': 'Please send the activity points value'
        }
    )


class LoggedActivitySchema(BaseSchema):
    """Creates a validation schema for logged activities."""

    status = fields.String(dump_only=True)
    value = fields.Integer(
        required=True,
        error_messages={
            'required': 'Please send the activity points value'
        }
    )
    user = fields.String(dump_only=True, attribute='user.name')
    society = fields.String(dump_only=True, attribute='society.name')
    approved_by = fields.Method('get_approver', dump_only=True)

    @staticmethod
    def get_approver(obj):
        """Get approver details."""
        if obj.approver_id:
            approver = User.query.get(obj.approver_id)
            return approver.name
        return


class ActivitySchema(BaseSchema):
    """Creates a validation schema for activities."""

    description = fields.String(
        required=True,
        error_messages={
            'required': {'message': 'A description is required.'}
        })
    activity_type_id = fields.String(
        required=True,
        error_messages={
            'required': {'message': 'An activity type ID is required.'}
        })
    activity_date = fields.Date(
        required=True,
        error_messages={
                'required': {'message': 'An activity date is required.'}
        })
    added_by = fields.String(dump_only=True)

    @post_load
    def verify_activity(self, data):
        """Extra validation for the Activity Schema."""
        invalid_activity_names = ['Blog', 'App', 'Open Source']
        activity_type = ActivityType.query.get(data['activity_type_id'])
        existing_activity = Activity.query.filter(
            Activity.name.ilike(data['name'])).first()

        if not activity_type:
            self.context = {'status_code': 404}
            raise ValidationError(
                {'message': 'Activity Type does not exist!'})

        if existing_activity:
            self.context = {'status_code': 409}
            raise ValidationError(
                {'message': 'Activity already exists!'})

        if any(name in data['name'] for name in invalid_activity_names):
            raise ValidationError(
                {'message': 'This is not a valid activity!'})

    @validates('activity_date')
    def validates_activity_date(self, value):
        """Validate the activity date field."""
        if value < date.today():
            raise ValidationError(
                {'message': 'Date is in the past! Please enter a valid date.'})
        else:
            return value


get_activity_types_schema = ActivityTypesSchema(many=True)
get_logged_activities_schema = LoggedActivitySchema(many=True)
post_activity_schema = ActivitySchema()
