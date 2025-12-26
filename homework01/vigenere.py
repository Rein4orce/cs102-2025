def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    key_index = 0

    for char in plaintext:
        key_char = keyword[key_index % len(keyword)]
        shift = ord(key_char.lower()) - ord("a")

        if char.isalpha():
            if "A" <= char <= "Z":
                base = ord("A")
            else:
                base = ord("a")
            ciphertext += chr((ord(char) - base + shift) % 26 + base)
        else:
            ciphertext += char

        key_index += 1

    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    key_index = 0

    for char in ciphertext:
        key_char = keyword[key_index % len(keyword)]
        shift = ord(key_char.lower()) - ord("a")

        if char.isalpha():
            if "A" <= char <= "Z":
                base = ord("A")
            else:
                base = ord("a")
            plaintext += chr((ord(char) - base - shift) % 26 + base)
        else:
            plaintext += char

        key_index += 1

    return plaintext
