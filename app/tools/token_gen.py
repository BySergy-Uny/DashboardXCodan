import hashlib

def generate_hash(value):
    return hashlib.sha256(value.encode()).hexdigest()

def generate_token(username, password):
    return generate_hash(username + "+" + password)

# EJEMPLO DE USO DE LA HERRAMIENTA

# print("Hash generate --> ", generate_hash('PASSWORD'))