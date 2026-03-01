import random, string

def generateRandomPassword():
    
    letters = string.ascii_letters
    digits = string.digits
    specials = string.punctuation

    password = [random.choice(letters), random.choice(digits), random.choice(specials)]

    allChars = letters + digits + specials
    password += random.choices(allChars, k=9)

    random.shuffle(password)

    return "".join(password)