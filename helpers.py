import hashlib, re, uuid
from flask import current_app

def encode_password(password):
    return generate_hash(password)

def validate_password(old_key, password):
    generated_key = generate_hash(password)
    return bool(generated_key == old_key)
    
def generate_hash(password):
    secret_key = current_app.config["SECRET_KEY"]
    generated_key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode("utf-8"),
        bytes(secret_key, 'utf-8'),
        100000
    )
    return generated_key.hex()

def are_params_valid(params, validation_schema):
    print(params)
    for param, info in validation_schema.items():
        if param in params:
            if not isinstance(params[param], info['type']):
                return False, f"{param} - type is not valid"
            if info['type'] == str and 'regex' in info and not validate_regex(params[param], info['regex']):
                return False, f"{param} is not valid"
            if 'allowed' in info and params[param] not in info['allowed']:
                return False, f"{param} is not allowed"
    return True, ''

def validate_regex(string, regex):
    pattern = re.compile(regex)
    return pattern.match(string)

def get_random_id():
    return str(uuid.uuid4())[:8]