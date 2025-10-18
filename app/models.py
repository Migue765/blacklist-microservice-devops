from datetime import datetime
from app import db

class Blacklist(db.Model):
    """Model for blacklisted emails"""

    __tablename__ = 'blacklists'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True, index=True)
    app_uuid = db.Column(db.String(36), nullable=False)  # UUID format
    blocked_reason = db.Column(db.String(255), nullable=True)
    client_ip = db.Column(db.String(45), nullable=False)  # IPv6 max length
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<Blacklist {self.email}>'

    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'email': self.email,
            'app_uuid': self.app_uuid,
            'blocked_reason': self.blocked_reason,
            'client_ip': self.client_ip,
            'created_at': self.created_at.isoformat() + 'Z'
        }
