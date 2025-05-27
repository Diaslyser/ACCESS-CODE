import random
import string
import json
from datetime import datetime, timedelta

def generate_code(length=14):
    chars = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}"
    return ''.join(random.choice(chars) for _ in range(length))

def generate_codes_file(nb_codes=20, filename='codes.json', expiry_hours=24):
    codes = {}
    expiry_time = datetime.utcnow() + timedelta(hours=expiry_hours)
    expiry_str = expiry_time.isoformat() + "Z"

    while len(codes) < nb_codes:
        code = generate_code()
        if code not in codes:
            codes[code] = {
                "status": "unused",
                "expires_at": expiry_str
            }

    with open(filename, 'w') as f:
        json.dump(codes, f, indent=4)
    print(f"{nb_codes} codes générés avec expiration à {expiry_str} UTC.")

if __name__ == "__main__":
    generate_codes_file()
