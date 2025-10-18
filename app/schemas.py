from marshmallow import Schema, fields, validate, ValidationError
import re
import uuid

class BlacklistSchema(Schema):
    """Schema for blacklist validation"""

    email = fields.Email(required=True, validate=validate.Length(max=255))
    app_uuid = fields.Str(required=True, validate=validate.Length(equal=36))
    blocked_reason = fields.Str(required=False, validate=validate.Length(max=255))

    def validate_app_uuid(self, value):
        """Validate UUID format"""
        try:
            uuid.UUID(value)
        except ValueError:
            raise ValidationError('Invalid UUID format')
        return value

class BlacklistResponseSchema(Schema):
    """Schema for blacklist response"""

    id = fields.Int()
    email = fields.Str()
    app_uuid = fields.Str()
    blocked_reason = fields.Str()
    client_ip = fields.Str()
    created_at = fields.DateTime()

class ErrorSchema(Schema):
    """Schema for error responses"""

    error = fields.Str(required=True)
    details = fields.Str(required=False)
    message = fields.Str(required=False)
