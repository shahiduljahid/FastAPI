from passlib.context import CryptContext

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash:
    def bcrypt(password: str):
        hashedPassword = pwd_cxt.hash(password)
        return hashedPassword

    def verify(plainPassword, HashedPassword):
        return pwd_cxt.verify(plainPassword, HashedPassword)
