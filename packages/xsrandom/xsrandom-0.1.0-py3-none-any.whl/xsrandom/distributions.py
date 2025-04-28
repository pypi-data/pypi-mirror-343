"""
Функции для генерации случайных значений с разными статистическими распределениями.
"""

import math as _math
import numpy as _np
import bisect as _bisect
from .core import random, uniform, choices, randint

def normal(mu=0.0, sigma=1.0):
    """
    Генерирует случайное число с нормальным (гауссовым) распределением.
    
    Args:
        mu: Математическое ожидание. По умолчанию 0.0.
        sigma: Стандартное отклонение. По умолчанию 1.0.
        
    Returns:
        float: Случайное число с нормальным распределением.
    """
    u1 = random()
    u2 = random()
    
    z0 = _math.sqrt(-2.0 * _math.log(u1)) * _math.cos(2.0 * _math.pi * u2)
    
    return mu + sigma * z0

def lognormal(mu=0.0, sigma=1.0):
    """
    Генерирует случайное число с логнормальным распределением.
    
    Args:
        mu: Математическое ожидание логарифма переменной. По умолчанию 0.0.
        sigma: Стандартное отклонение логарифма переменной. По умолчанию 1.0.
        
    Returns:
        float: Случайное число с логнормальным распределением.
    """
    return _math.exp(normal(mu, sigma))

def triangular(low=0.0, high=1.0, mode=None):
    """
    Генерирует случайное число с треугольным распределением.
    
    Args:
        low: Нижняя граница. По умолчанию 0.0.
        high: Верхняя граница. По умолчанию 1.0.
        mode: Мода распределения. По умолчанию среднее между low и high.
        
    Returns:
        float: Случайное число с треугольным распределением.
    """
    if mode is None:
        mode = (low + high) / 2.0
    
    if not low <= mode <= high:
        raise ValueError("Необходимо, чтобы low <= mode <= high")
    
    u = random()
    
    if u < (mode - low) / (high - low):
        return low + _math.sqrt(u * (high - low) * (mode - low))
    else:
        return high - _math.sqrt((1 - u) * (high - low) * (high - mode))

def beta(alpha, beta):
    """
    Генерирует случайное число с бета-распределением.
    
    Args:
        alpha: Первый параметр формы. Должен быть положительным.
        beta: Второй параметр формы. Должен быть положительным.
        
    Returns:
        float: Случайное число с бета-распределением в диапазоне [0, 1].
    """
    if alpha <= 0 or beta <= 0:
        raise ValueError("Параметры alpha и beta должны быть положительными")
    
    y1 = _np.random.gamma(alpha, 1)
    y2 = _np.random.gamma(beta, 1)
    
    return y1 / (y1 + y2)

def gamma(shape, scale=1.0):
    """
    Генерирует случайное число с гамма-распределением.
    
    Args:
        shape: Параметр формы. Должен быть положительным.
        scale: Параметр масштаба. Должен быть положительным. По умолчанию 1.0.
        
    Returns:
        float: Случайное число с гамма-распределением.
    """
    if shape <= 0 or scale <= 0:
        raise ValueError("Параметры shape и scale должны быть положительными")
    
    return _np.random.gamma(shape, scale)

def exponential(lambd):
    """
    Генерирует случайное число с экспоненциальным распределением.
    
    Args:
        lambd: Параметр распределения (1/среднее). Должен быть положительным.
        
    Returns:
        float: Случайное число с экспоненциальным распределением.
    """
    if lambd <= 0:
        raise ValueError("Параметр lambd должен быть положительным")
    
    return -_math.log(1.0 - random()) / lambd

def weibull(shape, scale=1.0):
    """
    Генерирует случайное число с распределением Вейбулла.
    
    Args:
        shape: Параметр формы. Должен быть положительным.
        scale: Параметр масштаба. Должен быть положительным. По умолчанию 1.0.
        
    Returns:
        float: Случайное число с распределением Вейбулла.
    """
    if shape <= 0 or scale <= 0:
        raise ValueError("Параметры shape и scale должны быть положительными")
    
    return scale * (-_math.log(1.0 - random())) ** (1.0 / shape)

def pareto(alpha):
    """
    Генерирует случайное число с распределением Парето.
    
    Args:
        alpha: Параметр формы. Должен быть положительным.
        
    Returns:
        float: Случайное число с распределением Парето.
    """
    if alpha <= 0:
        raise ValueError("Параметр alpha должен быть положительным")
    
    return 1.0 / ((1.0 - random()) ** (1.0 / alpha))

def vonmises(mu, kappa):
    """
    Генерирует случайное число с распределением фон Мизеса.
    
    Args:
        mu: Мода распределения. Должна быть в диапазоне [0, 2*pi].
        kappa: Параметр концентрации. Должен быть положительным.
        
    Returns:
        float: Случайное число с распределением фон Мизеса.
    """
    if kappa < 0:
        raise ValueError("Параметр kappa должен быть неотрицательным")
    
    if kappa == 0:
        return uniform(0, 2 * _math.pi)
    
    return _np.random.vonmises(mu, kappa)

def poisson(lam):
    """
    Генерирует случайное целое число с распределением Пуассона.
    
    Args:
        lam: Параметр распределения (среднее). Должен быть положительным.
        
    Returns:
        int: Случайное целое число с распределением Пуассона.
    """
    if lam <= 0:
        raise ValueError("Параметр lam должен быть положительным")
    
    L = _math.exp(-lam)
    k = 0
    p = 1.0
    
    while p > L:
        k += 1
        p *= random()
    
    return k - 1

def binomial(n, p):
    """
    Генерирует случайное целое число с биномиальным распределением.
    
    Args:
        n: Количество испытаний. Должно быть неотрицательным целым числом.
        p: Вероятность успеха в каждом испытании. Должна быть в диапазоне [0, 1].
        
    Returns:
        int: Случайное целое число с биномиальным распределением.
    """
    if n < 0 or not isinstance(n, int):
        raise ValueError("Параметр n должен быть неотрицательным целым числом")
    
    if p < 0 or p > 1:
        raise ValueError("Параметр p должен быть в диапазоне [0, 1]")
    
    successes = 0
    for _ in range(n):
        if random() < p:
            successes += 1
    
    return successes

def weighted_choice(population, weights):
    """
    Выбирает случайный элемент из population в соответствии с весами.
    
    Args:
        population: Последовательность элементов для выбора.
        weights: Последовательность весов для каждого элемента.
        
    Returns:
        Any: Случайно выбранный элемент.
    """
    if len(population) != len(weights):
        raise ValueError("Длины population и weights должны совпадать")
    
    if not weights:
        raise ValueError("weights не может быть пустым")
    
    if any(w < 0 for w in weights):
        raise ValueError("Все веса должны быть неотрицательными")
    
    cum_weights = []
    total = 0
    for w in weights:
        total += w
        cum_weights.append(total)
    
    x = uniform(0, total)
    i = _bisect.bisect(cum_weights, x)
    
    return population[i]

def zipf(a, size=1):
    """
    Генерирует случайные целые числа с распределением Зипфа.
    
    Args:
        a: Параметр распределения (должен быть > 1).
        size: Количество значений для генерации. По умолчанию 1.
        
    Returns:
        int или list: Случайное целое число или список целых чисел с распределением Зипфа.
    """
    if a <= 1:
        raise ValueError("Параметр a должен быть больше 1")
    
    result = _np.random.zipf(a, size)
    
    if size == 1:
        return int(result[0])
    else:
        return [int(x) for x in result]

def cauchy(x0=0, gamma=1):
    if gamma <= 0:
        raise ValueError("Параметр gamma должен быть положительным")
    
    return x0 + gamma * _math.tan(_math.pi * (random() - 0.5))

def laplace(mu=0, b=1):
    if b <= 0:
        raise ValueError("Параметр b должен быть положительным")
    
    u = random() - 0.5
    if u < 0:
        return mu + b * _math.log(1 + 2 * u)
    else:
        return mu - b * _math.log(1 - 2 * u)

def logistic(mu=0, s=1):
    if s <= 0:
        raise ValueError("Параметр s должен быть положительным")
    
    u = random()
    return mu + s * _math.log(u / (1 - u))

def rayleigh(scale=1.0):
    if scale <= 0:
        raise ValueError("Параметр scale должен быть положительным")
    
    return scale * _math.sqrt(-2.0 * _math.log(1.0 - random()))

def chisquare(df):
    if df <= 0:
        raise ValueError("Параметр df должен быть положительным")
    
    return 2.0 * gamma(df / 2.0, 1.0)

def student_t(df):
    if df <= 0:
        raise ValueError("Параметр df должен быть положительным")
    
    if df == _math.inf:
        return normal()
    
    y1 = normal()
    y2 = chisquare(df)
    
    return y1 / _math.sqrt(y2 / df)

def f(dfnum, dfden):
    if dfnum <= 0 or dfden <= 0:
        raise ValueError("Параметры dfnum и dfden должны быть положительными")
    
    return (chisquare(dfnum) / dfnum) / (chisquare(dfden) / dfden)

def dirichlet(alpha):
    if not all(a > 0 for a in alpha):
        raise ValueError("Все компоненты alpha должны быть положительными")
    
    samples = [gamma(a, 1) for a in alpha]
    return [s / sum(samples) for s in samples]

def mixture(distributions, weights=None):
    if weights is None:
        weights = [1] * len(distributions)
    
    if len(distributions) != len(weights):
        raise ValueError("Длины distributions и weights должны совпадать")
    
    if not weights:
        raise ValueError("weights не может быть пустым")
    
    if any(w < 0 for w in weights):
        raise ValueError("Все веса должны быть неотрицательными")
    
    dist = weighted_choice(distributions, weights)
    return dist()

def discrete_uniform(a, b):
    if a > b:
        raise ValueError("Параметр a должен быть не больше b")
    
    return randint(a, b)

def geometric(p):
    if p <= 0 or p > 1:
        raise ValueError("Параметр p должен быть в диапазоне (0, 1]")
    
    return _math.floor(_math.log(1.0 - random()) / _math.log(1.0 - p))

def negative_binomial(r, p):
    if r <= 0:
        raise ValueError("Параметр r должен быть положительным")
    
    if p <= 0 or p >= 1:
        raise ValueError("Параметр p должен быть в диапазоне (0, 1)")
    
    return sum(geometric(p) for _ in range(int(r)))

def hypergeometric(n, K, N):
    if not 0 <= K <= N:
        raise ValueError("Должно выполняться: 0 <= K <= N")
    
    if n > N:
        raise ValueError("Должно выполняться: n <= N")
    
    result = 0
    for _ in range(n):
        if random() < (K - result) / (N - _):
            result += 1
    
    return result

def multivariate_normal(mean, cov):
    n = len(mean)
    if cov.shape != (n, n):
        raise ValueError(f"Ковариационная матрица должна иметь форму ({n}, {n})")
    
    chol = _np.linalg.cholesky(cov)
    z = _np.array([normal() for _ in range(n)])
    return mean + _np.dot(chol, z)

def custom_distribution(pdf_function, xmin, xmax, max_pdf=None, max_tries=1000):
    if max_pdf is None:
        x_samples = [uniform(xmin, xmax) for _ in range(100)]
        max_pdf = max(pdf_function(x) for x in x_samples) * 1.1
    
    for _ in range(max_tries):
        x = uniform(xmin, xmax)
        y = uniform(0, max_pdf)
        
        if y <= pdf_function(x):
            return x
    
    raise RuntimeError(f"Не удалось сгенерировать значение за {max_tries} попыток. Возможно, max_pdf слишком мал.") 