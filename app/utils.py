from flask import request
import logging

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

def setup_logging():
    """Setup structured logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)
