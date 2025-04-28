"""
Примеры использования библиотеки xsrandom.
"""

import xsrandom
import time

def basic_examples():
    print("Базовые примеры:")
    print(f"Случайное число от 1 до 100: {xsrandom.randint(1, 100)}")
    print(f"Случайное число с плавающей точкой [0, 1): {xsrandom.random()}")
    print(f"Случайное число с плавающей точкой [5, 10): {xsrandom.uniform(5, 10)}")
    print(f"Случайный выбор из списка: {xsrandom.choice(['яблоко', 'банан', 'апельсин', 'груша'])}")
    print(f"Случайный выбор с учетом весов: {xsrandom.weighted_choice(['A', 'B', 'C'], [0.1, 0.3, 0.6])}")
    
    numbers = list(range(1, 11))
    xsrandom.shuffle(numbers)
    print(f"Перемешанный список: {numbers}")
    
    print(f"Случайная выборка из списка: {xsrandom.sample(range(1, 100), 5)}")
    print()

def string_examples():
    print("Примеры работы со строками:")
    print(f"Случайная строка: {xsrandom.string(length=10)}")
    print(f"Случайная строка только из цифр: {xsrandom.string(length=8, pattern='digits')}")
    print(f"Случайная HEX-строка: {xsrandom.string(length=8, pattern='hex')}")
    print(f"Случайная строка по шаблону: {xsrandom.string(length=12, charset='ACGT')}")
    print(f"Случайный пароль (слабый): {xsrandom.password(length=10, strength='weak')}")
    print(f"Случайный пароль (сильный): {xsrandom.password(length=12, strength='strong')}")
    print(f"Случайное имя пользователя: {xsrandom.username()}")
    print(f"Случайное слово: {xsrandom.word()}")
    print(f"Случайное предложение: {xsrandom.sentence()}")
    print()

def distribution_examples():
    print("Примеры работы с распределениями:")
    print(f"Нормальное распределение: {xsrandom.normal(0, 1)}")
    print(f"Логнормальное распределение: {xsrandom.lognormal(0, 1)}")
    print(f"Треугольное распределение: {xsrandom.triangular(0, 10, 5)}")
    print(f"Экспоненциальное распределение: {xsrandom.exponential(0.5)}")
    print(f"Распределение Вейбулла: {xsrandom.weibull(1.5)}")
    print(f"Распределение Парето: {xsrandom.pareto(1.5)}")
    print(f"Биномиальное распределение: {xsrandom.binomial(10, 0.5)}")
    print()

def datetime_examples():
    print("Примеры работы с датами и временем:")
    print(f"Случайная дата: {xsrandom.date()}")
    print(f"Случайная дата в диапазоне: {xsrandom.date('2020-01-01', '2020-12-31')}")
    print(f"Случайное время: {xsrandom.time()}")
    print(f"Случайная дата и время: {xsrandom.datetime()}")
    print(f"Случайная дата в будущем: {xsrandom.future_date(min_days=1, max_days=30)}")
    print(f"Случайная дата в прошлом: {xsrandom.past_date(min_days=1, max_days=30)}")
    print(f"Случайный день недели: {xsrandom.weekday(return_name=True)}")
    print(f"Случайный месяц: {xsrandom.month(return_name=True)}")
    print(f"Случайная метка времени: {xsrandom.timestamp()}")
    print()

def crypto_examples():
    print("Примеры работы с криптографическими функциями:")
    print(f"Случайные байты: {xsrandom.token_bytes(16)}")
    print(f"Случайная hex-строка: {xsrandom.token_hex(16)}")
    print(f"Случайная URL-safe строка: {xsrandom.token_urlsafe(16)}")
    print(f"Случайный UUID: {xsrandom.uuid()}")
    print(f"Случайный хеш: {xsrandom.random_hash('sha256')}")
    print(f"Безопасный ключ (hex): {xsrandom.secure_key(length=16, encoding='hex')}")
    print(f"Безопасный ключ (base64): {xsrandom.secure_key(length=16, encoding='base64')}")
    print(f"Случайный PIN-код: {xsrandom.secure_pin(length=6)}")
    print(f"Безопасный пароль: {xsrandom.secure_password(length=16)}")
    print(f"Случайный IP-адрес: {xsrandom.random_ip()}")
    print(f"Случайный IPv6-адрес: {xsrandom.random_ipv6()}")
    print(f"Случайный MAC-адрес: {xsrandom.random_mac()}")
    print()

def geo_examples():
    print("Примеры работы с географическими данными:")
    print(f"Случайная широта: {xsrandom.latitude()}")
    print(f"Случайная долгота: {xsrandom.longitude()}")
    print(f"Случайные координаты: {xsrandom.coordinates()}")
    print(f"Случайная точка на Земле: {xsrandom.point_on_earth()}")
    print(f"Случайная точка в радиусе 10 км от Москвы: {xsrandom.point_on_earth((55.7558, 37.6176), 10)}")
    print(f"Случайная высота над уровнем моря: {xsrandom.altitude()}")
    print(f"Случайный код страны: {xsrandom.country_code()}")
    print(f"Случайный тип места: {xsrandom.place_type()}")
    print()

def sequence_examples():
    print("Примеры работы с последовательностями:")
    print(f"Случайная перестановка: {xsrandom.permutation(range(1, 6))}")
    print(f"Случайное сочетание: {xsrandom.combination(range(1, 10), 3)}")
    print(f"Несколько случайных сочетаний: {xsrandom.random_combination(range(1, 10), 3, 2)}")
    print(f"Случайная последовательность уникальных чисел: {xsrandom.unique_sequence(5, 1, 20)}")
    print(f"Случайное подмножество: {xsrandom.subset(['A', 'B', 'C', 'D', 'E'])}")
    print(f"Случайное блуждание в 2D: {xsrandom.random_walk(steps=5, dimensions=2)}")
    
    states = ['Солнечно', 'Облачно', 'Дождь']
    transitions = [
        [0.7, 0.3, 0.0], 
        [0.4, 0.4, 0.2], 
        [0.1, 0.5, 0.4]  
    ]
    print(f"Последовательность на основе цепи Маркова (погода): {xsrandom.markov_sequence(states, transitions, length=7)}")
    
    print(f"Случайное разбиение числа: {xsrandom.random_partition(100, 5)}")
    print()

def performance_test():
    print("Тест производительности:")
    
    start_time = time.time()
    for _ in range(1_000_000):
        xsrandom.random()
    end_time = time.time()
    
    print(f"Время генерации 1 000 000 случайных чисел: {end_time - start_time:.4f} секунд")
    print()

def main():
    print("=== Примеры использования библиотеки xsrandom ===\n")
    
    xsrandom.seed()
    
    basic_examples()
    string_examples()
    distribution_examples()
    datetime_examples()
    crypto_examples()
    geo_examples()
    sequence_examples()
    performance_test()
    
    print("Все примеры выполнены успешно!")

if __name__ == "__main__":
    main() 