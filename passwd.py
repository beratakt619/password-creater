import hashlib
import requests
from difflib import SequenceMatcher
import random
def şifreoluşturma():
    
    kelime1 = input("1. Kelime ").strip()[:4]
    kelime2 = input("2. Kelime ").strip()[:4]
    kelime3 = input("3. Kelime ").strip()[:4]
    sayi = input("3-4 haneli sayı girin").strip()[:4]
    özelkarakter=random.choice("!@#$%&*")
    components = [
        kelime1.capitalize(),
        kelime2.upper(),
        kelime3.lower(),
        sayi,
        özelkarakter
    ]
    random.shuffle(components)
    password = ''.join(components)
    print(password)
şifreoluşturma()
