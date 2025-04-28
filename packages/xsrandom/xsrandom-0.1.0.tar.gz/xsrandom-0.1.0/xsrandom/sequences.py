import math as _math
import itertools as _itertools
from .core import randint, choice, choices, sample, shuffle, random

def permutation(iterable, k=None):
    items = list(iterable)
    
    if k is None:
        shuffle(items)
        return items
    else:
        if k <= 0 or k > len(items):
            raise ValueError("k должно быть положительным числом не больше длины iterable")
        
        return sample(items, k)

def combination(iterable, k):
    items = list(iterable)
    
    if k <= 0 or k > len(items):
        raise ValueError("k должно быть положительным числом не больше длины iterable")
    
    return sorted(sample(items, k))

def random_combination(iterable, k, count=1):
    items = list(iterable)
    
    if k <= 0 or k > len(items):
        raise ValueError("k должно быть положительным числом не больше длины iterable")
    
    if count <= 0:
        raise ValueError("count должно быть положительным числом")
    
    max_combinations = _math.comb(len(items), k)
    
    if count > max_combinations:
        raise ValueError(f"count не может быть больше {max_combinations} (всех возможных сочетаний)")
    
    result = set()
    max_attempts = count * 10
    attempts = 0
    
    while len(result) < count and attempts < max_attempts:
        comb = tuple(sorted(sample(items, k)))
        result.add(comb)
        attempts += 1
    
    return [list(comb) for comb in result]

def unique_sequence(length, min_val=0, max_val=None):
    if length <= 0:
        raise ValueError("length должно быть положительным числом")
    
    if max_val is None:
        max_val = min_val + length - 1
    
    if max_val < min_val:
        raise ValueError("max_val должно быть не меньше min_val")
    
    if max_val - min_val + 1 < length:
        raise ValueError(f"Диапазон [{min_val}, {max_val}] недостаточен для генерации {length} уникальных чисел")
    
    numbers = list(range(min_val, max_val + 1))
    shuffle(numbers)
    
    return numbers[:length]

def subset(iterable, min_size=0, max_size=None):
    items = list(iterable)
    
    if min_size < 0:
        raise ValueError("min_size должно быть неотрицательным числом")
    
    if max_size is None:
        max_size = len(items)
    
    if max_size < min_size or max_size > len(items):
        raise ValueError("max_size должно быть не меньше min_size и не больше длины iterable")
    
    size = randint(min_size, max_size)
    
    return sample(items, size) if size > 0 else []

def random_walk(steps=10, dimensions=1, step_size=1.0):
    if steps <= 0:
        raise ValueError("steps должно быть положительным числом")
    
    if dimensions <= 0:
        raise ValueError("dimensions должно быть положительным числом")
    
    position = [0.0] * dimensions
    walk = [position[:]] 
    
    for _ in range(steps):
        new_position = position[:]
        
        for i in range(dimensions):
            direction = 1 if random() < 0.5 else -1
            new_position[i] += direction * step_size
        
        walk.append(new_position[:])
        position = new_position
    
    return walk

def markov_sequence(states, transition_matrix, initial_state=None, length=10):
    if length <= 0:
        raise ValueError("length должно быть положительным числом")
    
    n_states = len(states)
    
    if len(transition_matrix) != n_states:
        raise ValueError("Количество строк в transition_matrix должно совпадать с количеством состояний")
    
    for i in range(n_states):
        if len(transition_matrix[i]) != n_states:
            raise ValueError(f"Количество столбцов в строке {i} transition_matrix должно совпадать с количеством состояний")
        
        row_sum = sum(transition_matrix[i])
        if not _math.isclose(row_sum, 1.0, rel_tol=1e-9):
            raise ValueError(f"Сумма вероятностей в строке {i} должна быть равна 1, получено {row_sum}")
    
    if initial_state is None:
        current_state_idx = randint(0, n_states - 1)
    else:
        try:
            current_state_idx = states.index(initial_state)
        except ValueError:
            raise ValueError(f"initial_state должно быть одним из {states}")
    
    sequence = [states[current_state_idx]]
    
    for _ in range(length - 1):
        current_transition_probs = transition_matrix[current_state_idx]
        next_state_idx = choices(range(n_states), weights=current_transition_probs)[0]
        
        sequence.append(states[next_state_idx])
        current_state_idx = next_state_idx
    
    return sequence

def random_partition(n, k, min_value=1):
    if n <= 0:
        raise ValueError("n должно быть положительным числом")
    
    if k <= 0:
        raise ValueError("k должно быть положительным числом")
    
    if min_value <= 0:
        raise ValueError("min_value должно быть положительным числом")
    
    if n < k * min_value:
        raise ValueError(f"n должно быть не меньше {k * min_value} для разбиения на {k} частей с min_value={min_value}")
    
    points = sorted(sample(range(1, n - k * min_value + 1), k - 1))
    points = [0] + points + [n - k * min_value + 1]
    partition = [points[i] - points[i-1] + min_value for i in range(1, k + 1)]
    return partition 