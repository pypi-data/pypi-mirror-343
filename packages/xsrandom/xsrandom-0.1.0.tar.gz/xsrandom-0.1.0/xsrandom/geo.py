"""
Функции для генерации случайных географических данных.
"""

import math as _math
from .core import random, uniform, randint, choice
from .distributions import normal

def latitude(min_lat=-90.0, max_lat=90.0, precision=6):
    """
    Генерирует случайную широту в указанном диапазоне.
    
    Args:
        min_lat: Минимальная широта. По умолчанию -90.0.
        max_lat: Максимальная широта. По умолчанию 90.0.
        precision: Точность (количество десятичных знаков). По умолчанию 6.
        
    Returns:
        float: Случайная широта.
    """
    if min_lat < -90.0 or max_lat > 90.0 or min_lat > max_lat:
        raise ValueError("Широта должна быть в диапазоне [-90.0, 90.0], и min_lat <= max_lat")
    
    lat = uniform(min_lat, max_lat)
    return round(lat, precision)

def longitude(min_lon=-180.0, max_lon=180.0, precision=6):
    """
    Генерирует случайную долготу в указанном диапазоне.
    
    Args:
        min_lon: Минимальная долгота. По умолчанию -180.0.
        max_lon: Максимальная долгота. По умолчанию 180.0.
        precision: Точность (количество десятичных знаков). По умолчанию 6.
        
    Returns:
        float: Случайная долгота.
    """
    if min_lon < -180.0 or max_lon > 180.0 or min_lon > max_lon:
        raise ValueError("Долгота должна быть в диапазоне [-180.0, 180.0], и min_lon <= max_lon")
    
    lon = uniform(min_lon, max_lon)
    return round(lon, precision)

def coordinates(min_lat=-90.0, max_lat=90.0, min_lon=-180.0, max_lon=180.0, precision=6):
    """
    Генерирует случайные координаты (широту и долготу) в указанном диапазоне.
    
    Args:
        min_lat: Минимальная широта. По умолчанию -90.0.
        max_lat: Максимальная широта. По умолчанию 90.0.
        min_lon: Минимальная долгота. По умолчанию -180.0.
        max_lon: Максимальная долгота. По умолчанию 180.0.
        precision: Точность (количество десятичных знаков). По умолчанию 6.
        
    Returns:
        tuple: Кортеж (широта, долгота).
    """
    lat = latitude(min_lat, max_lat, precision)
    lon = longitude(min_lon, max_lon, precision)
    
    return (lat, lon)

def point_on_earth(centered_on=None, max_distance_km=None, precision=6):
    """
    Генерирует случайную точку на земной поверхности, опционально ограниченную расстоянием от центральной точки.
    
    Args:
        centered_on: Центральная точка (широта, долгота) или None. По умолчанию None.
        max_distance_km: Максимальное расстояние в километрах от центральной точки или None. По умолчанию None.
        precision: Точность (количество десятичных знаков). По умолчанию 6.
        
    Returns:
        tuple: Кортеж (широта, долгота).
    """
    if centered_on is None or max_distance_km is None:
        u = random()
        v = random()
        
        lat = _math.acos(2 * u - 1) * (180 / _math.pi) - 90
        lon = v * 360 - 180
        
        return (round(lat, precision), round(lon, precision))
    else:
        if max_distance_km <= 0:
            raise ValueError("max_distance_km должно быть положительным числом")
        
        lat1, lon1 = centered_on
    
        R = 6371.0
        
        distance = random() * max_distance_km
        
        bearing = random() * 2 * _math.pi
        
        lat1_rad = _math.radians(lat1)
        lon1_rad = _math.radians(lon1)
        
        lat2_rad = _math.asin(_math.sin(lat1_rad) * _math.cos(distance / R) +
                             _math.cos(lat1_rad) * _math.sin(distance / R) * _math.cos(bearing))
        
        lon2_rad = lon1_rad + _math.atan2(_math.sin(bearing) * _math.sin(distance / R) * _math.cos(lat1_rad),
                                         _math.cos(distance / R) - _math.sin(lat1_rad) * _math.sin(lat2_rad))
        
        lat2 = _math.degrees(lat2_rad)
        lon2 = _math.degrees(lon2_rad)
        
        lon2 = ((lon2 + 180) % 360) - 180
        
        return (round(lat2, precision), round(lon2, precision))

def altitude(min_alt=-500, max_alt=8848, distribution='uniform'):
    """
    Генерирует случайную высоту над уровнем моря.
    
    Args:
        min_alt: Минимальная высота в метрах. По умолчанию -500 (Мертвое море).
        max_alt: Максимальная высота в метрах. По умолчанию 8848 (Эверест).
        distribution: Распределение ('uniform', 'normal', 'coastal'). По умолчанию 'uniform'.
        
    Returns:
        int: Случайная высота в метрах.
    """
    if min_alt > max_alt:
        raise ValueError("min_alt должно быть меньше или равно max_alt")
    
    if distribution == 'uniform':
        return randint(min_alt, max_alt)
    elif distribution == 'normal':
        mu = 0
        sigma = (max_alt - min_alt) / 6  
        
        alt = int(normal(mu, sigma))
        
        alt = max(min_alt, min(alt, max_alt))
        
        return alt
    elif distribution == 'coastal':
        if random() < 0.7:
            return randint(-10, 100)
        else:
            return randint(min_alt, max_alt)
    else:
        raise ValueError(f"Неизвестное распределение: {distribution}")

def country_code():
    """
    Генерирует случайный двухбуквенный код страны (ISO 3166-1 alpha-2).
    
    Returns:
        str: Случайный код страны.
    """
    codes = [
        'AF', 'AL', 'DZ', 'AS', 'AD', 'AO', 'AI', 'AQ', 'AG', 'AR', 'AM', 'AW', 'AU', 'AT', 'AZ',
        'BS', 'BH', 'BD', 'BB', 'BY', 'BE', 'BZ', 'BJ', 'BM', 'BT', 'BO', 'BQ', 'BA', 'BW', 'BV',
        'BR', 'IO', 'BN', 'BG', 'BF', 'BI', 'CV', 'KH', 'CM', 'CA', 'KY', 'CF', 'TD', 'CL', 'CN',
        'CX', 'CC', 'CO', 'KM', 'CG', 'CD', 'CK', 'CR', 'CI', 'HR', 'CU', 'CW', 'CY', 'CZ', 'DK',
        'DJ', 'DM', 'DO', 'EC', 'EG', 'SV', 'GQ', 'ER', 'EE', 'SZ', 'ET', 'FK', 'FO', 'FJ', 'FI',
        'FR', 'GF', 'PF', 'TF', 'GA', 'GM', 'GE', 'DE', 'GH', 'GI', 'GR', 'GL', 'GD', 'GP', 'GU',
        'GT', 'GG', 'GN', 'GW', 'GY', 'HT', 'HM', 'VA', 'HN', 'HK', 'HU', 'IS', 'IN', 'ID', 'IR',
        'IQ', 'IE', 'IM', 'IL', 'IT', 'JM', 'JP', 'JE', 'JO', 'KZ', 'KE', 'KI', 'KP', 'KR', 'KW',
        'KG', 'LA', 'LV', 'LB', 'LS', 'LR', 'LY', 'LI', 'LT', 'LU', 'MO', 'MG', 'MW', 'MY', 'MV',
        'ML', 'MT', 'MH', 'MQ', 'MR', 'MU', 'YT', 'MX', 'FM', 'MD', 'MC', 'MN', 'ME', 'MS', 'MA',
        'MZ', 'MM', 'NA', 'NR', 'NP', 'NL', 'NC', 'NZ', 'NI', 'NE', 'NG', 'NU', 'NF', 'MK', 'MP',
        'NO', 'OM', 'PK', 'PW', 'PS', 'PA', 'PG', 'PY', 'PE', 'PH', 'PN', 'PL', 'PT', 'PR', 'QA',
        'RE', 'RO', 'RU', 'RW', 'BL', 'SH', 'KN', 'LC', 'MF', 'PM', 'VC', 'WS', 'SM', 'ST', 'SA',
        'SN', 'RS', 'SC', 'SL', 'SG', 'SX', 'SK', 'SI', 'SB', 'SO', 'ZA', 'GS', 'SS', 'ES', 'LK',
        'SD', 'SR', 'SJ', 'SE', 'CH', 'SY', 'TW', 'TJ', 'TZ', 'TH', 'TL', 'TG', 'TK', 'TO', 'TT',
        'TN', 'TR', 'TM', 'TC', 'TV', 'UG', 'UA', 'AE', 'GB', 'US', 'UM', 'UY', 'UZ', 'VU', 'VE',
        'VN', 'VG', 'VI', 'WF', 'EH', 'YE', 'ZM', 'ZW'
    ]
    
    return choice(codes)

def place_type():
    """
    Генерирует случайный тип места.
    
    Returns:
        str: Случайный тип места.
    """
    types = [
        'city', 'town', 'village', 'hamlet', 'mountain', 'lake', 'river', 'forest',
        'desert', 'island', 'beach', 'park', 'cave', 'valley', 'hill', 'canyon',
        'waterfall', 'volcano', 'glacier', 'bay', 'cape', 'gulf', 'strait', 'peninsula',
        'reef', 'fjord', 'isthmus', 'plateau', 'wetland', 'swamp', 'marsh', 'dam',
        'airport', 'harbor', 'port', 'railway_station', 'bridge', 'tunnel'
    ]
    
    return choice(types)

def geohash(precision=9):
    chars = "0123456789bcdefghjkmnpqrstuvwxyz"
    return ''.join(choice(chars) for _ in range(precision))

def continent():
    continents = ["Africa", "Antarctica", "Asia", "Europe", 
                  "North America", "Australia", "South America"]
    return choice(continents)

def ocean():
    oceans = ["Pacific", "Atlantic", "Indian", "Southern", "Arctic"]
    return choice(oceans)

def country():
    countries = ["United States", "Canada", "Mexico", "Brazil", "Argentina", 
                 "United Kingdom", "Germany", "France", "Italy", "Spain", 
                 "Russia", "China", "Japan", "India", "Australia", 
                 "New Zealand", "South Africa", "Egypt", "Nigeria", "Kenya"]
    return choice(countries)

def city():
    cities = ["New York", "Los Angeles", "Chicago", "Houston", "Toronto", 
              "Mexico City", "Sao Paulo", "London", "Paris", "Berlin", 
              "Rome", "Madrid", "Moscow", "Beijing", "Tokyo", 
              "Delhi", "Sydney", "Auckland", "Cairo", "Lagos"]
    return choice(cities)

def street_name():
    prefixes = ["Main", "Park", "Oak", "Pine", "Maple", "Cedar", "Elm", 
                "Washington", "Lincoln", "Roosevelt", "Jefferson", "Adams", 
                "Lake", "Hill", "River", "View", "Green", "Forest"]
    suffixes = ["Street", "Avenue", "Boulevard", "Lane", "Road", "Drive", 
                "Court", "Place", "Circle", "Way", "Trail", "Parkway"]
    return f"{choice(prefixes)} {choice(suffixes)}"

def address():
    number = randint(1, 9999)
    return f"{number} {street_name()}"

def postal_code(country="US"):
    if country == "US":
        return f"{randint(10000, 99999)}"
    elif country == "CA":
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        return f"{choice(letters)}{randint(0, 9)}{choice(letters)} {randint(0, 9)}{choice(letters)}{randint(0, 9)}"
    elif country == "UK" or country == "GB":
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        return f"{choice(letters)}{choice(letters)}{randint(0, 9)} {randint(0, 9)}{choice(letters)}{choice(letters)}"
    else:
        return f"{randint(10000, 99999)}"

def coordinate_pair():
    return f"{latitude()}, {longitude()}"

def bounding_box():
    min_lat = uniform(-90, 80)
    max_lat = uniform(min_lat, 90)
    min_lon = uniform(-180, 170)
    max_lon = uniform(min_lon, 180)
    return (min_lat, min_lon, max_lat, max_lon)

def distance_between(point1, point2):
    lat1, lon1 = point1
    lat2, lon2 = point2
    
    lat1 = _math.radians(lat1)
    lon1 = _math.radians(lon1)
    lat2 = _math.radians(lat2)
    lon2 = _math.radians(lon2)
    
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    
    a = _math.sin(dlat/2)**2 + _math.cos(lat1) * _math.cos(lat2) * _math.sin(dlon/2)**2
    c = 2 * _math.atan2(_math.sqrt(a), _math.sqrt(1-a))
    
    earth_radius = 6371 
    return earth_radius * c 