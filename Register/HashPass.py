# Hash passwords
from os import urandom
import hashlib

class Hash():
    def __init__(self, password):
        self.password = password.encode("utf-8")
        self.sha_type = 'sha256'
        self.salt = urandom(32)

    def hash_data(self):
        print("Password used to hash is", self.password)
        
        return hashlib.pbkdf2_hmac(self.sha_type, self.password, self.salt, iterations=10000), self.salt



class HashWithSalt:
    def __init__(self, password, salt):
        self.password = password.encode("utf-8")
        self.salt = salt

    def hash_data(self):
        return hashlib.pbkdf2_hmac("sha256", self.password, self.salt, iterations=10000)