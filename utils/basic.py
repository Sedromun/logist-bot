import re


def normalize_rc_name(name):
    name = str(name).replace('"', '').replace("'", '')
    name = name.lower()
    name = re.sub(r'^(ао\s+тандер\s+)', '', name)  # убираем префикс в начале
    name = re.sub(r'\s+', ' ', name)
    name = re.sub(r'\s*,\s*', ',', name)
    name = re.sub(r'\s*\(\s*', '(', name)
    name = re.sub(r'\s*\)\s*', ')', name)
    name = name.strip()
    return name

