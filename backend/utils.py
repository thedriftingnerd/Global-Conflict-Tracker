import os
import json
from datetime import datetime
from functools import wraps
from flask import jsonify

def json_response(data, status=200):
    """Helper to return JSON responses"""
    return jsonify(data), status

def error_response(message, status=400):
    """Helper to return error responses"""
    return jsonify({'error': message}), status

def success_response(data, message="Success", status=200):
    """Helper to return success responses"""
    return jsonify({
        'success': True,
        'message': message,
        'data': data,
        'timestamp': datetime.now().isoformat()
    }), status

def require_json(f):
    """Decorator to require JSON content type"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.is_json:
            return error_response('Content-Type must be application/json', 415)
        return f(*args, **kwargs)
    return decorated_function

def rate_limit(max_requests=100):
    """Simple rate limiting decorator"""
    def decorator(f):
        requests_made = {}
        
        @wraps(f)
        def decorated_function(*args, **kwargs):
            from flask import request
            from time import time
            
            remote_addr = request.remote_addr
            now = time()
            
            if remote_addr not in requests_made:
                requests_made[remote_addr] = []
            
            # Clean old requests (> 60 seconds)
            requests_made[remote_addr] = [t for t in requests_made[remote_addr] if now - t < 60]
            
            if len(requests_made[remote_addr]) >= max_requests:
                return error_response('Rate limit exceeded', 429)
            
            requests_made[remote_addr].append(now)
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator
