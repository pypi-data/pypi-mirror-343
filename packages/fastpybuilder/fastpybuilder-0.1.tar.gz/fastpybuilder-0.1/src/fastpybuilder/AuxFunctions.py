import re
import string

def to_camel_case(text):
    parts = text.replace('_', ' ').split()
    return parts[0].lower() + ''.join(word.capitalize() for word in parts[1:])



def to_title_case_label(text):

    clean = re.sub(r"[_\-]+", " ", text)

    clean = re.sub(r"\s+", " ", clean).strip()

    return string.capwords(clean).replace(" ","")