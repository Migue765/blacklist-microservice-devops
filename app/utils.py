from flask import request
import logging
import json
import sys
import os
from datetime import datetime

def get_client_ip():
    """Get the real client IP address, considering X-Forwarded-For header"""
    # Check for X-Forwarded-For header (used by load balancers)
    if request.headers.get('X-Forwarded-For'):
        # X-Forwarded-For can contain multiple IPs, take the first one
        return request.headers.get('X-Forwarded-For').split(',')[0].strip()

    # Check for X-Real-IP header (alternative)
    if request.headers.get('X-Real-IP'):
        return request.headers.get('X-Real-IP')

    # Fallback to remote_addr
    return request.remote_addr


class JSONFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging compatible with New Relic"""
    
    def format(self, record):
        log_data = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
        }
        
        # Add exception info if present
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)
        
        # Add extra fields if present
        if hasattr(record, 'extra_fields'):
            log_data.update(record.extra_fields)
        
        # Add environment info
        if os.environ.get('DYNO'):
            log_data['dyno'] = os.environ.get('DYNO')
            log_data['source'] = 'heroku'
        elif os.environ.get('ECS_CONTAINER_METADATA_URI'):
            log_data['source'] = 'aws-ecs'
            # Try to get task ARN from metadata
            try:
                import requests
                metadata_uri = os.environ.get('ECS_CONTAINER_METADATA_URI')
                if metadata_uri:
                    task_metadata = requests.get(f"{metadata_uri}/task", timeout=2).json()
                    log_data['task_arn'] = task_metadata.get('TaskARN', 'unknown')
            except:
                pass
        
        # Add New Relic context if available
        try:
            import newrelic.agent
            if newrelic.agent._settings and newrelic.agent._settings.app_name:
                log_data['app_name'] = newrelic.agent._settings.app_name
        except:
            pass
        
        return json.dumps(log_data)


class StructuredLogger:
    """Structured logger that outputs to stdout for Heroku"""
    
    def __init__(self, name):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # Remove existing handlers to avoid duplicates
        self.logger.handlers = []
        
        # Create stdout handler (Heroku captures stdout/stderr)
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)
        
        # Use JSON formatter for New Relic compatibility, or simple formatter for local dev
        # Detect Heroku (DYNO) or AWS ECS (ECS_CONTAINER_METADATA_URI) or explicit flag
        is_production = (
            os.environ.get('HEROKU_APP_NAME') or 
            os.environ.get('DYNO') or 
            os.environ.get('ECS_CONTAINER_METADATA_URI') or  # AWS ECS
            os.environ.get('AWS_ENVIRONMENT') or  # Explicit flag
            os.environ.get('NEW_RELIC_LICENSE_KEY')  # If New Relic is configured, use JSON
        )
        
        if is_production:
            # Use JSON format for production environments (Heroku/AWS) and New Relic
            handler.setFormatter(JSONFormatter())
        else:
            # Use simple format for local development
            handler.setFormatter(logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            ))
        
        self.logger.addHandler(handler)
        self.logger.propagate = False
    
    def info(self, message, **kwargs):
        """Log info message with optional extra fields"""
        extra = {'extra_fields': kwargs} if kwargs else {}
        self.logger.info(message, extra=extra)
    
    def error(self, message, **kwargs):
        """Log error message with optional extra fields"""
        extra = {'extra_fields': kwargs} if kwargs else {}
        self.logger.error(message, extra=extra)
    
    def warning(self, message, **kwargs):
        """Log warning message with optional extra fields"""
        extra = {'extra_fields': kwargs} if kwargs else {}
        self.logger.warning(message, extra=extra)
    
    def debug(self, message, **kwargs):
        """Log debug message with optional extra fields"""
        extra = {'extra_fields': kwargs} if kwargs else {}
        self.logger.debug(message, extra=extra)


def setup_logging():
    """Setup structured logging compatible with Heroku and New Relic"""
    # Use structured logger for better New Relic integration
    return StructuredLogger(__name__)
