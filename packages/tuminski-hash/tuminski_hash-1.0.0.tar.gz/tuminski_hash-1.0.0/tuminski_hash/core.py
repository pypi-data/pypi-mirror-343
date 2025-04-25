import hashlib
import os
import base64
from hmac import compare_digest

class TuminskiHash:
    def __init__(self):
        self.assinatura = b"TUMINSKI"
        self.salt_size = 16

    def gerar(self, palavra: str) -> str:
        salt = os.urandom(self.salt_size)
        dados = salt + palavra.encode('utf-8') + self.assinatura
        hash_gerado = hashlib.sha512(dados).digest()
        return base64.b64encode(salt + hash_gerado).decode('utf-8')

    def verificar(self, palavra: str, hash_salvo: str) -> bool:
        try:
            decoded = base64.b64decode(hash_salvo)
            salt = decoded[:self.salt_size]
            hash_original = decoded[self.salt_size:]
            dados = salt + palavra.encode('utf-8') + self.assinatura
            novo_hash = hashlib.sha512(dados).digest()
            return compare_digest(novo_hash, hash_original)
        except Exception:
            return False
