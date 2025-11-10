import secrets

def generate_otp():
    """Generate a 6-digit numeric OTP as a string"""
    otp = ''.join([str(secrets.randbelow(10)) for _ in range(6)])
    return otp


