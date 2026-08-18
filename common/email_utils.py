import random
import string
def get_email_code():
    list = random.sample(string.ascii_letters+string.digits, 6)
    return "".join(list)

def send_email(email,code):
    pass