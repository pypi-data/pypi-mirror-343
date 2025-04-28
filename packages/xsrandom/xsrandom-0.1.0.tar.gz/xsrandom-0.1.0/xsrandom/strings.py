import string as _string
import random as _random
import re as _re
from .core import choice, choices, randint, random

_LOWERCASE = _string.ascii_lowercase
_UPPERCASE = _string.ascii_uppercase
_DIGITS = _string.digits
_PUNCTUATION = _string.punctuation
_LETTERS = _LOWERCASE + _UPPERCASE
_ALPHANUMERIC = _LETTERS + _DIGITS
_PRINTABLE = _ALPHANUMERIC + _PUNCTUATION

def string(length=10, charset=None, pattern="alphanumeric"):
    if charset is not None:
        chars = charset
    else:
        if pattern == "alphanumeric":
            chars = _ALPHANUMERIC
        elif pattern == "printable":
            chars = _PRINTABLE
        elif pattern == "letters":
            chars = _LETTERS
        elif pattern == "lowercase":
            chars = _LOWERCASE
        elif pattern == "uppercase":
            chars = _UPPERCASE
        elif pattern == "digits":
            chars = _DIGITS
        elif pattern == "hex":
            chars = _DIGITS + "abcdef"
        elif pattern == "binary":
            chars = "01"
        else:
            raise ValueError(f"Неизвестный шаблон: {pattern}")
    
    return "".join(choices(chars, k=length))

def ascii_string(length=10, include_special_chars=False):
    if include_special_chars:
        chars = _string.printable
    else:
        chars = _ALPHANUMERIC
    
    return "".join(choices(chars, k=length))

def password(length=12, strength="medium"):
    if strength == "weak":
        chars = _ALPHANUMERIC
    elif strength == "medium":
        chars = _ALPHANUMERIC
        result = [
            choice(_LOWERCASE),
            choice(_UPPERCASE),
            choice(_DIGITS)
        ]
        result.extend(choices(chars, k=length - 3))
        _random.shuffle(result)
        return "".join(result)
    elif strength == "strong":
        chars = _PRINTABLE
        result = [
            choice(_LOWERCASE),
            choice(_UPPERCASE),
            choice(_DIGITS),
            choice(_PUNCTUATION)
        ]
        result.extend(choices(chars, k=length - 4))
        _random.shuffle(result)
        return "".join(result)
    elif strength == "very_strong":
        chars = _PRINTABLE
        result = [
            choice(_LOWERCASE),
            choice(_LOWERCASE),
            choice(_UPPERCASE),
            choice(_UPPERCASE),
            choice(_DIGITS),
            choice(_DIGITS),
            choice(_PUNCTUATION),
            choice(_PUNCTUATION)
        ]
        result.extend(choices(chars, k=max(0, length - 8)))
        _random.shuffle(result)
        return "".join(result)
    else:
        raise ValueError(f"Неизвестная сила пароля: {strength}")
    
    return "".join(choices(chars, k=length))

def username(min_length=5, max_length=15):
    length = randint(min_length, max_length)
    first_char = choice(_LETTERS)
    rest_chars = choices(_LETTERS + _DIGITS + "_", k=length - 1)
    return first_char + "".join(rest_chars)

def hex_string(length=10, prefix=""):
    hex_chars = _DIGITS + "abcdef"
    return prefix + "".join(choices(hex_chars, k=length))

def binary_string(length=8, format_with_spaces=False, prefix=""):
    bin_str = "".join(choices("01", k=length))
    
    if format_with_spaces:
        groups = [bin_str[i:i+8] for i in range(0, len(bin_str), 8)]
        return prefix + " ".join(groups)
    else:
        return prefix + bin_str

def word(min_length=3, max_length=10):
    vowels = "aeiou"
    consonants = "bcdfghjklmnpqrstvwxyz"
    
    length = randint(min_length, max_length)
    word = []
    
    for i in range(length):
        if i % 2 == 0:
            char = choice(consonants)
        else:
            char = choice(vowels)
        word.append(char)
    
    if randint(1, 10) <= 3:
        word[0] = word[0].upper()
    
    return "".join(word)

def sentence(min_words=4, max_words=12):
    num_words = randint(min_words, max_words)
    words = [word() for _ in range(num_words)]
    words[0] = words[0].capitalize()
    
    sentence = " ".join(words)
    punctuation = choice(".!?")
    
    return sentence + punctuation

def paragraph(min_sentences=3, max_sentences=8):
    num_sentences = randint(min_sentences, max_sentences)
    sentences = [sentence() for _ in range(num_sentences)]
    return " ".join(sentences)

def lorem_ipsum(paragraphs=1, min_sentences_per_paragraph=3, max_sentences_per_paragraph=8):
    result = []
    for _ in range(paragraphs):
        result.append(paragraph(min_sentences_per_paragraph, max_sentences_per_paragraph))
    return "\n\n".join(result)

def email(domains=None):
    if domains is None:
        domains = ["example.com", "example.org", "example.net", "mail.com", "email.com"]
    
    local_part = username(min_length=5, max_length=10).lower()
    domain = choice(domains)
    
    return f"{local_part}@{domain}"

def domain_name(tlds=None):
    if tlds is None:
        tlds = ["com", "org", "net", "io", "co", "info", "biz", "dev"]
    
    name_length = randint(5, 15)
    domain_name = "".join(choices(_LOWERCASE + _DIGITS, k=name_length))
    tld = choice(tlds)
    
    return f"{domain_name}.{tld}"

def url(protocols=None, include_path=True, include_query=False):
    if protocols is None:
        protocols = ["http", "https"]
    
    protocol = choice(protocols)
    domain = domain_name()
    result = f"{protocol}://{domain}"
    
    if include_path:
        path_segments = randint(0, 3)
        if path_segments > 0:
            path = "/".join(word().lower() for _ in range(path_segments))
            result += f"/{path}"
    
    if include_query and random() > 0.5:
        query_params = randint(1, 3)
        query_parts = []
        for _ in range(query_params):
            key = word().lower()
            value = word().lower()
            query_parts.append(f"{key}={value}")
        result += "?" + "&".join(query_parts)
    
    return result

def html_color():
    return "#" + hex_string(6)

def regex_string(pattern):
    try:
        compiled = _re.compile(pattern)
    except _re.error:
        raise ValueError(f"Недопустимый регулярный паттерн: {pattern}")
    
    if hasattr(compiled, '_generate_random_string'):
        return compiled._generate_random_string()
    
    if pattern.startswith('^') and pattern.endswith('$'):
        pattern = pattern[1:-1]
    
    result = ""
    i = 0
    while i < len(pattern):
        if pattern[i] == '\\':
            if i + 1 < len(pattern):
                i += 1
                if pattern[i] == 'd':
                    result += choice(_DIGITS)
                elif pattern[i] == 'w':
                    result += choice(_LETTERS + _DIGITS + "_")
                elif pattern[i] == 's':
                    result += choice(" \t\n\r\f\v")
                else:
                    result += pattern[i]
        elif pattern[i] == '[':
            end = pattern.find(']', i)
            if end > i:
                chars = pattern[i+1:end]
                if chars and chars[0] == '^':
                    result += choice(_PRINTABLE)
                else:
                    result += choice(chars)
                i = end
        elif pattern[i] == '.':
            result += choice(_PRINTABLE)
        elif pattern[i] in "+*?{(|)":
            pass
        else:
            result += pattern[i]
        i += 1
    
    return result

def random_slug(min_parts=2, max_parts=5):
    parts = randint(min_parts, max_parts)
    words = [word().lower() for _ in range(parts)]
    return "-".join(words)

def random_hashtags(count=3, prefix="#"):
    tags = []
    for _ in range(count):
        tag_length = randint(3, 15)
        tag = word(min_length=3, max_length=tag_length).capitalize()
        tags.append(f"{prefix}{tag}")
    
    return tags

def random_emoji():
    emoji_ranges = [
        (0x1F600, 0x1F64F),
        (0x1F300, 0x1F5FF),
        (0x1F680, 0x1F6FF),
        (0x2600, 0x26FF),
        (0x2700, 0x27BF),
    ]
    
    range_choice = choice(emoji_ranges)
    emoji_code = randint(range_choice[0], range_choice[1])
    return chr(emoji_code)