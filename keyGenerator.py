# keyGenerator.py
# Created by Miguel Barba

import random

PublicKey = ''
validKeys = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123456789012345678901234567890"

for i in range(40):
    PublicKey += random.choice(validKeys)

print(PublicKey)
