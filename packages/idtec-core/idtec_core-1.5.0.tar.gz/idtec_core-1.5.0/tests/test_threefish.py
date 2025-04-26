
from idtec_core import threefish

def test_encrypt_decrypt():
    key = "0123456789abcdef0123456789abcdef"
    message = "Quantum Data"
    encrypted = threefish.encrypt_message(message, key)
    decrypted = threefish.decrypt_message(encrypted, key)
    assert decrypted == message
