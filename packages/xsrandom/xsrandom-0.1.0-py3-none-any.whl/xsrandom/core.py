"""
Основные функции для генерации случайных значений.
Этот модуль расширяет стандартный модуль random Python.
"""

import random as _random
import time as _time
import numpy as _np
import math as _math
import sys as _sys

# Генератор случайных чисел
_DEFAULT_GENERATOR = _random.Random()

def seed(a=None, version=2, entropy=None):
    """
    Инициализирует генератор случайных чисел.
    
    Args:
        a: Семя для инициализации генератора. По умолчанию None, что использует системное время.
        version: Версия алгоритма генерации. По умолчанию 2.
        entropy: Дополнительная энтропия для улучшения случайности.
    """
    if a is None:
        a = _time.time_ns()
    
    if entropy is not None:
        a = a ^ hash(entropy)
    
    _DEFAULT_GENERATOR.seed(a=a, version=version)

def random():
    """
    Возвращает случайное число с плавающей точкой в диапазоне [0.0, 1.0).
    
    Returns:
        float: Случайное число в диапазоне [0.0, 1.0).
    """
    return _DEFAULT_GENERATOR.random()

def randint(a, b):
    """
    Возвращает случайное целое число в диапазоне [a, b].
    
    Args:
        a: Нижняя граница диапазона.
        b: Верхняя граница диапазона.
        
    Returns:
        int: Случайное целое число в диапазоне [a, b].
    """
    return _DEFAULT_GENERATOR.randint(a, b)

def uniform(a, b):
    """
    Возвращает случайное число с плавающей точкой в диапазоне [a, b).
    
    Args:
        a: Нижняя граница диапазона.
        b: Верхняя граница диапазона.
        
    Returns:
        float: Случайное число в диапазоне [a, b).
    """
    return _DEFAULT_GENERATOR.uniform(a, b)

def choice(seq):
    """
    Возвращает случайный элемент из непустой последовательности.
    
    Args:
        seq: Непустая последовательность.
        
    Returns:
        Any: Случайный элемент из последовательности.
    """
    return _DEFAULT_GENERATOR.choice(seq)

def choices(population, weights=None, cum_weights=None, k=1):
    """
    Возвращает k элементов из population с заменой. 
    Если указаны weights, выбор осуществляется согласно весам.
    
    Args:
        population: Последовательность, из которой выбираются элементы.
        weights: Последовательность весов для каждого элемента. По умолчанию None.
        cum_weights: Последовательность кумулятивных весов. По умолчанию None.
        k: Количество элементов для выбора. По умолчанию 1.
        
    Returns:
        list: Список выбранных элементов длиной k.
    """
    return _DEFAULT_GENERATOR.choices(population, weights, cum_weights, k)

def sample(population, k):
    """
    Возвращает k уникальных элементов из population.
    
    Args:
        population: Последовательность, из которой выбираются элементы.
        k: Количество элементов для выбора.
        
    Returns:
        list: Список выбранных элементов длиной k.
    """
    return _DEFAULT_GENERATOR.sample(population, k)

def shuffle(x):
    """
    Перемешивает последовательность x на месте.
    
    Args:
        x: Изменяемая последовательность.
        
    Returns:
        None: Последовательность перемешивается на месте.
    """
    return _DEFAULT_GENERATOR.shuffle(x)

def randbytes(n):
    """
    Генерирует n случайных байтов.
    
    Args:
        n: Количество байтов для генерации.
        
    Returns:
        bytes: Случайные байты.
    """
    if hasattr(_DEFAULT_GENERATOR, 'randbytes'):
        return _DEFAULT_GENERATOR.randbytes(n)
    else:
        # Для обратной совместимости с Python < 3.9
        return bytes(randint(0, 255) for _ in range(n))

def getstate():
    """
    Возвращает текущее внутреннее состояние генератора случайных чисел.
    
    Returns:
        object: Текущее состояние генератора.
    """
    return _DEFAULT_GENERATOR.getstate()

def setstate(state):
    """
    Восстанавливает внутреннее состояние генератора случайных чисел.
    
    Args:
        state: Состояние генератора, полученное от getstate().
    """
    _DEFAULT_GENERATOR.setstate(state)

def bit_generator(width=32):
    """
    Генерирует случайное битовое значение указанной ширины.
    
    Args:
        width: Количество битов (8, 16, 32, 64, 128, 256, 512, 1024).
        
    Returns:
        int: Случайное битовое значение.
    """
    if width <= 0:
        raise ValueError("Ширина должна быть положительным числом")
    
    max_val = (1 << width) - 1
    return randint(0, max_val)

def randrange(start, stop=None, step=1):
    """
    Возвращает случайно выбранный элемент из диапазона range(start, stop, step).
    
    Args:
        start: Начало диапазона или конец, если stop не указан.
        stop: Конец диапазона. По умолчанию None.
        step: Шаг диапазона. По умолчанию 1.
        
    Returns:
        int: Случайный элемент из диапазона.
    """
    return _DEFAULT_GENERATOR.randrange(start, stop, step)

def random_bool(true_probability=0.5):
    return random() < true_probability

def dice(sides=6, num_dice=1):
    return [randint(1, sides) for _ in range(num_dice)]

def flip_coin(num_flips=1):
    return [choice(['H', 'T']) for _ in range(num_flips)]

def byte_array(length):
    return bytearray(randbytes(length))

def float_precision(a, b, precision=2):
    val = uniform(a, b)
    return round(val, precision)

def range_step(start, stop, step):
    return choice(range(start, stop, step))

def random_character(charset="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"):
    return choice(charset)

def seed_from_entropy():
    entropy = _time.time_ns()
    entropy = (entropy << 32) | _time.process_time_ns()
    if hasattr(_sys, 'getrefcount'):
        entropy ^= _sys.getrefcount(entropy)
    
    _DEFAULT_GENERATOR.seed(entropy)
    return entropy

def random_sign():
    return 1 if random() < 0.5 else -1

def randbelow(n):
    return _DEFAULT_GENERATOR.randrange(n)

def fract():
    return random()

def dual_distribution(prob_first, first_func, second_func, *args, **kwargs):
    if random() < prob_first:
        return first_func(*args, **kwargs)
    else:
        return second_func(*args, **kwargs)

def odd_even(odd_probability=0.5):
    if random() < odd_probability:
        return 2 * randint(0, 1000) + 1  # odd
    else:
        return 2 * randint(0, 1000)  # even

def prime_below(n):
    def is_prime(num):
        if num < 2:
            return False
        for i in range(2, int(_math.sqrt(num)) + 1):
            if num % i == 0:
                return False
        return True
    
    primes = [i for i in range(2, n) if is_prime(i)]
    if not primes:
        raise ValueError("Нет простых чисел меньше указанного значения")
    return choice(primes) 