import hashlib
import requests

class BreachChecker:
    API_URL = "https://api.pwnedpasswords.com/range/"

    @staticmethod
    def hash_password(password: str) -> str:
        sha1 = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
        return sha1

    @staticmethod
    def is_breached(password: str) -> bool:
        sha1_hash = BreachChecker.hash_password(password)
        prefix = sha1_hash[:5]
        suffix = sha1_hash[5:]

        try:
            response = requests.get(BreachChecker.API_URL + prefix, timeout=5)
            if response.status_code != 200:
                raise Exception(f"API error: {response.status_code}")
            
            hashes = (line.split(':') for line in response.text.splitlines())
            for hash_suffix, count in hashes:
                if hash_suffix == suffix:
                    return True
            return False

        except requests.RequestException as e:
            raise Exception(f"Error accessing breach check API: {str(e)}")
