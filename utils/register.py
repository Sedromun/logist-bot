from config import ADMIN_SECRET_CODE, FERNET, SECRET_END, SECRET_START
from database.controllers.role import create_role, get_role, update_role
from schemas.users import RoleModel


def check_code(code: str) -> str | RoleModel | None:
    if code == ADMIN_SECRET_CODE:
        return "admin"
    else:
        id = decrypt_code(code)
        if id is None:
            return None
        role = get_role(id)
        if role is None:
            return None
        if role.user is not None:
            return None
        return role


def create_code(role_name: str, company: str|None):
    role = create_role()
    code = encrypt_code(role.id)
    update_role(role.id, {"code": code, "company": company, "role_name": role_name})
    return code


def encrypt_code(id: int) -> str:
    word = SECRET_START + str(id) + SECRET_END
    word_enc = FERNET.encrypt(word.encode())
    return word_enc.decode()

def decrypt_code(code_enc: int) -> int | None:
    word_dec = FERNET.decrypt(code_enc.encode()).decode()
    try:
        id = int(word_dec[len(SECRET_START):(len(word_dec) - len(SECRET_END))])
    except Exception as e:
        return None
    return id
