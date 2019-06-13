import json
import string
import random

from passlib.hash import sha256_crypt as crypt


class Keystore:
    """Key storage and management"""

    KEY_LENGTH = 32
    ID_LENGTH = 4

    def __init__(self, filepath):
        self.file = filepath
        self.keys = {}
        self.load()

    def load(self):
        """Load the keys from the keys file"""
        try:
            with open(self.file, 'r') as f:
                self.keys = json.load(f)
        except FileNotFoundError:
            pass

    def save(self):
        """Save the keys to the keys file"""
        with open(self.file, 'w+') as f:
            json.dump(self.keys, f, indent=2)

    def add(self, name):
        """Generate a new key"""
        key_value = self.random(self.KEY_LENGTH)
        key_hash = crypt.encrypt(key_value)
        key_id = None

        while key_id is None or key_id in self.keys.keys():
            key_id = self.random(self.ID_LENGTH)

        self.keys[key_id] = {'hash': key_hash, 'name': name}
        return key_id + key_value

    def delete(self, key_id):
        """Delete a key by its ID"""
        try:
            del self.keys[key_id]
            return True
        except KeyError:
            return False

    def verify(self, key):
        """Verify a key against its stored hash"""
        key_id, key_value = key[:self.ID_LENGTH], key[self.ID_LENGTH:]
        key_hash = self.keys.get(key_id, {}).get('hash')
        return crypt.verify(key_value, key_hash)

    def random(self, length):
        """Generate a random string of letters and numbers"""
        choices = string.ascii_letters + string.digits
        chars = [random.SystemRandom().choice(choices) for x in range(length)]
        return ''.join(chars)
