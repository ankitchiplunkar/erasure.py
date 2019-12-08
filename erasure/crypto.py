from cryptography.fernet import Fernet


def generate_key():
    return Fernet.generate_key()


def encrypt(key, data):
    f = Fernet(key)
    return f.encrypt(bytes(data, 'utf-8'))


def decrypt(key, token):
    f = Fernet(key)
    return f.decrypt(token).decode('utf-8')
