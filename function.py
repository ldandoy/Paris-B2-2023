from flask_bcrypt import Bcrypt
from pprint import pprint


def valid_login(password_hash: str, password: str):
    return Bcrypt.check_password_hash(password_hash, password)


def reverse_word(word: str):
    return ''.join(reversed(word))


def calculate_tva(price: int, taux: int):
    return price * taux / 100


def calcuate_letter(word: str):
    count = 0

    for l in word:
        # if l.lower() == "e":

        # if l == "e" or l == "E":
        if l == "e":
            count = count + 1
        elif l == "E":
            count = count + 1

    return count
