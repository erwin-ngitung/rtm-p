import re
import warnings
warnings.filterwarnings("ignore")


def list_email():
    email = ["fernandaerwin277@gmail.com",
             "rayhanrizky@yahoo.com",
             "dominicusbagus@gmail.com",
             "agora.rtm-p@gmail.com"]

    return email


def check_email(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    if re.fullmatch(regex, email):
        value = "valid email"
    else:
        value = "invalid email"

    return value
