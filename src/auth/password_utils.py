import random, string

def generateRandomPassword():

    """
    Creates random password which fits password rules

    Returns:
        "".join(password) (str): Returns all characters from password, joined into a string
    """
    
    #Ensures that password contains at least one letter, digit, and special character
    letters = string.ascii_letters
    digits = string.digits
    specials = string.punctuation

    password = [random.choice(letters), random.choice(digits), random.choice(specials)]

    allChars = letters + digits + specials
    password += random.choices(allChars, k=9)

    #Orders password randomly to remove patterns
    random.shuffle(password)

    return "".join(password)