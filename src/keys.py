import json
import string
import random
from datetime import datetime

from passlib.hash import sha256_crypt as crypt


class Keystore:
    """Key storage and management"""

    KEY_LENGTH = 32
    ID_LENGTH = 5

    def __init__(self, filepath):
        self.file = filepath
        self.keys = {}
        self.load()

    def load(self):
        """Load the keys from the keys file"""
        try:
            with open(self.file, 'r') as f:
                self.keys = self.parse(json.load(f))
        except FileNotFoundError:
            pass

    def parse(self, keys):
        """Parse timestamps from loaded keys"""
        for key_id, key in keys.items():
            try:
                keys[key_id]['used'] = datetime.fromisoformat(key.get('used'))
            except TypeError:
                pass
        return keys

    def save(self):
        """Save the keys to the keys file"""
        with open(self.file, 'w+') as f:
            json.dump(self.keys, f, indent=2, default=str)

    def add(self, name):
        """Generate a new key"""
        key_value = self.random(self.KEY_LENGTH)
        key_hash = crypt.encrypt(key_value)
        key_id = None

        while key_id is None or key_id in self.keys.keys():
            key_id = self.random(self.ID_LENGTH).lower()

        self.keys[key_id] = {'hash': key_hash, 'name': name, 'used': False}
        self.save()
        return '{}-{}'.format(key_id, key_value)

    def delete(self, key_id):
        """Delete a key by its ID"""
        try:
            del self.keys[key_id]
            self.save()
            return True
        except KeyError:
            return False

    def verify(self, key):
        """Verify a key against its stored hash"""
        try:
            key_id, key_value = key.split('-')
            key_hash = self.keys[key_id]['hash']
            self.timestamp(key_id)
            return crypt.verify(key_value, key_hash)
        except (ValueError, KeyError, AttributeError):
            return False

    def timestamp(self, key_id):
        """Set the last used time of a key"""
        try:
            self.keys[key_id]['used'] = datetime.now()
            self.save()
        except KeyError:
            pass

    def random(self, length):
        """Generate a random string of letters and numbers"""
        choices = string.ascii_letters + string.digits
        chars = [random.SystemRandom().choice(choices) for x in range(length)]
        return ''.join(chars)
