import secrets
import string
import random


def generate_random_string():
    '''
    Generate a random string of length 6 or 10 characters in lowercase and uppercase letters.
    :return: string
    '''

    characters = string.ascii_letters + string.digits
    length = random.randint(6, 10)
    random_string = ''.join(secrets.choice(characters) for _ in range(length))
    return random_string
