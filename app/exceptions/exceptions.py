class ExpiredSignatureError_Exception(Exception):
    """The signature is expired"""
    pass

class InvalidJWTToken_Exception(Exception):
    """The JWT token is invalid"""
    pass