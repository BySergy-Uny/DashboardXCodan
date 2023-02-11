import hashlib

def generate_hash(value):
    return hashlib.sha256(value.encode()).hexdigest()


# EJEMPLO DE USO DE LA HERRAMIENTA

# print("Hash generate --> ", generate_hash('PASSWORD'))