"""
Функции для генерации криптографически стойких случайных значений.
"""

import os as _os
import uuid as _uuid
import base64 as _base64
import hashlib as _hashlib
import secrets as _secrets
import string as _string
from .core import randint, choice, uniform, choices
from .strings import string

def token_bytes(nbytes=32):
    """
    Генерирует случайную последовательность байтов с помощью безопасного генератора.
    
    Args:
        nbytes: Количество байтов для генерации. По умолчанию 32.
        
    Returns:
        bytes: Случайная последовательность байтов.
    """
    return _secrets.token_bytes(nbytes)

def token_hex(nbytes=32):
    """
    Генерирует случайную шестнадцатеричную строку с помощью безопасного генератора.
    
    Args:
        nbytes: Количество байтов для генерации (результат будет в 2 раза длиннее). По умолчанию 32.
        
    Returns:
        str: Случайная шестнадцатеричная строка.
    """
    return _secrets.token_hex(nbytes)

def token_urlsafe(nbytes=32):
    """
    Генерирует случайную URL-безопасную строку с помощью безопасного генератора.
    
    Args:
        nbytes: Количество байтов для генерации. По умолчанию 32.
        
    Returns:
        str: Случайная URL-безопасная строка.
    """
    return _secrets.token_urlsafe(nbytes)

def uuid(version=4):
    """
    Генерирует UUID (универсальный уникальный идентификатор).
    
    Args:
        version: Версия UUID (1, 3, 4 или 5). По умолчанию 4 (случайный UUID).
        
    Returns:
        uuid.UUID: Объект UUID.
    """
    if version == 1:
        return str(_uuid.uuid1())
    elif version == 3:
        namespace = _uuid.NAMESPACE_DNS
        name = str(randint(1, 1000000))
        return str(_uuid.uuid3(namespace, name))
    elif version == 4:
        return str(_uuid.uuid4())
    elif version == 5:
        namespace = _uuid.NAMESPACE_DNS
        name = str(randint(1, 1000000))
        return str(_uuid.uuid5(namespace, name))
    else:
        raise ValueError(f"Неподдерживаемая версия UUID: {version}")

def random_hash(algorithm="sha256"):
    """
    Генерирует случайный хеш с использованием указанного алгоритма.
    
    Args:
        algorithm: Алгоритм хеширования ('md5', 'sha1', 'sha256', 'sha512'). По умолчанию 'sha256'.
        
    Returns:
        str: Случайный хеш в шестнадцатеричном формате.
    """
    algorithms = {
        "md5": _hashlib.md5,
        "sha1": _hashlib.sha1,
        "sha224": _hashlib.sha224,
        "sha256": _hashlib.sha256,
        "sha384": _hashlib.sha384,
        "sha512": _hashlib.sha512,
        "blake2b": _hashlib.blake2b,
        "blake2s": _hashlib.blake2s,
    }
    
    if algorithm not in algorithms:
        raise ValueError(f"Неподдерживаемый алгоритм хеширования: {algorithm}")
    
    random_data = token_bytes(32)
    hash_function = algorithms[algorithm]
    
    return hash_function(random_data).hexdigest()

def secure_key(length=32, encoding="raw"):
    """
    Генерирует безопасный ключ заданной длины.
    
    Args:
        length: Длина ключа в байтах. По умолчанию 32.
        encoding: Кодировка результата ('hex', 'base64', 'base64url', 'bytes'). По умолчанию 'raw'.
        
    Returns:
        str или bytes: Безопасный ключ в указанной кодировке.
    """
    random_bytes = token_bytes(length)
    
    if encoding == "raw":
        return random_bytes
    elif encoding == "hex":
        return token_hex(length)
    elif encoding == "base64":
        return _base64.b64encode(random_bytes).decode('utf-8')
    elif encoding == "base32":
        return _base64.b32encode(random_bytes).decode('utf-8')
    elif encoding == "base16":
        return _base64.b16encode(random_bytes).decode('utf-8')
    else:
        raise ValueError(f"Неподдерживаемая кодировка: {encoding}")

def secure_pin(length=4):
    """
    Генерирует случайный PIN-код указанной длины.
    
    Args:
        length: Длина PIN-кода. По умолчанию 4.
        
    Returns:
        str: Случайный PIN-код.
    """
    if length <= 0:
        raise ValueError("Длина PIN-кода должна быть положительным числом")
    
    return ''.join(str(randint(0, 9)) for _ in range(length))

def secure_password(length=16, include_symbols=True, min_digits=2, min_uppercase=2, min_lowercase=2, min_symbols=2):
    """
    Генерирует безопасный случайный пароль.
    
    Args:
        length: Длина пароля. По умолчанию 16.
        include_symbols: Включать ли специальные символы. По умолчанию True.
        min_digits: Минимальное количество цифр. По умолчанию 2.
        min_uppercase: Минимальное количество заглавных букв. По умолчанию 2.
        min_lowercase: Минимальное количество строчных букв. По умолчанию 2.
        min_symbols: Минимальное количество специальных символов. По умолчанию 2.
        
    Returns:
        str: Безопасный случайный пароль.
    """
    if length < (min_digits + min_uppercase + min_lowercase + (min_symbols if include_symbols else 0)):
        raise ValueError("Длина пароля слишком мала для удовлетворения минимальных требований")
    
    lowercase = _string.ascii_lowercase
    uppercase = _string.ascii_uppercase
    digits = _string.digits
    symbols = _string.punctuation if include_symbols else ""
    
    password = []
    
    password.extend(choices(lowercase, k=min_lowercase))
    password.extend(choices(uppercase, k=min_uppercase))
    password.extend(choices(digits, k=min_digits))
    
    if include_symbols:
        password.extend(choices(symbols, k=min_symbols))
    
    all_chars = lowercase + uppercase + digits + symbols
    remaining_length = length - len(password)
    
    if remaining_length > 0:
        password.extend(choices(all_chars, k=remaining_length))
    
    _secrets.SystemRandom().shuffle(password)
    
    return ''.join(password)

def random_ip():
    """
    Генерирует случайный IPv4-адрес.
    
    Returns:
        str: Случайный IPv4-адрес.
    """
    return f"{randint(0, 255)}.{randint(0, 255)}.{randint(0, 255)}.{randint(0, 255)}"

def random_ipv6():
    """
    Генерирует случайный IPv6-адрес.
    
    Returns:
        str: Случайный IPv6-адрес.
    """
    segments = []
    for _ in range(8):
        segment = ''.join(choices("0123456789abcdef", k=4))
        segments.append(segment)
    
    return ":".join(segments)

def random_mac(separator=":"):
    """
    Генерирует случайный MAC-адрес.
    
    Args:
        separator: Разделитель между сегментами MAC-адреса. По умолчанию ":".
        
    Returns:
        str: Случайный MAC-адрес.
    """
    segments = []
    for _ in range(6):
        segment = ''.join(choices("0123456789abcdef", k=2))
        segments.append(segment)
    
    return separator.join(segments)

def sha1_digest(data):
    if isinstance(data, str):
        data = data.encode('utf-8')
    return _hashlib.sha1(data).hexdigest()

def sha256_digest(data):
    if isinstance(data, str):
        data = data.encode('utf-8')
    return _hashlib.sha256(data).hexdigest()

def sha512_digest(data):
    if isinstance(data, str):
        data = data.encode('utf-8')
    return _hashlib.sha512(data).hexdigest()

def md5_digest(data):
    if isinstance(data, str):
        data = data.encode('utf-8')
    return _hashlib.md5(data).hexdigest()

def hmac_digest(key, data, algorithm="sha256"):
    if isinstance(key, str):
        key = key.encode('utf-8')
    if isinstance(data, str):
        data = data.encode('utf-8')
    
    import hmac
    
    if algorithm == "sha1":
        return hmac.new(key, data, _hashlib.sha1).hexdigest()
    elif algorithm == "sha256":
        return hmac.new(key, data, _hashlib.sha256).hexdigest()
    elif algorithm == "sha512":
        return hmac.new(key, data, _hashlib.sha512).hexdigest()
    elif algorithm == "md5":
        return hmac.new(key, data, _hashlib.md5).hexdigest()
    else:
        raise ValueError(f"Неподдерживаемый алгоритм хеширования: {algorithm}")

def jwt_token(payload, secret_key=None):
    import json
    import time
    
    if secret_key is None:
        secret_key = token_bytes(32)
    
    if isinstance(secret_key, bytes):
        secret_key_str = secret_key.decode('latin1')
    else:
        secret_key_str = secret_key
    
    if isinstance(payload, str):
        try:
            payload = json.loads(payload)
        except json.JSONDecodeError:
            payload = {"data": payload}
    
    if not isinstance(payload, dict):
        payload = {"data": str(payload)}
    
    header = {
        "alg": "HS256",
        "typ": "JWT"
    }
    
    if "iat" not in payload:
        payload["iat"] = int(time.time())
    
    if "exp" not in payload:
        payload["exp"] = int(time.time()) + 3600  # +1 час
    
    header_json = json.dumps(header, separators=(',', ':'))
    payload_json = json.dumps(payload, separators=(',', ':'))
    
    header_b64 = _base64.urlsafe_b64encode(header_json.encode()).decode().rstrip('=')
    payload_b64 = _base64.urlsafe_b64encode(payload_json.encode()).decode().rstrip('=')
    
    to_sign = f"{header_b64}.{payload_b64}"
    signature = hmac_digest(secret_key_str, to_sign, "sha256")
    signature_b64 = _base64.urlsafe_b64encode(bytes.fromhex(signature)).decode().rstrip('=')
    
    return f"{header_b64}.{payload_b64}.{signature_b64}"

def ssl_cert_fingerprint():
    algorithms = ["sha1", "sha256", "md5"]
    algorithm = choice(algorithms)
    
    fingerprint_parts = []
    for _ in range(16 if algorithm == "md5" else (20 if algorithm == "sha1" else 32)):
        fingerprint_parts.append(token_hex(1))
    
    return ":".join(fingerprint_parts).upper() 